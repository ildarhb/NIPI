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
    V = 0
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
                return t_res, V
    return t_res, V


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

def get_gis_calc(gis):
    h_w = 0
    h_g = 0
    m_w = 0
    m_g = 0
    k_w = 0
    k_g = 0
    for i in range(len(gis)):
        if gis[i].curr_saturation == "В":
            h_w += float(gis[i].thickness)
            m_w += float(gis[i].thickness)*float(gis[i].porosity)
            k_w += float(gis[i].thickness)*float(gis[i].permeability)
        elif gis[i].curr_saturation == "Г":
            h_g += float(gis[i].thickness)
            m_g += float(gis[i].thickness)*float(gis[i].porosity)
            k_g += float(gis[i].thickness)*float(gis[i].permeability)
    return h_w , h_g, m_w/h_w, m_g/h_g, k_w/h_w, k_g/h_g

def get_k_h(gis, h_w , h_g, k_w, k_g,V_data):
    res1 = 0
    res2 = 0
    V1 = 0
    V2 = 0
    V3 = 0
    Volumes = []
    for i in range(len(gis)):
        if gis[i].thickness not in ['','None'] and gis[i].permeability not in ['','None']:
            res1 += float(gis[i].thickness)*float(gis[i].permeability)/(h_w*k_w+h_g*k_g)

    for i in range(len(gis)):
        if gis[i].thickness not in ['','None'] and gis[i].permeability not in ['','None']:
            res2 = float(gis[i].thickness)*float(gis[i].permeability)/(h_w*k_w+h_g*k_g)*res1
            V1 = res2*V_data[i][0]
            V2 = res2*V_data[i][1]
            V3 = res2*V_data[i][2]
            Volumes.append([V1, V2, V3])
        else:
            Volumes.append([0, 0, 0])
        

        

    return Volumes




def calculation_click(data):
    cachefile_gelling = CacheFile("Gelling")
    cache_gelling = cachefile_gelling.read().data
    
    gell = []
    gell.append(cache_gelling.get('Полимер'))
    gell.append(cache_gelling.get('Полимер 2'))
    gell.append(cache_gelling.get('Полимер 3'))

    radius_data = []
    volume_data = []
    for i in range(len(data.gis)):
        t1, V1 = step1(data.gis[i], gell[0])
        t2, V2 = step1(data.gis[i], gell[1])
        t3, V3 = step1(data.gis[i], gell[2])
        t = t1 + t2 + t3
        r1, r2, r3 = step2(t, data.gis[0], gell)
        volume_data.append([V1, V2, V3])
        radius_data.append([r1, r2, r3])


    image = io.BytesIO()
    df = pd.DataFrame(radius_data)
    df = df.rename(columns = {0:'Экран из 1 полимера, м', 1:'Экран из 2 полимера, м', 2:'Экран из 3 полимера, м'})
    #df['Скважина'] = 0.108
    df = df.reindex(columns=['Экран из 3 полимера, м', 'Экран из 2 полимера, м', 'Экран из 1 полимера, м']) 
    new_index = {i: f'{i+1}-й инт.' for i in range(len(df)+1)}
    df = df.rename(index=new_index)
    df = df[::-1]
    ax = df.plot.barh(stacked=True, figsize=(10, 12))
    for p in ax.patches:
        left, bottom, width, height = p.get_bbox().bounds
        ax.annotate(str(width.round(2)), xy=(left+width/2, bottom+height/2), 
                    ha='center', va='center')
    ax.figure.savefig(image)


    h_w , h_g, m_w, m_g, k_w, k_g = get_gis_calc(data.gis)
    #get_k_h(data.gis, h_w , h_g, k_w, k_g, volume_data
    return radius_data, image