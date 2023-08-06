__all__ = ['Facility']


from dataclasses import dataclass
from dhint import *
from dmodel import *


@dmcontext
@dataclass
class Facility(DetaModel):
    SEARCH_PARAM = 'search'
    name: str = StringValidator(required=True, search=True)
    phone: Phone = RegexValidator(search=True)
    email: Email = RegexValidator(search=True)
    address: str = StringValidator(search=True)
    city: str = StringValidator(search=True)
    cep: str = StringValidator()
    key: str = SelfKeyValidator()
    search: str = SearchValidator()
    
    def __str__(self):
        return '{} ({})'.format(self.name, self.email)

