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

a = Example.StructManager()
a.x = 3.0
a.y = 6.0
print(f"x: {a.x}, y: {a.y}")
print(a.add_nums())



