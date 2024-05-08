from bs4 import BeautifulSoup
import requests

class Wikiworker():
    def __init__(self):
        self._url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

    @staticmethod
    def _extract_companies(page_html):
        soup = BeautifulSoup(page_html, 'lxml')
        table = soup.find(id="constituents")
        table_rows = table.find_all('tr')
        for table_row in table_rows[1:]:  
            symbol = table_row.find('td').text.strip()  
            symbol = symbol.replace('.', '-')
            yield symbol

    def get_sp_500_companies(self):
        response = requests.get(self._url)
        if response.status_code != 200:
            print("Could'nt get entries")
            return []

        yield from self._extract_companies(response.text)

