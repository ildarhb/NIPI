import math
from Application.WindowData import WindowData
from Calculation.add_init import *

def step1(item, gell):
    temp = []
    if item.collector == "Да" and item.plast != "н/д":
        for i in range(10):
            t = (i+1)*30
            r = math.sqrt(t*float(gell.get("Q, м3/сут"))/(2*math.pi*float(item.thickness)*86400))+D
            w = r/t
            y = 4*alpha*w/(math.sqrt(8*float(item.permeability)*10**(-15)*float(item.porosity)/100))
            m = float(gell.get("К, Па*с"))*y**(float(gell.get("n"))-1)
            P = Ppl+m*y+m*float(gell.get("Q, м3/сут"))/86400*math.log(r/D)/(2*math.pi*float(item.permeability)*10**(-15)*float(item.thickness))
            V = float(gell.get("Q, м3/сут"))/86400*t

            if P <= Pkp and V <= 100:
                P_res = P
                V_res = V
                r_res = r
    return P_res, V_res, r_res


def step2(P_res):
    return []



def calculation_clic(data):
    print(step1(data.gis[0], data.gelling))