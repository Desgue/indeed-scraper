import json
import requests as req
from bs4 import BeautifulSoup 

## Send request to website and return the data to be parsed
def sendReq(url):
    headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    res = req.get(url,headers = headers,timeout=5)
    if res.status_code != 200:
        return False
    else:   
        data = res.text
        return data
    
## Parse the data, at the moment hardcoded parsing to parse all the job title from indeed
## with their respective links into a json file for acessing later
def parseData(data):
    jobs = {}
    page_content = BeautifulSoup(data,features="lxml")
    for link in page_content.find_all("a",{"data-tn-element": "jobTitle"}):
        job_title = link.get("title")
        job_link = link.get("href")
        jobs[job_title]=job_link
    with open('jobs.json', 'w') as outfile:
        jason = json.dump(jobs,outfile,indent=4)

##Collect the page links to crawl
def getPages(url):
    pages =[]
    
    data = sendReq(url)
    page_content = BeautifulSoup(data,features="lxml")
    for link in page_content.find_all("a", {"onmousedown":"addPPUrlParam && addPPUrlParam(this);"}):
        pages.append("https://www.indeed.pt"+link.get("href"))
    return pages

## Name says it all
def crawl():
    pages = getPages(url)
    for page in pages:
        data = sendReq(page)
        parseData(data)
    
    
vaga= "python"
cidade =  "porto"
url = "https://www.indeed.pt/jobs?q="+vaga+"&l="+cidade

    
    
