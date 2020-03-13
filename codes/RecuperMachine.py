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
        
        
    #set air_volume, enth_ratio and step for recuperation    
    def setter(self, air_volume, enthalpy_ratio, step):
        self.air_volume = air_volume
        self.enthalphy_ratio = enthalpy_ratio
        self.sample_min = step
        
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
                            , air_flow, self.temp_in, self.temp_out, 0.7)
        
        
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
        #objem vzduchu za jednu minutu, predpoklad vstup == vystup
        air_in_ex_per_min = 0.0166666667*air_flow_in
        air_out_ex_per_min = 0.0166666667*air_flow_out
        
        #teplota vtlacaneho vzduchu
        air_temp_in = efficienty*(temp_in + temp_out)
        
        #objem vtlaceneho a vytlaceneho vzduchu sa musi rovnat
        if (vol_room == (vol_room - air_flow_out + air_flow_in)):
            #ak sa rovna pokracujeme
            vol_of_temp_in = vol_room - air_out_ex_per_min #objem vzduchu ktory nam ostane pri odsani
            t_room = (vol_of_temp_in * temp_in + air_in_ex_per_min*air_temp_in)/(vol_of_temp_in + air_in_ex_per_min)
            #https://www.engineeringtoolbox.com/mixing-humid-air-d_694.html
            #miesanie plynov
            return t_room

        else:
            print("Nepomer vtlaceneho a vytlaceneho vzduchu!")
            return
        
        
    
    #generate equal "a" parameters into interval <-1, 0, 1>
	#pom func for abs hum func
    
    def __get_pws_water(self, temperature):
        exp_nnt = (7.591386 * temperature)/(temperature+240.7263)
        pws = 6.116241*10**(exp_nnt) #hPa
        return pws