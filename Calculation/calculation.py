import math
from Calculation.add_init import *
import pandas as pd
import numpy as np
import io
import matplotlib.pyplot as plt

def get_const(data):
    global D,Rc,Qj,Qg_init,VGF,Ppl_ishod,Ppl,count,alpha,Pkp,spz,cPzg,Pzab,kt,dt_init,Pbuf,Nvd, Pzab_after
    D = float(data.gis_after_watering.get('D скв. дол., мм'))/2000
    Ppl_ishod = float(data.gis_after_watering.get('Pпл, атм'))
    Ppl = Ppl_ishod*101325
    Rc = float(data.gis_after_watering.get('Rс, м'))
    Pzab = float(data.gis_after_watering.get('Pзаб, атм'))
    Qj = float(data.gis_after_watering.get('Qж, м3/сут'))
    Qg_init = float(data.gis_after_watering.get('Qг, тыс. м3/сут'))
    VGF = Qj/Qg_init
    spz = float(data.gis_after_watering.get('Вяз-ть пл.воды, сПз'))/1000
    cPzg = float(data.gis_after_watering.get('Плотность газа,  г/см3'))/1000
    kt = float(data.gis_after_watering.get('К-т сверхсжимаемости газа'))
    dt_init = float(data.gis_after_watering.get('ΔT м/у устьем и забоем, ℃'))
    Pbuf = float(data.gis_after_watering.get('Pбуф, атм'))
    Nvd = float(data.gis_after_watering.get('Hвд, м'))
    Pzab_after = float(data.gis_after_watering.get('Pзаб план-е после РИР, атм'))*101325

def calc_p(t, h_w, m_w, k_w, gell):
    r = math.sqrt(t*float(gell.get("Q, м3/сут"))/(2*math.pi*float(h_w)*86400))+D
    w = r/t
    y = 4*alpha*w/(math.sqrt(8*float(k_w)*10**(-15)*float(m_w)/100))
    m = float(gell.get("К, Па*с"))*y**(float(gell.get("n"))-1)
    P = Ppl+m*y+m*float(gell.get("Q, м3/сут"))/86400*math.log(r/D)/(2*math.pi*float(k_w)*10**(-15)*float(h_w))
    return P/101325, m

def get_graph_data(h_w, m_w, k_w, gell, t1_w, t2_w, t3_w):
    P_data = []
    Pust_data = []
    m_data = []
    t_data = []
    for i in range(10000):
        t = (i+1)*30
        t_data.append(t/60)

        P1, m1 = calc_p(t, h_w, m_w, k_w, gell[0])
        P2 = 0
        m2 = 0
        P3 = 0
        m3 = 0

        if t > t1_w:
            P2, m2 = calc_p(t-t1_w, h_w, m_w, k_w, gell[1])

        if t > (t1_w+t2_w):
            P3, m3 = calc_p(t-t2_w-t1_w, h_w, m_w, k_w, gell[2])

        if P2 == 0:
            P_res = P1
            m_res = m1
        elif P3 == 0:
            P_res = (P1+P2)/2
            m_res = (m1+m2)/2
        else:
            P_res = (P1+P2+P3)/3
            m_res = (m1+m2+m3)/3

        if t > (t1_w+t2_w+t3_w):
            P_res = 0
            m_res = 0 
        P_ust = (P_res - 1000*9.81*Nvd/101325 ) if P_res - 1000*9.81*Nvd/101325 > 0 else 0
        Pust_data.append(P_ust)
        P_data.append(P_res)
        m_data.append(m_res)

    return P_data, Pust_data, m_data, t_data
        


def calctable(h_w, m_w, k_w, gell, Vol):
    for i in range(10000):
        t = (i+1)*30
        r = math.sqrt(t*float(gell.get("Q, м3/сут"))/(2*math.pi*float(h_w)*86400))+D
        w = r/t
        y = 4*alpha*w/(math.sqrt(8*float(k_w)*10**(-15)*float(m_w)/100))
        m = float(gell.get("К, Па*с"))*y**(float(gell.get("n"))-1)
        P = Ppl+m*y+m*float(gell.get("Q, м3/сут"))/86400*math.log(r/D)/(2*math.pi*float(k_w)*10**(-15)*float(h_w))
        V = float(gell.get("Q, м3/сут"))/86400*t

        if P <= Pkp:
            t_res = t
            P_res = P
            r_res = r
            v_res = V
        else:
            return t_res, P_res, r_res, v_res
    return t_res, P_res, r_res, v_res

