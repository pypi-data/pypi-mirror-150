import requests



class Main:
    def __init__(self, url) -> None:
        self.url = url

    def get_status_code(self):
        return requests.get(self.url).status_code


print(Main('https://basalam.com').get_status_code())