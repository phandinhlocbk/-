import RPi.GPIO as GPIO
import time
import csv
from flask import Flask, render_template, request
app = Flask(__name__)


GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(21, GPIO.OUT)
GPIO.output(21, GPIO.LOW)
ledsts = 1
count2 = 0
buttonsts = 0
var = 0
var1 = 0


@app.route("/")
def index():
  global var
  buttonsts = GPIO.input(20)
  with open('tinhtoan.csv','rt')as f:
    data = csv.reader(f)
    l = [row for row in data]
    #print(l[0])
  if buttonsts == False:
     var = 0
  else :
     var = 1
  data = {
    'taikyu' : l[0],
    'error' : l[1],
    'errortime':l[2],
    'button' : var,
    'led' : ledsts
     }
  return render_template('taikyu.html', **data)

@app.route('/<deviceName>/<action>')
def action(deviceName, action):
  global  ledsts
  if action == 'on':
      GPIO.output(21, GPIO.HIGH)
      ledsts = ledsts + 1
  if action == 'off':
      GPIO.output(21, GPIO.LOW)
      ledsts = 0
  with open('tinhtoan.csv','rt')as f:
    data = csv.reader(f)
    l = [row for row in data]
    #print(l[0])
  data = {
           'taikyu' : l[0],
           'error' : l[1],
           'errortime':l[2],
           'led' : ledsts,
           'button' : var
          }
  
  return render_template('taikyu.html', **data)

def run():
  if GPIO.input(20) == True:
   print ("loop running")
  time.sleep(1) 


while True:
 run()
 app.run( host='192.168.200.72', port=500)
 time.sleep(2)
 request.eviron.get('werkzeug.server.shutdown')