def step1fin(h_w, m_w, k_w, gell, Vol):
    for i in range(10000):
        t = (i+1)*30
        r = math.sqrt(t*float(gell.get("Q, м3/сут"))/(2*math.pi*float(h_w)*86400))+D
        w = r/t
        y = 4*alpha*w/(math.sqrt(8*float(k_w)*10**(-15)*float(m_w)/100))
        m = float(gell.get("К, Па*с"))*y**(float(gell.get("n"))-1)
        P = Ppl+m*y+m*float(gell.get("Q, м3/сут"))/86400*math.log(r/D)/(2*math.pi*float(k_w)*10**(-15)*float(h_w))
        V = float(gell.get("Q, м3/сут"))/86400*t

        if P <= Pkp and V <= Vol:
            t_res = t
            P_res = P
            r_res = r
            v_res = V
        else:
            return t_res, P_res, r_res, v_res
    return t_res, P_res, r_res, v_res

def step2fin(t1,t2,t3, h_w, gell):
    if t1 != 0:
        r1 = round(math.sqrt((t1+t2+t3)*float(gell[0].get("Q, м3/сут"))/(2*math.pi*h_w*86400))+D, 2)
        r2 = round(math.sqrt((t2+t3)*float(gell[1].get("Q, м3/сут"))/(2*math.pi*h_w*86400))+D, 2)
        r3 = round(math.sqrt((t3)*float(gell[2].get("Q, м3/сут"))/(2*math.pi*h_w*86400))+D, 2)
    else:
        r1 = 0
        r2 = 0
        r3 = 0
    return r1, r2, r3

def get_r_data(h_w, gell, r_max, t_max):
    r_data = []
    for i in range(10000):
        t = (i+1)*30
        if t < t_max:
            r_data.append(0)
        else:
            r = math.sqrt((t-t_max)*float(gell.get("Q, м3/сут"))/(2*math.pi*float(h_w)*86400))+D
            if r < r_max:
                r_data.append(r)
            else:
                r_data.append(r_max)
    return r_data

def step1(item, gell, Vol):
    t_res = 0
    r = 0
    V = 0
    r_data = []
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
                return t_res
    return t_res


def step2(t1,t2,t3, item, gell):
    if (t1+t2+t3) != 0:
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
    Vol_w = 0
    Vol_g = 0

    for i in range(len(gis)):
        if gis[i].thickness not in ['','None'] and gis[i].permeability not in ['','None']:
            res1 += float(gis[i].thickness)*float(gis[i].permeability)/(h_w*k_w+h_g*k_g)
    for i in range(len(gis)):
        if gis[i].thickness not in ['','None'] and gis[i].permeability not in ['','None']:
            res2 = float(gis[i].thickness)*float(gis[i].permeability)/(h_w*k_w+h_g*k_g)*(1/res1)
            Volumes.append(res2*100)
            if gis[i].curr_saturation == 'В':
                Vol_w += res2*100
            else:
                Vol_g += res2*100
        else:
            Volumes.append(0)
    return Volumes, Vol_w, Vol_g

def get_temp(data, a, b, c):
    dP = Ppl - Pzab_after
    temp1 = 'x' if a*(D+data[0]) <= dP else 'да'
    temp2 = 'x' if b*(D+data[1]) <= dP else 'да'
    temp3 = 'x' if c*(D+data[2]) <= dP else 'да'
    if temp1 == 'да' or temp2 == 'да' or temp3 == 'да':
        temp4 = 'да'
    elif temp1 == '-':
        temp4 = '-'
    else:
        temp4 = 'x'
    return temp1, temp2, temp3, temp4

