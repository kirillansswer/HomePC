import calendar
import datetime
from datetime import date, time
from datetime import datetime

my_date = date.today()

CurrentDay = datetime.now().day
CurrentMonth = 0

#month check
if datetime.now().month == 1:
    CurrentMonth = "Января"
if datetime.now().month == 2:
    CurrentMonth = "Февраля"
if datetime.now().month == 3:
    CurrentMonth = "Марта"
if datetime.now().month == 4:
    CurrentMonth = "Апреля"
if datetime.now().month == 5:
    CurrentMonth = "Мая"
if datetime.now().month == 6:
    CurrentMonth = "Июня"
if datetime.now().month == 7:
    CurrentMonth = "Июля"
if datetime.now().month == 8:
    CurrentMonth = "Августа"
if datetime.now().month == 9:
    CurrentMonth = "Сентебря"
if datetime.now().month == 10:
    CurrentMonth = "Октября"
if datetime.now().month == 11:
    CurrentMonth = "Ноября"
if datetime.now().month == 12:
    CurrentMonth = "Декабря"

#weekdaycheck
if calendar.day_name[my_date.weekday()] == 'Monday':
    weekday = "Понедельник"
if calendar.day_name[my_date.weekday()] == 'Tuesday':
    weekday = "Вторник"
if calendar.day_name[my_date.weekday()] == 'Wednesday':
    weekday = "Среда"
if calendar.day_name[my_date.weekday()] == 'Thursday':
    weekday = "Четверг"
if calendar.day_name[my_date.weekday()] == 'Fridsay':
    weekday = "Пятница"
if calendar.day_name[my_date.weekday()] == 'Saturday':
    weekday = "Суббота"
if calendar.day_name[my_date.weekday()] == 'Sunday':
    weekday = "Воскресение"
print(CurrentMonth)
print(weekday)

