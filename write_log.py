from datetime import datetime
from time import time, sleep
from random import randrange
import csv

if __name__ == '__main__':
    current_seconds = int(datetime.fromtimestamp(time()).strftime('%S'))

    if current_seconds != 0:
        sleep(60 - current_seconds)

    while True:
        temp = randrange(60, 71)
        humidity = randrange(30, 101)
        time_stamp = time()
        print(temp)
        print(humidity)
        print(datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S'))

        current_date = datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d')
        current_time = datetime.fromtimestamp(time_stamp).strftime('%H:%M')
        hour = datetime.fromtimestamp(time_stamp).strftime('-%H00-')
        file_name = current_date + hour + 'weather.csv'
        print("Date:{} Time:{}".format(current_date, current_time))

        with open(file_name, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([current_date, current_time, temp, humidity])

        sleep(60)
