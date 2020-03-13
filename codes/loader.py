# -*- coding: utf-8 -*-

import pandas as pd
#nacitanie dat z csv
class Loader:
    
    def __init__(self, file_name, name_place):
        self.name_place = name_place
        self.file_name = file_name
        self.data = None
        
    #nacitanie x riadkov hodin
    #TODO prerobit aby nacitalo x hodin z daneho miesta
    def load_data_hours(self, hours):
        #nacitanie udajov ktore potrebujeme a dlzky ako chceme
        self.data = pd.read_csv('scraper-shmu-observations.csv',
                        index_col='name',
                        parse_dates=['date'],
                        usecols=["name","date","ta_2m","rh"])
        #self.data.head()
        
        #vyfiltrovanie udajov podla miesta
        edf = self.data.filter(like=self.name_place,axis=0)
        #kolko hodin chceme vypisat
        #print(edf[:hours])
        
        #vratenie objektu udajov daneho poctu hodin a miesta
        return edf[:hours]
        
    
    def load_data(self):
        #nacitanie udajov ktore potrebujeme 
        self.data = pd.read_csv('data/scraper-shmu-observations.csv',
                        index_col='name',
                        parse_dates=['date'],
                        usecols=["name","date","ta_2m","rh"])# ked nechceme vsetky [:20]
        #self.data.head()
        
        #vyfiltrovanie udajov podla miesta
        return self.data.filter(like=self.name_place,axis=0)
       
      
            
"""
pouzitie        
lod = Loader("scraper-shmu-observations.csv","ZILINA - DOLN")
ap = lod.load_data_hours(24)
print(ap)
"""

