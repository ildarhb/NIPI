from initdata import get_gis

data = get_gis()
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



result = {
    "k_h_const" : k_h_otn(),
    "h_w, м": thick_rezult_b(),
    "h_g, м": thick_rezult_g(),
    "m_w, м": porosity_rezult_b(),
    "m_g, м": porosity_rezult_g(),
    "k_w, м": permeability_rezult_b(),
    "k_g, м": permeability_rezult_g(),
    
}

for key,value in result.items():
    print(key, ':', value)