def ustoy(gis, radius_data):
    res = []
    temp1, temp2, temp3, temp4 = get_temp(radius_data[0], G_kr_w1, G_kr_w2, G_kr_w3)
    res.append([temp1, temp2, temp3, temp4])
    temp1, temp2, temp3, temp4 = get_temp(radius_data[1], G_kr_g1, G_kr_g2, G_kr_g3)
    res.append([temp1, temp2, temp3, temp4])

    for i in range(len(gis)):       
        if gis[i].curr_saturation == 'В':
            temp1, temp2, temp3, temp4 = get_temp(radius_data[i+2], G_kr_w1, G_kr_w2, G_kr_w3)   
        elif gis[i].curr_saturation == '':
            temp1 = '-'
            temp2 = '-'
            temp3 = '-'
            temp4 = '-'
        else:
            temp1, temp2, temp3, temp4 = get_temp(radius_data[i+2], G_kr_g1, G_kr_g2, G_kr_g3)            
        res.append([temp1, temp2, temp3, temp4])
    return res

def calcQw(gis, radius, gelling, ustoy):
    dP = Ppl - Pzab 
    
    Res = 0
    for i in range(1, len(gis)):
        if gis[i-1].permeability != '':
            temp = 2*math.pi*float(gis[i-1].permeability)*10**(-15)*float(gis[i-1].thickness)*dP/spz
            ln1 = (math.log(Rc / (radius[i][0] + D)) +(Rc -(radius[i][0] + D))/(Rc - D) + math.log(Rc / (radius[i][0] + D)) +(Rc -(radius[i][0] + D))/(Rc - D))**(-1)
            ln2 = (math.log(Rc / (radius[i][1] + D)) +(Rc -(radius[i][1] + D))/(Rc - D) + math.log(Rc / (radius[i][1] + D)) +(Rc -(radius[i][1] + D))/(Rc - D))**(-1)
            ln3 = (math.log(Rc / (radius[i][2] + D)) +(Rc -(radius[i][2] + D))/(Rc - D) + math.log(Rc / (radius[i][2] + D)) +(Rc -(radius[i][2] + D))/(Rc - D))**(-1)
            ln_min = min(ln1, ln2, ln3)
            Q1 = ln_min*temp*86400
            if ustoy[i][0] == 'да' or ustoy[i][1] == 'да' or ustoy[i][2] == 'да':
                Q1 = 0
            if gis[i].curr_saturation != "В":
                Q1 = 0
            ln1 = (math.log(Rc / (radius[i][0] + D)) +(Rc -(radius[i][0] + D))/(Rc - D) + float(gelling[0].get("Rост_в"))*math.log(Rc / (radius[i][0] + D)) +(Rc -(radius[i][0] + D))/(Rc - D))**(-1)
            ln2 = (math.log(Rc / (radius[i][1] + D)) +(Rc -(radius[i][1] + D))/(Rc - D) + float(gelling[1].get("Rост_в"))*math.log(Rc / (radius[i][1] + D)) +(Rc -(radius[i][1] + D))/(Rc - D))**(-1)
            ln3 = (math.log(Rc / (radius[i][2] + D)) +(Rc -(radius[i][2] + D))/(Rc - D) + float(gelling[2].get("Rост_в"))*math.log(Rc / (radius[i][2] + D)) +(Rc -(radius[i][2] + D))/(Rc - D))**(-1)
            ln_min = min(ln1, ln2, ln3)
            Q = ln_min*temp*86400
            if ustoy[i-1][0] == 'да' or ustoy[i-1][1] == 'да' or ustoy[i-1][2] == 'да':
                Q = 0
            if gis[i-1].curr_saturation != "В":
                Q = 0
            if gis[i-1].paker_isolation != "нет":
                Q = Q1
            Res += Q
    return Res


