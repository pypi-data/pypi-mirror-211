# %%
# Function imports
import pandas as pd
import numpy as np
import string
import re
from fuzzywuzzy import fuzz
from fuzzywuzzy import process




# %%
# Function to clean the datasets
def clean_ratings(df_ratings_input, df_books_input, n_ratings_to_keep_books=25, n_ratings_to_keep_users=25, use_implicit='no'):

    df_ratings = df_ratings_input.copy()
    df_books = df_books_input.copy()

    # Get unique ISBNs in both dfs
    a_ratings_ISBN = df_ratings.ISBN.unique()
    a_books_ISBN = df_books.ISBN.unique()
    # And filter ratings down to only ISBNS in the books df
    df_ratings = df_ratings.query('ISBN in @a_books_ISBN').reset_index(drop=True)

    # Compress a couple authors into the same author
    d_author_replace = {
        'Dean R. Koontz': 'Dean Koontz'
        }
    df_books['Book-Author'] = df_books['Book-Author'].replace(d_author_replace)

    # Now deal with there being many ISBNs for the same book in the eeasiest way possible
    # Group by (cleaned) title author combo, to create a parent isbn
    # Then remap the ratings isbns to that new parent
    # The raw list here is kind of dumb, but effective for the popular authors and I got in too deep
    l_replace_general = [
        "'"
        , 'Uncut Edition', 'Oprahs Book Club'
        , 'A Stephanie Plum Novel', 'Stephanie Plum Novels', 'Janet Evanovichs Full Series'
        , 'Lives of the Mayfair Witches', 'Or There and Back Again', ': The Enchanting Prelude to The Lord of the Rings'
        , 'Grafton, Sue. Kinsey Millhone Mysteries.'
        , 'Kinsey Millhone Mysteries', 'A Kinsey Millhone Mystery', 'Tom Clancys Op Center'
        , 'Tom Clancys Power Plays', 'Dollanger Saga', ': A Memoir', 'An Anita Blake, Vampire Hunter Novel'
        , 'An Alex Delaware Novel', ': The Nice and Accurate Prophecies of Agnes Nutter, Witch'
        , ': A Fairy Story'
        ]
    l_replace_general = [item.lower() for item in l_replace_general]
    l_replace_general.sort(key=len, reverse=True)
    l_replace_other = [
        "'"
        , 'the', 'and', '&', 'amp'
        , 'Paperback', 'Hardcover', 'Paper', 'A Novel', 'Anniversary edition', 'A memoir'
        , 'Large print', 'reissue'
        , ' a ', 'ss ', 's '
        ]
    l_replace_other = [item.lower() for item in l_replace_other]
    l_replace = l_replace_general + l_replace_other
    # Function for string replace
    def string_simplify(s):
        s = s.lower()
        for item in l_replace:
            s = s.replace(item, '')
        s = re.sub("\(.*\)", '', s)
        s = re.sub('ss$', '', s) # This weird bit helps handle apostrophe s combinations that weren't already handled
        s = re.sub('s$', '', s)
        s = s.replace(' ', '').translate(str.maketrans('', '', string.punctuation))
        return s
    # Initial setup for this
    df_books.fillna('Unknown', inplace=True)
    df_books['title_simple'] = df_books['Book-Title'].apply(string_simplify)
    df_books['author_simple'] = df_books['Book-Author'].apply(string_simplify)
    df_books['title_author_key'] = df_books.title_simple + df_books.author_simple
    df_books.sort_values(by='Year-Of-Publication', ascending=False, inplace=True) # arbitrarily keep the first
    # Create a unique set by title-author in order to create a dictionary mapping
    df_books_unique = df_books.drop_duplicates(subset='title_author_key', keep='first')
    d_title_author_isbn = dict(zip(df_books_unique.title_author_key, df_books_unique.ISBN))
    # Map the parent back to all entries in the books df
    df_books['ISBN_parent'] = df_books.title_author_key.apply(lambda x: d_title_author_isbn[x])
    # Now get the child to parent mappings and apply those to the ratings df
    d_isbn_isbnparent = dict(zip(df_books.ISBN, df_books.ISBN_parent))
    df_ratings['ISBN'] = df_ratings.ISBN.apply(lambda x: d_isbn_isbnparent[x])
    # Now clean back up the books df dropping down to one row per parent
    df_books['ISBN'] = df_books.ISBN_parent
    df_books = df_books.drop_duplicates(subset='ISBN', keep='first').reset_index(drop=True)
    df_books.drop(columns=['title_simple', 'author_simple', 'title_author_key', 'ISBN_parent'], inplace=True)

    # Now, regardless of other choices, remove users that have no nonzero ratings
    df_user_max_all = df_ratings.groupby('User-ID')[['Book-Rating']].max().reset_index()
    l_nonzero_users = df_user_max_all.query('`Book-Rating` > 0')['User-ID'].unique().tolist()
    df_ratings = df_ratings.query('`User-ID` in @l_nonzero_users').reset_index(drop=True)

    # If we want to use the implicit ratings, some handling below
    # Basic case, add 1 to keep it from the nonzero group
    if use_implicit == 'yes':
        df_ratings['Book-Rating'] = df_ratings['Book-Rating'] + 1
    # Or replace 0s with the mean user rating
    elif use_implicit == 'as mean':
        df_user_means_nonzero = df_ratings.query('`Book-Rating` > 0')\
            .groupby('User-ID')[['Book-Rating']].mean()\
            .reset_index()
        d_user_mean = dict(zip(df_user_means_nonzero['User-ID'], df_user_means_nonzero['Book-Rating']))
        df_ratings['Book-Rating'] = df_ratings.apply(lambda x:
                                                     d_user_mean[x['User-ID']] if int(x['Book-Rating']) == 0 else x['Book-Rating']
                                                     , axis=1)
    # Or replace with the lower quantile
    elif use_implicit == 'as quantile':
        df_user_means_nonzero = df_ratings.query('`Book-Rating` > 0')\
            .groupby('User-ID')[['Book-Rating']].quantile(0.25)\
            .reset_index()
        d_user_mean = dict(zip(df_user_means_nonzero['User-ID'], df_user_means_nonzero['Book-Rating']))
        df_ratings['Book-Rating'] = df_ratings.apply(lambda x:
                                                     d_user_mean[x['User-ID']] if int(x['Book-Rating']) == 0 else x['Book-Rating']
                                                     , axis=1)     
    # Otherwise leave things alone
    else:
        pass

    # Get unique ISBNs in both dfs (again in case used by code below)
    a_ratings_ISBN = df_ratings.ISBN.unique()
    a_books_ISBN = df_books.ISBN.unique()

    # Create a copy df of ratings without nonzero values
    df_ratings_nonzero = df_ratings.query('`Book-Rating` > 0').reset_index(drop=True).copy()

    # Now determine which books to keep based on how many times they show up in the ratings
    s_books_values = df_ratings_nonzero.ISBN.value_counts()
    l_books_keep = s_books_values[s_books_values > n_ratings_to_keep_books].index.to_list()
    print(f'You are keeping a total of {len(l_books_keep)} books out of {len(s_books_values)}.')

    # Now remove books with not enough ratings from our dfs
    df_ratings = df_ratings.query('ISBN in @l_books_keep').reset_index(drop=True)
    df_ratings_nonzero = df_ratings_nonzero.query('ISBN in @l_books_keep').reset_index(drop=True)

    # Similarly, determine which users to keep based on how many nonzero ratings
    s_user_ratings = df_ratings_nonzero['User-ID'].value_counts()
    l_users_keep = s_user_ratings[s_user_ratings >= n_ratings_to_keep_users].index.to_list()
    print(f'You are keeping a total of {len(l_users_keep)} users out of {len(s_user_ratings)}.')

    # Remove users accordingly
    df_ratings = df_ratings.query('`User-ID` in @l_users_keep').reset_index(drop=True)
    df_ratings_nonzero = df_ratings_nonzero.query('`User-ID` in @l_users_keep').reset_index(drop=True)

    # Now downfilter the books dataframe to only books left with ratings
    l_books_remaining = df_ratings_nonzero.ISBN.unique().tolist()
    df_books = df_books.query('ISBN in @l_books_remaining').reset_index(drop=True)

    # Because we are using the parent ISBN in the ratings, it's now possible to have duplicate ratings
    # In these cases (i.e. n children on one parent) we will take the mean, so grouping the ratings works
    df_ratings = df_ratings.groupby(['User-ID', 'ISBN'])[['Book-Rating']].mean().reset_index()
    df_ratings_nonzero = df_ratings_nonzero.groupby(['User-ID', 'ISBN'])[['Book-Rating']].mean().reset_index()

    return df_ratings_nonzero, df_books




