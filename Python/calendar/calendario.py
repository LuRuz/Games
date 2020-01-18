import calendar
import datetime

a = datetime.datetime.now()


'''anio = a.year
mes = a.month
dia = a.day

fecha = datetime.date(anio, mes, dia)
print(fecha.strftime('%A').upper())'''

anio = a.year

c = calendar.HTMLCalendar(calendar.MONDAY)
str = c.formatmonth(anio, 1)

fic = open("page/datos.html", "w")
fic.write(str)
fic.close()