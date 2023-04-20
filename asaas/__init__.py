# https://asaasv3.docs.apiary.io
from typing import Optional
from typing import List
from requests import Session
from requests.exceptions import HTTPError
from urllib.parse import urljoin
from typing import Optional
from datetime import date

from asaas.customers import Customer

from asaas import payments
from asaas.payments import Payment

from asaas.exceptions import ErroAsaas

class Asaas():
    def __init__(self, access_token, production = False):

        self.access_token = access_token

        if production:
            self.url = 'https://www.asaas.com'
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

        try:
            response.raise_for_status()
        except HTTPError as e:
            if 'errors' in response.json():
                raise ErroAsaas(response.json())

        return response.json()
    
    def post(self, endpoint: str, json: Optional[dict] = None) -> dict:

        response = self.session.post(
            url     = urljoin(self.url, endpoint),
            headers = self.default_headers,
            json    = json
        )

        try:
            response.raise_for_status()
        except HTTPError as e:
            if 'errors' in response.json():
                raise ErroAsaas(response.json())

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
        
        new_customer = Customer(
            id = response.get('id'),
            dateCreated = date.fromisoformat(response.get('dateCreated')),
            name = response.get('name'),
            cpfCnpj = response.get('cpfCnpj'),
            email = response.get('email'),
            phone = response.get('phone'),
            mobilePhone = response.get('mobilePhone'),
            address = response.get('address'),
            addressNumber = response.get('addressNumber'),
            complement = response.get('complement'),
            province = response.get('province'),
            postalCode = response.get('postalCode'),
            externalReference = response.get('externalReference'),
            notificationDisabled = response.get('notificationDisabled'),
            additionalEmails = response.get('additionalEmails'),
            municipalInscription = response.get('municipalInscription'),
            stateInscription = response.get('stateInscription'),
            observations = response.get('observations')
        )
        
        return new_customer

class Payments:
    
    def __init__(self, asaas: Asaas) -> None:
        
        self.endpoint = 'api/v3/payments'

        self.asaas = asaas

    def get(self, id: str) -> dict:
        customer = self.asaas.get(
            endpoint = self.endpoint + '/' + id
        )

        return customer

    def new(self,
            customer: Customer,
            billingType: payments.BillingType,
            value: float,
            dueDate: date,
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

    roberto = asaas.customers.new('Roberto', '24971563792')

    pagamento = asaas.payments.new(
        customer = roberto,
        billingType = payments.BillingType.CREDIT_CARD,
        value = 100,
        dueDate = date.today(),
        creditCard = payments.CreditCard(
            holderName = 'marcelo h almeida',
            number = '5162306219378829',
            expiryYear = '2024', expiryMonth = '05',
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
