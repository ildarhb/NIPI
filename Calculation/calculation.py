import math
from Calculation.add_init import *
import pandas as pd
import io
import matplotlib.pyplot as plt

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
            m_res = (m1+m2+m3)/2

        if t > (t1_w+t2_w+t3_w):
            P_res = 0
            m_res = 0 
        P_ust = (P_res - 1000*9.81*1757/101325 ) if P_res - 1000*9.81*1757/101325 > 0 else 0
        Pust_data.append(P_ust)
        P_data.append(P_res)
        m_data.append(m_res)

    return P_data, Pust_data, m_data, t_data
        


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
        else:
            return t_res
    return t_res

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
                return t_res
    return t_res


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
    Vol_w = 0
    Vol_g = 0

    for i in range(len(gis)):
        if gis[i].thickness not in ['','None'] and gis[i].permeability not in ['','None']:
            res1 += float(gis[i].thickness)*float(gis[i].permeability)/(h_w*k_w+h_g*k_g)

    for i in range(len(gis)):
        if gis[i].thickness not in ['','None'] and gis[i].permeability not in ['','None']:
            res2 = float(gis[i].thickness)*float(gis[i].permeability)/(h_w*k_w+h_g*k_g)*res1
            Volumes.append(res2*100)
            if gis[i].curr_saturation == 'В':
                Vol_w += res2*100
            else:
                Vol_g += res2*100
        else:
            Volumes.append(0)
    return Volumes, Vol_w, Vol_g

def get_temp(data, a, b, c):
    dP = 7.1*10**5
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

def calcQ(gis, radius, gelling, ustoy):
    dP = 7.1*10**5
    spz = 0.00082
    Rc = 250
    D = 0.108 
    
    Res = 0
    for i in range(len(gis)):
        if gis[i].permeability != '':
            temp = 2*math.pi*float(gis[i].permeability)*10**(-15)*float(gis[i].thickness)*dP/spz
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
            # if ustoy[i][0] == 'да' or ustoy[i][1] == 'да' or ustoy[i][2] == 'да':
            #     Q = 0
            if gis[i].curr_saturation != "В":
                Q = 0
            # if gis[i].paker_isolation == "нет":
            #     Q = Q1
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

    t1_w= step1fin(h_w, m_w, k_w, data.gelling[0], Vol_w)
    t2_w = step1fin(h_w, m_w, k_w, data.gelling[1], Vol_w)
    t3_w= step1fin(h_w, m_w, k_w, data.gelling[2], Vol_w)
    r1_w, r2_w, r3_w = step2fin(t1_w, t2_w, t3_w, h_w, data.gelling)

    t1_g = step1fin(h_g, m_g, k_g, data.gelling[0], Vol_g)
    t2_g = step1fin(h_g, m_g, k_g, data.gelling[1], Vol_g)
    t3_g = step1fin(h_g, m_g, k_g, data.gelling[2], Vol_g)
    r1_g, r2_g, r3_g = step2fin(t1_g, t2_g, t3_g, h_g, data.gelling)
    
    radius_data.insert(0, [r1_g, r2_g, r3_g])
    radius_data.insert(0, [r1_w, r2_w, r3_w])
    ustoy_data = ustoy(data.gis, radius_data)

    #res = calcQ(data.gis, radius_data[2:], data.gelling, ustoy_data[2:])

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

    return [radius_data, ustoy_data, '', plt]


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

    t1_w= step1fin(h_w, m_w, k_w, data.gelling[0], Vol_w)
    t2_w = step1fin(h_w, m_w, k_w, data.gelling[1], Vol_w)
    t3_w= step1fin(h_w, m_w, k_w, data.gelling[2], Vol_w)
    r1_w, r2_w, r3_w = step2fin(t1_w, t2_w, t3_w, h_w, data.gelling)

    t1_g = step1fin(h_g, m_g, k_g, data.gelling[0], Vol_g)
    t2_g = step1fin(h_g, m_g, k_g, data.gelling[1], Vol_g)
    t3_g = step1fin(h_g, m_g, k_g, data.gelling[2], Vol_g)
    r1_g, r2_g, r3_g = step2fin(t1_g, t2_g, t3_g, h_g, data.gelling)

    image1 = io.BytesIO()
    df = pd.DataFrame(radius_data)
    df = df.rename(columns = {0:'Экран из 1 полимера, м', 1:'Экран из 2 полимера, м', 2:'Экран из 3 полимера, м'})
    #df['Скважина'] = 0.108
    df = df.reindex(columns=['Экран из 3 полимера, м', 'Экран из 2 полимера, м', 'Экран из 1 полимера, м']) 
    new_index = {i: f'{i+1}-й инт.' for i in range(len(df)+1)}
    df = df.rename(index=new_index)
    df = df[::-1]
    row_w = pd.Series([r1_w, r2_w, r3_w], index=df.columns, name='Рез-т. В')
    row_g = pd.Series([r1_g, r2_g, r3_g], index=df.columns, name='Рез-т. Г')
    row = pd.Series([0,0,0], index=df.columns, name='')
    df = pd.concat([df, row.to_frame().T])
    df = pd.concat([df, row_g.to_frame().T])
    df = pd.concat([df, row_w.to_frame().T])
    ax1 = df.plot(kind='barh', stacked=True, width=1, figsize=(10, 12))
    ax1.set_xticks(range(len(df.columns)))
    ax1.set_xticklabels([], rotation=90)
    for p in ax1.patches:
        left, bottom, width, height = p.get_bbox().bounds
        temp = str(width.round(2)) if width != 0 else ''
        ax1.annotate(temp, xy=(left+width/2, bottom+height/2), 
                    ha='center', va='center')
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

    t1_w= step1fin(h_w, m_w, k_w, data.gelling[0], Vol_w)
    t2_w = step1fin(h_w, m_w, k_w, data.gelling[1], Vol_w)
    t3_w= step1fin(h_w, m_w, k_w, data.gelling[2], Vol_w)
    r1_w, r2_w, r3_w = step2fin(t1_w, t2_w, t3_w, h_w, data.gelling)

    t1_g = step1fin(h_g, m_g, k_g, data.gelling[0], Vol_g)
    t2_g = step1fin(h_g, m_g, k_g, data.gelling[1], Vol_g)
    t3_g = step1fin(h_g, m_g, k_g, data.gelling[2], Vol_g)
    r1_g, r2_g, r3_g = step2fin(t1_g, t2_g, t3_g, h_g, data.gelling)
    

    P_data, Pust_data, m_data, t_data = get_graph_data(h_w, m_w, k_w, data.gelling, t1_w, t2_w, t3_w)
    plt.figure(figsize=(20, 12))
    plt.plot(t_data,P_data)
    plt.plot(t_data,P_data, 'b', label='P, атм')
    plt.plot(t_data,Pust_data, 'g', label='Pуст, атм')
    #plt.plot(t_data,m_data, color='black', linestyle='dashed', label='ⴜ (t) , Па')
    parallel_line_y = 390
    plt.axhline(y=parallel_line_y, color='r', linestyle='--', label='Pкрт, атм')
    plt.legend()
    plt.xlabel('Время закачки, мин')
    plt.ylabel('Давление, атм / Объем, м3')
    plt.show()