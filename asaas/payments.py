from typing import Optional
from typing import List
from urllib.parse import urljoin
from datetime import date

from asaas.customers import Customer

from asaas.utils import pickable

class Status:
    PENDING = 'PENDING'
    RECEIVED = 'RECEIVED'
    CONFIRMED = 'CONFIRMED' 
    OVERDUE = 'OVERDUE'
    REFUNDED = 'REFUNDED'
    RECEIVED_IN_CASH = 'RECEIVED_IN_CASH'
    REFUND_REQUESTED = 'REFUND_REQUESTED'
    REFUND_IN_PROGRESS = 'REFUND_IN_PROGRESS'
    CHARGEBACK_REQUESTED = 'CHARGEBACK_REQUESTED'
    CHARGEBACK_DISPUTE = 'CHARGEBACK_DISPUTE'
    AWAITING_CHARGEBACK_REVERSAL = 'AWAITING_CHARGEBACK_REVERSAL'
    DUNNING_REQUESTED = 'DUNNING_REQUESTED'
    DUNNING_RECEIVED = 'DUNNING_RECEIVED'
    AWAITING_RISK_ANALYSIS = 'AWAITING_RISK_ANALYSIS'

class BillingType:
    BOLETO = 'BOLETO'
    CREDIT_CARD = 'CREDIT_CARD'
    UNDEFINED = 'UNDEFINED'
    DEBIT_CARD = 'DEBIT_CARD'
    TRANSFER = 'TRANSFER'
    DEPOSIT = 'DEPOSIT'
    PIX = 'PIX'

class Discount(pickable):

    class Type:
        FIXED = 'FIXED'
        PERCENTAGE = 'PERCENTAGE'

    def __init__(self, value: float, dueDateLimitDays: int, type: Type) -> None:
        self.value = value
        self.dueDateLimitDays = dueDateLimitDays
        self.type = type

class Interest(pickable):
    def __init__(self, value: float) -> None:
        self.value = value

class Fine(pickable):
    def __init__(self, value: float) -> None:
        self.value = value

class Split(pickable):
    def __init__(self, walletId: str, fixedValue: float, percentualValue: float) -> None:
        self.walletId = walletId
        self.fixedValue = fixedValue
        self.percentualValue = percentualValue

