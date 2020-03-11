from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import os
import re

def getTxtUrls():
    """
    returns list of ALL downloadable weekly turnstile data download urls
    """

    print("scraping urls")
    source_url = "http://web.mta.info/developers/turnstile.html"
    response = requests.get(source_url)
    soup = bs(response.content,'html.parser')
    urls = soup.findAll('a',href=re.compile(r'data/nyct/turnstile/turnstile_*'))
    for i in range(len(urls)):
        urls[i] = 'http://web.mta.info/developers/' + urls[i]['href']

    return urls


def createUrlSubset(urls):
    """
    returns a subset of all the downloadable urls based on provided starting
    and ending point
    """

    print("creating url subset")
    starting_point =  '171230'
    stopping_point = '1612'
    index_to_start = 0
    index_to_stop = len(urls) - 1

    for i in range(len(urls)):
        if starting_point and starting_point in urls[i]:
            index_to_start = i
        if stopping_point and stopping_point in urls[i]:
            index_to_stop = i
            break

    if not index_to_stop:
        response = input("No stopping point was specified. enter to download everything")

    return urls[index_to_start:index_to_stop+1]



def downloadCSVs(urls):
    """
    Downloads csvs from provided urls and output files into a directory.
    Retains MTA naming convention. Data gets transformed with pandas as it
    removes leading zeros from entry and exit count when converted to a dataframe.
    """

    print("download started")
    dl_location = 'raw_turnstile_data'
    if not os.path.exists(dl_location):
        os.makedirs(dl_location)

    for url in urls:
        filename = url.split('/')[-1]
        filepath = dl_location + '/' + filename

        print("processing", filename)

        df = pd.read_csv(url)
        df.to_csv(filepath, index=False)


if __name__ == '__main__':
    urls = getTxtUrls()
    url_subset = createUrlSubset(urls)
    downloadCSVs(url_subset)
