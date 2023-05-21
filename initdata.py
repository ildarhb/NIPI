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
    data.append(InitGis(
            #интервал
            name = "Данные ГИС по скважине",
            #пласт
            plast = "Пласт",
            #пропласток
            proplast = "Пропласток",
            #глубина
            depth = "Глубина по стволу H (md), м",
            #толщина
            thickness = "Толщина по стволу L (md), м,",
            #глубина абсотлют
            abs_depth = "Глубина абсолютная H (abs), м",
            #тольщина абсолют
            abs_thickness = "Толщина абсолютная L (abs), м", 
            #пористость
            porosity =  "Пористость, %" ,
            #проницаемость
            permeability = "Проницаемость, мД",
            #литология
            lithology = "Литология",
            #коллектор
            collector = "Коллектор",
            #начальная насыщенность
            init_saturation = "Начальная насыщенность",
            #конченая насыщенность
            curr_saturation = "Текущая насыщенность",
            #склективаня изоляция пакером
            paker_isolation = "Селективная изол-я пакером (искл. из расчета) )"))
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

def get_data(path= "doc/data.xlsx"):
    book = openpyxl.open(path, read_only=True, data_only=True)
    sheet = book.active
    data = {
        "дата_после" :  sheet[2][1].value,
        "пласт" : sheet[4][2].value,
        "Pпл, атм" : sheet[5][2].value,
        "Pзаб, атм" : sheet[6][2].value,
        "Qж, м3/сут" : sheet[7][2].value,
        "Qг, тыс. м3/сут" : sheet[8][2].value,
        "ВГФ, м3/тыс. м3" : sheet[7][2].value/sheet[8][2].value,
        "Dэ/к, мм" : sheet[11][2].value,
        "Dнкт, мм" : sheet[12][2].value,
        "Rс, м" : sheet[13][2].value,
        "Hвд, м" : sheet[14][2].value,
        "Удл, м" : sheet[15][2].value,
        "D скв. дол., мм" : sheet[16][2].value,
        "Н перф, м" : sheet[17][2].value,
        "Толщина стенок НКТ, мм" : sheet[18][2].value,
        "Толщина стенок Э/К, мм" : sheet[19][2].value,
        "Давл. опрессовки, атм" : sheet[20][2].value,
        "Закачка с пакером" : sheet[21][2].value,
        "Вяз-ть пл.воды, сПз" : sheet[23][2].value,
        "Вяз-ть газа, сПз" : sheet[24][2].value,
        "Плотность газа,  г/см3" : sheet[25][2].value,
        "Пл-ть пл.воды, г/см3" : sheet[26][2].value,
        "К-т сверхсжимаемости газа" : sheet[27][2].value,
        "ΔT м/у устьем и забоем, ℃" : sheet[28][2].value,
        "Pбуф, атм" : sheet[29][2].value,
    }
    return data

<<<<<<< HEAD
if __name__=="__main__":
    for item in get_gis():
        print(item.name)
=======
if __name__ == "__main__":
    gis_dat = get_gis()
    test = 2

>>>>>>> f05b0ad5307e25143dc4f2dbb483ece8ff1a13e3
