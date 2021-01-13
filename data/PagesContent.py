import urllib
import requests
from bs4 import BeautifulSoup
import re
import numpy as np

class PagesContent():
    def __init__(self, pages, filters, min_count, user_agent):
        self.pages = pages
        self.filters = filters
        self.min_count = min_count
        self.user_agent = user_agent
        
    def _clean_text(self, text):
        return text.lower()\
                .replace("\n", " ")\
                .replace("\r", " ")\
                .replace("\t", " ")\
                .replace(".", " ")\
                .replace(",", " ")\
                .replace('"', " ")
    
    def _array_filter(self, function, array):
        match = np.vectorize(function)
        return match(array)
    
    def _clean_page(self, soup):
        words = self._clean_text(soup.text).split(" ")
        words = np.asarray(words)
        for f in self.filters:
            words = words[self._array_filter(f, words)]
            if len(words) == 0:
                return None
        return words
    
    def _get_unique_words(self, pages_content):
        words_pages = np.concatenate(pages_content, axis = 0)
        unique_words, counts = np.unique(words_pages, return_counts = True)
    
        zipped = zip(unique_words, counts)
        words_counts = np.asarray(list(zipped))

        mask = self._array_filter(lambda c: int(c) > self.min_count, words_counts[:, 1:])
        words = words_counts[mask.reshape(-1), 0]
        
        return words
    
    def _download_page(self, url):
        try:
            response = requests.get(url, headers = {"user-agent": self.user_agent})
            print(response.status_code)
        except:
            return None
        
        soup = BeautifulSoup(response.content)        
        return self._clean_page(soup)
    
    def _clean_page_content(self, page_content, unique_words):
        mask = self._array_filter(lambda w: w in unique_words, page_content)
        return page_content[mask]
    
    def load(self):
        pages_content = []
        print("Pages count -> {}".format(len(self.pages)))
        
        for p in self.pages:
            pages_content.append(self._download_page(p))
            print("Download page -> {}".format(p))
        pages_content = [pc for pc in pages_content if not pc is None]

        unique_words = self._get_unique_words(pages_content)
        print("Unique words done.")
        
        for i in range(len(pages_content)):
            pages_content[i] = self._clean_page_content(pages_content[i], unique_words)
            print("Clean page -> {}".format(i))
            
        self.content = pages_content
        self.unique = unique_words
        return self