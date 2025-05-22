###############################################################################
# Iterate tuples
###############################################################################
bike_tuple = ("Specialized","Canyon","Ibis")
myit = iter(bike_tuple)
print(next(myit))
print(next(myit))
print(next(myit))

###############################################################################
# Iterate string
###############################################################################
bike_string = ("Bronson")
myit =  iter(bike_string)

for x in bike_string:
# for each in range(len(bike_string)):
    print(next(myit))

try:
    print(next(myit))
except StopIteration:
    print('You exceeded iterator end!')

###############################################################################
# Iterate dictionary multiple ways
###############################################################################
bike_dict = {
    "SantaCruz": "Bronson",
    "Pivot": "Firebird",
    "Ibis": "Mojo 3"
}

myit = iter(bike_dict)

# Loop on the set of key words, then access what you need inside the loop
for x in bike_dict:
    print(next(myit))   # return keyword
    print(bike_dict[x]) # lookup val

# For loop returns tuples key-value pairs using items() method
for key, value in bike_dict.items(): 
    print(f'{key} makes the {value} enduro MTB')

# Dictionary iteration by unpacking 
values = '{SantaCruz}-{Pivot}-{Ibis}'.format(*bike_dict,**bike_dict)
print(values)

###############################################################################
# Iterate a list
###############################################################################
bike_list = ['SantaCruz','Pivot','Ibis']

print('## simple for loop')
for mfr in bike_list:
        print(f'{mfr}')

print('## one liner with print')
print(*bike_list, sep='\n')

###############################################################################
# Iterator math
###############################################################################

lst = [x + 2 for x in range(5,10) if x % 2 == 1]
print(lst)
       