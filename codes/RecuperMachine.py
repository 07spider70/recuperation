
# -*- coding: utf-8 -*-

#hlavna trieda, reprezentuje rekuperator

class RecuperMachine:
    #inicilization  of some default values and all req values
    def __init__(self, air_volume = 400.0, enthalphy_ratio = 0.7, step = 1.0):
        self.air_volume = air_volume
        self.enthalphy_ratio = enthalphy_ratio
        self.temp_in = 0.0
        self.hum_in = 0.0
        self.temp_out = 0.0
        self.hum_out = 0.0
        self.abs_in = 0.0
        self.abs_out = 0.0
        self.bilance = 0.0
        self.sample_min = step
        
        
        self.vrpm = 0
        
        #constants for co2 gain
        
        #normal pressure
        self.pressure = 105
        #burn temp of glucose
        self.hsp = 2.8158*10**9
        #gas constant
        self.r = 8314
        #energetic outgo
        self.E = 2.083
        
        #constants for ventilation
        
        #inside wanted co2 ppmv
        self.xp = 700        
        #outside co2 ppmv
        self.x0 = 400
        
        
    #set air_volume, enth_ratio and step for recuperation    
    def setter(self, air_volume, enthalpy_ratio, step):
        self.air_volume = air_volume
        self.enthalphy_ratio = enthalpy_ratio
        self.sample_min = step
        
        
    def setter_of_co2_gain(self, pressure = 105, hsp = 2.8158*10**9,
                           r = 8314, E = 2.083):
        self.pressure = pressure
        self.hsp = hsp
        self.r = r
        self.E = E
        
    def setter_of_ventilation(self, xp = 700, x0 = 400):
        self.xp = xp
        self.x0 = x0
    #process of recuperation
    #return relativ humidity

    def process(self, to, ho, ti, hi, air_flow, err_usr):
        """
        @PAM temp_outside, hum_outside, temp_inside, hum_inside, air_flow, err_of usr
        @RETURN float of relative humidity, float of temperature
        """
        self.temp_in = ti
        self.hum_in = hi
        self.temp_out = to
        self.hum_out = ho
        
        self.abs_in = self.abs_hum(self.temp_in, self.hum_in)
        self.abs_out = self.abs_hum(self.temp_out, self.hum_out)
        
        self.bilance = self.ah_bilance(self.temp_out, self.hum_out, self.temp_in, self.hum_in, self.enthalphy_ratio)
        
        val = (self.air_volume * self.abs_in) + ((self.sample_min/60)*air_flow*self.bilance) + err_usr
        val = val / self.air_volume
        
        res = self.rel_hum(self.temp_in, val)
        
        temp_room = self.room_chg_aft_ex(self.air_volume, air_flow
                            , air_flow, self.temp_in, self.temp_out, 0)
        
        
        return (res, temp_room)
    
    def abs_hum(self, temperature, rh_humidity):
        """
        compute absolute humidity from relative based on temperature
        """
        
        pws = self.__get_pws_water(temperature)
        pw = pws * rh_humidity
        res = 2.16679 * pw / (273.15 + temperature)
        return res
    
    def rel_hum(self, temperature, abs_hum_val):
        """
        compute relative hum from absolute hum
        """
        pws = self.__get_pws_water(temperature)
        pw = (abs_hum_val * (273.15 + temperature))/2.16679
        res = pw/pws
        return res
    
    def ah_bilance(self, t_out, rh_out, t_in, rh_in, effectivity):
    
        res = - (self.abs_hum(t_in, rh_in) - ( effectivity * (self.abs_hum(t_in, rh_in) - self.abs_hum(t_out, rh_out)) + self.abs_hum(t_out, rh_out)))
        return res
    
    def room_chg_aft_ex(self, vol_room = 100, air_flow_in = 100
                            , air_flow_out = 100, temp_in = 20, temp_out = 0, efficienty = 0.7):
        
        
        #kolko litrov treba vyvetrat za minutu
        #experimentalne, nefunguje!
        
        ad = self.get_ad(1.92,90)
        gen_r = self.co2_generation_rate(ad)
        np = self.np(gen_r)
        vrps = self.ventilation_rate_per_s(np, 60)
        self.vrpm = self.ventilation_rate_per_minute(vrps)
        
        #print(f"Za minutu treba vyvetrat {vrpm} L/min")
        
        
        #objem vzduchu za jednu minutu, predpoklad vstup == vystup
        air_in_ex_per_min = 0.0166666667*air_flow_in
        air_out_ex_per_min = 0.0166666667*air_flow_out
        
        #teplota vtlacaneho vzduchu
        air_temp_in = temp_in + efficienty*(temp_out - temp_in)/2
        
        
        vrpsm3 = 0.001*self.vrpm
        
        
        
        
        #objem vtlaceneho a vytlaceneho vzduchu sa musi rovnat
        if (vol_room == (vol_room - air_flow_out + air_flow_in)):
            #ak sa rovna pokracujeme
            vol_of_temp_in = vol_room - vrpsm3 #objem vzduchu ktory nam ostane pri odsani
            t_room = (vol_of_temp_in * temp_in + vrpsm3*air_temp_in)/(vol_room)
            #https://www.engineeringtoolbox.com/mixing-humid-air-d_694.html
            #miesanie plynov
            return t_room

        else:
            print("Nepomer vtlaceneho a vytlaceneho vzduchu!")
            return
        
        
    #experiment na zistenie kolko treba vetrat
    
    #https://www.epa.gov/sites/production/files/2017-06/documents/co2-generate-ciaq-7june2017_draft1.pdf page 7
    def get_ad(self, height, weight):
        return 0.203*height**(0.725)*weight**(0.425)
        
    def co2_generation_rate(self,ad):
        return (0.00276*ad*58*0.85)/(0.23*0.85+0.77)
    
    
    #http://www.scienceasia.org/2001.27.n4/v27_279_284.pdf 
    def np(self, gen_rate):
        return gen_rate/0.3
    
    def ventilation_rate_per_s(self, np, volume, diversity = 1):
        return 3*np*diversity + 0.35*volume
    
    def ventilation_rate_per_minute(self,ventil_rate_per_s):
        return ventil_rate_per_s*60
    
    
    
    #generate equal "a" parameters into interval <-1, 0, 1>
	#pom func for abs hum func
    
    def __calvin_from_celsius(self, temp):
        return temp + 273.15
    
    def __celsius_from_calvin(self, calvin):
        return calvin - 273.15
        
    
    def __get_pws_water(self, temperature):
        exp_nnt = (7.591386 * temperature)/(temperature+240.7263)
        pws = 6.116241*10**(exp_nnt) #hPa
        return pws

