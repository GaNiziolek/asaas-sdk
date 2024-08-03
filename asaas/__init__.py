# https://asaasv3.docs.apiary.io
from typing import Optional
from typing import List
from requests import Session
from requests.exceptions import HTTPError
from urllib.parse import urljoin
from typing import Optional
from datetime import date


from asaas import payments
from asaas.payments import Payment
from asaas.customers import Customer
from asaas.pix import Pix

from asaas.exceptions import raise_for_error

class Asaas():
    def __init__(self, access_token, production=False, url_production = 'https://api.asaas.com'):

        self.access_token = access_token
        self.url_production = url_production

        if production:
            self.url = url_production
        else:
            self.url = 'https://sandbox.asaas.com'

        self.session = Session()

        self.default_headers = {
            'access_token': access_token
        }

        self.customers = Customers(self)
        self.payments = Payments(self)

    def get(self, endpoint: str, params: Optional[dict] = None):

        response = self.session.get(
            url     = urljoin(self.url, endpoint),
            headers = self.default_headers,
            params  = params
        )

        raise_for_error(response)

        return response.json()
    
    def post(self, endpoint: str, json: dict) -> dict:

        response = self.session.post(
            url     = urljoin(self.url, endpoint),
            headers = self.default_headers,
            json    = json
        )

        raise_for_error(response)        

        return response.json()

