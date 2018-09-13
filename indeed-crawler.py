import json
import requests as req
from bs4 import BeautifulSoup
banner_en = """


#   __        __     _                                _           _    _                      
#   \ \      / /___ | |  ___  ___   _ __ ___    ___  | |_  ___   | |_ | |__    ___            
#    \ \ /\ / // _ \| | / __|/ _ \ | '_ ` _ \  / _ \ | __|/ _ \  | __|| '_ \  / _ \           
#     \ V  V /|  __/| || (__| (_) || | | | | ||  __/ | |_| (_) | | |_ | | | ||  __/           
#      \_/\_/  \___||_| \___|\___/ |_| |_| |_| \___|  \__|\___/   \__||_| |_| \___|           
#    ___             _                  _   ____                                              
#   |_ _| _ __    __| |  ___   ___   __| | / ___|   ___  _ __  __ _  _ __   _ __    ___  _ __ 
#    | | | '_ \  / _` | / _ \ / _ \ / _` | \___ \  / __|| '__|/ _` || '_ \ | '_ \  / _ \| '__|
#    | | | | | || (_| ||  __/|  __/| (_| |  ___) || (__ | |  | (_| || |_) || |_) ||  __/| |   
#   |___||_| |_| \__,_| \___| \___| \__,_| |____/  \___||_|   \__,_|| .__/ | .__/  \___||_|   
#                                                                   |_|    |_|                


"""
banner_pt="""


#    ____                            _             _                                          
#   | __ )   ___  _ __ ___   __   __(_) _ __    __| |  ___     __ _   ___                     
#   |  _ \  / _ \| '_ ` _ \  \ \ / /| || '_ \  / _` | / _ \   / _` | / _ \                    
#   | |_) ||  __/| | | | | |  \ V / | || | | || (_| || (_) | | (_| || (_) |                   
#   |____/  \___||_| |_| |_|   \_/  |_||_| |_| \__,_| \___/   \__,_| \___/                    
#    ___             _                  _   ____                                              
#   |_ _| _ __    __| |  ___   ___   __| | / ___|   ___  _ __  __ _  _ __   _ __    ___  _ __ 
#    | | | '_ \  / _` | / _ \ / _ \ / _` | \___ \  / __|| '__|/ _` || '_ \ | '_ \  / _ \| '__|
#    | | | | | || (_| ||  __/|  __/| (_| |  ___) || (__ | |  | (_| || |_) || |_) ||  __/| |   
#   |___||_| |_| \__,_| \___| \___| \__,_| |____/  \___||_|   \__,_|| .__/ | .__/  \___||_|   
#                                                                   |_|    |_|                
#
#
# Siga as instruções que forem aparecendo e tudo será só sucesso meu jovem, desejo muita sorte
# e fé nessa tua caminhada para achar emprego!
"""
indeeds =["https://www.indeed.com.br/empregos?q=","https://www.indeed.pt/ofertas?q="]
## Send request to website and return the data to be parsed
def sendReq(url):
    headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    res = req.get(url,headers = headers,timeout=5)
    if res.status_code != 200:
        return False
    else:   
        data = res.text
        print("sendReq is saying: this is the url the req was sent: "+url)
        print("returning data from request\n")
        return data
    
## Parse the data, at the moment hardcoded parsing to parse all the job title from indeed
## with their respective links into a json file for acessing later
def parseData(data,file):
    jobs = {}
    page_content = BeautifulSoup(data,features="lxml")
    for link in page_content.find_all("a",{"data-tn-element": "jobTitle"}):
        job_title = link.get("title")
        job_link = link.get("href")
        jobs[job_title]=job_link
    with open(file+'.json', 'a') as outfile:
        jason = json.dump(jobs,outfile,indent=4)
        print("\nparseData is saying: json just got saved\n")
    print("\nparseData is saying:  function is finished\n")

##Collect the page links to crawl
def getPages(url,lang):
    pages =[]
    urls=["https://www.indeed.com.br","https://www.indeed.pt"]
    
    data = sendReq(url)
    page_content = BeautifulSoup(data,features="lxml")
    print("getPages is saying: this is the url to be geted\n",url)
    for link in page_content.find_all("a", {"onmousedown":"addPPUrlParam && addPPUrlParam(this);"}):
        print(link)
        print(urls[lang])
        pages.append(urls[lang]+link.get("href"))
    print("\ngetPages is saying:  function is finished\n")
    print("this is the url being used: "+url)
    print("this is the pages list after getPages is executed\n",pages)
    del pages[-1]
    return pages

## Name says it all
def crawl(url,file,lang):
    url = url
    file=file
    pages = getPages(url,lang)
    print("\nCrawl function is saying: this is pages array at crawl function\n",pages)
    for page in pages:
        print("\nCrawl function is saying: this is the page in the for loop:\n",page)
        data = sendReq(page)
        parseData(data,file)
        
def init():
    print(banner_pt)
    lang = int(input("""
# Selecione 1 para pesquisar no Indeed Brasileiro
# Selecione 2 para pesquisar no Indeed Portugues
------> """))-1
    job = input("# Escolha a vaga: ")
    location = input("# Escolha uma região: ")
    file_name=input("# choose a filename to save in json: ")
    url = indeeds[lang]+job+"&l="+location
    print("Starting to crawl with this url: ",url,"\n")
    crawl(url,file_name,lang)

    
if __name__ == "__main__":
    init()

