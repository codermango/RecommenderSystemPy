#coding=utf-8
import json
from MovieInfo import *
from types import InstanceType
import random
import math


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
            movie.movieGenres = jsonMovie['genres']
            
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
    
    
    #############################################################################
    def get_TFIDF(self, userPreferenceVector,  totalNumOfGenreInLikedMovies, totalGenreInAllMovies):
        numOfGenreInAllMovies = self.get_sum_of_genre_vector_in_all_movies(self.allMovieList) # 所有标签在所有电影中出现的次数
        numOfGenreInLikedMovies = userPreferenceVector;

        print "用户喜好列表中Genre的总数：", totalNumOfGenreInLikedMovies
        print "所有电影中Genre总数：", totalGenreInAllMovies
        print numOfGenreInAllMovies, numOfGenreInLikedMovies

        tfidfVector = []
        for k in range(0, len(numOfGenreInLikedMovies)):
            num1 = numOfGenreInLikedMovies[k]
            num2 = numOfGenreInAllMovies[k]
            
            ifidf = None
            if num2 == 0:
                ifidf = 0
            else:
                ifidf = (float(num1) / float(totalNumOfGenreInLikedMovies)) / (float(num2) / float(totalGenreInAllMovies))
                         
            tfidfVector.append(ifidf)
        
        return tfidfVector


    def get_sum_of_genre_vector_in_all_movies(self, movieList):
        #以第一个电影的标签值初始化
        sumVector = self.get_genre_vector_from_movie(movieList[0])

        for i in range(1, len(movieList)):
            movie = movieList[i]
            vector = self.get_genre_vector_from_movie(movie)
            sumVector = list(map(lambda x: x[0]+x[1], zip(sumVector, vector))) 

        return sumVector
    
    
    def get_genre_vector_from_movie(self, movie):
        genreVector = []
        genreList = movie.movieGenres
        
        for genre in genreList:
            if genre.isOwned:
                genreVector.append(1)
            else:
                genreVector.append(0)
        return genreVector
    
    def get_relevant_movies(self, tfidfVector, allMovieList):
        irrelevantGenreId = []
        relevantMovies = allMovieList;

        for i in range(0, len(tfidfVector)):
            if tfidfVector[i] == 0.0:
                irrelevantGenreId.append(i)

        for k in irrelevantGenreId:
            irrelevantId = k
            
            for movie in relevantMovies:
                genres = movie.movieGenres
                if genres[irrelevantId].isOwned:
                    relevantMovies.remove(movie)

        return relevantMovies;
    
    def get_cos_values(self, relevantMovies, tfidfVector):
        cosValues = {}

        for movie in relevantMovies:
            genreVector = self.get_genre_vector_from_movie(movie)

            # 计算余弦值
            num1 = 0.0  # num1=a1*b1+a2*b2+a3*b3
            num2 = 0.0  # num2=sqrt(a1^2+a2^2+a3^2) * sqrt(b1^2+b2^2+b3^2)

            for i in range(0, len(tfidfVector)):
                num1 += tfidfVector[i] * genreVector[i]

            tmp1 = 0.0
            tmp2 = 0.0
            for i in range(0, len(tfidfVector)):
                tmp1 += math.sqrt(tfidfVector[i] ** 2)  
                tmp2 += math.sqrt(genreVector[i] ** 2) 
                
            num2 = tmp1 * tmp2
            print num1, num2
            cos = 0.0
            if num2 != 0:
                cos = num1 / num2
            else:
                cos = 0.0
            #cosValues[movie.movieId, cos]
            cosValues.setdefault(movie.movieId, cos)
        return cosValues
    
    
    def get_recommended_movieId(self, cosValues, numOfRecommendedMovies):
        sortedItems = sorted(cosValues.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
        for k in range(0, 101):
            print sortedItems[k]
        
    #############################################################################
    
        
     
    def recommend(self, userPreferenceVector, numOfRecommendedMovies, totalNumOfGenreInLikedMovies, totalGenreInAllMovies):
        # 计算标签的TF-IDF
        tfidfVector = self.get_TFIDF(userPreferenceVector,  totalNumOfGenreInLikedMovies, totalGenreInAllMovies)
        print tfidfVector
        # 剔除向量空间标签为0的电影，返回新电影列表
        relevantMovies = self.get_relevant_movies(tfidfVector, self.allMovieList)
        print 'relevant movies: ', relevantMovies.__len__()
        
        # 获取relevantMovies中电影和TF-IDF进行余弦相似计算后的列表
        cosValues = self.get_cos_values(relevantMovies, tfidfVector)
        print cosValues
        
        # 以value排序，取得前numOfRecommendedMovies个电影，作为推荐电影
        recommendedMovieId = self.get_recommended_movieId(cosValues, numOfRecommendedMovies)
        print recommendedMovieId
#         return recommendedMovieId;
     
    def show_movies(self):
        for k in self.moviesDic:
            movieId = k 
            movie = self.moviesDic[k]
            
            genres = []
            for genre in movie.movieGenres:
                
                if genre.isOwned:
                    genres.append(genre.genreName)

            print movieId, movie.movieName, genres
 
 
 
#############################################################################################################        

    
def get_genrevector_from_movieid(movieId):
    vector = []
    movie = cbr.moviesDic[movieId]
    for k in movie.movieGenres:
        if k.isOwned:
            vector.append(1)
        elif not k.isOwned:
            vector.append(0)
    
    #print vector
    return vector
    
def get_sum_of_genre_vector(userLikedMovieId):
    v0 = get_genrevector_from_movieid(userLikedMovieId[0])
    v1 = get_genrevector_from_movieid(userLikedMovieId[1])
    
    sumVector = list(map(lambda x: x[0]+x[1], zip(v0, v1)))
    
    for k in range(2, len(userLikedMovieId)):
        
        v = get_genrevector_from_movieid(userLikedMovieId[k])

        sumVector = list(map(lambda x: x[0]+x[1], zip(sumVector, v)))  
        
    return sumVector


def get_total_num_of_genre_in_liked_movies(userLikedMovieId):
    num = 0
    for k in userLikedMovieId:
        movie = cbr.moviesDic[k]
        num += movie.get_num_of_genres()

    return num


def get_total_genre_in_all_movies():
    total = 0
    for k in cbr.allMovieList:
        total += k.get_num_of_genres()

    return total



#########################################################################################################################################

cbr = CBRecommender()
cbr.show_movies()

#生成测试数据
numOfMovies = len(cbr.allMovieList)
print numOfMovies
userLikedMovieId = []
for i in range(1, 51):
    userLikedMovieId.append(str(i))


#把userLikedList中的Movie的genre各项相加,生成uerPreferenceVector
userPreferenceVector = get_sum_of_genre_vector(userLikedMovieId);
print userPreferenceVector


numOfRecommendedMovies = 100

totalNumOfGenreInLikedMovies = get_total_num_of_genre_in_liked_movies(userLikedMovieId)
print totalNumOfGenreInLikedMovies

totalGenreInAllMovies = get_total_genre_in_all_movies()
print totalGenreInAllMovies

# 推荐
recommendedMovieId = cbr.recommend(userPreferenceVector, numOfRecommendedMovies, totalNumOfGenreInLikedMovies, totalGenreInAllMovies)
print recommendedMovieId











































































































