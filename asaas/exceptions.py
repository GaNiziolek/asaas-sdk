from requests import Response
from requests.exceptions import HTTPError

def raise_for_error(response: Response):

    if response.status_code == 400:
        # Retorna somente o primeiro erro que o Asaas gerar
        error = response.json().get('errors')[0]
        
        code        = error.get('code')
        description = error.get('description')

        match code:

            case 'invalid_action':
                raise InvalidAction(description)
            
            case 'invalid_creditCard':
                raise InvalidCreditCard(description)
            
            case 'invalid_value':
                raise InvalidValue(description)
        
            case 'invalid_billingType':
                raise InvalidBillingType(description)
            
            case 'invalid_customer':
                raise InvalidCustomer(description)
            
            case 'invalid_dueDate':
                raise InvalidDueDate(description)

            case 'invalid_name':
                raise InvalidName(description)
            
    elif response.status_code == 404:
        raise NotFound(response.url)
    
    else:
        try:
            response.raise_for_status()

        except HTTPError as e:
            raise AsaasError(e)

class AsaasError(Exception):
    ...

class InvalidAction(AsaasError):
    ...

class InvalidCreditCard(AsaasError):
    ...

class InvalidValue(AsaasError):
    ...

class InvalidBillingType(AsaasError):
    ...

class InvalidCustomer(AsaasError):
    ...

class InvalidDueDate(AsaasError):
    ...

class InvalidName(AsaasError):
    ...

class NotFound(AsaasError):
    ...

    