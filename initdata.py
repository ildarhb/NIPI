import openpyxl

class InitGis():
    def __init__(self, name, plast, proplast, depth, 
                thickness,abs_depth,abs_thickness,
                porosity,permeability,lithology,
                collector,init_saturation,curr_saturation, paker_isolation):
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
        self.paker_isolation = paker_isolation

def get_gis(path="doc/gis.xlsx"):
    book = openpyxl.open(path, read_only=True, data_only=True)
    sheet = book.active
    data = []
    for col in range(0,sheet.max_column):
        data.append(InitGis(
            #интервал
            name = sheet[1][col].value,
            #пласт
            plast = sheet[2][col].value,
            #пропласток
            proplast = sheet[3][col].value,
            #глубина
            depth = sheet[4][col].value,
            #толщина
            thickness = sheet[5][col].value,
            #глубина абсотлют
            abs_depth = sheet[6][col].value,
            #тольщина абсолют
            abs_thickness = sheet[7][col].value,
            #пористость
            porosity = sheet[8][col].value if sheet[8][col].value != None else 0, 
            #проницаемость
            permeability = sheet[9][col].value if sheet[9][col].value != None else 0,
            #литология
            lithology = sheet[10][col].value if sheet[10][col].value != None else 0,
            #коллектор
            collector = sheet[11][col].value,
            #начальная насыщенность
            init_saturation = sheet[12][col].value,
            #конченая насыщенность
            curr_saturation = sheet[13][col].value,
            #склективаня изоляция пакером
            paker_isolation = sheet[14][col].value))
    return data



