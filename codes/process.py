# -*- coding: utf-8 -*-
from codes.RecuperMachine import RecuperMachine
from codes.logger import Logger
from codes.loader import Loader
import random

#simulacia, jeden proces simuluje napr spravanie pocas dna atd


def process_test():
    rec = RecuperMachine()
    rec.setter(400.0, 0.7, 1.0)
    
    inside_rh = rec.process(0, 100, 22, 50, 100, 0)
    print("Final relative humidity: %2.4f\n" % (inside_rh))
    
    
    
def process_month(air_flow = 100):

    rec = RecuperMachine()
    log_data = Logger("data.txt", 2)

    #daily humidity intake made by humans 6700g/day
    #computed to g per min
    err_daily = 6700.0/(24*60)

    #setting plant into 400m3 house, 70% humidity returning by heat exchanger, 1min time step for computing
    rec.setter(400.0, 0.6, 1.0)

    #starting relative indoor hummidity inside
    inside_rh = 50.0

    for i in range(1,((60*24)*30)):
        inside_rh = rec.process(-10, 100, 22, inside_rh, air_flow, err_daily)
        log_data.add(i, inside_rh)
    

    print("Final Relative Hummidity: %2.4f\n"% inside_rh)

    log_data.save()

def process_month_rnd():

    rec = RecuperMachine()
    log_data = Logger("data_rand.txt", 2)

    #daily humidity intake made by humans 6700g/day
    #computed to g per min
    #err_daily = 6700.0/(24*60)
    err_daily = random.randint(0,10)
    #setting plant into 400m3 house, 70% humidity returning by heat exchanger, 1min time step for computing
    rec.setter(400, 0.7, 1.0)

    #starting relative indoor hummidity inside
    inside_rh = 50.0

    for i in range(1,((60*24)*30)):
        
        err_daily = random.randint(0,10)
        inside_rh = rec.process(0, 100, 22, inside_rh, 100, err_daily)
        log_data.add(i, inside_rh)

    print("Final Relative Hummidity: %2.4f\n" % (inside_rh))

    log_data.save()
    
    
def process_day_extern_data(air_flow = 100):
    rec = RecuperMachine()
    log_data = Logger("data_extern_day.txt", 2)
    
    #nacitanie externych dat
    ext_data = Loader("scraper-shmu-observations.csv","ZILINA - DOLNY HRICOV").load_data_hours(24)
    
    data_list = ext_data.values.tolist()

    
    #daily humidity intake made by humans 6700g/day
    #computed to g per min
    err_daily = 6700.0/(24*60)

    #setting plant into 400m3 house, 70% humidity returning by heat exchanger, 1min time step for computing
    rec.setter(400, 0.7, 1.0)

    #starting relative indoor hummidity inside
    inside_rh = 50.0

    count_hours = 0

    for i in range(1,(60*24)):
        
        if(i%60==0):
            count_hours += 1
        #temp_outside, hum_outside, temp_inside, hum_inside, air_flow, err_of usr
        inside_rh = rec.process(data_list[count_hours][2]
                    , data_list[count_hours][0], 22, inside_rh, air_flow, err_daily)
        log_data.add(i, inside_rh)
    

    print("Final Relative Hummidity: %2.4f\n" % (inside_rh))

    log_data.save()


#nacitanie externych dat
#TODO dorobit nacitanie cez nazov, nie index
def process_month_extern_data(start_point = 1, air_flow = 100):
    rec = RecuperMachine()
    log_data = Logger("data_extern_mont_temp.txt", 2)
    
    #nacitanie externych dat
    ext_data = Loader("data/scraper-shmu-observations.csv","ZILINA - DOLNY HRICOV").load_data()
    
    data_list = ext_data.values.tolist()

    #
    
    #daily humidity intake made by humans 6700g/day
    #computed to g per min
    err_daily = 6700.0/(24*60)

    #setting plant into 400m3 house, 70% humidity returning by heat exchanger, 1min time step for computing
    rec.setter(400, 0.7, 1.0)

    #starting relative indoor hummidity and tempeature inside
    inside_rh = (50.0,20)

    count_hours = 0

    
    for i in range(start_point, start_point+(60*24)):
        
        if(i%60==0):
            count_hours += 1
            #vypisanie pomocnych udajov
            print(f"Time: {count_hours} HUM out: {data_list[count_hours][0]} TEMP out: {data_list[count_hours][2]} TEMP IN: {inside_rh[1]}")
        #temp_outside, hum_outside, temp_inside, hum_inside, air_flow, err_of usr
        inside_rh = rec.process(data_list[count_hours][2]
                    , data_list[count_hours][0], inside_rh[1], inside_rh[0], air_flow, err_daily)
        log_data.add(i, inside_rh[0])
        
        
    

    print("Final Relative Hummidity: %2.4f\nFinal Temp Room: %2.4f" % (inside_rh[0], inside_rh[1]))
    print(f"Ventilation rate: {rec.vrpm} L/min")

    log_data.save()


def process_year_extern_data(start_point = 1, air_flow = 100):
    rec = RecuperMachine()
    log_data = Logger("data_extern_year.txt", 2)
    
    #nacitanie externych dat
    ext_data = Loader("data/scraper-shmu-observations.csv","ZILINA - DOLNY HRICOV").load_data()
    
    data_list = ext_data.values.tolist()

    #
    
    #daily humidity intake made by humans 6700g/day
    #computed to g per min
    err_daily = 6700.0/(24*60)

    #setting plant into 400m3 house, 70% humidity returning by heat exchanger, 1min time step for computing
    rec.setter(400, 0.7, 1.0)

    #starting relative indoor hummidity inside
    inside_rh = 50.0

    count_hours = 0

    print(len(data_list))
    for i in range(1, (60*24*30*6)):
        
        if(i%60==0):
            count_hours += 1
            #vypisanie pomocnych udajov
            #print(f"Time: {count_hours} \t HUM out: {data_list[count_hours][0]} TEMP out: {data_list[count_hours][2]}")
        #temp_outside, hum_outside, temp_inside, hum_inside, air_flow, err_of usr
        inside_rh = rec.process(data_list[count_hours][2]
                    , data_list[count_hours][0], 22, inside_rh, air_flow, err_daily)
        log_data.add(i, inside_rh)
        
        
    

    print("Final Relative Hummidity: %2.4f\n" % (inside_rh))

    log_data.save()