# %%
# The actual class for the book recommender
class BookRecommender():

    def __init__(self):

        self.d_isbn_idx = None
        self.d_idx_isbn = None
        self.d_isbn_title = None
        self.df_books = None
        self.d_isbn_count = None
        self.embeddings = None
        self.dot_prod = None

    def store_metadata(self, df_matrix, df_books, df_ratings):

        # Get list of isbns and corresponding indices
        l_isbns = df_matrix.index.to_list()
        a_isbn_idx = np.arange(0, len(l_isbns))
        # Merge these together into dicts
        d_isbn_idx = dict(zip(l_isbns, a_isbn_idx))
        d_idx_isbn = dict(zip(a_isbn_idx, l_isbns))
        # Store in the class
        self.d_isbn_idx = d_isbn_idx
        self.d_idx_isbn = d_idx_isbn

        # Now create isbn to title map from books metadata
        d_isbn_title = dict(zip(df_books['ISBN'], df_books['Book-Title']))
        self.d_isbn_title = d_isbn_title

        # Easiest to also just store the books df
        self.df_books = df_books

        # We also want the counts out of df_ratings per ISBN
        # This helps (later) to identify which isbn (of a title) is more common
        s_isbn_counts = df_ratings.ISBN.value_counts()
        self.d_isbn_count = dict(zip(
            s_isbn_counts.index.tolist()
            , s_isbn_counts.values
            ))

    def store_embeddings(self, embeddings):

        self.embeddings = embeddings

    def store_dotprod_function(self, func):

        self.dot_prod = func

    def get_dotprod(self, a1, a2):

        return self.dot_prod(a1, a2)

    def find_isbn_from_title(self, title):

        # Looks up and shows the most similar titles and isbns from a given string
        l_titles = list(self.d_isbn_title.values())
        query_results = process.extractBests(query=title, choices=l_titles, limit=5, scorer=fuzz.token_sort_ratio)
        l_matches = [result[0] for result in query_results]
        l_scores = [result[1] for result in query_results]
        d_match_scores = dict(zip(l_matches, l_scores))
        df_matches = self.df_books.query('`Book-Title` in @l_matches').copy()
        df_matches['match_score'] = df_matches['Book-Title'].apply(lambda x: d_match_scores[x])
        df_matches['ratings_count'] = df_matches['ISBN'].apply(lambda x: self.d_isbn_count[x])
        display(df_matches.sort_values(by='match_score', ascending=False))
    
    def recommend_books(self, isbn, top_n=5):

        # Run the recommendation
        querry_idx = self.d_isbn_idx[isbn]
        querry_ebmedding = self.embeddings[querry_idx]
        a_similarity_scores = self.get_dotprod(self.embeddings, querry_ebmedding)
        a_top_scores = np.sort(a_similarity_scores)[::-1][1:top_n+1]
        a_similar_idxs = a_similarity_scores.argsort()[::-1][1:top_n+1]
        l_similar_isbns = [self.d_idx_isbn[isbn_idx] for isbn_idx in a_similar_idxs]
        d_isbn_score = dict(zip(l_similar_isbns, a_top_scores))

        # Now sculpt the output as a convenient df
        df_similar = self.df_books.query('ISBN in @l_similar_isbns').copy()
        df_similar['similarity_score'] = df_similar.ISBN.apply(lambda x: d_isbn_score[x])
        df_similar.sort_values(by='similarity_score', ascending=False, inplace=True)

        return df_similar