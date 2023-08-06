from dotenv import load_dotenv
import os
import re
from unittest import TestCase
from sdk import LOTR
from models.movie import Movie
from models.quote import Quote

load_dotenv()
TOKEN = os.getenv('TOKEN')

class MountDoomTesting(TestCase):
    def test_passes_when_user_initializes_lotr_without_auth_token(self):
        lotr = LOTR()
        self.assertTrue(lotr.token == None)


    def test_passes_when_user_initializes_lotr_with_auth_token(self):
        lotr = LOTR(token=TOKEN)
        self.assertTrue(lotr.token == TOKEN)

    
    def test_passes_when_user_gets_movie_objects(self):
        lotr = LOTR(token=TOKEN)
        movies = lotr.get_movies()
        for movie in movies:
            self.assertTrue(isinstance(movie, Movie))

    
    def test_passes_when_user_gets_401_error_without_auth_token(self):
        lotr = LOTR()
        with self.assertRaises(Exception) as context:
            lotr.get_movies()
        self.assertTrue('401' in str(context.exception))


    def test_passes_when_user_gets_quote_objects(self):
        lotr = LOTR(token=TOKEN)
        quotes = lotr.get_quotes()
        for quote in quotes:
            self.assertTrue(isinstance(quote, Quote))


    def test_passes_when_user_gets_movie_by_specific_movie_id(self):
        lotr = LOTR(token=TOKEN)
        movies = lotr.get_movies()
        specific_movie = lotr.get_movie_by_id(movies[0]._id)
        self.assertTrue(specific_movie._id == movies[0]._id)


    def test_passes_when_user_gets_quotes_by_specific_movie_id(self):
        lotr = LOTR(token=TOKEN)
        movies = lotr.get_movies()

        two_towers = [movie for movie in movies if movie.name == 'The Two Towers'][0]
        quotes = lotr.get_quotes_by_movie_id(two_towers._id)

        for quote in quotes:
            self.assertTrue(two_towers._id == quote.movie)
            self.assertTrue(isinstance(quote, Quote))


    def test_passes_when_user_gets_quote_by_specific_quote_id(self):
        lotr = LOTR(token=TOKEN)
        movies = lotr.get_movies()
        
        two_towers = [movie for movie in movies if movie.name == 'The Two Towers'][0]
        quotes = lotr.get_quotes_by_movie_id(two_towers._id)

        specific_quote = lotr.get_quote_by_id(quotes[0]._id)
        self.assertTrue(quotes[0]._id == specific_quote._id)


    def test_passes_when_user_sets_limit_to_2_movies(self):
        lotr = LOTR(token=TOKEN)
        movies = lotr.get_movies(limit=2)
        self.assertTrue(len(movies) == 2)


    def test_passes_when_user_sets_sort_to_reverse(self):
        lotr = LOTR(token=TOKEN)
        movies = lotr.get_movies(sort_by='name')
        movies_reverse = lotr.get_movies(sort_by='name', reverse_sort=True)
        for x, y in zip(movies, movies_reverse[::-1]):
            self.assertTrue(x._id == y._id)


    def test_passes_when_user_sets_filter_for_name_match(self):
        lotr = LOTR(token=TOKEN)
        movies = lotr.get_movies(filters={
            'match': ('name', 'The Two Towers')
        })
        self.assertTrue(movies[0].name == 'The Two Towers')


    def test_passes_when_user_sets_filter_for_name_match_to_excude_two_towers(self):
        lotr = LOTR(token=TOKEN)
        movies = lotr.get_movies(filters={
            'not_match': ('name', 'The Two Towers')
        })
        for movie in movies:
            self.assertTrue(movie.name != 'The Two Towers')


    def test_passes_when_user_sets_filter_for_name_to_include_two_movies(self):
        lotr = LOTR(token=TOKEN)
        movies = lotr.get_movies(filters={
            'match': ('name', ['The Fellowship of the Ring', 'The Two Towers'])
        })
        movie_names = sorted([movie.name for movie in movies])
        self.assertTrue(movie_names == ['The Fellowship of the Ring', 'The Two Towers'])

    def test_passes_when_user_sets_filter_for_movie_to_include_rotten_tomatoes_score(self):
        lotr = LOTR(token=TOKEN)
        movies = lotr.get_movies(filters={
            'exist': 'rottenTomatoesScore'
        })
        for movie in movies:
            self.assertTrue(movie.rottenTomatoesScore)

    def test_passes_when_user_sets_filter_for_name_to_include_two_adjacent_vowels(self):
        lotr = LOTR(token=TOKEN)
        movies = lotr.get_movies(filters={
            're_match': ('name', '[aeiou]{2}')
        })
        for movie in movies:
            self.assertTrue(re.search(r'[aeiou{2}]', movie.name))

    
    def test_passes_when_user_sets_filter_for_name_to_exclude_two_adjacent_vowels(self):
        lotr = LOTR(token=TOKEN)
        movies = lotr.get_movies(filters={
            're_not_match': ('name', '[aeiou]{2}')
        })
        for movie in movies:
            self.assertFalse(re.search(r'[aeiou]{2}', movie.name))


    def test_passes_when_user_sets_filter_for_movie_to_be_greater_than_240_minutes(self):
        lotr = LOTR(token=TOKEN)
        movies = lotr.get_movies(filters={
            'compare': ('runtimeInMinutes', '>240')
        })
        for movie in movies:
            self.assertTrue(movie.runtimeInMinutes > 240)
