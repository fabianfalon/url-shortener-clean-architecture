class UrlNotFound(Exception):
    def __init__(self):
        super().__init__(f"Url not found.")
