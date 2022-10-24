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
from tkinter import *
from PIL import ImageTk,Image
from tkinter import filedialog
global full_path
from tkinter import ttk
    
def dateindex():
    #Function that generate a date index
    date_str = '1/1/2020'
    start = pd.to_datetime(date_str) - pd.Timedelta(days=365)
    hourly_periods = 8760
    drange = pd.date_range(start, periods=hourly_periods, freq='H')
    return drange



def affichage(filename):
    path2=[]
    global full_path 
    plt.close('ALL')   
    i=0
    import os
    
    #find all the files
    for path in os.listdir(str(filename)):
        full_path = os.path.join(str(filename), path)
        if os.path.isfile(full_path): 
            i=i+1
            path2.append(full_path)
            

    top=Toplevel()
    top.title('Run'+str(count)+'_'+namefile)
    top.geometry("1600x650")
    col=1 # start from column 1
    row=1 # start from row 3 
        
    main_fram2=Frame(top)
    main_fram2.pack(fill=BOTH, expand=1)
   
    main_canvas2= Canvas(main_fram2)
    main_canvas2.pack(side=LEFT,fill=BOTH, expand=1)
   
    my_scrollbar2 =tk.Scrollbar(main_fram2,orient=VERTICAL, command= main_canvas2.yview)
    my_scrollbar2.pack(side=RIGHT,fill=Y)
   
    main_canvas2.configure(yscrollcommand= my_scrollbar2.set)
    main_canvas2.bind('<Configure>',lambda e: main_canvas2.configure(scrollregion= main_canvas2.bbox("all") ))
   
    second_fram2=Frame(main_canvas2)
   
    main_canvas2.create_window((0,0),window=second_fram2, anchor="s")     
    
    full_path=path2
    if i>5:    
        full_path = tk.filedialog.askopenfilename(multiple=True,initialdir=filename,filetypes=(('PNG Files','*.png'),("all files", "*.*")))

    #show the files
    for f in full_path:
        img=Image.open(f) # read the image file
        img=img.resize((800,650)) # new width & height
        img=ImageTk.PhotoImage(img)
        e1 =Label(second_fram2)
        e1.grid(row=row,column=col)
        e1.image = img
        e1['image']=img # garbage collection 
        if(col==2): # start new line after third column
            row=row+1# start wtih next row
            # row=1
            col=1    # start with first column
        else:       # within the same row 
            col=col+1 # increase to next column 
            
            
