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


def abs_thick_rezult_b():
    temp = 0
    for item in data:
        if item.curr_saturation == "В":
            temp += item.abs_thickness
    return temp

def abs_thick_rezult_g():
    temp = 0
    for item in data:
        if item.curr_saturation == "Г":
            temp += item.abs_thickness
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

result = {
    "res1" : thick_rezult_b(),
    "res2" : thick_rezult_g(),
    "h_w, м": abs_thick_rezult_b(),
    "h_g, м": abs_thick_rezult_g(),
    "m_w, м": porosity_rezult_b(),
    "m_g, м": porosity_rezult_g(),
    "k_w, м": permeability_rezult_b(),
    "k_g, м": permeability_rezult_g(),
}

for key,value in result.items():
    print(key, ':', value)
