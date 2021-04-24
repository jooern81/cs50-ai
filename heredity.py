import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    probability = 1
    
    #calculate probabilities for people with one gene
    
    for person in one_gene:
        if people[person]['father'] != None:  #check if person has parent
            print(person + "has one gene and has a father")
            print (people[person]['father'])
            print(one_gene, two_genes)
            print(people[person]['father'] not in one_gene and people[person]['father'] not in two_genes)
            father_genes = 0
            if people[person]['father'] not in one_gene and people[person]['father'] not in two_genes:
                father_genes = 0
                print('Father has 0 genes')
            if people[person]['father'] in one_gene:
                father_genes = 1
                print('Father has 1 gene')
            if people[person]['father'] in two_genes:
                print('Father has 2 genes')
                father_genes = 2
                
        if people[person]['mother'] != None:  #check if person has parent
            print(person + "has one gene and has a mother")
            mother_genes = 0
            if people[person]['mother'] not in one_gene and people[person]['mother'] not in two_genes:
                mother_genes = 0
                print('Mother has 0 genes')
            if people[person]['mother'] in one_gene:
                mother_genes = 1
                print('Mother has 1 gene')
            if people[person]['mother'] in two_genes:
                mother_genes = 2
                print('Mother has 2 genes')
        
        if people[person]['mother'] != None or people[person]['father'] != None:
            print(person + "has parents, calcuating probability_gene")
            if mother_genes == 0 and father_genes == 0:
                
                
                probability_gene = 0.01 * 0.99 + 0.01 * 0.99 #one parent gene mutates, the other does not
                print(person + ": mother no gene, father no gene. probability_gene: " + str(probability_gene) )
            if (mother_genes == 1 and father_genes == 0) or (mother_genes == 0 and father_genes == 1):
                #three cases: a) the parent with one gene passes it on (0.5) and the gene does not mutate (0.99) while the partner does not mutate (0.99)) 
                #             b) the parent with one gene passes on the non mutated one (0.5 and it mutates (0.01), while the partner does not mutate (0.99)
                #             c) the parent with one gene does not pass on the mutated gene (0.5) and it does not mutate (0.99) while the parter's gene mutates (0.01)

                probability_gene = 0.5 * 0.99 * 0.99 + 0.5 * 0.01 * 0.99 + 0.5 * 0.99 * 0.01 
                print(person + ": parent A has one gene, parent B has no genes. probability_gene: " + str(probability_gene) )
            if (mother_genes == 1 and father_genes == 1):
                #3 unique cases: a) a parent passes it on (0.5) and the gene does not mutate (0.99) while the partner does not pass on the mutated gene (0.5) and it does not mutate (0.99))
                #                b) a parent passes on the non-mutated gene (0.5) and it mutates (0.01), while the parter does not pass on the mutated gene (0.5) and it does not mutate (0.99)
                #                c) a parent passes on the mutated gene and does not mutate while the parter passes on the mutated gene  and it mutates
                probability_gene = (0.5 * 0.01 * 0.5 * 0.99) * 2 + ((0.5 * 0.99 * 0.5 * 0.99) + (0.5 * 0.01 * 0.5 * 0.01)) * 2 + (0.5 * 0.99 * 0.5 * 0.01) * 2
                print(person + ": mother one gene, father one gene. probability_gene: " + str(probability_gene) )
            
            if (mother_genes == 1 and father_genes == 2) or (mother_genes == 2 and father_genes == 1):
         # father pass on        
                probability_gene = (0.01 * 0.5 * 0.99) + (0.99 * 0.5 * 0.01) + (0.01 * 0.5 * 0.01) + (0.99 * 0.5 * 0.99)
                print(person + ": mother 1 gene, father 2 genes. probability_gene: " + str(probability_gene) )
                
            if (mother_genes == 2 and father_genes == 0) or (mother_genes == 0 and father_genes == 2):       
                probability_gene = (0.99 * 0.99) + (0.01 * 0.01)
                print(person + ": paren A has 2 genes, parent B has 0 genes. probability_gene: " + str(probability_gene) )
                
            if (mother_genes == 2 and father_genes == 2):
                
                probability_gene = (0.01 * 0.99) * 2
                print(person + ": mother 2 genes, father has genes. probability_gene: " + str(probability_gene) )
        
        if people[person]['father'] == None or people[person]['mother'] == None:
            probability_gene = PROBS["gene"][1]
            print(person + ": no parents: " + str(probability_gene) )
            
            
        if person in have_trait:
            probability_trait = PROBS["trait"][1][True]
        else:
            probability_trait = PROBS["trait"][1][False]
        
        probability = probability * probability_gene * probability_trait
        print('1. joint prob factoring in one gene: ' + str(probability))
            
    #calculate probabilities for people with two genes
            
    for person in two_genes:
        if people[person]['father'] != None:  #check if person has parent
            father_genes = 0
            if people[person]['father'] not in one_gene and people[person]['father'] not in two_genes:
                father_genes = 0
            if people[person]['father'] in one_gene:
                father_genes = 1
            if people[person]['father'] in two_genes:
                father_genes = 2
                
        if people[person]['mother'] != None:  #check if person has parent
            mother_genes = 0
            if people[person]['mother'] not in one_gene and people[person]['mother'] not in two_genes:
                mother_genes = 0
            if people[person]['mother'] in one_gene:
                mother_genes = 1
            if people[person]['mother'] in two_genes:
                mother_genes = 2

        if people[person]['mother'] != None or people[person]['father'] != None:       
            if mother_genes == 0 and father_genes == 0:
                probability_gene = 0.01 * 0.01
            
            if (mother_genes == 1 and father_genes == 0) or (mother_genes == 0 and father_genes == 1):
               probability_gene = 0.5 * 0.99 * 0.01 + 0.5 * 0.01 * 0.01 
            
            if (mother_genes == 1 and father_genes == 1):
                probability_gene = (0.5 * 0.99 * 0.5 * 0.01 * 2) * 2 + 0.5 * 0.01 * 0.5 * 0.01 + 0.5 * 0.99 * 0.5 * 0.99 
            
            if (mother_genes == 1 and father_genes == 2) or (mother_genes == 2 and father_genes == 1):
                probability_gene = 0.5 * 0.99 * 0.99 + 0.5 * 0.01 * 0.99

            if (mother_genes == 2 and father_genes == 0) or (mother_genes == 0 and father_genes == 2):       
                probability_gene = (0.99 * 0.01)
                print(person + ": paren A has 2 genes, parent B has 0 genes. probability_gene: " + str(probability_gene) )
              
            
            if (mother_genes == 2 and father_genes == 2):  
                probability_gene = 0.99 * 0.99


        if people[person]['father'] == None or people[person]['mother'] == None:
            probability_gene = PROBS["gene"][2]
            
        if person in have_trait:
            probability_trait = PROBS["trait"][2][True]
        else:
            probability_trait = PROBS["trait"][2][False]
            
            
        probability = probability * probability_gene * probability_trait
        print('2. joint prob factoring in two genes: ' + str(probability))

    for person in people:
        #calculate probability_gene of no gene
        if (person not in one_gene) and (person not in two_genes):
            if people[person]['father'] != None:  #check if person has parent
                father_genes = 0
                if people[person]['father'] not in one_gene and people[person]['father'] not in two_genes:
                    father_genes = 0
                if people[person]['father'] in one_gene:
                    father_genes = 1
                if people[person]['father'] in two_genes:
                    father_genes = 2
                    
            if people[person]['mother'] != None:  #check if person has parent
                mother_genes = 0
                if people[person]['mother'] not in one_gene and people[person]['mother'] not in two_genes:
                    mother_genes = 0
                if people[person]['mother'] in one_gene:
                    mother_genes = 1
                if people[person]['mother'] in two_genes:
                    mother_genes = 2
            
            if people[person]['father'] != None or people[person]['mother'] != None:
                if mother_genes == 0 and father_genes == 0:
                    probability_gene = 0.99 * 0.99
                
                if (mother_genes == 1 and father_genes == 0) or (mother_genes == 0 and father_genes == 1):
                   probability_gene = 0.5 * 0.01 * 0.99 + 0.5 * 0.99 * 0.99 
                
                if (mother_genes == 1 and father_genes == 1):
                    probability_gene = 0.5 * 0.01 *0.5 * 0.01 + (0.5 * 0.01 * 0.5 * 0.99) * 2 + 0.5 * 0.99 * 0.5 * 0.99
                
                if (mother_genes == 1 and father_genes == 2) or (mother_genes == 2 and father_genes == 1):
                    probability_gene = 0.5 * 0.99 * 0.01 + 0.5 * 0.01 * 0.01
                    
                if (mother_genes == 2 and father_genes == 0) or (mother_genes == 0 and father_genes == 2):       
                    probability_gene = (0.01 * 0.99)
                    print(person + ": paren A has 2 genes, parent B has 0 genes. probability_gene: " + str(probability_gene) )
                        
                if (mother_genes == 2 and father_genes == 2):  
                    probability_gene = 0.01 * 0.01
            
            if people[person]['father'] == None or people[person]['mother'] == None:
                probability_gene = PROBS["gene"][0]
                


            if person in have_trait:
                probability_trait = PROBS["trait"][0][True]
            else:
                probability_trait = PROBS["trait"][0][False]       

            probability = probability * probability_gene * probability_trait
            print('3. joint prob factoring in no gene: ' + str(probability))
                
    print(people, one_gene, two_genes, have_trait)

    
    return(probability)


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    
    for person in probabilities:
        if (person not in one_gene) and (person not in two_genes):
            probabilities[person]['gene'][0] = probabilities[person]['gene'][0] + p
            if person in have_trait:
                 probabilities[person]['trait'][True] = probabilities[person]['trait'][True] + p
            if person not in have_trait:
                probabilities[person]['trait'][False] = probabilities[person]['trait'][False] + p
        
        if person in one_gene:
            probabilities[person]['gene'][1] = probabilities[person]['gene'][1] + p
            if person in have_trait:
                 probabilities[person]['trait'][True] = probabilities[person]['trait'][True] + p
            if person not in have_trait:
                probabilities[person]['trait'][False] = probabilities[person]['trait'][False] + p
        
        if person in two_genes:
            probabilities[person]['gene'][2] = probabilities[person]['gene'][2] + p
            if person in have_trait:
                 probabilities[person]['trait'][True] = probabilities[person]['trait'][True] + p
            if person not in have_trait:
                probabilities[person]['trait'][False] = probabilities[person]['trait'][False] + p

def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    
    for person in probabilities:
        gene_total_value = probabilities[person]['gene'][2] + probabilities[person]['gene'][1] + probabilities[person]['gene'][0]
        probabilities[person]['gene'][2] = probabilities[person]['gene'][2]/gene_total_value
        probabilities[person]['gene'][1] = probabilities[person]['gene'][1]/gene_total_value
        probabilities[person]['gene'][0] = probabilities[person]['gene'][0]/gene_total_value

        trait_total_value = probabilities[person]['trait'][True] + probabilities[person]['trait'][False]
        probabilities[person]['trait'][True] = probabilities[person]['trait'][True]/trait_total_value
        probabilities[person]['trait'][False] = probabilities[person]['trait'][False]/trait_total_value


if __name__ == "__main__":
    main()
