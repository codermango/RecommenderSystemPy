'''
Created on Mar 2, 2015

@author: M
'''

class Genre:
    
    genreId = ''
    genreName = ''
    genreWeight = ''
    isOwned = False
    
    
class Movie:
    movieId = ''
    movieName = ''
    movieGenres = []
    
    def get_num_of_genres(self):
        num = 0
        for k in self.movieGenres:
            if k.isOwned:
                num += 1 
        return num
    
    def get_genres_name(self):
        genres = []
        for k in self.movieGenres:
            genres.append(k.genreName)
        return genres    
    
    
class User:
    likedMovies = []
    
    
    
    