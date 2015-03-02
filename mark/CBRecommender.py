#coding=utf-8
import json
from MovieInfo import *
from types import InstanceType
import random



class CBRecommender:
    
    moviesDic = {}
    allMovieList = []
    
    def __init__(self):
        f = open('movies.json')
        
        line = f.readline()
        while line:
            #print line
            jsonMovie = json.loads(line)
            
            movie = Movie()
            movie.movieId = jsonMovie['movieId']
            movie.movieName = jsonMovie['movieName']
            #movie.movieGenres = jsonMovie['genres']
            
            genreList = []
            for genreItem in movie.movieGenres:
                
                genre = Genre()
                genre.genreId = genreItem['genre_id']
                genre.genreName = genreItem['genre_name']
                genre.genreWeight = genreItem['genre_weight']
                genre.isOwned = genreItem['is_owned']
                
                genreList.append(genre)
            
            movie.movieGenres = genreList
            self.allMovieList.append(movie)
            self.moviesDic[movie.movieId] = movie           
            
            line = f.readline()
        
    
     
    def show_movies(self):
        for k in self.moviesDic:
            print k, self.moviesDic[k]

        
cbr = CBRecommender()
cbr.show_movies()

#生成测试数据
numOfMovies = len(cbr.allMovieList)
print numOfMovies
userLikedMovieId = []
for i in range(0, 50):
    print i,











































































