class Application():
    def __init__(self, root,title,geometry):  
        global count #Count the number of run
        global count2
        global CBenergy
        global CBcomfort

        """ WINDOWS SETTINGS """
        
        
        self.root = root
        self.root.title(title)
        self.root.geometry(geometry)
        
        self.main_fram1=Frame(root,width=10)
        self.main_fram1.pack(side=TOP, anchor="w")
        label1 = Label(self.main_fram1, text="Select the Button to Open the File", font=('Aerial 11'))
        label1.grid(row=0,column=0)
        count=0
        count2=0
        """ BUTTONS """
        #IDF Button
        self.btn1=Button(self.main_fram1,text="Select IDF file", command=self.open_file)
        self.btn1.grid(row=1,column=0, pady= 10)
 
        CBcomfort = IntVar()
        #Comfort Button
        self.btn2=Checkbutton(self.main_fram1,text="Show Comfort GRAPH !",variable=CBcomfort)
        self.btn2.grid(sticky="W",row=2,column=0, pady= 2)
        
        
        CBenergy = IntVar()
        self.btn3=Checkbutton(self.main_fram1,text="Show Energy GRAPH !",variable=CBenergy)
        self.btn3.grid(sticky="W",row=3,column=0, pady= 2)
        
        #Run sim Button
        self.btn4=Button(self.main_fram1,text="Show the GRAPHS !", command=self.run_choice)
        self.btn4.grid(row=4,column=0, pady= 10)
        
        self.main_fram12=Frame(root,width=100)
        self.main_fram12.place(x=250,y=0)
        
        #IYlim
        label2 = Label(self.main_fram12, text="Set Ylimit energy consumption", font=('Aerial 9'))
        label2.grid(row=0,column=0)
        
        self.entry= Entry(self.main_fram12, width= 8)
        self.entry.focus_set()
        self.entry.grid(row=0,column=1)

        #Start day
        label3 = Label(self.main_fram12, text="Starting day ", font=('Aerial 9'))
        label3.grid(row=1,column=0)
        
        self.entry2= Entry(self.main_fram12, width= 8)
        self.entry2.focus_set()
        self.entry2.grid(row=1,column=1)


        #end day
        label4 = Label(self.main_fram12, text="ending day", font=('Aerial 9'))
        label4.grid(row=2,column=0)
        
        self.entry3= Entry(self.main_fram12, width= 8)
        self.entry3.focus_set()
        self.entry3.grid(row=2,column=1)
        
        self.main_fram13=Frame(root,width=100)
        self.main_fram13.place(x=250,y=70)
        label13 = Label(self.main_fram13, text=" Day numbers : \n January 1st : 1 \n February 1st : 32 \n March 1st : 60 \n April 1st : 91 \n May 1st : 121 \n June 1st : 152 " , font=('Aerial 9'), anchor="w")
        label13.grid(sticky="W",row=0,column=0)

        label14 = Label(self.main_fram13, text="           \n July 1st : 182 \n August 1st : 213 \n September 1st : 244 \n October 1st : 274 \n November 1st : 305 \n December 1st : 335 " , font=('Aerial 9'), anchor="w")
        label14.grid(sticky="W",row=0,column=1)
        
        #close win
        self.btn6=Button(self.main_fram1,text="Close Windows !", command=self.close)
        self.btn6.grid(row=10,column=0)
        
        #Frame
        self.main_fram=Frame(root,width=100,highlightbackground='red',highlightthickness=3)
        self.main_fram.pack(side=LEFT,pady=10,padx=35)
        self.main_canvas= Canvas(self.main_fram)
        self.main_canvas.pack(side=LEFT,fill=BOTH)
        self.my_scrollbar =tk.Scrollbar(self.main_fram,orient=VERTICAL, command= self.main_canvas.yview)
        self.my_scrollbar.pack(side=RIGHT,fill=Y)
        self.main_canvas.configure(yscrollcommand= self.my_scrollbar.set)
        self.main_canvas.bind('<Configure>',lambda e: self.main_canvas.configure(scrollregion= self.main_canvas.bbox("all") ))
        
        self.second_fram=Frame(self.main_canvas)
        
        self.main_canvas.create_window((0,0),window=self.second_fram, anchor="s")
        
        
    
        
        pass
    

        
    
        
    def open_file(self):
        """ Open IDF file """
        global idffilename
        global save
        global namefile 

        
        #Find the directory
        idffilename = filedialog.askopenfilename(multiple=True,initialdir=r"Desktop", title="Select a file",filetypes=(("idf files", "*.idf"),("all files", "*.*")))
        for f in idffilename:
            mylabel=Label(self.second_fram,text=f).pack(side=BOTTOM,pady=5,padx=15)
        save=1
        
    def run_choice(self):
        
        if CBenergy.get()==1:
            self.run_graph()
        if CBcomfort.get()==1:
            self.comfortzone()
        
    def run_graph(self):
        """ Calcul + plotting + saving """
        global count
        global entry   
        global namefile 
        upper1=self.entry.get()
        

            
        
        #No IDF
        try : idffilename
        except NameError: 
            mylabel=Label(self.second_fram,text='please select IDF file runned on EnergyPlus V9.4',fg='red').pack(side=BOTTOM,pady=5,padx=15)
            return
        
            
        count=count+1
        for f in idffilename:
            # Making new folder for the plot for the running session
            script_dir = os.path.dirname(f)
            
            #constant
            co2elec=0.0002958 #tCO₂/kWh
            co2gas=0.0002022 #tCO₂/kWh
            month = [ "Jan", "Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    
            
            """-------------- Reading the input -----------"""
            
            idf=len(f)-4
            
            #No CSV
            if (os.path.exists(f[:idf]+"Meter.csv")==False):
                mylabel=Label(self.second_fram,text='No simulation found, please run the simulation on E+ V9.4',fg='red').pack(side=BOTTOM,pady=5,padx=15)
                return
            
            meterfile=f[:idf]+"Meter.csv"
            namefile=os.path.basename(meterfile)
            idf=len(namefile)-9
            namefile=namefile[:idf]
    
            results_dir = os.path.join(script_dir, 'Results/'+str(count)+'_'+str(namefile)+'/')

            df=pd.read_csv( meterfile, 
                            parse_dates=[0],
                            index_col=[0],
                          )
     
            #hourly -> MONTHLY
            if (len(df.index)>12):
                df['Date']=dateindex()
                df = df.resample('M', on='Date').sum()
                df = df.replace('Hourly','Monthly', regex=True)
            
            try: 
                upper1=int(upper1)
            except:
                upper1=2000
                if((df.iloc[0,0]/3600000)>2000):
                    upper1=5000
         
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
                        # upper=5000
                    except:
                        heating=((df['Electricity:Facility [J](Monthly)']-(df["InteriorEquipment:Electricity [J](Monthly)"]+df["InteriorLights:Electricity [J](Monthly)"]))/3600000)
                        case=3
                            
    
                                
            """-------------- Plotting setting -----------"""
            #Base configutation figure 
            fig, ax = plt.subplots(figsize =(16, 9))
            X_axis = np.arange(len(month))
            plt.xticks(X_axis,month)
            plt.grid(color = 'green', linestyle = '--', linewidth = 0.5)
            plt.xlabel('Month')
            plt.ylabel('energy consumption [kWh]') 
            plt.ylim(0, upper1)
            plt.title("Monthly energy consumption [kWh]")
            
            """-------------- Plotting the heating result -----------"""
           
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
            sample_file_name="Figure1_"+str(namefile)
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
            plt.ylim(0, 2)
            plt.bar(X_axis,co2,0.35, color="chartreuse",label = 'CO₂ Emission [tCO₂]')
            plt.legend(title="Legend",loc='upper center', bbox_to_anchor=(0.5, -0.05),
                      fancybox=True, shadow=True, ncol=5)
            plt.title("Monthly CO₂ emission [tCO₂]")
            plt.show()
            
            
            sample_file_name="Figure2"
            plt.savefig(os.path.join(results_dir, sample_file_name))
            plt.close('all')       
            
            
            
            
            #Showing the picture saved in the folder
            affichage(results_dir)
            
        pass
    
    def comfortzone(self):
        global count2
        global save
        global namefile
        start=self.entry2.get()
        end=self.entry3.get()
        
       
        
        #No CSV
        try : idffilename
        except NameError: 
            mylabel=Label(self.second_fram,text='please select IDF file runned on EnergyPlus V9.4',fg='red').pack(side=BOTTOM,pady=5,padx=15)
            return
        
        
        count2=count2+1
        for f in idffilename:
            save=idffilename
            idf=len(f)-4
        
            if (os.path.exists(f[:idf]+".csv") == False):
                mylabel=Label(self.second_fram,text='No simulation found, please run the simulation on E+ V9.4',fg='red').pack(side=BOTTOM,pady=5,padx=15)
                return
            
            
            comfortfile=f[:idf]+".csv"
            namefile=os.path.basename(comfortfile)
            idf=len(namefile)-4
            namefile=namefile[:idf]
            

            df2=pd.read_csv( comfortfile, 
                            parse_dates=[0],
                            index_col=[0],
                          )
                   
            try: 
                start=int(start)
            except:
                start=0
                
            try: 
                end=int(end)
            except:
                end=1
                
            if ((start or end)>365):
                start=0
                end=1 
                    
            start=start*24
            end=end*24
            
            df2=df2.filter(regex='Zone Thermal Comfort Fanger Model PMV \[]\(Hourly:ON\)') 
            df2=df2.iloc[start:end]    
            
            if (df2.empty ==True ):
                mylabel=Label(self.second_fram,text='No the right output on E+',fg='red').pack(side=BOTTOM,pady=5,padx=15)
                return
            
     
            
            i=0         
            for row in df2:
                zone = row.split(':')
                script_dir = os.path.dirname(f) 
                results_dir = os.path.join(script_dir, 'Results_Comfort/'+str(count2)+'_'+str(namefile)+'/')
                
                """-------------- Plotting setting -----------"""
                #Base configutation figure 
                ax = plt.figure(figsize =(16, 9))
                X_axis =list(range(start, end))
                plt.grid(color = 'green', linestyle = '--', linewidth = 0.5)
                plt.xlabel('Hours')
                plt.ylabel('Comfort')
                plt.ylim(-4.1, 4.1)
                plt.title(zone[1])
                plt.plot(X_axis,df2[row],label=zone[1])
                plt.legend(title="Legend",loc='upper center', bbox_to_anchor=(0.5, -0.05),
                              fancybox=True, shadow=True, ncol=5)  
                plt.show()
                
                os.makedirs(results_dir, exist_ok=True)
                sample_file_name=zone[1]+str(i)
                plt.savefig(os.path.join(results_dir, sample_file_name))
                plt.close("all")
                i=i+1
                
        affichage(results_dir)
        
    def close(self):
        """ Open IDF file """
        plt.close('all')
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Toplevel):
                widget.destroy()

def main():
    
    count=0
    root= Tk()    
    e=Application(root,"Energy plotting tool","500x400")


    root.mainloop()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())





