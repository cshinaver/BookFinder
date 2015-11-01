from bookfinder.db.connect import execute_sql_query


class BaseModel:
    def __repr__(self):
        properties = self.get_properties()
        repr_str = '{cls}\n'.format(cls=self.__class__.__name__)
        for p in properties:
            value = getattr(self, p)
            repr_str += '{p}: {value}\n'.format(
                p=p,
                value=value,
            )
        return repr_str

    @classmethod
    def get_properties(cls):
        # Somewhat hacky trick to get all class properties
        return [
            i for i in vars(cls)
            if not callable(
                getattr(cls, i)
            )
            and '_' not in i
        ]

    @classmethod
    def _tuple_to_obj(cls, t):
        instance = cls()
        properties = cls.get_properties()
        for prop in properties:
            setattr(instance, prop, t[str(prop)])
        return instance

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
        class_name = self.__class__.__name__
        properties = self.get_properties()
        properties = [p for p in properties if p != 'id']
        values = []
        for prop in properties:
            value = getattr(self, prop)
            if isinstance(value, basestring):
                values.append("'{value}'".format(value=value))
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
