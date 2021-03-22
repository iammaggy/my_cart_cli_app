from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.types import *
import json

Base = declarative_base()


class User(Base):
    __tablename__ = 'user_management'
    id = Column(Integer(), primary_key=True)
    username = Column(Text())
    password = Column(Text())
    first_name = Column(Text())
    last_name = Column(Text())
    email = Column(Text())
    user_role = Column(Text())
    create_datetime = Column(DateTime())

    def to_dict(self):
        import datetime
        import decimal
        fields = {}
        for field in [x for x in dir(self) if
                      not x.startswith('_') and x != 'metadata' and not hasattr(x, 'call') and not x.startswith(
                          'query')]:
            data = self.__getattribute__(field)
            try:
                if isinstance(data, datetime.date):
                    data = data.strftime('%Y-%m-%d')
                if isinstance(data, decimal.Decimal):
                    data = float(data)
                json.dumps(data)  # this will fail on non-encodable values, like other classes
                fields[field] = data
            except TypeError:
                fields[field] = None
        # a json-encodable dict
        return fields

    __table_args__ = {'schema': 'public'}


class Categories(Base):
    __tablename__ = 'categories'
    id = Column(Integer(), primary_key=True)
    category_name = Column(Text())
    category_level = Column(Integer())
    base_category = Column(Text())

    def to_dict(self):
        import datetime
        import decimal
        fields = {}
        for field in [x for x in dir(self) if
                      not x.startswith('_') and x != 'metadata' and not hasattr(x, 'call') and not x.startswith(
                          'query')]:
            data = self.__getattribute__(field)
            try:
                if isinstance(data, datetime.date):
                    data = data.strftime('%Y-%m-%d')
                if isinstance(data, decimal.Decimal):
                    data = float(data)
                json.dumps(data)  # this will fail on non-encodable values, like other classes
                fields[field] = data
            except TypeError:
                fields[field] = None
        # a json-encodable dict
        return fields

    __table_args__ = {'schema': 'public'}


class Products(Base):
    __tablename__ = 'products'
    id = Column(Integer(), primary_key=True)
    category_id = Column(Integer())
    category_name = Column(Text())
    product_name = Column(Text())
    product_details = Column(Text())
    product_price = Column(Numeric())

    def to_dict(self):
        import datetime
        import decimal
        fields = {}
        for field in [x for x in dir(self) if
                      not x.startswith('_') and x != 'metadata' and not hasattr(x, 'call') and not x.startswith(
                          'query')]:
            data = self.__getattribute__(field)
            try:
                if isinstance(data, datetime.date):
                    data = data.strftime('%Y-%m-%d')
                if isinstance(data, decimal.Decimal):
                    data = float(data)
                json.dumps(data)  # this will fail on non-encodable values, like other classes
                fields[field] = data
            except TypeError:
                fields[field] = None
        # a json-encodable dict
        return fields

    __table_args__ = {'schema': 'public'}


class Cart(Base):
    __tablename__ = 'cart'
    id = Column(Integer(), primary_key=True)
    client_id = Column(Integer())
    product_id = Column(Integer())
    status = Column(Text())
    client_username = Column(Text())

    def to_dict(self):
        import datetime
        import decimal
        fields = {}
        for field in [x for x in dir(self) if
                      not x.startswith('_') and x != 'metadata' and not hasattr(x, 'call') and not x.startswith(
                          'query')]:
            data = self.__getattribute__(field)
            try:
                if isinstance(data, datetime.date):
                    data = data.strftime('%Y-%m-%d')
                if isinstance(data, decimal.Decimal):
                    data = float(data)
                json.dumps(data)  # this will fail on non-encodable values, like other classes
                fields[field] = data
            except TypeError:
                fields[field] = None
        # a json-encodable dict
        return fields

    __table_args__ = {'schema': 'public'}


class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer(), primary_key=True)
    client_id = Column(Integer())
    product_id = Column(Integer())
    product_name = Column(Text())
    product_details = Column(Text())
    actual_price = Column(Numeric())
    net_price = Column(Numeric())

    def to_dict(self):
        import datetime
        import decimal
        fields = {}
        for field in [x for x in dir(self) if
                      not x.startswith('_') and x != 'metadata' and not hasattr(x, 'call') and not x.startswith(
                          'query')]:
            data = self.__getattribute__(field)
            try:
                if isinstance(data, datetime.date):
                    data = data.strftime('%Y-%m-%d')
                if isinstance(data, decimal.Decimal):
                    data = float(data)
                json.dumps(data)  # this will fail on non-encodable values, like other classes
                fields[field] = data
            except TypeError:
                fields[field] = None
        # a json-encodable dict
        return fields

    __table_args__ = {'schema': 'public'}


