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

class InitData():
    def __init__(self, data, plast, ppl, pzab, qj, qg,
                vgf, dek,dnkt, rc, nvd, udl, dskv, hpref,
                tolnkt, tolek, dav, zak,vzv, vzg, plg,
                  plvod,kt, dt, pbuf, pkon,rach,pzabpos):
        self.data = data
        self.plast = plast
        self.ppl = ppl
        self.pzab = pzab
        self.qj = qj
        self.qg = qg
        self.vgf = vgf
        self.dek = dek
        self.dnkt = dnkt
        self.rc = rc
        self.nvd = nvd
        self.udl = udl
        self.dskv = dskv
        self.hpref = hpref
        self.tolnkt = tolnkt
        self.tolek = tolek
        self.dav = dav
        self.zak = zak
        self.vzv = vzv
        self.vzg = vzg
        self.plg = plg
        self.plvod = plvod
        self.kt = kt
        self.dt = dt
        self.pbuf = pbuf
        self.pkon = pkon
        self.rach = rach
        self.pzabpos = pzabpos


def get_initdata(path="doc/initdata.xlsx"):
    book = openpyxl.open(path, read_only=True, data_only=True)
    sheet = book.active
    data = []
    data.append(InitData(
        data = "дата_после",
        plast = "пласт",
        ppl = "Pпл, атм",
        pzab = "Pзаб, атм",
        qj = "Qж, м3/сут",
        qg = "Qг, тыс. м3/сут",
        vgf = "ВГФ, м3/тыс. м3",
        dek = "Dэ/к, мм",
        dnkt = "Dнкт, мм",
        rc = "Rс, м",
        nvd = "Hвд, м",
        udl = "Удл, м",
        dskv = "D скв. дол., мм",
        hpref = "Н перф, м",
        tolnkt = "Толщина стенок НКТ, мм",
        tolek = "Толщина стенок Э/К, мм",
        dav = "Давл. опрессовки, атм",
        zak = "Закачка с пакером",
        vzv = "Вяз-ть пл.воды, сПз",
        vzg = "Вяз-ть газа, сПз",
        plg = "Плотность газа,  г/см3",
        plvod = "Пл-ть пл.воды, г/см3",
        kt = "К-т сверхсжимаемости газа",
        dt = "ΔT м/у устьем и забоем, ℃",
        pbuf = "Pбуф, атм",
        pkon = "P конечное на устье, атм",
        rach = "Расход жидкости, м3/сут",
        pzabpos = "Pзаб план-е после РИР, атм"
    ))
    for row in range(1,sheet.max_row-5):
        data.append(InitData(
        data = sheet[row+2][3].value,
        plast = sheet[row+2][9].value,
        ppl = sheet[row+2][20].value,
        pzab = sheet[row+2][18].value,
        qj = sheet[row+2][32].value,
        qg = sheet[row+2][31].value,
        vgf = sheet[row+2][1].value,
        dek = sheet[row+2][1].value,
        dnkt = sheet[row+2][1].value,
        rc = sheet[row+2][26].value,
        nvd = sheet[row+2][11].value,
        udl = sheet[row+2][1].value,
        dskv = sheet[row+2][1].value,
        hpref = sheet[row+2][1].value,
        tolnkt = sheet[row+2][1].value,
        tolek = sheet[row+2][1].value,
        dav = sheet[row+2][1].value,
        zak =sheet[row+2][1].value,
        vzv = sheet[row+2][1].value,
        vzg = sheet[row+2][1].value,
        plg = sheet[row+2][1].value,
        plvod = sheet[row+2][1].value,
        kt = sheet[row+2][1].value,
        dt = sheet[row+2][1].value,
        pbuf = sheet[row+2][1].value,
        pkon = sheet[row+2][1].value,
        rach = sheet[row+2][1].value,
        pzabpos =sheet[row+2][1].value,
        ))
    return data

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

def compositions():
    result = {
        "Наименование" : ['Полимер 1', 'Полимер 2', 'Полимер 3'],
        "К, Па*с" : [0.33,0.48,0.23],
        "n" :[0.50,0.51,0.57],
        "Rост_в" :[50,70,100],
        "Rост_г" :	[1.5,1.7,2.0],
        "Кр.гр.дав_в, атм/м" :	[5, 7, 8],
        "Кр.гр.дав_г, атм/м" :	[2, 3, 4],
        "Q, м3/сут" :[120, 72, 48],
        "V, м3"	:[100, 100, 100],
        "Пл-ть, г/см3" : ['-','-','-'],
        "Время геле-обр-я., мин" :[1000, 1000, 1000],
    }
    return result

if __name__=="__main__":
    df = get_initdata()
    for item in df:
        print(item.data)
