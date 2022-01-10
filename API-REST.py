"""
APIS involucradas: 

TestDive y OMDB
* relacionar peliculas para una lista completa de titulos.
* ordenar acorde a la puntuacion de Rotten Tomatoes
"""

# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages
# get_sorted_recommendations(["Bridesmaids", "Sherlock Holmes"])
import requests_with_caching
import json

def get_movies_from_tastedive(title):
    baseUrl = "https://tastedive.com/api/similar"
    params = {}
    
    params['q'] = title
    params['type'] = "movies"
    params['limit']= "5"
    
    response = requests_with_caching.get(baseUrl, params=params)
    
    return response.json()

def extract_movie_titles(d):
    titles = []
    for t in d['Similar']['Results']:
        titles.append(t['Name'])
        
    return titles

def get_related_titles(myList):
    titleMovies = [] 
    for p in myList:
        movies = get_movies_from_tastedive(p)
        singleTitle = extract_movie_titles(movies)
        
        titleMovies.extend(singleTitle)
    
    return list(set(titleMovies))

def get_movie_data(title):
    baseUrl = "http://www.omdbapi.com/"
    params = {}
    
    params['t'] = title
    params['r'] = "json"
    
    response = requests_with_caching.get(baseUrl, params=params)
    
    return response.json()

def get_movie_rating(d):
    value = 0
    for t in d['Ratings']:
        if 'Rotten Tomatoes' in t['Source']:
            value = int(t['Value'][:2])
            
    return  value

def get_sorted_recommendations(mylist):
    titulos = get_related_titles(mylist)
    datos = {}
  
    for movie in titulos:
        d = get_movie_rating(get_movie_data(movie))
        datos[movie] = d
        
    orden = [x[0] for x in sorted(datos.items(), 
                                  key=lambda titulo:(titulo[1], titulo[0]), 
                                  reverse=True)]
    return orden

#print(get_sorted_recommendations(["Bridesmaids", "Sherlock Holmes"]))





