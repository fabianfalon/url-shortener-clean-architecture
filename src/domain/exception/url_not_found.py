class UrlNotFound(Exception):
    def __init__(self):
        super().__init__("Url not found.")