def calcQg(gis, radius, gelling, ustoy):
    dP = Ppl**2 - Pzab**2 
    
    Res = 0
    for i in range(1, len(gis)):
        if gis[i-1].permeability != '':
            temp = math.pi*float(gis[i-1].permeability)*10**(-15)*float(gis[i-1].thickness)*dP/(cPzg*10**(5))
            ln1 = (math.log(Rc / (radius[i][0] + D)) +(Rc -(radius[i][0] + D))/(Rc - D) + math.log(Rc / (radius[i][0] + D)) +(Rc -(radius[i][0] + D))/(Rc - D))**(-1)
            ln2 = (math.log(Rc / (radius[i][1] + D)) +(Rc -(radius[i][1] + D))/(Rc - D) + math.log(Rc / (radius[i][1] + D)) +(Rc -(radius[i][1] + D))/(Rc - D))**(-1)
            ln3 = (math.log(Rc / (radius[i][2] + D)) +(Rc -(radius[i][2] + D))/(Rc - D) + math.log(Rc / (radius[i][2] + D)) +(Rc -(radius[i][2] + D))/(Rc - D))**(-1)
            ln_min = min(ln1, ln2, ln3)
            Q1 = ln_min*temp*86400
            if ustoy[i][0] == 'да' or ustoy[i][1] == 'да' or ustoy[i][2] == 'да':
                Q1 = 0
            if gis[i].curr_saturation != "В":
                Q1 = 0
            ln1 = (math.log(Rc / (radius[i][0] + D)) +(Rc -(radius[i][0] + D))/(Rc - D) + float(gelling[0].get("Rост_г"))*math.log(Rc / (radius[i][0] + D)) +(Rc -(radius[i][0] + D))/(Rc - D))**(-1)
            ln2 = (math.log(Rc / (radius[i][1] + D)) +(Rc -(radius[i][1] + D))/(Rc - D) + float(gelling[1].get("Rост_г"))*math.log(Rc / (radius[i][1] + D)) +(Rc -(radius[i][1] + D))/(Rc - D))**(-1)
            ln3 = (math.log(Rc / (radius[i][2] + D)) +(Rc -(radius[i][2] + D))/(Rc - D) + float(gelling[2].get("Rост_г"))*math.log(Rc / (radius[i][2] + D)) +(Rc -(radius[i][2] + D))/(Rc - D))**(-1)
            ln_min = min(ln1, ln2, ln3)
            Q = ln_min*temp*86400/1000
            if ustoy[i-1][0] == 'да' or ustoy[i-1][1] == 'да' or ustoy[i-1][2] == 'да':
                Q = 0
            if gis[i-1].curr_saturation != "Г":
                Q = 0
            if gis[i-1].paker_isolation != "нет":
                Q = Q1
            Res += Q
    return Res
        



    
