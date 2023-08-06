import json
import requests
from .models.movie import Movie
from .models.quote import Quote

class LOTR:
    """
    The LOTR class manages the different endpoints for the LOTR API and returns Python-friendly objects.
    It currently provides access to a list of movies and a list of quotes.
    :param token: str - The authorization token needed to access the API.

    LOTR methods include:
    * get_movies(**kwargs)
    * get_movie_by_id(get_movie_by_id)
    * get_quotes_by_movie_id(movie_id, **kwargs)
    * get_quotes(self, **kwargs)
    * get_quote_by_id(self, quote_id)

    The kwargs allowed for all of the methods above include:
    * limit: int - Limit the amount of movies/quote objects.
    * page: int - Set the page number, assuming a limit is placed.
    * offset: int - Set the offset of the objects.
    * sort_by: str - Sort by any of the values within individual movie/quote objects.
    * reverse_sort: bool - If True, then reverses the order to descending.
    * filters: dict - A set of possible filters such as matching movie names (described below).

    Filters
    Add any of these filters to filter the movies or quotes from the API.
    Note that these are in dictionary format.
    
    Include a value(s) within an object. Use a string for one value or a list for multiple values.
    * match: tuple(match_key: str, match_value: str | list) - Example: filters={'match': ('name': 'The Two Towers')}
    
    Exclude a value(s) within an object. Use a string for one value or a list for multiple values.
    * not_match: tuple(match_key: str, match_value: str | list) - Example: filters={'not_match': ('name': 'The Two Towers')}

    Include a value within an object using a regex. Use only strings.
    * re_match: tuple(match_key: str, match_value: str) - Example: filters={'re_match': ('name': '[aeiou]{2}')}

    Exclude a value within an object using a regex. Use only strings.
    * re_not_match: tuple(match_key: str, match_value: str) - Example: filters={'re_not_match': ('name': '[aeiou]{2}')}

    Use >, >=,  <, or <= to compare a value within an object. Use only strings.
    * compare: tuple(match_key: str, match_value: str) - Example: filters={'compare': ('runtimeInMinutes', '>240')}

    Include a value as long as it exists within the object.
    * exist: match_key: str - Example: filters={'exist': 'rottenTomatoesScore'}
    
    Include a value as long as it does not exist within the object.
    * not_exist: match_key: str - Example: filters={'not_exist': 'rottenTomatoesScore'}
    """
    def __init__(self, token=None):
        self.token = token
        self.baseURL = 'https://the-one-api.dev/v2'


    def get_request(self, endpoint: str, **kwargs):
        """
        get_request performs an HTTP request and checks for certain status codes.
        :param endpoint: str - The API endpoint of the Lord of the Rings API.
        :param kwargs: dict - Keyword arguments for pagination, sorting, and filtering.
        :return: Returns a dictionary of the API content.
        """
        queries = self.get_queries(kwargs)
        r = requests.get(
            url=f'{self.baseURL}{endpoint}{queries}',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        if r.status_code == 401:
            raise Exception('Error 401. You need to add an authorization token to the LOTR class to access this API endpoint.')
        elif r.status_code != 200:
            raise Exception(r.status_code)
        return json.loads(r.content)
    

    def get_queries(self, kwargs):
        """
        get_queries parses all the keyword arguments from the get_request method.
        :param kwargs: dict - Keyword arguments for pagination, sorting, and filtering.
        :return: A URL-friendly string to add to the end of the API call.
        """
        if 'kwargs' not in kwargs:
            return ''
        
        params = []
        queries = kwargs['kwargs']
        for key, value in queries.items():
            # Parse the pagination keyword arguments.
            if key in ['limit', 'page', 'offset']:
                params.append(f'{key}={value}')
            # Parse the sorting keyword arguments.
            elif key == 'sort_by':
                if 'reverse_sort' in queries and queries['reverse_sort']:
                    params.append(f'sort={value}:desc')
                else:
                    params.append(f'sort={value}:asc')
            # Parse the filter keyword arguments.
            elif key == 'filters':
                for filter_key in value:
                    params.append(self.parse_filter_args(value, filter_key))
                    
        return '?' + '&'.join(params)
    

    def parse_filter_args(self, filter_dict, key):
        """
        parse_filter_args parses all the filter keyword argument from the get_request method.
        :param kwargs: dict - Keyword arguments for filtering.
        :return: A URL-friendly string to add to the end of the API call.
        """
        if key in ['match', 'not_match', 're_match', 're_not_match', 'compare']:
            match_key, match_value = filter_dict[key]
            if 'match' in filter_dict:
                match_value = ','.join(match_value) if isinstance(match_value, list) else match_value
                return f'{match_key}={match_value}'
            elif 'not_match' in filter_dict:
                match_value = ','.join(match_value) if isinstance(match_value, list) else match_value
                return f'{match_key}!={match_value}'
            elif 're_match' in filter_dict:
                return f'{match_key}=/{match_value}/i'
            elif 're_not_match' in filter_dict:
                return f'{match_key}!=/{match_value}/i'
            elif 'compare' in filter_dict:
                match_key, match_value = filter_dict['compare']
                return f'{match_key}{match_value}'
        elif key == 'exist':
            return filter_dict['exist']
        elif key == 'not_exist':
            return f'!{filter_dict["exist"]}'
        else:
            raise Exception(f'The filter key `{key}` does not exist.')


    def get_movies(self, **kwargs):
        """
        get_movies does a request for all the movies based on the pagination, sorting, and filtering criteria.
        :param kwargs: dict - Keyword arguments for pagination, sorting, and filtering.
        :return: A list of Movie objects of each matching movie.
        """
        movies = self.get_request('/movie', kwargs=kwargs)
        return [Movie(movie) for movie in movies['docs']]
    

    def get_movie_by_id(self, movie_id):
        """
        get_movies_by_id does a request for a single movies based on a movie id.
        :param movie_id: str - A string of the movie id.
        :return: A Movie object for the matching movie.
        """
        movie = self.get_request(f'/movie/{movie_id}')
        return Movie(movie['docs'][0])
    

    def get_quotes_by_movie_id(self, movie_id, **kwargs):
        """
        et_quotes_by_movie_id does a request for all the quotes from a single movie based on a movie id.
        :param movie_id: str - A string of the movie id.
        :param kwargs: dict - Keyword arguments for pagination, sorting, and filtering.
        :return: A list of Quote objects for the matching movie.
        """
        quotes = self.get_request(f'/movie/{movie_id}/quote', kwargs=kwargs)
        return [Quote(quote) for quote in quotes['docs']]
    

    def get_quotes(self, **kwargs):
        """
        get_quotes does a request for all the quotes based on the pagination, sorting, and filtering criteria.
        :param kwargs: dict - Keyword arguments for pagination, sorting, and filtering.
        :return: A list of Quote objects from every movie.
        """
        quotes = self.get_request('/quote', kwargs=kwargs)
        return [Quote(quote) for quote in quotes['docs']]
    

    def get_quote_by_id(self, quote_id):
        """
        get_quote_by_id does a request for a single quote based on a quote id.
        :param quote_id: str - A string of the quote id.
        :return: A Quote object for the matching quote.
        """
        quote = self.get_request(f'/quote/{quote_id}')
        return Quote(quote['docs'][0])
    
