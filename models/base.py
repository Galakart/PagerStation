"""База для моделей"""
from sqlalchemy.orm import declarative_base
from sqlalchemy_repr import PrettyRepresentableBase

Base = declarative_base(cls=PrettyRepresentableBase)
