# -*- coding: utf-8 -*-

"""
class for saving data to file for graphs
"""
class Logger:
    def __init__(self, txt_filename, set_count):
        self.txt_file = txt_filename
        #dict for data
        self.data = {}
        
        

    #add data to dict
    def add(self, minute, rel_hum):
        self.data[minute] = rel_hum
                
    #save dict to file, each line is minute and hum
    def save_txt(self):
        f = open("data/"+self.txt_file, "w")
        
        for i in self.data:
            
            f.write("%f\t%f" %(i, self.data[i]))
                
            f.write("\n")
            
        f.close()
        
    def save(self):
        self.save_txt();
