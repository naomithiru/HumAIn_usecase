# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # Keyword extraction using TextRank
# %% [markdown]
# ## Preprocessing & Keyword extraction 

# %%
#### EXTRACT KEYWORDS FROM TEXTS #### 

def get_text_keywords(docs: list, scores: bool) -> list, list:

    """This function gets a list of texts and returns 1) a list with nested lists, each of which corresponds to the keywords of each text; 2) a list of texts after cleaning and lemmatization"""

    # Import libraries
    import spacy
    import re

    # Import class from py module (required)
    from textrank4keyword import TextRank4Keyword

    # init spacy nlp object
    nlp = spacy.load("en_core_web_sm")

    # remove punctuations
    docs = [re.sub('[^a-zA-Z]', ' ', text) for text in docs]
    
    # convert to lowercase
    # docs = [text.lower() for text in docs]
    
    # remove tags
    docs = [re.sub("&lt;/?.*?&gt;"," &lt;&gt; ",text) for text in docs]
    
    # remove special characters and digits
    docs = [re.sub("(\\d|\\W)+"," ",text) for text in docs]

    texts_nlp = [nlp(doc) for doc in docs]

    # lemmatize text before extracting keywords
    lemmatized = [" ".join([token.lemma_ for token in text]) for text in texts_nlp]

    ## Generate keywords with TextRank4Keyword class
    # init textrank object
    tr4w = TextRank4Keyword()

    # apply TextRank to all texts in the dataset and store a list of keywords for each text
    list_of_keywords_lists_w3 = []

    for doc in lemmatized:
        # We only include Nouns (common and proper nouns), a windows-size of 3 and keep words' case
        tr4w.analyze(doc, candidate_pos = ['NOUN', 'PROPN'], window_size=3, lower=False)
        list_of_keywords_lists_w3.append(tr4w.get_keywords(7))

    # return list of lists of keywords with or without scores
    list_of_keywords_lists = []

    # decide whether you want the list with keywords' scores or not
    if scores == True:
        list_of_keywords_lists = list_of_keywords_lists_w3
    else:
        for kwlist in list_of_keywords_lists_w3:
            kw_list = [kw for kw, value in kwlist]
            list_of_keywords_lists.append(kw_list)
            
    # return the lists
    return list_of_keywords_lists, lemmatized

# %% [markdown]
# ## Post-processing

# %%
#### POST-PROCESSING #### 


def get_cooc_keywords(texts_keywords: list, texts: list) -> list:
"""TextRank requires a post-processing in which we check whether single words in a list of keywords form actually a multiword. We check whether keyword pairs (co-occurrences) occur in their respective text. If so, then the keywords are collapsed into a single keyword."""

    ## Generate all possible pair keyword combinations in all orders ('AB', 'BA')
    import itertools
    combinations_1 = [list(itertools.combinations(kw_list,2)) for kw_list in texts_keywords]

    # Reverse order of tuples elements
    def reverse(tuples): 
        new_tup = tuples[::-1] 
        return new_tup 
    
    combinations_2 = []
    for comb_list in combinations_1:
        lst = [reverse(pair) for pair in comb_list]
        combinations_2.append(lst)

    # Convert tuples into strings for combinations_1 and 2 and save them into two lists
    def convertTuple(tup): 
        str =  ' '.join(tup) 
        return str

    pairs_strings_1 = []
    for comb_list in combinations_1:
        lst = [convertTuple(pair) for pair in comb_list]
        pairs_strings_1.append(lst)

    pairs_strings_2 = []
    for comb_list in combinations_2:
        lst = [convertTuple(pair) for pair in comb_list]
        pairs_strings_2.append(lst)
    
    # Check if combinations of keyword pairings appear in their respective texts. 
    multiword_keyword_list = []

    for i in range(len(texts)):

        pair_list = []

        for j in pairs_strings_1[i]:
            if j in texts[i]:
                pair_list.append(j)
        multiword_keyword_list.append(pair_list)

        for j in pairs_strings_2[i]:
            if j in texts[i]:
                multiword_keyword_list[i].append(j)
    
    ## Merge multiword and singleword keywords in one single list
    single_words = []

    for kw_text, multiword in zip(texts_keywords, multiword_keyword_list):
        pair_list = [w for w in kw_text if w not in str(multiword)]  
        single_words.append(pair_list)

    # Map index of single_words list and multiword list.
    # The result is a nested list that needs to be flatten
    lst_zip = list(zip(single_words, multiword_keyword_list))


    # Function to flatten the list
    def flattenNestedList(nestedList):
        ''' Converts a nested list to a flat list '''
        flatList = []
        # Iterate over all the elements in given list
        for elem in nestedList:
            # Check if type of element is list
            if isinstance(elem, list):
                # Extend the flat list by adding contents of this element (list)
                flatList.extend(flattenNestedList(elem))
            else:
                # Append the element to the list
                flatList.append(elem)    
        return flatList

    # Convert lst_zip into list (zip() returns a tuple)
    fl = [list(elem) for elem in lst_zip]

    # Obtain a single list of keywords with single and multiwords in a single list
    multiword_singleword_keywords_by_text = [flattenNestedList(elem) for elem in fl]

    return multiword_singleword_keywords_by_text

