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
        return len(self.movieGenres)
    
    
class User:
    likedMovies = []
    
    
    
    