class Chargeback(pickable):

    class Status:
        REQUESTED = 'REQUESTED'
        IN_DISPUTE = 'IN_DISPUTE'
        DISPUTE_LOST = 'DISPUTE_LOST'
        REVERSED = 'REVERSED'
        DONE = 'DONE'

    class Reason:
        ABSENCE_OF_PRINT = 'ABSENCE_OF_PRINT'
        ABSENT_CARD_FRAUD = 'ABSENT_CARD_FRAUD'
        CARD_ACTIVATED_PHONE_TRANSACTION = 'CARD_ACTIVATED_PHONE_TRANSACTION'
        CARD_FRAUD = 'CARD_FRAUD'
        CARD_RECOVERY_BULLETIN = 'CARD_RECOVERY_BULLETIN'
        COMMERCIAL_DISAGREEMENT = 'COMMERCIAL_DISAGREEMENT'
        COPY_NOT_RECEIVED = 'COPY_NOT_RECEIVED'
        CREDIT_OR_DEBIT_PRESENTATION_ERROR = 'CREDIT_OR_DEBIT_PRESENTATION_ERROR'
        DIFFERENT_PAY_METHOD = 'DIFFERENT_PAY_METHOD'
        FRAUD = 'FRAUD'
        INCORRECT_TRANSACTION_VALUE = 'INCORRECT_TRANSACTION_VALUE'
        INVALID_CURRENCY = 'INVALID_CURRENCY'
        INVALID_DATA = 'INVALID_DATA'
        LATE_PRESENTATION = 'LATE_PRESENTATION'
        LOCAL_REGULATORY_OR_LEGAL_DISPUTE = 'LOCAL_REGULATORY_OR_LEGAL_DISPUTE'
        MULTIPLE_ROCS = 'MULTIPLE_ROCS'
        ORIGINAL_CREDIT_TRANSACTION_NOT_ACCEPTED = 'ORIGINAL_CREDIT_TRANSACTION_NOT_ACCEPTED'
        OTHER_ABSENT_CARD_FRAUD = 'OTHER_ABSENT_CARD_FRAUD'
        PROCESS_ERROR = 'PROCESS_ERROR'
        RECEIVED_COPY_ILLEGIBLE_OR_INCOMPLETE = 'RECEIVED_COPY_ILLEGIBLE_OR_INCOMPLETE'
        RECURRENCE_CANCELED = 'RECURRENCE_CANCELED'
        REQUIRED_AUTHORIZATION_NOT_GRANTED = 'REQUIRED_AUTHORIZATION_NOT_GRANTED'
        RIGHT_OF_FULL_RECOURSE_FOR_FRAUD = 'RIGHT_OF_FULL_RECOURSE_FOR_FRAUD'
        SALE_CANCELED = 'SALE_CANCELED'
        SERVICE_DISAGREEMENT_OR_DEFECTIVE_PRODUCT = 'SERVICE_DISAGREEMENT_OR_DEFECTIVE_PRODUCT'
        SERVICE_NOT_RECEIVED = 'SERVICE_NOT_RECEIVED'
        SPLIT_SALE = 'SPLIT_SALE'
        TRANSFERS_OF_DIVERSE_RESPONSIBILITIES = 'TRANSFERS_OF_DIVERSE_RESPONSIBILITIES'
        UNQUALIFIED_CAR_RENTAL_DEBIT = 'UNQUALIFIED_CAR_RENTAL_DEBIT'
        USA_CARDHOLDER_DISPUTE = 'USA_CARDHOLDER_DISPUTE'
        VISA_FRAUD_MONITORING_PROGRAM = 'VISA_FRAUD_MONITORING_PROGRAM'
        WARNING_BULLETIN_FILE = 'WARNING_BULLETIN_FILE'

    def __init__(self, status: Status, reason: Reason) -> None:
        self.status = status
        self.reason = reason

class Refund(pickable):

    class Status:
        PENDING = 'PENDING'
        CANCELLED = 'CANCELLED'
        DONE = 'DONE'

    def __init__(self, 
        dateCreated: date, 
        status: Status, 
        value: str,
        description: str,
        transactionReceiptUrl: str
    ) -> None:

        self.dateCreated = dateCreated
        self.status = status
        self.value = value
        self.description = description
        self.transactionReceiptUrl = transactionReceiptUrl

class CreditCard(pickable):
    def __init__(self,
        holderName: str,
        number: str, 
        expiryMonth: str, 
        expiryYear: str,
        ccv: str
    ) -> None:
        self.holderName = holderName
        self.number = number
        self.expiryMonth = expiryMonth
        self.expiryYear = expiryYear
        self.ccv = ccv

class CreditCardHolderInfo(pickable):
    def __init__(self,
        name: str,
        email: str, 
        cpfCnpj: str, 
        postalCode: str,
        addressNumber: str,
        addressComplement: str,
        phone: str,
        mobilePhone: Optional[str] = None
    ) -> None:
        self.name = name
        self.email = email
        self.cpfCnpj = cpfCnpj
        self.postalCode = postalCode
        self.addressNumber = addressNumber
        self.addressComplement = addressComplement
        self.phone = phone
        self.mobilePhone = mobilePhone

class CreditCardToken(pickable):
    def __init__(self, 
        creditCardNumber: str, 
        creditCardBrand: str, 
        creditCardToken: str
    ) -> None:
        self.creditCardNumber = creditCardNumber
        self.creditCardBrand = creditCardBrand
        self.creditCardToken = creditCardToken

