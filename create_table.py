import calendar
import datetime
import sqlite3
import json

if __name__ == '__main__':
    PATH_SYMPTOMS = 'data/symptoms.json'
    #Соединение с базой данных
    con = sqlite3.connect('data/database.db')
    cur = con.cursor()


    #Создание таблицы с симптомами
    try:
        with open(PATH_SYMPTOMS, encoding='utf-8') as f:
            symp = json.load(f)
    except FileNotFoundError:
        print(f'symptoms.json not found in {PATH_SYMPTOMS}')
        raise FileNotFoundError
        
    cur.execute(f'CREATE TABLE symptoms(profession VARCHAR(255), symptom VARCHAR(255))')
    con.commit()

    for key in symp.keys():
        for value in symp[f"{key}"]:
            cur.execute(f'INSERT INTO symptoms VALUES("{key}", "{value}")')
            con.commit()
    #______________________________________________
    #Создаем таблицу с информацией о пациенте (ФИО пациента, его номер, дата записи, время записи, ФИО врача)
    cur.execute(f'CREATE TABLE records(id VARCHAR(255), name VARCHAR(255), phone VARCHAR(255), date DATE, time TIME, doc_prof VARCHAR(255), doc_name VARCHAR(255), ticket VARCHAR(255))')
    con.commit()
    #______________________________________________
    #Создаем основную таблицу

    #Формируем столбцы временных окон
    time_var = ''
    for i in range(9, 19):
        time_var+=(f"t{i} BOOL, t{i}30 BOOL, ")

    time_var+=("t19 BOOL, t1930 BOOL")

    #Создаем таблицу
    cur.execute(f'CREATE TABLE timetable(profession VARCHAR(255), name VARCHAR(255), date DATE, {time_var})')
    con.commit()

    #Заполняем данные о времени на день
    def fill_time(start, stop):
        time = []
        #0 - свободно
        #1 - занято
        for i in range(9, 20):
            if i >= start and i < stop:
                time.append(0)
                time.append(0)
            else:
                time.append(1)
                time.append(1)

        return str(time)[1:-1]


    #Заводим календарь расписания
    my_calendar = calendar.Calendar(firstweekday=0)

    #Текущая дата
    curYear = datetime.datetime.now().year
    curMonth = datetime.datetime.now().month
    curDay = datetime.datetime.now().day

    recording = [] 
    delta_time = 3 

    year = curYear
    month = curMonth
    for m in range(curMonth, curMonth+delta_time):
        #Заполняем данные на месяц 

        if month > 12:
            month%=12
            year+=1

        days = []
        for i in range(7):
            days.append([])
        
        for date in my_calendar.monthdayscalendar(year, month):
            for i in range(7):
                if date[i] != 0 and (date[i] >= curDay or month > curMonth or year > curYear):
                    days[i].append(date[i])
            
        recording.append(days)

        #Разбиваем все дни месяца по дням недели
        Monday = recording[-1][0]
        Tuesday = recording[-1][1]
        Wednesday = recording[-1][2]
        Thursday = recording[-1][3]
        Friday = recording[-1][4]
        Saturday = recording[-1][5]
        Sunday = recording[-1][6]

        #Терапевт
        #____________________________________________________
        dates_ther = sorted(Monday + Wednesday + Friday)
        time_ther = fill_time(9, 16)

        for d in dates_ther:
            date = str(datetime.date(year, month, d))
            cur.execute(f'INSERT INTO timetable VALUES("Терапевт", "Айболит Сергей Сергеевич", "{date}", {time_ther})')
            cur.execute(f'INSERT INTO timetable VALUES("Терапевт", "Лечебников Антон Иванович", "{date}", {time_ther})')
        con.commit()


        #Хирург
        #____________________________________________________
        dates_surg = sorted(Tuesday + Saturday)
        time_surg = fill_time(10, 14)

        for d in dates_surg:
            date = str(datetime.date(year, month, d))
            cur.execute(f'INSERT INTO timetable VALUES("Хирург", "Резник Максим Владимирович", "{date}", {time_surg})')
        con.commit()

        #Гастроэнтеролог
        #____________________________________________________
        dates_gastr = sorted(Tuesday + Friday)
        time_gastr = fill_time(14, 20)

        for d in dates_gastr:
            date = str(datetime.date(year, month, d))
            cur.execute(f'INSERT INTO timetable VALUES("Гастроэнтеролог", "Пузикова Лидия Васильевна", "{date}", {time_gastr})')
        con.commit()

        #Кардиолог
        #____________________________________________________
        dates_card = sorted(Monday + Wednesday + Saturday)
        time_card = fill_time(15, 19) 

        for d in dates_card:
            date = str(datetime.date(year, month, d))
            cur.execute(f'INSERT INTO timetable VALUES("Кардиолог", "Ишемитов Марат Ренатович", "{date}", {time_card})')
        con.commit()
        
        month += 1