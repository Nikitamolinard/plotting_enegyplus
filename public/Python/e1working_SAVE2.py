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
import tkinter as tk
# import _tkinter as tk
from tkinter import *
from PIL import ImageTk,Image
from tkinter import filedialog
# from tkinter import ttk
# from matplotlib.backends.backend_tkagg import (FigureCanvasAgg,NavigationToolbar2Tk)
# from matplotlib.figure import Figure
# import glob
global full_path
path1=np.array(["1","2"], dtype='object')


def affichage(filename):
    
    global full_path 
    plt.close('ALL')   
    i=0
    import os
    # d = "dir"
    for path in os.listdir(str(filename)):
        full_path = os.path.join(str(filename), path)
        if os.path.isfile(full_path):  
            # path2=full_path
            # path1.append(full_path[i])
            path1[i]=str(full_path)
            i=i+1
            
    top=Toplevel()
    top.title('Run'+str(count))
    col=1 # start from column 1
    row=1 # start from row 3 
        
    full_path="r"+"'"+str(path1[0])+"'"+", "+"r'"+str(path1[1])+"'"

    for f in path1:
        img=Image.open(f) # read the image file
        img=img.resize((750,550)) # new width & height
        img=ImageTk.PhotoImage(img)
        e1 =Label(top)
        e1.grid(row=row,column=col)
        e1.image = img
        e1['image']=img # garbage collection 
        if(col==3): # start new line after third column
            row=row+1# start wtih next row
            row=1
            col=1    # start with first column
        else:       # within the same row 
            col=col+1 # increase to next column 
            
            
class Application():
    def __init__(self, root,title,geometry):  
        global count #Count the number of run
        """ WINDOWS SETTINGS """
        self.root = root
        self.root.title(title)
        self.root.geometry(geometry)
        label1 = Label(self.root, text="Select the Button to Open the File", font=('Aerial 11'))
        label1.pack(pady=30)
        count=0
        """ BUTTONS """
        self.btn3=Button(root,text="IDF file", command=self.open_file)
        self.btn3.pack(pady=5)
 
        self.btn5=Button(root,text="RUN SIMULATION !", command=self.run_simulation)
        self.btn5.place(relx = 1, x =-40, y = 350, anchor = NE)
        pass
    
        
    def open_file(self):
        """ Open IDF file """
        global idffilename
        #Find the directory
        idffilename = filedialog.askopenfilename(initialdir=r"Desktop", title="Select a file",filetypes=(("idf files", "*.idf"),("all files", "*.*")))
        mylabel=Label(self.root,text=idffilename).pack()
        
    def run_simulation(self):
        """ Calcul + plotting + saving """
        global count
        count=count+1
        
        # Making new folder for the plot for the running session
        script_dir = os.path.dirname(__file__)
        results_dir = os.path.join(script_dir, 'Results/'+str(count)+'/')
        
        #constant
        co2elec=0.0002958 #tCO₂/kWh
        co2gas=0.0002022 #tCO₂/kWh
        month = [ "Jan", "Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

        
        """-------------- Reading the input -----------"""
        
        idf=len(idffilename)-4
        meterfile=idffilename[:idf]+"Meter.csv"
        # meterfile=idffilename
        df=pd.read_csv( meterfile, 
                        parse_dates=[0],
                        index_col=[0],
                      )
        upper=2000
        
        #Sorting the type of heating 
        try :
            heating=(df["NaturalGas:Facility [J](Monthly)"]/3600000)
            case=heating.sum(axis=0)
        except:
            try:
                heating=(df["Gas:Facility [J](Monthly)"]/3600000)
                case=heating.sum(axis=0)
            except:
                try :
                    heating=(df["FuelOilNo1:Facility [J](Monthly)"]/3600000)
                    case=heating.sum(axis=0)
                    upper=5000
                except:
                    case=3   

        """-------------- Plotting setting -----------"""
        #Base configutation figure 
        fig, ax = plt.subplots(figsize =(16, 9))
        X_axis = np.arange(len(month))
        plt.xticks(X_axis,month)
        plt.grid(color = 'green', linestyle = '--', linewidth = 0.5)
        plt.xlabel('Month')
        plt.ylabel('energy consumption [kWh]')  
        plt.ylim(0, upper)
        plt.title("Monthly energy consumption [kWh]")
        
        """-------------- Plotting the heating result -----------"""
        #Sorting the type of plot in function of heating system 
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
        
        #Saving the file and closing the figure
        os.makedirs(results_dir, exist_ok=True)
        sample_file_name="Figure1"
        plt.savefig(os.path.join(results_dir, sample_file_name))
        plt.close('all')

        """-------------- Others Plotting  result -----------"""
        #Plotting CO2 emissions
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
        
        #Saving the file and closing the figure
        os.makedirs(results_dir, exist_ok=True)
        sample_file_name="Figure2"
        plt.savefig(os.path.join(results_dir, sample_file_name))
        plt.close('all')       
        
        
        
        
        #Showing the picture saved in the folder
        affichage(results_dir)
        
        pass

def main():
    
    count=0
    root= Tk()    
    e=Application(root,"Energy plotting tool","500x400")
    

    root.mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())





