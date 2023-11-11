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
print(f"adding nums: {a.add_nums()}")
b = a.set_nums()
print(f"x: {a.x}, y: {a.y}")
print(a.add_nums())

point = a.get_pointer()
print(point)
print(type(point))

print()
print("Making a new object from pointer")
b = Example.StructManager()
b.copy_pointer(point)
print(f"x: {b.x}, y: {b.y}")

#a = Example.StructManager()
#print(f"x: {a.x}, y: {a.y}")
#print(float(a.x))



