from .source_loader import SourceLoader

class UrlLoader(SourceLoader):
    
    def __init__(self, url: str):
        self.url = url

    def load(self) -> bytes:
        import requests
        resp = requests.get(self.url)
        resp.raise_for_status()
        return resp.content
