from typing import Optional
from urllib.parse import urljoin

class Customers():
    
    def __init__(self, asaas) -> None:
        
        self.endpoint = 'api/v3/customers'

        self.asaas = asaas

    def list(self, 
            name:              Optional[str] = None, 
            email:             Optional[str] = None, 
            cpfCnpj:           Optional[str] = None, 
            groupName:         Optional[str] = None, 
            externalReference: Optional[str] = None,
            offset:            Optional[int] = None, 
            limit:             Optional[int] = None
        ) -> dict:
        
        list = self.asaas.get(
            endpoint = self.endpoint, 
            params = {
                'name':              name,
                'email':             email,
                'cpfCnpj':           cpfCnpj,
                'groupName':         groupName,
                'externalReference': externalReference,
                'offset':            offset,
                'limit':             limit
            }
        )

        return list

    def get(self, id: str) -> dict:
        customer = self.asaas.get(
            endpoint = self.endpoint + '/' + id
        )

        return customer

    def new(self,
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
            observations: Optional[str] = None,
            groupName: Optional[str] = None
        ):
        
        new_customer = self.asaas.post(
            endpoint = self.endpoint,
            json = {
                'name': name,
                'cpfCnpj': cpfCnpj,
                'email': email,
                'phone': phone,
                'mobilePhone': mobilePhone,
                'address': address,
                'addressNumber': addressNumber,
                'complement': complement, 
                'province': province,
                'postalCode': postalCode,
                'externalReference': externalReference,
                'notificationDisabled': notificationDisabled,
                'additionalEmails': additionalEmails,
                'municipalInscription': municipalInscription,
                'stateInscription': stateInscription,
                'observations': observations,
                'groupName': groupName
            }
        )
        
        return new_customer