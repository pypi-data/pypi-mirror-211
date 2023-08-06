__all__ = ['Person']

import datetime
import re
from dataclasses import dataclass
from dhint import *
from dmodel import *


@dmcontext
@dataclass
class Person(DetaModel):
    SEARCH_PARAM = 'search_name'
    fname: str = StringValidator(search=True)
    lname: str = StringValidator(search=True)
    bdate: datetime.date = Validator(search=True)
    gender: Gender = SelectValidator(search=True)
    cpf: CPF = RegexValidator(search=True)
    transgender: bool = BoolValidator()
    non_binary: bool = BoolValidator()
    name: str = StringValidator(search=True)
    key: str = SelfKeyValidator()
    search_name: str = AutoUpdateValidator(func=lambda self: self.search_getter)
    code: str = AutoValidator(func=lambda self: self.code_getter)
    

    def __str__(self):
        return self.fullname
    
    @property
    def code_getter(self):
        return '{}{}{}{}'.format(
                self.gender.name,
                self.bdate.isoformat().replace('-', ''),
                self.fname[:2].upper(),
                self.lname.split()[-1][:2].upper()
        )

    @property
    def fullname(self):
        return self.name if all([self.name is not None, self.name != '']) else f'{self.fname} {self.lname}'
