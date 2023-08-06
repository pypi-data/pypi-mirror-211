__all__ = ['MedicalVisit']

import datetime
from dataclasses import dataclass
from smartjs.functions import *
from dhint import *
from dmodel import *
from .user import *
from .profile import *

@dmcontext
@dataclass
class MedicalVisit(DetaModel):
    SINGULAR = 'Visita Médica'
    PLURAL = 'Visitas Médicas'
    patient_key: Patient = KeyValidator(required=True)
    date: datetime.date = DateValidator(required=True)
    start: datetime.datetime = DateTimeValidator(required=True)
    main_complaint: str = StringValidator()
    intro: str = TextAreaValidator()
    subjective: str = TextAreaValidator()
    treatment: str = TextAreaValidator()
    response: str = TextAreaValidator()
    complement: str = TextAreaValidator()
    context: str = TextAreaValidator()
    objective: str = TextAreaValidator()
    assessment: str = TextAreaValidator()
    plan: str = TextAreaValidator()
    creator: User = KeyValidator(item_name='provider', default='zjhm79ltaw87')
    # provider_key: User = KeyValidator()
    next: int = IntValidator()
    end: datetime.datetime = DateTimeValidator()
    key: str = SelfKeyValidator()
    
    # def __post_init__(self):
    #     if self.creator:
    #         self.provider_key = self.creator
    #     elif self.provider_key:
    #         self.creator = self.provider_key
            
    def __lt__(self, other):
        return self.date < other.date

