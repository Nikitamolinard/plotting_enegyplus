# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 10:58:57 2022
vf
@author: James
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os,sys
from tkinter import *
from PIL import ImageTk,Image
from tkinter import filedialog
from tkinter import ttk



class Application():
    def __init__(self, root,title,geometry):       
        """ WINDOWS SETTINGS """
        self.root = root
        self.root.title(title)
        self.root.geometry(geometry)
        label1 = Label(self.root, text="Select the Button to Open the File", font=('Aerial 11'))
        label1.pack(pady=30)
          
        """ BUTTONS """
        self.btn3=Button(root,text="CSV file", command=self.open_file3)
        self.btn3.pack(pady=5)
 
        self.btn5=Button(root,text="RUN SIMULATION !", command=self.run_simulation)
        self.btn5.place(relx = 1, x =-40, y = 350, anchor = NE)
        pass
    
        
    def open_file3(self):
        global idffilename
        #Find the directory
        idffilename = filedialog.askopenfilename(initialdir=r"Desktop", title="Select a file",filetypes=(("csv files", "*.csv"),("all files", "*.*")))
        mylabel=Label(self.root,text=idffilename).pack()
        
    def run_simulation(self): 
        #constant
        co2elec=0.0002958 #tCO₂/kWh
        co2gas=0.0002022 #tCO₂/kWh
        month = [ "January", "February","March","April","May","June","July","August","September","October","November","December"]
        
        """-------------- Reading the input -----------"""
        meterfile=idffilename
        df=pd.read_csv( meterfile, 
                        parse_dates=[0],
                        index_col=[0],
                      )
        try :
            heating=(df["NaturalGas:Facility [J](Monthly)"]/3600000)
            case=heating.sum(axis=0)
        except:
            try:
                heating=(df["Gas:Facility [J](Monthly)"]/3600000)
                case=heating.sum(axis=0)
            except:
                case=3   

        """-------------- Plotting setting -----------"""
        #Base figure 
        fig, ax = plt.subplots(figsize =(16, 9))
        X_axis = np.arange(len(month))
        plt.xticks(X_axis,month)
        plt.grid(color = 'green', linestyle = '--', linewidth = 0.5)
        plt.xlabel('Month')
        plt.ylabel('energy consumption [kWh]')  
        plt.ylim(0, 2000)
        plt.title("Monthly energy consumption [kWh]")
        
        """-------------- Plotting the result -----------"""
        if (case ==0 or case ==3):
              #case HP
              elec=(((df["InteriorEquipment:Electricity [J](Monthly)"]+df["InteriorLights:Electricity [J](Monthly)"]))/3600000)
              heating=((df['Electricity:Facility [J](Monthly)']-(df["InteriorEquipment:Electricity [J](Monthly)"]+df["InteriorLights:Electricity [J](Monthly)"]))/3600000)#"DistrictHeating:Facility [J](Monthly)"
              plt.bar(X_axis, heating, 0.35,color='palegreen', label='Electricity used for heating  [kWh]')
              plt.bar(X_axis, elec, 0.35,bottom=heating,color='coral',
                     label='Non heating electricity [kWh]')
              
        else:
               #case Boiler
               elec=(df['Electricity:Facility [J](Monthly)']/3600000)
               # heating=(df["Gas:Facility [J](Monthly)"]/3600000)#"DistrictHeating:Facility [J](Monthly)"   
               plt.bar(X_axis - 0.2, heating, 0.4,color="salmon", label = 'Heating [kWh]')
               plt.bar(X_axis + 0.2, elec, 0.4,color="orange", label = 'Electricity [kWh]')

        plt.legend(title="Legend",loc='upper center', bbox_to_anchor=(0.5, -0.05),
                  fancybox=True, shadow=True, ncol=5)
        plt.show()    
        
        co2=(heating)*co2gas+(elec*co2elec)
        fig, ax = plt.subplots(figsize =(16, 9))
        X_axis = np.arange(len(month))
        plt.xticks(X_axis,month)
        plt.grid(color = 'green', linestyle = '--', linewidth = 0.5)
        plt.xlabel('Month')
        plt.ylabel('CO₂ emission [tCO₂]')  
        plt.ylim(0, 1)
        plt.bar(X_axis,co2,0.35, color="chartreuse",label = 'CO₂ Emission [tCO₂]')
        plt.legend(title="Legend",loc='upper center', bbox_to_anchor=(0.5, -0.05),
                  fancybox=True, shadow=True, ncol=5)
        plt.title("Monthly CO₂ emission [tCO₂]")
        plt.show() 
    pass

def main():

    root= Tk()    
    e=Application(root,"Energy plotting tool","500x400")
    
    root.mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())





