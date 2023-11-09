import requests
from bs4 import BeautifulSoup
# from pprint import pprint  || for print array
import json
import os

class Scraping:
    result = [];
    base = "https://notes.ayushsharma.in/";
    content_name = "";
    
    def __init__(self, content_name):
        self.content_name = content_name
        
    def getQuery(self):
        return self.content_name
    
    def getRequest(self):
        url = self.base + self.content_name
        req_data = requests.get(url)
        html = BeautifulSoup(req_data.text , 'html.parser');
        
        articles = html.select('a.post-card');
        
        for article in articles:
            picture = ""
            try:
                image = article.select('.card img')[0];
                if image is not None:
                    picture = image['src']
            except:
                print("Not Found Image");
                
            title = article.select('.card-title')[0].getText();
            excerpt = article.select('.card-text')[0].getText();
            public_date = article.select('.card-footer')[0].getText();
                
            ## append to list
            
            self.result.append({
                "image": picture,
                "title": title,
                "excerpt": excerpt,
                "public_date": public_date
            })
    
    def writeJson(self):
        try:
            folder_name = "data"
            if not os.path.exists(folder_name):
                os.makedirs(folder_name);
                
            path = folder_name + "/" + self.content_name + '.json'
            with open(path, 'w' ) as file:
                ## convert array to string and write this to data.json
                result_string = json.dumps(self.result , indent=2)
                file.write(result_string);
        except:
            print("write file json failed.")

# list page for scape data

listOfPage = [
    'life-stuff',
    'technology',
    'video-games',
    'meta',
]

for page in listOfPage:
    scrap = Scraping(page);
    scrap.getRequest();
    scrap.writeJson();
    
print("Scape Data Success!");