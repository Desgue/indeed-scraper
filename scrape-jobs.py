import  argparse,sys, sqlite3
from core.scraper import scrape 

##TODO 
# 1. Better handling of database data insertion
# 2. Add funcionality to scrape each job posting collected individually


def main():

    parser = argparse.ArgumentParser(description="""Scrape and save job postings from ideed into
    a SQL database""")

    parser.add_argument("lang", type=str,
                        help="""What country to search (eg. "Br" for www.indeed.com.br
                    or "Pt" for www.indeed.pt).""")

    parser.add_argument("searchterm", type=str, help ="""Search Term (eg. Python).To separate
words utilize underscore (eg. Data_Science)""") # Ainda não é possivel pesquisar mais de uma palavra

    parser.add_argument("-l", "--location" , type=str, default="",
                        help="Location to search for.")

    parser.add_argument("-f", "--file", type=str, default="indeedData.db",
                        help="File to save scraped data. (Defalut is indeedData.db)")

    args = parser.parse_args()
    sys.stdout.write(str(args))

    if args.lang.lower() in ["pt","portugal"]:
        base_url = "http://www.indeed.pt"
    elif args.lang.lower() in ["br","brasil","huehuehuebr"]:
        base_url = "http://www.indeed.com.br"
        
    
    scraped_data = scrape(base_url,args.searchterm, args.location)
    
    print(scraped_data[0])
    
    conn = sqlite3.connect(str(args.file))
    c = conn.cursor()
    c.execute(""" CREATE TABLE IF NOT EXISTS resultsData(id INTEGER, title TEXT, link TEXT,
location TEXT, company TEXT)""")
    c.executemany(" INSERT INTO resultsData VALUES (?,?,?,?,?)", scraped_data)
    conn.commit()
    c.close()
        
if __name__ == "__main__":
    main()
