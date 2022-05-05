# -*- coding: utf-8 -*-
"""
Created on Thu May  5 03:49:44 2022

@author: clovi
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class Resistance:
    def __init__(self, x_label, y_label, fount_color, line_color, text_color, font_style):
        self.x_label = x_label
        self.y_label = y_label
        self.title = x_label + ' x ' + y_label
        self.fount_color = fount_color
        self.line_color = line_color
        self.text_color = text_color
        self.font_style = font_style
        self.exact = False
        self.negative = False
    
    def formula(self, Vr, power = 0, min_value = 0.1, max_value = 5, steps = 0.1, val_round = 3, full = False):
        self.power = power
        self.Vr = Vr
        self.min_value = min_value
        self.max_value = max_value
        self.steps = steps
        self.full = full
        
        if power < 0 or min(Vr) < 0:
            self.negative = True
            return "There are no results for negative values of tension or power"
        
        V = sum(self.Vr)
        r = []
        if type(power) != int and type(power) != float:
            power = 0
        if power > 0:
            r = tuple([((V*voltage)/self.power)for voltage in Vr])
            self.R = r
            self.exact = True
            return r
        else:
            self.power = np.arange(self.min_value,self.max_value,self.steps )
            for p in self.power:
                r += [tuple([(round(V*voltage/p, val_round)) for voltage in Vr])]
            resistance_values = pd.DataFrame(r)
            resistance_values.columns = ['R1(Ω)', 'R2(Ω)']
            resistance_values["R Total(Ω)"] = [round(sum(r[R]),val_round) for R in range(0,len(r))]
            resistance_values["Power(W)"] = self.power
            resistance_values["Current(A)"] = [round(V/sum(r[R]),val_round) for R in range(0,len(r))]
            self.values = resistance_values


    def graphs(self, file_name = str):
        
        info = "Vr1 = {}V".format(self.Vr[0]) + "\nVr2 = {}V".format(self.Vr[1])
        
        if self.negative == True:
            return "Uncapable of plotting graphics for negative power or voltage values"
        if self.exact == True:
            
            max_full = {False: self.power + self.power/2, True: self.max_value}
            min_full = {False: self.power - self.power/2, True: self.min_value}
            max_value = max_full[self.full]
            min_value = min_full[self.full]
            power = self.power
            i = sum(self.Vr)/sum(self.R)
            values_dict = {"Power(W)": power, "Current(A)": i, "R Total(Ω)": sum(self.R)}
            self.formula(self.Vr, 0, steps = self.steps , max_value = max_value, min_value=min_value)
            
            
            plt.tight_layout()
            plt.figure(figsize=[11,5])
            plt.xlabel(self.x_label,fontsize=15, color=self.text_color,  fontdict={'family':self.font_style})
            plt.ylabel(self.y_label,fontsize=15, color=self.text_color,  fontdict={'family':self.font_style})
            
            plt.yticks(fontsize=13, color=self.text_color)
            plt.xticks(fontsize=13, color=self.text_color)
    
            plt.title(self.title, fontdict={'fontweight':'bold','family':self.font_style}, color = self.fount_color)
            plt.plot(self.values[self.x_label], self.values[self.y_label], linewidth = 2.5, color = self.line_color)
            plt.plot(values_dict[self.x_label], values_dict[self.y_label], marker="o", markersize=8, markeredgecolor="black", markerfacecolor="red")
        
            plt.xlim([plt.xlim()[0],plt.xlim()[1]])
            plt.ylim([plt.ylim()[0],plt.ylim()[1]])
            
            x = 0.5*(plt.xlim()[0]+plt.xlim()[1])
            y = plt.ylim()[1]*0.9
            plt.grid(True, linestyle = ':', color='black', zorder = 0)
            plt.text(x=x,y = y, s=info,fontsize=8,
                     fontdict={'family':'sans-serif','color':'black'},horizontalalignment='center',verticalalignment='center',
                     bbox=dict(facecolor='palegoldenrod', edgecolor='black', boxstyle='round', pad = 1))
            
            
            if file_name==str:
                file_name = self.title
                
            plt.savefig(file_name+'(with value).jpg', bbox_inches="tight", dpi = 500)
            plt.show()
        
        else: 
            plt.tight_layout()
            plt.figure(figsize=[11,5])
            
            plt.xlabel(self.x_label,fontsize=15, color=self.text_color,  fontdict={'family':self.font_style})
            plt.ylabel(self.y_label,fontsize=15, color=self.text_color,  fontdict={'family':self.font_style})
           
            plt.yticks(fontsize=13, color=self.text_color)
            plt.xticks(fontsize=13, color=self.text_color)
            
            plt.title(self.title, fontdict={'fontweight':'bold','family':self.font_style}, color = self.fount_color)
            plt.plot(self.values[self.x_label], self.values[self.y_label], linewidth = 2.5, color = self.line_color)
            
            plt.xlim([0,plt.xlim()[1]])
            plt.ylim([0,plt.ylim()[1]])
            
            x = 0.5*(plt.xlim()[0]+plt.xlim()[1])
            y = plt.ylim()[1]*0.9
            plt.grid(True, linestyle = ':', color='black', zorder = 0)
            plt.text(x=x,y = y, s=info,fontsize=8,
                     fontdict={'family':'sans-serif','color':'black'},horizontalalignment='center',verticalalignment='center',
                     bbox=dict(facecolor='palegoldenrod', edgecolor='black', boxstyle='round', pad = 1))
            
            if file_name==str:
                file_name = self.title
                
            plt.savefig(file_name+'.jpg', bbox_inches="tight", dpi = 500)
            plt.show()
        

current_x_power = Resistance("Current(A)","Power(W)","black","darkcyan","black","serif")
R = current_x_power.formula([12,4], power=0.3)
current_x_power.graphs()

current_x_resistance = Resistance("Current(A)","R Total(Ω)","black","darkcyan","black","serif")
R = current_x_resistance.formula([12,4], power=0.3, steps = 0.01, full=(True))
current_x_resistance.graphs()

power_x_resistance = Resistance("Power(W)","R Total(Ω)","black","darkcyan","black","serif")
R = power_x_resistance.formula([12,4], power=0.3, steps=0.01)
power_x_resistance.graphs()

'''#############################################################################################################'''

current_x_power_2 = Resistance("Current(A)","Power(W)","black","darkcyan","black","serif")
R = current_x_power_2.formula([6,4])
current_x_power_2.graphs()

current_x_resistance_2 = Resistance("Current(A)","R Total(Ω)","black","darkcyan","black","serif")
R = current_x_resistance_2.formula([2,4])
current_x_resistance_2.graphs()

power_x_resistance_2 = Resistance("Power(W)","R Total(Ω)","black","darkcyan","black","serif")
R = power_x_resistance_2.formula([7,3])
power_x_resistance_2.graphs()