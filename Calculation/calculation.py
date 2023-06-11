import math
from Application.WindowData import WindowData
from Calculation.add_init import *
from Application.CacheFile import CacheFile
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import io

class Radius():
    def __init__(self, r1, r2, r3):
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3


def step1(item, gell):
    t_res = 0
    V_res = 0
    P_res = 0
    if item.collector == "Да" and item.plast != "н/д":
        for i in range(10000):
            t = (i+1)*30
            r = math.sqrt(t*float(gell.get("Q, м3/сут"))/(2*math.pi*float(item.thickness)*86400))+D
            w = r/t
            y = 4*alpha*w/(math.sqrt(8*float(item.permeability)*10**(-15)*float(item.porosity)/100))
            m = float(gell.get("К, Па*с"))*y**(float(gell.get("n"))-1)
            P = Ppl+m*y+m*float(gell.get("Q, м3/сут"))/86400*math.log(r/D)/(2*math.pi*float(item.permeability)*10**(-15)*float(item.thickness))
            V = float(gell.get("Q, м3/сут"))/86400*t

            if P <= Pkp and V <= 100:
                t_res = t
            else:
                return t_res
    return t_res


def step2(t, item, gell):
    if t != 0:
        r1 = round(math.sqrt(t*float(gell[0].get("Q, м3/сут"))/(2*math.pi*float(item.thickness)*86400))+D, 2)
        r2 = round(math.sqrt(t*float(gell[1].get("Q, м3/сут"))/(2*math.pi*float(item.thickness)*86400))+D, 2)
        r3 = round(math.sqrt(t*float(gell[2].get("Q, м3/сут"))/(2*math.pi*float(item.thickness)*86400))+D, 2)
    else:
        r1 = 0
        r2 = 0
        r3 = 0
    return r1, r2, r3



def calculation_click(data):
    cachefile_gelling = CacheFile("Gelling")
    cache_gelling = cachefile_gelling.read().data
    
    gell = []
    gell.append(cache_gelling.get('Полимер'))
    gell.append(cache_gelling.get('Полимер 2'))
    gell.append(cache_gelling.get('Полимер 3'))

    radius_data = []
    for i in range(len(data.gis)):
        t1 = step1(data.gis[i], gell[0])
        t2 = step1(data.gis[i], gell[1])
        t3 = step1(data.gis[i], gell[2])
        t = t1 + t2 + t3
        r1, r2, r3 = step2(t, data.gis[0], gell)
        radius_data.append([r1, r2, r3])


    image = io.BytesIO()
    df = pd.DataFrame(radius_data)
    df = df.rename(columns = {0:'Экран из 1 полимера, м', 1:'Экран из 2 полимера, м', 2:'Экран из 3 полимера, м'})
    ax = df.plot.barh(stacked=True, figsize=(10, 12))
    for p in ax.patches:
        left, bottom, width, height = p.get_bbox().bounds
        ax.annotate(str(width), xy=(left+width/2, bottom+height/2), 
                    ha='center', va='center')
    ax.figure.savefig(image)


    return radius_data, image