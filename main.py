from data import GoogleResults, PagesContent
import re

def get_stop_words(file_url):
    with open(file_url, "rb") as f:
        return f.read()\
            .decode("UTF-8").split("\n")

query = "search?q=Kwiaciarnia"
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
stop_words = get_stop_words("./stopwords/polish.stopwords.txt")
regex = re.compile("[AaBbCcdEeFfGgHhIiJjKkLlMmNnOoÓóPpRrSsŚśTtUuWwYyZzŻżŹź]")

google_results = GoogleResults(query, user_agent).load()
pagees_content = PagesContent(
    pages = google_results.pages,
    filters = [
        lambda w: bool(regex.match(w)),
        lambda w: len(w) > 4 and len(w) < 20,
        lambda w: not w in stop_words
    ],
    min_count = 5,
    user_agent = user_agent
).load()

