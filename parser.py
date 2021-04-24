import nltk
import sys
nltk.download('punkt')

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj S | NP VP Conj VP
AP -> Adj | Adj AP
NP -> N | Det NP | AP NP | NP PP
PP -> P NP | P S
VP -> V | V NP | V NP PP | V PP | VP Adv | Adv VP
"""
grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)
    print(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return
    
    print(trees)

    # Print each tree with noun phrase chunks
    
    tree = trees[0]

    tree.pretty_print()

    print("Noun Phrase Chunks")
    for np in np_chunk(tree):
        print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    sentence = sentence.lower()
    sentence = nltk.word_tokenize(sentence)
    
    for word in sentence:
        alpha  = False
        for character in word:
            if character.isalpha() == True:
                alpha = True
        if alpha == False:
            sentence.remove(word)  
            # print("Sentence: ")
            # print(sentence)
    return(sentence)

NP_list = []
def return_np_chunks(tree):
    NP_subtree = False
    for subtree in tree.subtrees():
        if subtree.label() == 'NP' and subtree != tree and len(subtree) > 0:
            NP_subtree == True
            # print('Tree is: ')
            # print(tree)
            # print("Subtree is: ")
            # print(subtree)
            return_np_chunks(subtree)
        else:
            1
            # print('No sub trees')
        
        if NP_subtree == False and tree.label() == 'NP' and len(tree) == 1 and (tree not in NP_list):
            # print('Appended the following:')
            # print(tree)
            NP_list.append(tree)
            break
    
def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    return_np_chunks(tree)
    return(NP_list)


if __name__ == "__main__":
    main()
