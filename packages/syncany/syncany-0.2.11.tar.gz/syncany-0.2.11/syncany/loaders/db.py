# -*- coding: utf-8 -*-
# 18/8/6
# create by: snower

import copy
from collections import defaultdict
from .loader import Loader
from ..valuers.valuer import Contexter, ContextRunner, ContextDataer, LoadAllFieldsException


class DBLoader(Loader):
    def __init__(self, db, name, *args, **kwargs):
        super(DBLoader, self).__init__(*args, **kwargs)

        self.db = db
        self.name = name
        self.contexter = False
        self.last_data = None

    def clone(self):
        loader = self.__class__(self.db, self.name, self.primary_keys, self.valuer_type)
        loader.contexter = self.contexter
        schema = {}
        for key, valuer in self.schema.items():
            schema[key] = valuer.clone()
        loader.schema = schema
        loader.filters = [filter for filter in self.filters]
        loader.orders = [order for order in self.orders]
        loader.intercepts = [intercept.clone() for intercept in self.intercepts]
        loader.key_matchers = [matcher.clone() for matcher in self.key_matchers]
        return loader

    def next(self):
        if not self.loaded:
            return True
        if self.db:
            return self.db.is_streaming(self.name)
        return False

    def is_dynamic_schema(self):
        return self.db.is_dynamic_schema(self.name)

    def is_streaming(self):
        return self.db.is_streaming(self.name)

    def set_streaming(self, is_streaming=None):
        if is_streaming is None:
            return
        self.db.set_streaming(self.name, is_streaming)

    def load(self, timeout=None):
        if self.loaded:
            return

        fields = set([])
        if not self.key_matchers:
            try:
                for name, valuer in self.schema.items():
                    for field in valuer.get_fields():
                        fields.add(field)
            except LoadAllFieldsException:
                fields = []

        query = self.db.query(self.name, self.primary_keys, list(fields))

        in_exps = defaultdict(list)
        for key, exp, value in self.filters:
            if exp == "in":
                in_exps[key].extend(value)

        for key, exp, value in self.filters:
            if exp == "eq":
                in_exps[key].append(value)

        for key, exp, value in self.filters:
            if exp == "eq":
                if key not in in_exps:
                    continue

                if len(in_exps[key]) > 1:
                    exp, value = "in", in_exps.pop(key)

            if key is None:
                getattr(query, "filter_%s" % exp)(value)
            else:
                getattr(query, "filter_%s" % exp)(key, value)

        primary_orders = {} if len(self.orders) >= len(self.primary_keys) else None
        for i in range(len(self.orders)):
            order = self.orders[i]
            query.order_by(*order)
            if primary_orders is None:
                continue
            if i < len(self.primary_keys) and order[0] != self.primary_keys[i]:
                primary_orders = None
                continue
            primary_orders[order[0]] = order[1]

        if self.current_cursor:
            query.filter_cursor(*self.current_cursor, primary_orders=primary_orders)

        self.datas, query = query.commit(), None
        self.last_data = copy.copy(self.datas[-1]) if self.datas else {}
        self.loader_state["query_count"] += 1
        self.loader_state["load_count"] += len(self.datas)
        self.loaded = True

    def get(self):
        if self.geted:
            return self.datas
        if not self.loaded:
            self.load()

        if not self.key_matchers:
            loader_contexter = self.contexter
            if loader_contexter is False:
                if not self.valuer_type:
                    return self.fast_get()
                return super(DBLoader, self).get()

            if loader_contexter is not None:
                for i in range(len(self.datas)):
                    data, context_dataer = self.datas[i], ContextDataer(loader_contexter)
                    loader_contexter.values = context_dataer.values
                    for key, field in self.schema.items():
                        field.fill(data)
                    self.datas[i] = context_dataer
                return super(DBLoader, self).get()

            contexter_schema = [(key, field, field.contexter if hasattr(field, "contexter") else None)
                                for key, field in self.schema.items()]
            for i in range(len(self.datas)):
                data, odata, contexter_values = self.datas[i], {}, {}
                for key, field, contexter in contexter_schema:
                    if contexter is None:
                        contexter = Contexter()
                        field = field.clone(contexter)
                    odata[key] = ContextRunner(contexter, field, contexter_values).fill(data)
                self.datas[i] = odata
            return super(DBLoader, self).get()

        for i in range(len(self.datas)):
            data = {}
            for key, value in self.datas[i].items():
                if key in self.schema:
                    data[key] = value
                    continue
                for key_matcher in self.key_matchers:
                    if not key_matcher.match(key):
                        continue
                    self.schema[key] = key_matcher.create_key(key)
                    data[key] = value
                    break
            self.datas[i] = data
        return super(DBLoader, self).get()

    def fast_get(self):
        if not self.intercepts:
            for i in range(len(self.datas)):
                data = self.datas[i]
                self.datas[i] = {name: valuer.fill_get(data) for name, valuer in self.schema.items()}
            self.geted = True
            return self.datas

        datas, self.datas = self.datas, []
        datas.reverse()
        while datas:
            data = datas.pop()
            odata = {name: valuer.fill_get(data) for name, valuer in self.schema.items()}
            if self.check_intercepts(odata):
                continue
            self.datas.append(odata)
        self.geted = True
        return self.datas

    def statistics(self):
        return {
            "querys": self.loader_state["query_count"],
            "rows": self.loader_state["load_count"]
        }