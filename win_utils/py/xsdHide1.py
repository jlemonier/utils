import os

s1 = """<OrderPaymentTerms>
    <PaymentDays>0</PaymentDays>
    <DiscountDays>0</DiscountDays> 
    <PaymentTerms>TT 0</PaymentTerms> 
</OrderPaymentTerms>
<OrderPaymentTerms>
    <PaymentDays>7</PaymentDays>
    <DiscountDays>8</DiscountDays> 
    <PaymentTerms>TT 0</PaymentTerms> 
</OrderPaymentTerms>
  """

def hideElements(s):
    s = s.replace("<PaymentDays>0</PaymentDays>", "<!-- < PaymentDays>0</PaymentDays > -->")
    s = s.replace("<DiscountDays>0</DiscountDays>", "<!-- < DiscountDays>0</DiscountDays > -->")

    return s

s2 = hideElements(s1)
s2 = hideElements(s2)
s2 = hideElements(s2)
s2 = hideElements(s2)

print "%s ==> \n\n%s \n*** done" %(s1, s2)

"""
folder = r"C:\GT\Data\MssgServer\62745"
orig = r"%s\orig"%(folder)
fixed = r"%s\fixed"%(folder)

for root, dirs, files in os.walk(orig):
    for fname in files:
        print "%s => %s "%(root, fname)
        data = file(os.path.join(root, fname)).read()
        fOut = file(os.path.join(fixed, fname), "w")

        data = hideElements(data)
        fOut.write(data)
        fOut.close()

"""
