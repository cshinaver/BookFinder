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
    def get(cls, id):
        query = (
            '''
                select *
                from {table_name}
                where id={id}
            '''.format(
                table_name=cls.__name__,
                id=id,
            )
        )
        t = execute_sql_query(query)
        return cls._tuple_to_obj(t[0])

    def save(self):
        def _save_as_new_object():
            class_name = self.__class__.__name__
            properties = self.get_properties()
            properties = [p for p in properties if p != 'id']
            values = []
            for prop in properties:
                value = getattr(self, prop)
                if isinstance(value, basestring):
                    values.append("'{value}'".format(value=value))
                elif not value:
                    values.append('NULL')
                else:
                    values.append('{value}'.format(value=value))
            query = (
                '''
                    insert into {table_name}
                    ({properties})
                    values
                    ({values})
                    returning id
                '''.format(
                    table_name=class_name,
                    properties=','.join(properties),
                    values=','.join(values),
                )
            )
            id = execute_sql_query(query)[0][0]
            self.id = id

        def _save_as_existing_object():
            class_name = self.__class__.__name__
            properties = self.get_properties()
            properties = [p for p in properties if p != 'id']
            kv_pairs = []
            for prop in properties:
                value = getattr(self, prop)
                if isinstance(value, basestring):
                    value = "'{value}'".format(value=value)
                elif not value:
                    value = 'NULL'
                else:
                    value = "{value}".format(value=value)
                kv_pairs.append(
                    '{key} = {value}'.format(
                        key=prop,
                        value=value,
                    )
                )

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
            execute_sql_query(query)

        if hasattr(self, 'id'):
            if self.id:
                _save_as_existing_object()
            else:
                _save_as_new_object()
        else:
            _save_as_new_object()
