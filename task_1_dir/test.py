from datetime import datetime, timedelta

s1 = '07.02.2022'
s2 = '09.02.2022'

d1 = datetime.strptime(s1, '%d.%m.%Y')
d2 = datetime.strptime(s2, '%d.%m.%Y')
d3 = d2 + timedelta(days=1)

print(str(d3.strftime('%d.%m.%Y')))