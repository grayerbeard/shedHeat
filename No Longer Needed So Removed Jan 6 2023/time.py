from datetime import datetime,timedelta
logTime = datetime.now()
minuteStep = 5
time_change = timedelta(minutes=minuteStep)
lastHourInDay = 0
errorLimit = 8
lastDayInWeek = 0
for count in range(0,20000):
	logTime  +=  time_change 
	dayInWeek = logTime.weekday()
	hourInDay = round(logTime.hour + (logTime.minute/60),4)
	change = round((hourInDay - lastHourInDay) * 60,4)
	lastHourInDay = hourInDay
	lowLimit = minuteStep*(1-(errorLimit/100))
	highLimit = minuteStep*(1+(errorLimit/100))
	error = (((change - minuteStep)/minuteStep)-1)*100
	if dayInWeek == lastDayInWeek:
		if (change < lowLimit) and count != 0:
			print("low","lowLimit",lowLimit,"change",change,"highLimit",highLimit,error)
			print("logTime",logTime,"dayInWeek",dayInWeek,"lastHourInDay",lastHourInDay,"hourInDay",hourInDay,"change",change)
			print("\n")
		if (change > highLimit) and count != 0:
			print("high","lowLimit",lowLimit,"change",change,"highLimit",highLimit,error)
			print("logTime",logTime,"dayInWeek",dayInWeek,"lastHourInDay",lastHourInDay,"hourInDay",hourInDay,"change",change)
			print("\n")
	lastDayInWeek = dayInWeek
	
