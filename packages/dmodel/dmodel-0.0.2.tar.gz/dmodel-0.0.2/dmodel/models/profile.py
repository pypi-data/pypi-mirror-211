__all__ = ['Patient', 'Doctor', 'Therapist', 'Employee']


from dataclasses import dataclass
from smartjs.functions import *
from dhint import *
from dmodel import *
from .person import *
from .facility import *

@dataclass
class Profile(DetaModel):
    SEARCH_PARAM = 'search'
    person_key: Person = KeyValidator(search=True, required=True)

    def __str__(self):
        return self.person.fullname
    
    @property
    def age(self):
        return age(self.person.bdate)
    

@dataclass
class Staff(Profile):
    facility_key: Facility = KeyValidator(required=True)

@dmcontext
@dataclass
class Patient(Profile):
    SINGULAR = 'Paciente'
    phone: Phone = RegexValidator()
    email: Email = RegexValidator()
    address: str = StringValidator()
    city: str = StringValidator()
    notes: str = TextAreaValidator()
    key: str = SelfKeyValidator()
    search: str = SearchValidator()


@dmcontext
@dataclass
class Doctor(Staff):
    SINGULAR = 'Médico'
    register: str = StringValidator(required=True)
    university: str = StringValidator()
    graduation_field: GraduationField = SelectValidator()
    graduation_year: int = IntValidator()
    specialties: list[str] = Validator()
    health_insuances: list[str] = Validator()  # todo: modificar para health_insurances
    notes: str = TextAreaValidator()
    key: str = SelfKeyValidator()
    search: str = SearchValidator()
    
    def __str__(self):
        return '{} {} ({})'.format(
                'Dr.' if self.person.gender == Gender.M else 'Dra.',
                str(self.person),
                self.graduation_field.value
        )


@dmcontext
@dataclass
class Therapist(Doctor):
    SINGULAR = 'Terapeuta'


@dmcontext
@dataclass
class Employee(Staff):
    SINGULAR = 'Colaborador'
        
    scope: EmployeeScope = SelectValidator()
    active: bool = BoolValidator()
    phone: Phone = RegexValidator()
    email: Email = RegexValidator()
    address: str = StringValidator()
    city: str = StringValidator()
    base_value: float = FloatValidator()
    salary_indexed: bool = BoolValidator()
    days_month: int = IntValidator()
    hours_day: int = IntValidator()
    external: bool = BoolValidator()
    financial: bool = BoolValidator()
    housekeeping: bool = BoolValidator()
    management: bool = BoolValidator()
    reception: bool = BoolValidator()
    telephonist: bool = BoolValidator()
    key: str = SelfKeyValidator()
    search: str = SearchValidator()
    
    def __str__(self):
        return '{} ({})'.format(
                str(self.person),
                self.scope.value
        )