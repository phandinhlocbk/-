import RPi.GPIO as GPIO
import datetime 
import csv, time

c = 20
count = 0
count2 = 0
timestart = 0
lasttime = time.time()
gap = 0
now = 'no'
error = 'no'

GPIO.setmode(GPIO.BCM)            # Numbers GPIOs by physical location
GPIO.setup(c, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def tinhtoan():
   var=GPIO.input(c)
   global count, now, lasttime, gap, error, timestart
   if var==False:
     count = count + 1   
     time.sleep(1)
     if timestart == 0:
      lasttime = time.time()
      timestart = time.time()
     else:
      nowtime = time.time()
      gap = nowtime-lasttime
      gap = round(gap)
      if gap > 2:
        error = 'yes'
        now = str(datetime.datetime.now())
      else:
        error = 'no'
      lasttime = nowtime
   else:
      nowtime = time.time()
      gap = nowtime-lasttime
      gap = round(gap)
      if gap > 2:
        error = 'yes'
        now = str(datetime.datetime.now())
      else:
        error = 'no'
   print (error)
   return count



def csvwrite():
   with open('tinhtoan.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',')
    spamwriter.writerow([count])
    spamwriter.writerow([error])
    spamwriter.writerow([now])

try:
  while True:
   csvwrite()
   tinhtoan()
  

except KeyboardInterrupt:           # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
  pass
  GPIO.output(LedPin, GPIO.LOW)     # led off
  GPIO.cleanup()                    # Release resource
