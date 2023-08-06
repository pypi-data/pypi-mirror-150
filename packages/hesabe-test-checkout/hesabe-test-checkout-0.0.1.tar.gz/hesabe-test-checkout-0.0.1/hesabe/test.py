import checkout

checkout.key = 'XZx9dzjrPM748jwBdvNlpOkbVYyBALGR'
checkout.iv = 'PM748jwBdvNlpOkb'
checkout.accessCode = '128fdace-aafa-456e-b87a-ffaa015cd1b4'
checkout.url = "http://sandbox.hesabe.com/checkout"


sample_data = {"data": "HELLO"}
a = checkout.Hesabe(data=sample_data)
print(a.checkout())


