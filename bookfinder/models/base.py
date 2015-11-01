from bookfinder.db.connect import execute_sql_query


class BaseModel:
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
    def _tuple_to_obj(cls, t, properties):
        instance = cls()
        for i in xrange(0, len(t)):
            setattr(instance, properties[i], t[i])
        return instance

    @classmethod
    def get(cls, obj_id):
        properties = cls.get_properties()
        properties_str = ','.join(properties)
        query = (
            '''
                select ({properties})
                from {table_name}
                where id={id}
            '''.format(
                properties=properties_str,
                table_name=cls.__name__,
                id=obj_id,
            )
        )
        t = execute_sql_query(query)
        return cls._tuple_to_obj(t[0], properties)
