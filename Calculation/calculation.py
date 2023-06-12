import math
from Application.WindowData import WindowData
from Calculation.add_init import *
from Application.CacheFile import CacheFile
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import io



def step1(item, gell, Vol):
    t_res = 0
    r = 0
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

            if P <= Pkp and V <= Vol:
                t_res = t
            else:
                return t_res, V
    return t_res, V


def step2(t1,t2,t3, item, gell):
    if t1 != 0:
        r1 = round(math.sqrt((t1+t2+t3)*float(gell[0].get("Q, м3/сут"))/(2*math.pi*float(item.thickness)*86400))+D, 2)
        r2 = round(math.sqrt((t2+t3)*float(gell[1].get("Q, м3/сут"))/(2*math.pi*float(item.thickness)*86400))+D, 2)
        r3 = round(math.sqrt((t3)*float(gell[2].get("Q, м3/сут"))/(2*math.pi*float(item.thickness)*86400))+D, 2)
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

def get_k_h(gis, h_w , h_g, k_w, k_g):
    res1 = 0
    res2 = 0
    Volumes = []
    for i in range(len(gis)):
        if gis[i].thickness not in ['','None'] and gis[i].permeability not in ['','None']:
            res1 += float(gis[i].thickness)*float(gis[i].permeability)/(h_w*k_w+h_g*k_g)

    for i in range(len(gis)):
        if gis[i].thickness not in ['','None'] and gis[i].permeability not in ['','None']:
            res2 = float(gis[i].thickness)*float(gis[i].permeability)/(h_w*k_w+h_g*k_g)*res1
            Volumes.append(res2*100)
        else:
            Volumes.append(0)
    return Volumes




def calculation_click(data):
    h_w , h_g, m_w, m_g, k_w, k_g = get_gis_calc(data.gis)
    Volumes = get_k_h(data.gis, h_w , h_g, k_w, k_g)
    radius_data = []
    temp_data = []
    for i in range(len(data.gis)):
        t1, V1 = step1(data.gis[i], data.gelling[0], Volumes[i])
        t2, V2 = step1(data.gis[i], data.gelling[1], Volumes[i])
        t3, V3 = step1(data.gis[i], data.gelling[2], Volumes[i])
        r1, r2, r3 = step2(t1, t2, t3, data.gis[i], data.gelling)
        radius_data.append([r1, r2, r3])
        temp_data.append([i+1, t1, t2, t3])


    image = io.BytesIO()
    df = pd.DataFrame(radius_data)
    df = df.rename(columns = {0:'Экран из 1 полимера, м', 1:'Экран из 2 полимера, м', 2:'Экран из 3 полимера, м'})
    #df['Скважина'] = 0.108
    df = df.reindex(columns=['Экран из 3 полимера, м', 'Экран из 2 полимера, м', 'Экран из 1 полимера, м']) 
    new_index = {i: f'{i+1}-й инт.' for i in range(len(df)+1)}
    df = df.rename(index=new_index)
    df = df[::-1]
    ax = df.plot(kind='barh', stacked=True, width=1, figsize=(10, 12))
    ax.set_xticks(range(len(df.columns)))
    ax.set_xticklabels([], rotation=90)
    for p in ax.patches:
        left, bottom, width, height = p.get_bbox().bounds
        temp = str(width.round(2)) if width != 0 else ''
        ax.annotate(temp, xy=(left+width/2, bottom+height/2), 
                    ha='center', va='center')
    ax.figure.savefig(image)

    return radius_data, image