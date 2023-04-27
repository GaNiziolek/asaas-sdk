# asaas-sdk
Biblioteca não oficial de comunicação com a API de pagamento do ASAAS

Baseado na documentação especificada em https://asaasv3.docs.apiary.io/

## Instalação

Instale o pacote via pip:

```sh
pip install asaas-sdk
```

## Utilização

```py
from asaas import Asaas

asaas = Asaas(access_token = 'acess_token', production = False)

``` 
A variável `acess_token` deve receber um [token válido](https://asaasv3.docs.apiary.io/#introduction/autenticacao).


### Customers
```py
new_customer = asaas.customers.new(name = 'Roberto', cpfCnpj = '24971563792')

print(new_customer)
# Customer(id=cus_000005263646, name=Roberto, email=None)
```

### Payments

#### Cartão de crédito

```py

from asaas.payments import CreditCard, CreditCardHolderInfo, BillingType
from datetime import date

credit_card = CreditCard(
            holderName = 'marcelo h almeida',
            number = '5162306219378829',
            expiryYear = '2024', expiryMonth = '05',
            ccv = '318'
        )

credit_card_holder_info = CreditCardHolderInfo(
            name = 'Marcelo Henrique Almeida',
            email = 'marcelo.almeida@gmail.com',
            cpfCnpj = '24971563792',
            postalCode = '89223-005',
            addressNumber = '277',
            addressComplement = '',
            phone = '4738010919'
        )

pagamento = asaas.payments.new(
        customer = new_customer,
        billingType = BillingType.CREDIT_CARD,
        value = 100,
        dueDate = date.today(),
        creditCard = credit_card.json(),
        creditCardHolderInfo = credit_card_holder_info.json()
    )

print(pagamento)
# Payment(id=pay_6954209428403551, customer=Customer(id=cus_000005263646, name=Roberto, email=None), billingType=CREDIT_CARD, value=100)

```

#### Boleto


```py


pagamento = asaas.payments.new(
        customer = new_customer,
        billingType = BillingType.BOLETO,
        value = 100,
        dueDate = date.today()
    )

print(pagamento)
# Payment(id=pay_6954209428403552, customer=Customer(id=cus_000005263646, name=Roberto, email=None), billingType=BOLETO, value=100, invoiceUrl=https://sandbox.asaas.com/i/6997545710784231)

```

#### Pix


```py

pagamento = asaas.payments.new(
        customer = new_customer,
        billingType = BillingType.PIX,
        value = 100,
        dueDate = date.today()
    )

print(pagamento)
# Payment(id=pay_6954209428403553, customer=Customer(id=cus_000005263646, name=Roberto, email=None), billingType=PIX, value=100)

pix_info = asaas.payments.get_pix_qr(pagamento.id)

print(pix_info)
# 'Pix(success=True, expirationDate=2023-04-27 23:59:59, payload=00020101021226820014br.gov.bcb.pix2560qrpix-...)'

```