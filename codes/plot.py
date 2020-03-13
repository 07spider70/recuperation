import matplotlib.pyplot as plt

#tvorba grafov na zaklade dat
class Plotter:
    def __init__(self, file_name, name):
        
        self.data = {}
        self.name = name
        with open(file_name, "r") as f:
            for line in f:
                temp = line.split()
                self.data[temp[0]] = float(temp[1])


    
    def plot(self):
        hum = []
        for i in self.data.values():
            hum.append(i)
        plt.plot(hum)
        
        #plt.yscale('linear')
        plt.ylabel("Humidity [%]")
        plt.xlabel("Time [t]")
        
        plt.savefig("graphs/" + self.name, bbox_inches='tight')
        plt.show()
        

"""
dat_rand = Plotter("data_rand.txt", "rand.png")
dat_rand.plot()

dat_month = Plotter("data.txt", "month.png")
dat_month.plot()

dat_ext = Plotter("data_extern_day.txt", "ext.png")
dat_ext.plot()
"""


