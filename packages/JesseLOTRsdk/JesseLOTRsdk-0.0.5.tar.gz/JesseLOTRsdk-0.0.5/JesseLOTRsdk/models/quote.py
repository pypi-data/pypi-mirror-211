class Quote:
    def __init__(self, json_obj):
        self._id = json_obj['_id']
        self.dialog = json_obj['dialog']
        self.movie = json_obj['movie']
        self.character = json_obj['character']

    def __str__(self):
        return f'<Quote id="{self._id}">'
    

    def __repr__(self):
        return f'<Quote id="{self._id}">'