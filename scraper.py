import requests as req
from bs4 import BeautifulSoup
import re

class Scraper:
    
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
  
    def __init__(self, base_url, search_term, location=""):

        self.base_url = base_url
        self.search_term = search_term
        self.location = location
        self.url = "{}ofertas?q={}&l={}".format(self.base_url,self.search_term,self.location)
        self.response = req.get(self.url, headers=self.headers)
        self.soup = BeautifulSoup(self.response.text,features="lxml")
        
    def no_results(self):
        if self.soup.find("div",{"class":"no_results"}): return True
        else: return False

    def get_pagination(self):
        search_count = str(self.soup.find(id="searchCount"))
        total_jobs=re.findall("\d+",search_count)
        if len(total_jobs) > 3:
            self.num_jobs = 1000
        else:
            self.num_jobs=int(total_jobs[2])

        num_pages = int(self.num_jobs/10)

        self.search_pages = ["{}&start={}".format(self.url,index*10) for index in range(0,num_pages)]
        print(num_pages)
        
    def scrape(self):
        _id = 1
        self.dic = {}
        for url in self.search_pages:
            data = req.get(url,headers=self.headers)
            soup = BeautifulSoup(data.text,features="lxml")

            #scrape for job titles and respective links
            for div in soup.find_all("div",{"data-tn-component": "organicJob"}):
                _location = div.find("span",{"class":"location"}).text
                print(_location)
                link = div.find("a",{"data-tn-element":"jobTitle"})
                job_title= link.get("title")
                job_link= "{}{}".format(self.base_url,link.get("href"))
                self.dic[_id] = {job_title:job_link}
                _id += 1
