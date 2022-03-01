from rest_open_hours.database import session
import os
import csv
import typing

from datetime import datetime
from rest_open_hours import database
path, filename = os.path.split(os.path.realpath(__file__))
import logging

logging.basicConfig(level=logging.INFO)
week_day = {member.name: int(member.value) for member in database.WeekDays}


def read_csv() -> typing.List:
    """This function will load the CSV in memory"""
    data_open = []
    with open(path + '/rest_open_hours.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            logging.info(row)
            line_count += 1
            data_open.append({'name': row[0], 'open_range': row[1]})
        logging.info(f'Processed {line_count} lines.')
    return data_open


def convert_to_time(time_date: datetime) -> str:
    """
    This function convert the datetime to time
    :param time_date:
    :return:
    """
    if len(time_date.split(":")) > 1:
        time_date = datetime.strptime(time_date, '%I:%M %p')
    else:
        time_date = datetime.strptime(time_date, '%I %p')
    return str(time_date.time())


def convert_open_range(open_range: str) -> list:
    """
    This function is responsible to generate to extract the information
    begin, end time of restaurants are open and day of the week
    :param open_range:
    :return:
    """
    week_days = dict()
    result = []
    time_hours = []
    list_spaced = open_range.split(" ")
    for i in range(len(list_spaced)):
        if list_spaced[i].lower() == 'pm':
            time_hours.append(list_spaced[i - 1] + ' ' + 'PM')
        if list_spaced[i].lower() == 'am':
            time_hours.append(list_spaced[i - 1] + ' ' + 'AM')

    open_range = open_range.replace(" ", "")
    index = 0
    pos = 0
    while pos < len(open_range):
        if open_range[pos:pos+3].lower() in week_day:
            if index not in week_days:
                week_days[index] = []

            week_days[index].append(open_range[pos:pos+3].lower())
            if open_range[pos + 3] == ',':
                index += 1
        pos+=1

    for k in week_days.keys():
        p = 0
        if len(week_days[k]) > 1:
            p = 1
        open_time = {'week_day_begin': week_days[k][0],
                     'week_day_end': week_days[k][p],
                     'time_begin': time_hours[0],
                     'time_end': time_hours[1]}
        result.append(open_time)
    return result


def create_restaurant(name: str):
    """
    create new restaurant
    :param name:
    :return:
    """

    restaurant = database.Restaurant(name=name)
    try:
        database.session.add(restaurant)
        database.session.commit()
    except:
        pass

    return restaurant


def insert_to_model(object_dict: dict, restaurant: database.Restaurant) -> None:
    """ Create a entire object """
    model = database.OpenHours()
    model.restaurant = restaurant.id
    model.week_day_begin = week_day[object_dict['week_day_begin'].lower()]
    model.week_day_end = week_day[object_dict['week_day_end'].lower()]
    model.time_begin = convert_to_time(object_dict['time_begin'])
    model.time_end = convert_to_time(object_dict['time_end'])
    try:
        database.session.add(model)
        database.session.commit()
    except:
        pass


def list_open_restaurants(date_dt: datetime):
    """
    Query que restaurants that open in the given date"
    :param date_dt:
    :return:
    """
    week = date_dt.weekday()
    time_start = str(date_dt.time())
    conn = database.engine.connect()
    stm = f"""SELECT 
              r.name, 
              time(hours.time_begin) AS hours_start,
              time(hours.time_end) AS hours_end    
              FROM open_hours AS hours  
              INNER JOIN restaurant AS r ON r.id =hours.restaurant
              WHERE 
              {week} BETWEEN hours.week_day_begin AND hours.week_day_end AND
              time('{time_start}') BETWEEN time(hours.time_begin) AND time(hours.time_end)"""
    result = conn.execute(stm)
    response = []
    for ele in result.fetchall():
        response.append(ele)
        logging.info(ele)
    return response


def query_open_hours():
    """
    Query que restaurants that open in the given date"
    :param date_dt:
    :return:
    """

    result = session.query(database.OpenHours).all()
    return result


def parse_csv_into_table() -> None:
    """This function will parse the given csv into a table"""
    csv_rows = read_csv()
    for row in csv_rows:
        restaurant = create_restaurant(row['name'])
        for item in row['open_range'].split('/'):
            open_hour = convert_open_range(item)
            for ele in open_hour:
                insert_to_model(ele, restaurant)
