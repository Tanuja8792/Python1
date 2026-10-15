#  program 1
RAMA_HEIGHT=1.3
RAJA_HEIGHT=1.7
if RAMA_HEIGHT>RAJA_HEIGHT:
    print("Rama is Taller")
else:
    print("Raja is taller")

# program2
total=float(input("Enter the total purchase amount:"))
if total>=1000:
    discount=total*0.10
    final_amount=total-discount
    print("Discount Applied:",discount)
    print("Final amount to pay:",final_amount)
else:
    print("No Discount Applied")
    print("Total amount:",total)