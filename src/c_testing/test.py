import Example

x = Example.findPrimes(1, 10)
print(f"status: {x}")

y = Example.return_two()
print(y)

z = Example.Custom()
print(z.number)
z.number = 3.2
print(z.number)
print(z.number1)


