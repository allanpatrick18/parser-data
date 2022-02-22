from rest_open_hours.database import session
import os
import csv
import typing
from datetime import datetime
from rest_open_hours import database
path, filename = os.path.split(os.path.realpath(__file__))
import logging

week_day = {member.name: str(member.value) for member in database.WeekDays}


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


def convert_open_range(open_range: str) -> dict:
    """
    This function is responsible to generate to extract the information
    begin, end time of restaurants are open and day of the week
    :param open_range:
    :return:
    """
    result = []
    open_range = open_range.replace('-', ' ')
    open_range = open_range.replace(',', ' ')
    open_range = open_range.split(" ")
    list_final = [x for x in open_range if x != '']

    index = 0
    if len(list_final) < 6:
        open_time = {'week_day_begin': list_final[0],
                     'week_day_end': list_final[0],
                     'time_begin': list_final[1] + ' ' + list_final[2].upper(),
                     'time_end': list_final[-2] + ' ' + list_final[-1].upper()}
        result.append(open_time)
        logging.info(open_time)
        return result

    open_time = {'week_day_begin': list_final[0],
                 'week_day_end': list_final[1]}
    if "".join(list_final[2]).lower() in week_day:
        open_time_2 = {'week_day_begin': list_final[2],
                         'week_day_end': list_final[2],
                         'time_begin': list_final[3] + ' ' + list_final[4].upper(),
                         'time_end': list_final[-2] + ' ' + list_final[-1].upper()}
        index = 1
        result.append(open_time_2)
        logging.info(open_time_2)

    open_time['time_begin'] = list_final[2 + index] + ' ' + list_final[3 + index].upper()
    open_time['time_end'] = list_final[-2] + ' ' + list_final[-1].upper()
    result.append(open_time)
    logging.info(open_time)
    return result


def create_restaurant(name: str):
    """
    create new restaurant
    :param name:
    :return:
    """

    restaurant = database.Restaurant(name=name)
    database.session.add(restaurant)
    database.session.commit()
    return restaurant


def insert_to_model(object_dict: dict, restaurant: database.Restaurant) -> None:
    """ Create a entire object """
    model = database.OpenHours()
    model.restaurant = restaurant.id
    model.week_day_begin = object_dict['week_day_begin'].lower()
    model.week_day_end = object_dict['week_day_end'].lower()
    model.time_begin = convert_to_time(object_dict['time_begin'])
    model.time_end = convert_to_time(object_dict['time_end'])
    database.session.add(model)
    database.session.commit()


def query_open_restaurants(date_dt: datetime):
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
    for ele in result.fetchall():
        logging.info(ele)
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
