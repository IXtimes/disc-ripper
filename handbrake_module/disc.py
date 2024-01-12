class Disc:
    # Disc properties
    disc_title: str
    episode_range: str
    skip_to_title: int
    
    def __init__(self, title, range, skip):
        self.disc_title = title
        self.episode_range = range
        self.skip_to_title = skip
    