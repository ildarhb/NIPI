import openpyxl

book = openpyxl.open("doc/gis.xlsx", read_only=True, data_only=True)
sheet = book.active

class InitGis():
    def __init__(self, name, plast, proplast, depth, 
                thickness,abs_depth,abs_thickness,
                porosity,permeability,lithology,
                collector,init_saturation,curr_saturation):
        self.name = name
        self.plast = plast
        self.proplast = proplast
        self.depth = depth
        self.thickness = thickness
        self.abs_depth = abs_depth
        self.abs_thickness = abs_thickness 
        self.porosity = porosity
        self.permeability = permeability
        self.lithology = lithology
        self.collector = collector
        self.init_saturation = init_saturation
        self.curr_saturation = curr_saturation

    
data = []
for col in range(0,sheet.max_column):
    data.append(InitGis(
        name = sheet[1][col].value,
        plast = sheet[2][col].value,
        proplast = sheet[3][col].value,
        depth = sheet[4][col].value,
        thickness = sheet[5][col].value,
        abs_depth = sheet[6][col].value,
        abs_thickness = sheet[7][col].value,
        porosity = sheet[8][col].value,
        permeability = sheet[9][col].value,
        lithology = sheet[10][col].value,
        collector = sheet[11][col].value,
        init_saturation = sheet[12][col].value,
        curr_saturation = sheet[13][col].value))

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

print(permeability_rezult_b())
