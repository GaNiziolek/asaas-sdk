from typing import Optional
from urllib.parse import urljoin
from datetime import date

class Customer:
    def __init__(self,
        id: str,
        dateCreated: date,
        name: str,
        cpfCnpj: str,
        **kwargs
    ) -> None:
        
        self.id                   = id 
        self.dateCreated          = dateCreated if type(dateCreated) == date else date.fromisoformat(dateCreated)
        self.name                 = name 
        self.cpfCnpj              = cpfCnpj 
        self.email                = kwargs.get('email', None)
        self.phone                = kwargs.get('phone', None)
        self.mobilePhone          = kwargs.get('mobilePhone', None)
        self.address              = kwargs.get('address', None)
        self.addressNumber        = kwargs.get('addressNumber', None)
        self.complement           = kwargs.get('complement', None)
        self.province             = kwargs.get('province', None)
        self.postalCode           = kwargs.get('postalCode', None)
        self.externalReference    = kwargs.get('externalReference', None)
        self.notificationDisabled = kwargs.get('notificationDisabled', None)
        self.additionalEmails     = kwargs.get('additionalEmails', None)
        self.municipalInscription = kwargs.get('municipalInscription', None) 
        self.stateInscription     = kwargs.get('stateInscription', None) 
        self.observations         = kwargs.get('observations', None)

    def __repr__(self) -> str:
        return f'Customer(id={self.id}, name={self.name}, email={self.email})'