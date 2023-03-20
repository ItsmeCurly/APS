from sqlalchemy.orm import declarative_base


class CustomBase:
    __abstract__ = True


Base = declarative_base(cls=CustomBase)


def get_class_by_tablename(tablename: str):
    for c in Base._decl_class_registry.values():
        if hasattr(c, "__tablename__") and c.__tablename == tablename:
            return c
