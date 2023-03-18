class MovieAttributes(object):
    """A dataclass to represent the properties of
    a movie as modified through the REST api.
    """
    def __init__(self, liked: bool=False, deleted: bool=False):
        self.liked = liked
        self.deleted = deleted
    
    def __repr__(self):
        return f"(liked={self.liked}, deleted={self.deleted})"