def calculation_click(data):    
    h_w , h_g, m_w, m_g, k_w, k_g = get_gis_calc(data.gis)
    Volumes, Vol_w, Vol_g = get_k_h(data.gis, h_w , h_g, k_w, k_g)
    radius_data = []
    for i in range(len(data.gis)):
        t1 = step1(data.gis[i], data.gelling[0], Volumes[i])
        t2 = step1(data.gis[i], data.gelling[1], Volumes[i])
        t3 = step1(data.gis[i], data.gelling[2], Volumes[i])
        r1, r2, r3 = step2(t1, t2, t3, data.gis[i], data.gelling)
        radius_data.append([r1, r2, r3])
    


    t1_w, P1_w, r1_res_w, v1_res_w = step1fin(h_w, m_w, k_w, data.gelling[0], Vol_w)
    t2_w, P2_w, r2_res_w, v2_res_w = step1fin(h_w, m_w, k_w, data.gelling[1], Vol_w)
    t3_w, P3_w, r3_res_w, v3_res_w = step1fin(h_w, m_w, k_w, data.gelling[2], Vol_w)
    r1_w, r2_w, r3_w = step2fin(t1_w, t2_w, t3_w, h_w, data.gelling)

    t1_g, P1_g, r1_res_g, v1_res_w = step1fin(h_g, m_g, k_g, data.gelling[0], Vol_g)
    t2_g, P2_g, r1_res_g, v2_res_w = step1fin(h_g, m_g, k_g, data.gelling[1], Vol_g)
    t3_g, P3_g, r1_res_g, v3_res_w = step1fin(h_g, m_g, k_g, data.gelling[2], Vol_g)
    r1_g, r2_g, r3_g = step2fin(t1_g, t2_g, t3_g, h_g, data.gelling)

    t1_w_c, P1_w_c, r1_res_w_c, v1_res_w_c = calctable(h_w, m_w, k_w, data.gelling[0], Vol_w)
    t2_w_c, P2_w_c, r2_res_w_c, v2_res_w_c = calctable(h_w, m_w, k_w, data.gelling[1], Vol_w)
    t3_w_c, P3_w_c, r3_res_w_c, v3_res_w_c = calctable(h_w, m_w, k_w, data.gelling[2], Vol_w)
    
    radius_data.insert(0, [r1_g, r2_g, r3_g])
    radius_data.insert(0, [r1_w, r2_w, r3_w])
    ustoy_data = ustoy(data.gis, radius_data)
    Qw = calcQw(data.gis, radius_data[2:], data.gelling, ustoy_data[2:])
    Qg = calcQg(data.gis, radius_data[2:], data.gelling, ustoy_data[2:])
    a1 = Qw*Kw
    a2 = a1-Qj
    a3 = a2/Qj*100
    b1 =(Qg*273.15*Ppl_ishod)/(kt * Pbuf * (273.15 + dt_init))*Kg
    b2 = b1 - Qg_init
    b3 = b2/Qg_init*100
    c1 = a1/b1
    c2 = c1 - VGF
    c3 = c2/VGF*100
    table6 = {
        'Qж, м3/сут' : [a1,a2,a3],
        'Qг, тыс. м3/сут':[b1,b2,b3],
        'ВГФ, м3/м3':[c1,c2,c3]
    }
    table1 = {
        '1-й полимер в вод. пл, м' : r1_w,
        '2-й полимер в вод. пл, м' : r2_w,
        '3-й полимер в вод. пл, м' : r3_w,
        '1-й полимер в газ. пл, м' : r2_g,
        '2-й полимер в газ. пл, м' : r2_g,
        '3-й полимер в газ. пл, м' : r2_g,
    }
    table2 = {
        '1-й полимер в вод. пл, м' : ustoy_data[0][0],
        '2-й полимер в вод. пл, м' : ustoy_data[0][1],
        '3-й полимер в вод. пл, м' : ustoy_data[0][2],
        '1-й полимер в газ. пл, м' : ustoy_data[1][0],
        '2-й полимер в газ. пл, м' : ustoy_data[1][1],
        '3-й полимер в газ. пл, м' : ustoy_data[1][2],
    }
    table3 = { 
        'Расч' : {
        '1-й полимер' : [P1_w_c/101325, r1_res_w_c, v1_res_w_c, v1_res_w_c / float(data.gelling[0].get("Q, м3/сут"))*1440],
        '2-й полимер' : [P2_w_c/101325, r2_res_w_c, v2_res_w_c, v2_res_w_c / float(data.gelling[1].get("Q, м3/сут"))*1440],
        '3-й полимер' : [P3_w_c/101325, r3_res_w_c, v3_res_w_c, v3_res_w_c / float(data.gelling[2].get("Q, м3/сут"))*1440],
        },
        'Прин' : {
        '1-й полимер' : [P1_w/101325, r1_res_w, Vol_w, Vol_w / float(data.gelling[0].get("Q, м3/сут"))*1440],
        '2-й полимер' : [P2_w/101325, r2_res_w, Vol_w, Vol_w / float(data.gelling[1].get("Q, м3/сут"))*1440],
        '3-й полимер' : [P3_w/101325, r3_res_w, Vol_w, Vol_w / float(data.gelling[2].get("Q, м3/сут"))*1440],
        }
    }
    table4 = {
        '1-го полимера, мин' : t1_w/60,
        '2-го полимера, мин' : t2_w/60,
        '3-го полимера, мин' : t3_w/60,
        'Итого, мин' : (t1_w + t2_w + t3_w)/60
    }
    table5 = {
        '1-го полимера, м3' : Vol_w,
        '2-го полимера, м3' : Vol_w,
        '3-го полимера, м3' : Vol_w,
        'Итого, м3' : 3*Vol_w
    }
    table = {
        'Радиусы эранов' : table1,
        'Устойчивость экранов' : table2,
        'Время закачки' : table3,
        'Объем закачки в вод. пл.' : table4,
        'Объем закачки в вод. пл.' : table5,
        'Прогноз-е пар-ры работы скв' : table6
    }




    ustoy_data.insert(0, ['Экран из 1 полимера, м', 'Экран из 2 полимера, м', 'Экран из 3 полимера, м', 'Экран'])
    ustoy_data[0].insert(0, 'Устойчивость экранов')
    ustoy_data[1].insert(0, 'Рез-т. В')
    ustoy_data[2].insert(0, 'Рез-т. Г')
    for i in range(len(ustoy_data)-3):
        ustoy_data[i+3].insert(0, f'{i+1}-й инт.')

    radius_data.insert(0, ['Экран из 1 полимера, м', 'Экран из 2 полимера, м', 'Экран из 3 полимера, м'])
    radius_data[0].insert(0, 'Радиусы эранов')
    radius_data[1].insert(0, 'Рез-т. В')
    radius_data[2].insert(0, 'Рез-т. Г')
    for i in range(len(radius_data)-3):
        radius_data[i+3].insert(0, f'{i+1}-й инт.')

    return [radius_data, ustoy_data, table]