# %% [markdown]
# ## Word and Text embeddings, and cosine similarity

# %%
#### WORD EMBEDDINGS AND COSINE SIMILARITY ####

def flair_embed_docPool(sentence: str) -> Vector :
    """ Embed words with Flair's WordEmbeddings and DocumentPoolEmbeddings (for multi-words)"""

    from flair.embeddings import WordEmbeddings, DocumentPoolEmbeddings, FlairEmbeddings
    from flair.data import Sentence
    
    # init the word embeddings
    flair_embedding_forward = FlairEmbeddings('news-forward')

    # initialize the document embeddings, mode = mean
    document_embeddings = DocumentPoolEmbeddings([flair_embedding_forward])

    # create an example sentence
    sentence = Sentence(sentence)

    # embed the sentence with our document embedding
    document_embeddings.embed(sentence)

    # now check out the embedded sentence.
    return sentence.get_embedding()

# Define function to calculate cosine similarity
def get_cosine_similarity(vector1, vector2):
    from sklearn.metrics.pairwise import cosine_similarity
    return cosine_similarity(vector1.reshape(1, -1), vector2.reshape(1, -1))[0][0]

# Embed words, calculate cosine similarity and get the results (see below) 
def cosine_list(keywords_by_text: list, ai_entities: list) -> list, dict:
    thresh_dicts = {}

    keys_list = []
    values_list = []
    thresh_dict = {}

    threshold = 0.60

    for ai in ai_entities:
        for words_list in keywords_by_text:
            try:
                res = get_cosine_similarity(flair_embed_docPool(words_list), flair_embed_docPool(ai))
                #print(f"The cosine similarity between the keywords in [{words_list}] and [{ai}] is: {res*100}")
                if res > threshold:
                    keys_list.append(ai)
                    values_list.append(round(res*100,3))
            except IndexError:
                pass
        
        for index in range(len(keywords_by_text)):

            thresh_dict = {}
            for i in range(len(keys_list)):
                thresh_dict[keys_list[i]] = values_list[i]
                thresh_dicts[index] = thresh_dict

    list_entities = [value for value in thresh_dicts.items()]

    all_dicts = [x[1] for x in list_entities]

    mother_lst = []

    for a_dict in all_dicts:
        mother_lst.append(sorted(a_dict, key=a_dict.get, reverse=True)[0])

    # Return a list with top1 ai_entities or industries per text, and the dictionary with cosine similarity values > than threshold    
    return mother_lst, thresh_dicts

# %% [markdown]
# ### Run code

# %%
########### Import libraries ###########

import pandas as pd
import numpy as np
import re 
import spacy



########### Load data ###########

## Main data
df = pd.read_csv('all_data.csv')
#df.drop(["Unnamed: 0.1", "Unnamed: 0"], axis = 1, inplace = True)

## List of ai entities
ai_entities = pd.read_csv('custom_entities_def.csv')
ai_ent = ai_entities['Applications'].to_list()

## List of industries
industries = pd.read_csv('industries.csv')
ind = industries['industries'].to_list()



########### Lemmatize industries ###########

nlp = spacy.load("en_core_web_sm")
    
# Convert to lowercase
ind_list = [industry.lower() for industry in ind]
    
# Remove special characters and digits
ind_list = [re.sub("(\\d|\\W)+"," ",industry) for industry in ind_list]

industry_nlp = [nlp(industry) for industry in ind_list]

# We lemmatize industry before extracting keywords
lemmatized_industries = [" ".join([token.lemma_ for token in industry]) for industry in industry_nlp]



########### Prepare data for passing it through functions ###########

## Unify title and text to extract keywords from
df['titext'] = df['title'] + ' ' + df['text']

docs = df['titext'].to_list()


# %%
# ### SAMPLE TO TRY CODE ### 

# Uncomment and execute the lines below if you want to try your code first with a small sample (change n value)

# data_sample = df.sample(n = 2, replace=False, random_state = 123, axis = 0)
# docs = data_sample['titext'].to_list()


# %%
########### GET KEYWORDS ###########

# Get the keywords and the lemmatized text
texts_keywords, lemmatized_text = get_text_keywords(docs, scores = False)

# Get complete keywords
complete_keywords = get_cooc_keywords(texts_keywords, lemmatized_text)

# Save keywords in the dataframe
df['def_keywords'] = complete_keywords


# %%
########### GET RESULTS OF COSINE SIMILARITY ###########

#Get list with keywords by text in string form (needed to proceed to embedding)
keywords_by_text = [" ".join(map(str, text_keywords)) for text_keywords in complete_keywords]

#Execute word embeddings + cosine similarity between each keyword list and each AI usecase/entity
top1_ai_entities, entities_above_threshold = cosine_list(keywords_by_text, ai_ent)
#top1_ai_entities

#Execute word embeddings + cosine similarity between each keyword list and each industry
top1_industries, industries_above_threshold = cosine_list(keywords_by_text, lemmatized_industries)
#top1_industries


# %%
##### SAVE RESULTS IN THE DF AND IN A CSV FILE ####

df["top1_entities"] = top1_ai_entities
df["top1_industries"] = top1_industries

# Select the columns that you need
data_final = df[["title","text","date","source","top1_entities","top1_industries"]]
data_final.to_csv('results.csv')


