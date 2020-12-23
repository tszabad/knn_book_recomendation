# import libraries (you may add additional imports but you may not have to)
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt

# get data files
!wget https://cdn.freecodecamp.org/project-data/books/book-crossings.zip

!unzip book-crossings.zip

books_filename = 'BX-Books.csv'
ratings_filename = 'BX-Book-Ratings.csv'

# import csv data into dataframes
df_books = pd.read_csv(
    books_filename,
    encoding = "ISO-8859-1",
    sep=";",
    header=0,
    names=['isbn', 'title', 'author'],
    usecols=['isbn', 'title', 'author'],
    dtype={'isbn': 'str', 'title': 'str', 'author': 'str'})

df_ratings = pd.read_csv(
    ratings_filename,
    encoding = "ISO-8859-1",
    sep=";",
    header=0,
    names=['user', 'isbn', 'rating'],
    usecols=['user', 'isbn', 'rating'],
    dtype={'user': 'int32', 'isbn': 'str', 'rating': 'float32'})


combined_rating = pd.merge(df_ratings, df_books, on='isbn')
combined_rating.head()

counts1 = df_ratings['user'].value_counts()
counts2 = df_ratings['isbn'].value_counts()

df_ratings = df_ratings[~df_ratings['user'].isin(counts1[counts1 < 200].index)]
df_ratings = df_ratings[~df_ratings['isbn'].isin(counts2[counts2 < 100].index)]

combined = pd.merge(right=df_ratings, left = df_books, on="isbn")

combined = combined.drop_duplicates(["title", "user"])

combined_pivot = combined.pivot(index='title', columns='user', values='rating').fillna(0) 
combined_pivot.head()

matrix = combined_pivot.values
titles = list(combined_pivot.index.values)
print(titles)

def get_recommends(book = ""):
  
  book1 = titles.index(book)
  query_index = book1
  distances, indices = model_knn.kneighbors(combined_pivot.loc[book].values.reshape(1, -1), len(titles), True)
  recommended_books = [book, sum([[[combined_pivot.index[indices.flatten()[i]], distances.flatten()[i]]] for i in range(3,0,-1)], [])]

  return recommended_books
  
print(get_recommends("Where the Heart Is (Oprah's Book Club (Paperback))"))
