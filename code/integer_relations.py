#!/usr/bin/env python3
from itertools import product,combinations
from math import gcd
import csv
from functools import reduce
"""
Load a CSV into this whose format is (starting at the second row) rows of the format "label, value." Value should be interpretable as a floating point number.
"""

class DataPair:
    """
    Basically just a tuple, but OOP.
    This class is unnecessary and self-explanitory.
    """
    def __init__(self, label, value):
        self.label = label
        self.value = value

    def __str__(self):
        return self.label

def get_data(path="../data/volumes.csv",decimals=3):
    """
    Get and unfold the data.
    """
    with open(path,'r') as dfile:
        # make iterable and skip the header
        dreader = csv.reader(dfile)
        next(dreader,None)
        
        # unfold pairs into the above class, rounded to prescribed decimal place
        pairs = []
        for row in dreader:
            pairs += [DataPair(row[0],int(float(row[1])*(10**decimals)))]
        return pairs

def compute_multiples(pairs, possible_coefficients, num_nonzero_coefficients):
    """
    Compute all integer multiples whose coefficients are pulled from the (nonzero) n-tuples of values from possible_coefficients.
    Arguments:
    --pairs: this is an iterable of DataPairs whose values are being compared.
    --possible_coefficients: this is a subset of a ring (not including 0) who is implimented with exact coefficients (no floating point allowed)
    --num_nonzero_coefficients: this is the max number of nonzero coefficients to test.
    """
    assert num_nonzero_coefficients > 0
    assert len(pairs) >= num_nonzero_coefficients
    assert 0 not in possible_coefficients

    values = {}

    for num in range(1,num_nonzero_coefficients+1):
        for coeffs in product(possible_coefficients,repeat=num):
            for relevant_pairs in combinations(pairs,num):
                comb = 0
                for i in range(num):
                    comb += relevant_pairs[i].value*coeffs[i]
                values[comb] = values.get(comb,[]) + [(relevant_pairs,coeffs,comb)]
    return values

# credit for the following: stackoverflow user Ayoub ABOUNAKIF
# why does python not natively compute the GCD of a list
def find_gcd(list):
    x = reduce(gcd, list)
    return x

def list_collisions(values,deflate_digits=0,require_coprime=True):
    """
    Once you've run compute_multiples, this nicely displays all of the collisions in values.
    Arguments:
    --values: output of compute_mulitples
    --deflate_digits: number of digits to divide by to couteract integer-ization
    --require_coprime: don't report on (redundant) multiples of integer relations
    """
    collisions = []
    for chain in values.values():
        if len(chain) > 1:
            reduced_chain = []
            for tup in chain:
                g = find_gcd(tup[1])
                if (not require_coprime) or g==1:
                    reduced_chain += [tup]
            is_coprime = (len(reduced_chain) > 0)

            lab_counts = {}
            for tup in chain:
                for lab in tup[0]:
                    lab_counts[lab] = lab_counts.get(lab,0) + 1
            for n in lab_counts.values():
                is_coprime = (is_coprime and n <= 1)
            
            if is_coprime or not require_coprime: 
                summary = str(round(float(chain[0][2])*10**(-deflate_digits),deflate_digits))
                for tup in chain:
                    summary += "\n\t"
                    for i in range(len(tup[0])):
                        summary += "(" + tup[0][i].label + ", " + str(round(float(tup[0][i].value)*(10**(-deflate_digits)),deflate_digits)) + ", " + str(tup[1][i]) + ") "
                collisions += [summary]
    return collisions

# code to get process knot data
# tuning
num_decimals = 5
pairs = get_data(decimals=num_decimals)
possible_coefficients = range(1,3)
num_nonzero_coefficients = 2
require = True
output_path="../data/integer_multiples_output"

# this does not follow pep8
with open(output_path,"w") as outfile:
    for s in list_collisions(compute_multiples(pairs,possible_coefficients,num_nonzero_coefficients),deflate_digits=num_decimals,require_coprime=require):
        outfile.write(s + "\n")


"""
# test code
pairs = [DataPair("a",2),
        DataPair("b",3),
        DataPair("c",4)]
possible_coefficients = [1,2,3]
num_nonzero_coefficients = 2

for s in list_collisions(compute_multiples(pairs,possible_coefficients,num_nonzero_coefficients),require_coprime=False):
    print(s)
"""
