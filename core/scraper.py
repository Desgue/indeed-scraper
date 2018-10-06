import requests, re
from bs4 import BeautifulSoup

headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) \
    AppleWebKit/537.36 (KHTML, like Gecko)'}


def scrape(base_url, searchterm, location=""):
    main_url = "{}/jobs?q={}&l={}".format(base_url, searchterm, location)

    data = requests.get(main_url, headers=headers).text

    soup = BeautifulSoup(data, features = "lxml")

    def no_results(soup):
        if soup.find("div",{"class":"no_results"}): return True
        else: return False

    if no_results(soup):
        print("""No results found.
Try a broader searchterm, check for misspell and run the program again.""")
        return

    try:
        pagination = str(soup.find(id="searchCount"))
        total_jobs = re.findall("\d+", pagination)

        if len(total_jobs)  > 3:
            num_jobs = 1000 # as indeed does not show more then 1000 jobs

        else:
            num_jobs = int(total_jobs[2])

        num_pages = int(num_jobs / 10)

        all_urls = ["{}&start={}".format(main_url, index*10) for index in range(0, num_pages)]

    except Exception as e:
        raise e

    scraped_data = list()
    _id = 1
    for url in all_urls:
        _data = requests.get(url, headers=headers).text
        _soup = BeautifulSoup(_data, features="lxml")

        for div in soup.find_all("div",{"data-tn-component": "organicJob"}):
                
                link = div.find("a",{"data-tn-element":"jobTitle"})
                
                _title= link.get("title")
                _link= "{}{}".format(base_url,link.get("href"))
                _location = div.find("span",{"class":"location"}).text
                _company = div.find("span",{"class":"company"}).text
                temp = (_id, _title, _link, _location, _company)
                scraped_data.append(temp)
                _id+=1
    return scraped_data