def get_radius_image(data):
    h_w , h_g, m_w, m_g, k_w, k_g = get_gis_calc(data.gis)
    Volumes, Vol_w, Vol_g = get_k_h(data.gis, h_w , h_g, k_w, k_g)
    radius_data = []
    for i in range(len(data.gis)):
        t1 = step1(data.gis[i], data.gelling[0], Volumes[i])
        t2 = step1(data.gis[i], data.gelling[1], Volumes[i])
        t3 = step1(data.gis[i], data.gelling[2], Volumes[i])
        r1, r2, r3 = step2(t1, t2, t3, data.gis[i], data.gelling)
        radius_data.append([r1, r2, r3])

    t1_w, P1_w, r1_res_w, v1_res_w = step1fin(h_w, m_w, k_w, data.gelling[0], Vol_w)
    t2_w, P2_w, r2_res_w, v2_res_w = step1fin(h_w, m_w, k_w, data.gelling[1], Vol_w)
    t3_w, P3_w, r3_res_w, v3_res_w = step1fin(h_w, m_w, k_w, data.gelling[2], Vol_w)
    r1_w, r2_w, r3_w = step2fin(t1_w, t2_w, t3_w, h_w, data.gelling)

    t1_g, P1_g, r1_res_g, v1_res_w = step1fin(h_g, m_g, k_g, data.gelling[0], Vol_g)
    t2_g, P2_g, r1_res_g, v2_res_w = step1fin(h_g, m_g, k_g, data.gelling[1], Vol_g)
    t3_g, P3_g, r1_res_g, v3_res_w = step1fin(h_g, m_g, k_g, data.gelling[2], Vol_g)
    r1_g, r2_g, r3_g = step2fin(t1_g, t2_g, t3_g, h_g, data.gelling)

    image1 = io.BytesIO()
    df = pd.DataFrame(radius_data)
    df = df.rename(columns = {0:'Экран из 1 полимера, м', 1:'Экран из 2 полимера, м', 2:'Экран из 3 полимера, м'})
    #df['Скважина'] = 0.108
    df = df.reindex(columns=['Экран из 3 полимера, м', 'Экран из 2 полимера, м', 'Экран из 1 полимера, м']) 
    new_index = {i: f'{i+1}-й инт.' for i in range(len(df)+1)}
    df = df.rename(index=new_index)
    df = df[::-1]
    row_w = pd.Series([r3_w, r2_w, r1_w], index=df.columns, name='Рез-т. В')
    row_g = pd.Series([r3_g, r2_g, r1_g], index=df.columns, name='Рез-т. Г')
    row = pd.Series([0,0,0], index=df.columns, name='')
    df = pd.concat([df, row.to_frame().T])
    df = pd.concat([df, row_g.to_frame().T])
    df = pd.concat([df, row_w.to_frame().T])
    df['Экран из 2 полимера, м'] -= df['Экран из 3 полимера, м']
    df['Экран из 1 полимера, м'] -= (df['Экран из 2 полимера, м']+df['Экран из 3 полимера, м'])

    ax1 = df.plot(kind='barh', stacked=True, width=1, figsize=(10, 12), color=['orange', 'gray', 'lightgray'])
    ax1.set_xticks(range(len(df.columns)))

    temps=[]
    for i, p in enumerate(ax1.patches):
        left, bottom, width, height = p.get_bbox().bounds
        temps.append(width.round(2))

    for i in range(len(temps)):
        if i > len(df) and i <= 2*len(df):
            temps[i] = temps[i] + temps[i-len(df)]
        elif i > len(df) and i <= 3*len(df):
            temps[i] = temps[i] + temps[i-len(df)]

    y_ticks = np.arange(0, math.ceil(max(temps))+0.2 , 0.2)
    ax1.set_xticks(y_ticks)
    ax1.xaxis.set_ticks_position('top')

    for i, p in enumerate(ax1.patches):
        left, bottom, width, height = p.get_bbox().bounds
        temp = str(temps[i].round(2)) if width != 0 else ''
        ax1.annotate(temp, xy=(left+width/2, bottom+height/2), 
                    ha='center', va='center')
    ax1.set_xlabel("Радиус экрана, м")
    ax1.xaxis.set_label_coords(0.5, 1.08)
    ax1.set_ylabel("Интервал притока")
    plt.show()


