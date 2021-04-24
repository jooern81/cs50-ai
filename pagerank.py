import os
import random
import re
import sys
import copy

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    
    probability_distribution = {}
    print("Page is: " + str(page))
    linked_pages = corpus[page] #returns the set of all pages linked to by the page
    
    for page in corpus:
        probability = (1 - damping_factor)/len(corpus) 
        if page in linked_pages:
            probability += damping_factor * 1/len(linked_pages)
            probability_distribution[page] = probability
     
    return(probability_distribution)


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    sample_list = []
    
    
    sample_key = random.choice(list(corpus.keys()))
    
    print("Sample key is: " + str(sample_key))
    
    sample_list.append(sample_key)
    
    for sample_count in range(n):
        if len(transition_model(corpus, sample_key, damping_factor)) > 0:
            next_sample_probability_distribution = transition_model(corpus, sample_key, damping_factor)
            sample_key = random.choices(list(next_sample_probability_distribution.keys()),list(next_sample_probability_distribution.values()))[0]
            sample_list.append(sample_key)
        else:
            sample_key = random.choice(list(corpus.keys()))
            
        
    pagerank_dict = {}
    
    for sample in sample_list:
        if sample not in list(pagerank_dict.keys()):
            pagerank_dict[sample] = sample_list.count(sample)/len(sample_list)
        
    return(pagerank_dict)


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    previous_pagerank = {}
    current_pagerank = {}
    
    
    #initiate pagerank
    
    for page in list(corpus.keys()):
        current_pagerank[page] = 1/len(list(corpus.keys()))
        
        print("Initiated pagerank: " + str(current_pagerank))
    
    largest_error = 1
    
    while largest_error > 0.001:
        previous_pagerank = copy.deepcopy(current_pagerank)
        for page in list(corpus.keys()):
            probability_visit_page = 0
            for other_pages in list(corpus.keys()):
                if page in corpus[other_pages]:
                    print('Page is: ' + str(page))
                    print("Corpus[page] is: " + str(corpus[page]))
                    probability_visit_page += damping_factor * (current_pagerank[other_pages]/len(corpus[other_pages]))
                    print("Probability of visiting page: " + str(probability_visit_page))
                if len(corpus[page]) == 0:
                    for page in current_pagerank:
                        probability_visit_page += damping_factor * (1/len(current_pagerank))
                    
                
            current_pagerank[page] = (1 - damping_factor)/len(list(corpus.keys())) + probability_visit_page
            
            #normalize probabilities after changing the probability for all pages
            for page in current_pagerank:
                current_pagerank[page] = current_pagerank[page]/sum(list(current_pagerank.values()))
                print("Normalized page rank: " + str(current_pagerank))
            
            #find the error between the previous iteration pagerank and current interation pagerank
            for page in current_pagerank:
                error_list = []
                print("Current pagerank: " + str(current_pagerank))
                print("Previous pagerank: " + str(previous_pagerank))
                error = abs(current_pagerank[page] - previous_pagerank[page])
                error_list.append(error)
                
            largest_error = max(error_list)
            print("Largest error: " + str(largest_error))
            print("Sum of Values: " + str(sum(list(current_pagerank.values()))))
            

    return(current_pagerank)


if __name__ == "__main__":
    main()
