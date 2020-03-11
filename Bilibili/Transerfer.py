import pymysql
import pymongo
import re
from TranserferSettings import *
from tqdm import tqdm
class Transfer(object):

    def __init__(self):
        self.mongoclient=pymongo.MongoClient(host='localhost',port=27017)
        self.mysqldb=pymysql.connect(host='localhost',user=MySqlUser,password=MySqlPasswd,port=3306,db=MySqlDB)
        self.collection=self.mongoclient[MongoDB][MongoCol]
        self.cursor=self.mysqldb.cursor()
        print('Building Connections...')

    def close(self):
        self.cursor.close()
        self.mysqldb.close()
        self.mongoclient.close()
        print('All Connections are closed!')

    def run(self):
        Csql='CREATE TABLE IF NOT EXISTS Tvs(badge varchar(255),index_show varchar(255),title varchar(255),play varchar(255),link varchar(255),primary key(link)   )'
        self.cursor.execute(Csql)

        datas=self.collection.find({},{"_id":0,"badge":1,"index_show":1,"play":1,"title":1,"link":1})
        for data in tqdm(datas):
            try:
                play=re.search('(\d+).(\d+)万',data["play"])
                if play:
                    play=re.search('(\d+).(\d+)',play.group())
                    play=str(10000*float(play.group()))
                    data["play"]=play
                else:
                    play=re.search('(\d+).(\d+)',data["play"])
                    data["play"]=play.group()

                keys=','.join(data.keys())
                values=','.join(['%s']*len(data))

                sql='INSERT INTO spiders.Tvs({keys}) VALUES({values})'.format(keys=keys,values=values)
                try:
                    if self.cursor.execute(sql,tuple(data.values())):
                        self.mysqldb.commit()
                except:
                    self.mysqldb.rollback()
            except:
                pass

        self.close()


if __name__=="__main__":
    t=Transfer()
    t.run()