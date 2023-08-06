class Movie:
    def __init__(self, json_obj):
        self._id = json_obj['_id']
        self.name = json_obj['name']
        self.runtimeInMinutes = json_obj['runtimeInMinutes']
        self.budgetInMillions = json_obj['budgetInMillions']
        self.boxOfficeRevenueInMillions = json_obj['boxOfficeRevenueInMillions']
        self.academyAwardNominations = json_obj['academyAwardNominations']
        self.academyAwardWins = json_obj['academyAwardWins']
        self.rottenTomatoesScore = json_obj['rottenTomatoesScore']


    def __str__(self):
        return f'<Movie id="{self._id}">'
    

    def __repr__(self):
        return f'<Movie id="{self._id}">'