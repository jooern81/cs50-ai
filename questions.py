import nltk
import sys
import os 
import numpy as np

# nltk.download('stopwords')

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    
    file_name_dict = {}
    dir_path = os.getcwd() #get current working directory
    corpus_path = os.path.join(dir_path,directory)
    
    for filename in os.listdir(corpus_path):
        if filename.endswith(".txt"):
            f = open(os.path.join(dir_path,directory,filename), encoding="utf8")
            lines = f.read()
            file_name_dict[filename] = lines
            
    return(file_name_dict)
      
    


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    document = document.lower()
    document = nltk.word_tokenize(document) #it is now a list of words
    for word in document.copy():
        if word in nltk.corpus.stopwords.words("english") or word.isalpha == False:
            document.remove(word)
    return(document)
            
def count_files_with_word(documents,word):
    count = 0
    for text in documents:
        if word in documents[text]:
            count += 1
    return count
            

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    
    idf_value_dict = {}
    
    for text in documents:
        words = documents[text]
        for word in words:
            if word not in idf_value_dict:
                    idf_value_dict[word] = np.log(len(documents)/count_files_with_word(documents, word))
                    
    return idf_value_dict
            



def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    scored_files_list = []
    top_n_files = []
    
    for file in files:
        total_tf_idf_score = 0
        list_of_words = files[file]
        
        for word in set(list_of_words):
            if word in query:
                tf = list_of_words.count(word)
                idf = float(idfs[word])
                tf_idf = tf * idf
                total_tf_idf_score += tf_idf
                
        scored_files_list.append((file,total_tf_idf_score))
        
    scored_files_list.sort(key = lambda x: -x[1])
    
    for index in range(0,n):
        top_n_files.append(scored_files_list[index][0])
        
    return top_n_files


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    
    scored_sentences_list = []
    top_n_sentences = []
    
    for sentence in sentences:
        total_idf_score = 0
        query_density = 0
        list_of_words = sentences[sentence]
        
        
        for word in set(list_of_words):
            if word in query:
                idf = float(idfs[word])
                total_idf_score += idf
                query_density += 1/len(query)
                
        scored_sentences_list.append((sentence,total_idf_score,query_density))
    
    scored_sentences_list = sorted(scored_sentences_list, key = lambda x: (-x[1], -x[2]))
    
        
    for index in range(0,n):
        top_n_sentences.append(scored_sentences_list[index][0])
        
        
    return top_n_sentences


if __name__ == "__main__":
    main()