class Customers():
    
    def __init__(self, asaas: Asaas) -> None:
        
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
        
        customers = self.asaas.get(
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

        customers_list = []
        
        for customer in customers.get('data'):
            customers_list.append(
                Customer(**customer)
            )

        return customers_list

    def get(self, id: str) -> dict:
        customer = self.asaas.get(
            endpoint = self.endpoint + '/' + id
        )

        return Customer(**customer)

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
        ) -> Customer:
        
        response = self.asaas.post(
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

        return Customer(**response)

class Payments:
    
    def __init__(self, asaas: Asaas) -> None:
        
        self.endpoint = 'api/v3/payments'

        self.asaas = asaas

    def get(self, id: str) -> Payment:
        customer = self.asaas.get(
            endpoint = self.endpoint + '/' + id
        )

        return Payment(**customer)

    def get_pix_qr(self, id) -> Pix:

        pix = self.asaas.get(
            endpoint = f'{self.endpoint}/{id}/pixQrCode'  
        )

        return Pix(**pix)

    def new(self,
            customer: Customer,
            billingType: payments.BillingType,
            dueDate: date,
            value: Optional[float] = None,
            totalValue: Optional[float] = None, 
            description: Optional[str] = None,
            externalReference: Optional[str] = None,
            installmentCount: Optional[str] = None,
            installmentValue: Optional[str] = None, 
            discount: Optional[payments.Discount] = None,
            interest: Optional[payments.Interest] = None,
            fine: Optional[payments.Fine] = None,
            postalService: Optional[bool] = None,
            split: Optional[List[payments.Split]] = None,
            creditCard: Optional[payments.CreditCard] = None,
            creditCardHolderInfo: Optional[payments.CreditCardHolderInfo] = None,
            creditCardToken: Optional[str] = None,
        ) -> Payment:
        
        response = self.asaas.post(
            endpoint = self.endpoint,
            json = {
                'customer': customer.id,
                'billingType': billingType,
                'value': value,
                'dueDate': dueDate.isoformat(),
                'description': description,
                'externalReference': externalReference,
                'installmentCount': installmentCount,
                'installmentValue': installmentValue,
                'totalValue': totalValue, 
                'discount': discount,
                'interest': interest,
                'fine': fine,
                'postalService': postalService,
                'split': split,
                'creditCard': creditCard,
                'creditCardHolderInfo': creditCardHolderInfo,
                'creditCardToken': creditCardToken,
            }
        )

        if response.get('discount'):
            discount = payments.Discount(
                value            = response.get('discount').get('value'),
                dueDateLimitDays = response.get('discount').get('dueDateLimitDays'),
                type             = response.get('discount').get('type')
            )
        else:
            discount = None

        if response.get('interest'):
            interest = payments.Interest(
                value = response.get('interest').get('value')
            )
        else:
            interest = None

        if response.get('fine'):
            fine = payments.Fine(
                value = response.get('fine').get('value')
            )
        else:
            fine = None

        split = []

        if response.get('split'):
            for _split in response.get('split'):
                split.append(payments.Split(
                    walletId = _split.get('walletId'),
                    fixedValue = _split.get('fixedValue'),
                    percentualValue = _split.get('percentualValue'),
                ))

        if response.get('chargeback'):
            chargeback = payments.Chargeback(
                status = response.get('chargeback').get('status'),
                reason = response.get('chargeback').get('reason')
            )
        else:
            chargeback = None

        refunds = []

        if response.get('refunds'):
            for refund in response.get('refunds'):
                refunds.append(payments.Refund(
                    dateCreated = refund.get('dateCreated'),
                    status = refund.get('status'),
                    value = refund.get('value'),
                    description = refund.get('description'),
                    transactionReceiptUrl = refund.get('transactionReceiptUrl'),
                ))

        if response.get('creditCard'):
            creditCardToken = payments.CreditCardToken(
                creditCardNumber = response.get('creditCard').get('creditCardNumber'),
                creditCardBrand = response.get('creditCard').get('creditCardBrand'),
                creditCardToken = response.get('creditCard').get('creditCardToken')
            )
        else:
            creditCardToken = None

        if response.get('confirmedDate'):
            confirmedDate = date.fromisoformat(response.get('confirmedDate'))
        else:
            confirmedDate = None

        if response.get('paymentDate'):
            paymentDate = date.fromisoformat(response.get('paymentDate'))
        else:
            paymentDate = None
        
        if response.get('clientPaymentDate'):
            clientPaymentDate = date.fromisoformat(response.get('clientPaymentDate'))
        else:
            clientPaymentDate = None

        new_payment = Payment(
            id = response.get('id'),
            dateCreated = response.get('dateCreated'),
            customer = customer,
            dueDate = response.get('dueDate'),
            value = response.get('value'),
            netValue = response.get('netValue'),
            paymentLink = response.get('paymentLink'),
            subscription = response.get('subscription'),
            installment = response.get('installment'),
            discount = discount,
            interest = interest,
            fine = fine,
            billingType = response.get('billingType'),
            canBePaidAfterDueDate = response.get('canBePaidAfterDueDate'),
            status = response.get('status'),
            pixTransaction = response.get('pixTransaction'),
            pixQrCodeId = response.get('pixQrCodeId'),
            description = response.get('description'),
            externalReference = response.get('externalReference'),
            originalDueDate = response.get('originalDueDate'),
            originalValue = response.get('originalValue'),
            interestValue = response.get('interestValue'),
            confirmedDate = confirmedDate,
            paymentDate   = paymentDate,
            clientPaymentDate = clientPaymentDate,
            installmentNumber = response.get('installmentNumber'),
            invoiceUrl = response.get('invoiceUrl'),
            bankSlipUrl = response.get('bankSlipUrl'),
            transactionReceiptUrl = response.get('transactionReceiptUrl'),
            invoiceNumber = response.get('invoiceNumber'),
            deleted = response.get('deleted'),
            postalService = response.get('postalService'),
            anticipated = response.get('anticipated'),
            split = split,
            chargeback = chargeback,
            refunds = refunds,
            municipalInscription = response.get('municipalInscription'),
            stateInscription = response.get('stateInscription'),
            canDelete = response.get('canDelete'),
            cannotBeDeletedReason = response.get('cannotBeDeletedReason'),
            canEdit = response.get('canEdit'),
            cannotEditReason = response.get('cannotEditReason'),
            creditCard = creditCardToken
        )
        
        return new_payment
    

if __name__ == '__main__':
    from dotenv import load_dotenv
    import os

    load_dotenv()

    acess_token = os.getenv('acess_token')

    asaas = Asaas(acess_token, production = False)

    pix = asaas.payments.get_pix_qr('pay_6318443155441227')

    exit()

    roberto = asaas.customers.get('cus_00000526a7821')

    pagamento = asaas.payments.new(
        customer = roberto,
        billingType = payments.BillingType.CREDIT_CARD,
        value = 100,
        dueDate = date.today(),
        creditCard = payments.CreditCard(
            holderName = 'marcelo h almeida',
            number = '5184019740373151',
            expiryYear = '2024', 
            expiryMonth = '05',
            ccv = '318'
        ).json(),
        creditCardHolderInfo = payments.CreditCardHolderInfo(
            name = 'Marcelo Henrique Almeida',
            email = 'marcelo.almeida@gmail.com',
            cpfCnpj = '24971563792',
            postalCode = '89223-005',
            addressNumber = '277',
            addressComplement = '',
            phone = '4738010919'
        ).json()
    )

    pass
