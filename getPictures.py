import requests
import pymongo
import time
from tqdm import tqdm
import os


class Fetch(object):

    def __init__(self):
        self.urls=[]
        self.index=0
        self.headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36'
        }

    def setAttr(self,col,db='Bilibili',host='localhost',port=27017):
        self.DB_Name=db
        self.COL_Name=col
        self.client=pymongo.MongoClient(host=host,port=port)
        self.db=self.client[self.DB_Name]
        self.collection=self.db[self.COL_Name]
        self.path='img\\{}'.format(self.COL_Name)
        if os.path.exists(self.path)==False:
            os.mkdir(self.path)
        os.chdir(self.path)

    def downloads(self,url,index):
        req=requests.get(url=url,headers=self.headers)
        if req.status_code==200:
            open('{}.jpg'.format(str(index)),'wb').write(req.content)
        else:
            print(url+' parse error!')

    def geturls(self):

        datas=self.collection.find()
        for data in datas:
            try:
                url=data["pic"]
                title=data["title"]
                self.urls.append((url,title))
            except:
                print('No pics!')



    def run(self):
        self.geturls()
        for item in tqdm(self.urls):
            try:
                self.downloads(item[0],item[1])
            except:
                pass
            time.sleep(1)
        print('All Finished!')

if __name__=="__main__":
    f=Fetch()
    f.setAttr('MoviesInfo')
    f.run()