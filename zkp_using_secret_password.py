import hashlib;
import random;

## INITIALISATION ##

# Step 1 : Pascal (Prover) and Victoire (Verifier) agree on an random value generator and a prime number (p)
generator = 51; #It's important to have a big number to make the puzzle harder to solve
p = 1999; #To secure the puzzle and make faster the calculation of the hash!

# Step 2 : Pascal calculates password's hash using SHA-256 and converts it into an int
password = 'this_is_a_password';
hashed_password = int(hashlib.sha256(password).hexdigest()[:8], 16) % p;
print('Hashed password ' + str(hashed_password));
# Step 3 : Pascal creates a difficult puzzle so that it's consume a lot of power to solve, but easy to verify
# IMPORTANT : this value is sent to Victoire (Verifier) and she stores it !
puzzle = pow(generator,hashed_password, p); # pow function integrates mod as the third parameter


## LOG IN ##

# Step 4: Pascal wants to login, so he will generate a random value v and calculate another puzzle!
v = random.randint(1, 10000);
puzzle_v = pow(generator, v, p);
print('Puzzle_V is '  + str(puzzle_v));
# Step 5: Victoire generates a random value called the challenge and sends it to Pascal
challenge = random.randint(1, 1000); #We assume it's the number that Pascal received!

# Step 6: Pascal will generate a value r taking the challenge and his hashed password
r = v - (challenge * hashed_password);
print('R value is ' + str(r));

# FINAL STEP : Victoire will compute generator(r) * puzzle(challenge)
# Pascal is verified if generator(r) * puzzle(c) = generator(v) (which is the variable puzzle_v)

# IMPORTANT : We should calculate the inverse mod in case of r is negative: we will need two functions
def egcd(a, b): # Extended Great Common Divisor
    if a == 0:
        return (b, 0, 1)
    g, y, x = egcd(b%a,a)
    return (g, x - (b//a) * y, y)
def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('No modular inverse')
    return x % m #  Modulo Inverse of a given number

if (r < 0):
    final_value = (modinv(generator ** -r, p) * pow(puzzle, challenge, p)) % p;
else:
    final_value = (pow(generator, r, p) * pow(puzzle, challenge, p)) % p;
print('Final Value is '  + str(final_value));

if (final_value == puzzle_v):
    print('Pascal is verified!')
else:
    print('Pascal is not verified!')
