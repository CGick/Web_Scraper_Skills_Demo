import requests


class Web_Scraper(object):
    """
    Class used to perform simple http requests
    """
    def __init__(self, url):
        self.url = url

    def get_html(self, endpoint='', method="GET", *args, **kwargs):
        """
        Performs and http GET request and returns the retrieved html

        :param endpoint: string of additional http navigation(optional)
        :param args: used to add addition parameters such as body or headers
        :param kwargs: used to add addition parameters such as body or headers
        :return: string html
        """
        response = requests.request(
            method,
            self.url + endpoint,
            *args,
            **kwargs
        )
        return response


if __name__ == "__main__":
    url = "http://python.org"
    scraper = Web_Scraper(url)
    page = scraper.get_html()
    print page.content
