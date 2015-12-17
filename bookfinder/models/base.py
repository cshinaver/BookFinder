from bookfinder.db.connect import execute_sql_query


class BaseModel:
    def __repr__(self):
        properties = self.get_properties()
        repr_str = '<{cls} '.format(cls=self.__class__.__name__)
        for p in properties:
            value = getattr(self, p)
            repr_str += '{p}: {value}, '.format(
                p=p,
                value=value,
            )
        repr_str += '>'
        return repr_str

    @classmethod
    def all(cls):
        table = cls.__name__
        query = (
            '''
                select *
                from {table}
            '''.format(table=table)
        )
        results = execute_sql_query(query)
        return [cls._tuple_to_obj(t) for t in results]

    @classmethod
    def get_properties(cls):
        # Somewhat hacky trick to get all class properties
        return [
            i for i in vars(cls)
            if not callable(
                getattr(cls, i)
            )
            and '__' not in i
        ]

    @classmethod
    def _tuple_to_obj(cls, t):
        instance = cls()
        properties = cls.get_properties()
        for prop in properties:
            # Postgresql ignores case, so returns all lowercase
            value = t[str(prop).lower()]
            setattr(instance, prop, value)
        return instance

    @classmethod
    def delete(cls, obj):
        table_name = cls.__name__
        query = (
            '''
                delete from {table_name}
                where id = {id}
            '''.format(
                table_name=table_name,
                id=obj.id,
            )
        )
        execute_sql_query(query)
        obj.id = None

    @classmethod
    def get(cls, **kwargs):
        query = (
            '''
                select *
                from {table_name}
                where
            '''.format(
                table_name=cls.__name__,
            )
        )
        if kwargs:
            where_args = {}
            for k, v in kwargs.iteritems():
                if isinstance(v, basestring):
                    v = "'{v}'".format(v=v)
                else:
                    v = str(v)
                where_args[k] = v
            where_str = ' and '.join(
                "{k}={v}".format(
                    k=k,
                    v=v,
                )
                for (k, v) in where_args.iteritems())
            query += where_str

        t = execute_sql_query(query)
        n_tuples = len(t)
        if n_tuples == 0:
            result = None
        elif n_tuples == 1:
            result = cls._tuple_to_obj(t[0])
        else:
            result = [cls._tuple_to_obj(o) for o in t]
        return result

    def save(self):
        def _save_as_new_object():
            class_name = self.__class__.__name__
            properties = self.get_properties()
            properties = [p for p in properties if p != 'id']
            values = [getattr(self, prop) for prop in properties]
            column_field_names = ', '.join([p for p in properties])
            value_field_placeholders = ', '.join(['%s' for v in values])
            query = (
                '''
                    insert into {table_name}
                    ({column_field_names})
                    values
                    ({value_field_placeholders})
                    returning id
                '''.format(
                    table_name=class_name,
                    column_field_names=column_field_names,
                    value_field_placeholders=value_field_placeholders,
                )
            )
            params = values
            id = execute_sql_query(query, params)[0][0]
            self.id = id

        def _save_as_existing_object():
            class_name = self.__class__.__name__
            properties = self.get_properties()
            properties = [p for p in properties if p != 'id']
            kv_pairs = []
            values = []
            for prop in properties:
                value = getattr(self, prop)
                kv_pairs.append(
                    '{key} = %s'.format(
                        key=prop,
                        value=value,
                    )
                )
                values.append(value)

            query = (
                '''
                    update {table_name}
                    set {kv_pairs}
                    where id = {id}
                '''.format(
                    table_name=class_name,
                    kv_pairs=','.join(kv_pairs),
                    id=self.id,
                )
            )
            execute_sql_query(query, params=values)

        if hasattr(self, 'id'):
            if self.id:
                _save_as_existing_object()
            else:
                _save_as_new_object()
        else:
            _save_as_new_object()
