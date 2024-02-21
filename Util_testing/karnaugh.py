from pyeda.inter import exprvars, truthtable, espresso_tts

# Define the variables x[0], x[1], and x[2]
X = exprvars('x', 4)

# Define the truth table
f = truthtable(X, "0001010111101001")

# Minimize the truth table using Espresso
fm = espresso_tts(f)

# Print the minimized form
# print(fm)
# print(len(fm))

print(type(fm[0]))
print(fm[0])