class Payment(pickable):
    def __init__(self,
        id: str,
        dateCreated: date,
        customer: Customer,
        dueDate: date,
        value: float,
        netValue: Optional[float] = None,
        paymentLink: Optional[str] = None,
        subscription: Optional[str] = None,
        installment: Optional[str] = None,
        discount: Optional[Discount] = None,
        interest: Optional[Interest] = None,
        fine: Optional[Fine] = None,
        billingType: Optional[BillingType] = None,
        canBePaidAfterDueDate: Optional[bool] = None,
        status: Optional[Status] = None,
        pixTransaction: Optional[str] = None,
        pixQrCodeId: Optional[str] = None,
        description: Optional[str] = None,
        externalReference: Optional[str] = None,
        originalDueDate: Optional[str] = None,
        originalValue: Optional[float] = None,
        interestValue: Optional[float] = None,
        confirmedDate: Optional[date] = None,
        paymentDate: Optional[date] = None,
        clientPaymentDate: Optional[date] = None,
        installmentNumber: Optional[int] = None,
        invoiceUrl: Optional[str] = None,
        bankSlipUrl: Optional[str] = None,
        transactionReceiptUrl: Optional[str] = None,
        invoiceNumber: Optional[str] = None,
        deleted: Optional[bool] = None,
        postalService: Optional[bool] = None,
        anticipated: Optional[bool] = None,
        split: Optional[List[Split]] = None,
        chargeback: Optional[Chargeback] = None,
        refunds: Optional[List[Refund]] = None,
        municipalInscription: Optional[str] = None,
        stateInscription: Optional[str] = None,
        canDelete: Optional[str] = None,
        cannotBeDeletedReason: Optional[str] = None,
        canEdit: Optional[str] = None,
        cannotEditReason: Optional[str] = None,
        creditCard: Optional[CreditCardToken] = None
    ) -> None:
        
        self.id = id
        self.dateCreated = dateCreated
        self.customer = customer
        self.dueDate = dueDate
        self.value = value
        self.netValue = netValue
        self.paymentLink = paymentLink
        self.subscription = subscription
        self.installment = installment
        self.discount = discount
        self.interest = interest
        self.fine = fine
        self.billingType = billingType
        self.canBePaidAfterDueDate = canBePaidAfterDueDate
        self.status = status
        self.pixTransaction = pixTransaction
        self.pixQrCodeId = pixQrCodeId
        self.description = description
        self.externalReference = externalReference
        self.originalDueDate = originalDueDate
        self.originalValue = originalValue
        self.interestValue = interestValue
        self.confirmedDate = confirmedDate
        self.paymentDate = paymentDate
        self.clientPaymentDate = clientPaymentDate
        self.installmentNumber = installmentNumber
        self.invoiceUrl = invoiceUrl
        self.bankSlipUrl = bankSlipUrl
        self.transactionReceiptUrl = transactionReceiptUrl
        self.invoiceNumber = invoiceNumber
        self.deleted = deleted
        self.postalService = postalService
        self.anticipated = anticipated
        self.split = split
        self.chargeback = chargeback
        self.refunds = refunds
        self.municipalInscription = municipalInscription
        self.stateInscription = stateInscription
        self.canDelete = canDelete
        self.cannotBeDeletedReason = cannotBeDeletedReason
        self.canEdit = canEdit
        self.cannotEditReason = cannotEditReason
        self.creditCard = creditCard

    def __repr__(self) -> str:
        return f'Payment(id={self.id}, customer={self.customer}, billingType={self.billingType}, value={self.value})'
    
if __name__ == '__main__':
    import jsonpickle
    import json
    credit_card_holder = CreditCardHolderInfo(
            name = 'Marcelo Henrique Almeida',
            email = 'marcelo.almeida@gmail.com',
            cpfCnpj = '24971563792',
            postalCode = '89223-005',
            addressNumber = '277',
            addressComplement = '',
            phone = '4738010919'
        )
    
    credit_card_holder.json()

    pass