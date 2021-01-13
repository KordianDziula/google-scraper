import urllib
import requests
from bs4 import BeautifulSoup
import re
import numpy as np

class GoogleResults:
    def __init__(self, query: str, user_agent: str):
        self.query = query
        self.user_agent = user_agent
    
    def _get_page(self, href):
        headers = {"user-agent" : self.user_agent}
        url = "https://google.com/{}".format(href)
        
        response = requests\
            .get(url, headers = headers)
        return BeautifulSoup(response.content, "html.parser")
    
    def _get_page_content(self, soup):
        return list(map(lambda x: x.find("a")["href"],
                   soup.findAll("div", {"class":"rc"})))
    
    def _get_page_links(self, soup):
        return list(map(lambda x: x["href"], 
                   soup.findAll("a", {"aria-label": re.compile("Page")})))
    
    def load(self):
        self.pages = []
        
        page = self._get_page(self.query)
        self.pages += self._get_page_content(page)
        
        links = self._get_page_links(page)
        for l in links:
            page = self._get_page(l)
            self.pages += self._get_page_content(page)
            
        return self