def get_injection_image(data):
    h_w , h_g, m_w, m_g, k_w, k_g = get_gis_calc(data.gis)
    Volumes, Vol_w, Vol_g = get_k_h(data.gis, h_w , h_g, k_w, k_g)
    radius_data = []
    for i in range(len(data.gis)):
        t1 = step1(data.gis[i], data.gelling[0], Volumes[i])
        t2 = step1(data.gis[i], data.gelling[1], Volumes[i])
        t3 = step1(data.gis[i], data.gelling[2], Volumes[i])
        r1, r2, r3 = step2(t1, t2, t3, data.gis[i], data.gelling)
        radius_data.append([r1, r2, r3])

    t1_w, P1_w, r1_res_w, v1_res_w = step1fin(h_w, m_w, k_w, data.gelling[0], Vol_w)
    t2_w, P2_w, r2_res_w, v2_res_w = step1fin(h_w, m_w, k_w, data.gelling[1], Vol_w)
    t3_w, P3_w, r3_res_w, v3_res_w = step1fin(h_w, m_w, k_w, data.gelling[2], Vol_w)

    P_data, Pust_data, m_data, t_data = get_graph_data(h_w, m_w, k_w, data.gelling, t1_w, t2_w, t3_w)
    plt.figure(figsize=(20, 12))
    plt.plot(t_data,P_data)
    plt.plot(t_data,P_data, 'b', label='P, атм')
    plt.plot(t_data,Pust_data, 'g', label='Pуст, атм')
    parallel_line_y = 390
    plt.axhline(y=parallel_line_y, color='r', linestyle='--', label='Pкрт, атм')
    plt.legend()
    plt.xlabel('Время закачки, мин')
    plt.ylabel('Давление, атм / Объем, м3')
    plt.show()

def get_radius_graph(data):
    h_w , h_g, m_w, m_g, k_w, k_g = get_gis_calc(data.gis)
    Volumes, Vol_w, Vol_g = get_k_h(data.gis, h_w , h_g, k_w, k_g)
    radius_data = []
    for i in range(len(data.gis)):
        t1 = step1(data.gis[i], data.gelling[0], Volumes[i])
        t2 = step1(data.gis[i], data.gelling[1], Volumes[i])
        t3 = step1(data.gis[i], data.gelling[2], Volumes[i])
        r1, r2, r3 = step2(t1, t2, t3, data.gis[i], data.gelling)
        radius_data.append([r1, r2, r3])

    t1_w, P1_w, r1_res_w, v1_res_w = step1fin(h_w, m_w, k_w, data.gelling[0], Vol_w)
    t2_w, P2_w, r2_res_w, v2_res_w = step1fin(h_w, m_w, k_w, data.gelling[1], Vol_w)
    t3_w, P3_w, r3_res_w, v3_res_w = step1fin(h_w, m_w, k_w, data.gelling[2], Vol_w)
    r1_w, r2_w, r3_w = step2fin(t1_w, t2_w, t3_w, h_w, data.gelling)

    r1_data = get_r_data(h_w, data.gelling[0], r1_w, 0)
    r2_data = get_r_data(h_w, data.gelling[1], r2_w, t1_w)
    r3_data = get_r_data(h_w, data.gelling[2], r3_w, t1_w+t2_w)


    P_data, Pust_data, m_data, t_data = get_graph_data(h_w, m_w, k_w, data.gelling, t1_w, t2_w, t3_w)
    plt.figure(figsize=(20, 12))
    plt.plot(t_data,r1_data, color='yellow', label='Экран из 1 полимера, м')
    plt.plot(t_data,r2_data, color='orange', label='Экран из 2 полимера, м')
    plt.plot(t_data,r3_data, color='grey', label='Экран из 3 полимера, м')
    plt.plot(t_data,m_data, color='black', linestyle='dashed', label='ⴜ (t) , Па')
    plt.legend()
    plt.xlabel('Время закачки, мин')
    plt.ylabel('Давление, атм / Объем, м3')
    plt.show()



