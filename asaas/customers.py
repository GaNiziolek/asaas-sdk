from typing import Optional
from urllib.parse import urljoin
from datetime import date

class Customer:
    def __init__(self,
        id: str,
        dateCreated: date,
        name: str,
        cpfCnpj: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        mobilePhone: Optional[str] = None,
        address: Optional[str] = None,
        addressNumber: Optional[str] = None,
        complement: Optional[str] = None, 
        province: Optional[str] = None,
        postalCode: Optional[str] = None,
        externalReference: Optional[str] = None,
        notificationDisabled: Optional[bool] = None,
        additionalEmails: Optional[str] = None,
        municipalInscription: Optional[str] = None,
        stateInscription: Optional[str] = None,
        observations: Optional[str] = None
    ) -> None:
        
        self.id = id 
        self.dateCreated = dateCreated
        self.name = name 
        self.cpfCnpj = cpfCnpj 
        self.email = email
        self.phone = phone
        self.mobilePhone = mobilePhone
        self.address = address
        self.addressNumber = addressNumber
        self.complement = complement
        self.province = province
        self.postalCode = postalCode
        self.externalReference = externalReference
        self.notificationDisabled = notificationDisabled
        self.additionalEmails = additionalEmails
        self.municipalInscription = municipalInscription 
        self.stateInscription = stateInscription 
        self.observations = observations

    def __repr__(self) -> str:
        return f'Customer(id={self.id}, name={self.name}, email={self.email})'