from initdata import *
import math


data = get_gis()[1:]
def thick_rezult_b():
    temp = 0
    for item in data:
        if item.curr_saturation == "В":
            temp += item.thickness
    return temp

def thick_rezult_g():
    temp = 0
    for item in data:
        if item.curr_saturation == "Г":
            temp += item.thickness
    return temp

def porosity_rezult_b():
    temp = 0
    for item in data:
        if item.curr_saturation == "В":
            temp += item.porosity*item.thickness
    return temp/thick_rezult_b()

def porosity_rezult_g():
    temp = 0
    for item in data:
        if item.curr_saturation == "Г":
            temp += item.porosity*item.thickness
    return temp/thick_rezult_g()

def permeability_rezult_b():
    temp = 0
    for item in data:
        if item.curr_saturation == "В":
            temp += item.permeability*item.thickness
    return temp/thick_rezult_b()

def permeability_rezult_g():
    temp = 0
    for item in data:
        if item.curr_saturation == "Г":
            temp += item.permeability*item.thickness
    return temp/thick_rezult_g()

def k_h_otn():
    temp1 = 0
    temp2 = 0
    for item in data:
        if item.paker_isolation == "нет":
            temp1 += (item.abs_thickness * item.permeability)/(thick_rezult_b()*permeability_rezult_b()+thick_rezult_g()*permeability_rezult_g())
        else:
            temp1 += 0
    for item in data:
        if item.paker_isolation == "нет":
            temp2 += (item.abs_thickness * item.permeability)/(thick_rezult_b()*permeability_rezult_b()+thick_rezult_g()*permeability_rezult_g())*(1/temp1)
        else:
            temp2 += 0
    return temp2


def get_calc_res():
    result = {
        "k_h_отн" : k_h_otn(),
        "h_w, м": thick_rezult_b(),
        "h_g, м": thick_rezult_g(),
        "m_w, м": porosity_rezult_b(),
        "m_g, м": porosity_rezult_g(),
        "k_w, м": permeability_rezult_b(),
        "k_g, м": permeability_rezult_g(),
    }
    return result
D = 0.108
Q = compositions()["Q, м3/сут"][0]
V_con = 71.08
for i in range(1,10):
    r = math.sqrt(30*i*Q/(2*math.pi*thick_rezult_b()*86400))+D
    w = r/(30*i)
    y =4*0.052*(w)/math.sqrt(8*permeability_rezult_b()*10**(-15)*porosity_rezult_b()/100)
    m = compositions()["К, Па*с"][0]*y**(compositions()["n"][0]-1)
    P = 15908025.0 + m * y + m * Q /86400*math.log(r/D)/(2*math.pi*permeability_rezult_b()*thick_rezult_b()*10**(-15))
    dP = P - 15401400
    V = Q/86400*30*i
    P_N = P if P <= 40000000 else 0
    V_N = V if P <= 40000000 else 0
    r_N = r if P <= 40000000 else 0
    PN_N = P if V <= V_con else 0
    VN_N = V_N if V_N <= V_con else 0
    rN_N = r_N if V_N <= V_con else 0
    print(rN_N)

# if __name__=="__main__":
#     for key,value in compositions().items():
#         print(key, ':', value)
    
