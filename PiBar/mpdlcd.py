#!/usr/bin/python
import math
import time
import re

from time import sleep
from os import popen

import Adafruit_CharLCD as LCD

# Raspberry Pi configuration:
lcd_rs = 27  # Change this to pin 21 on older revision Raspberry Pi's
lcd_en = 22
lcd_d4 = 25
lcd_d5 = 24
lcd_d6 = 23
lcd_d7 = 18
lcd_red   = 4
lcd_green = 17
lcd_blue  = 7  # Pin 7 is CE1

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows    = 2

# Initialize the LCD using the pins above.
lcd = LCD.Adafruit_RGBCharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_red, lcd_green, lcd_blue)

re_volume = re.compile('volume:\s*(\d+)%')

previous_title = ''
previous_volume = 0
previous_state = ''

while True:
  mpc_proc = popen('mpc -f "%title%"') 
  title = mpc_proc.readline().rstrip()
  state = mpc_proc.readline().rstrip().split(' ')[0]
  if state != previous_state:
    previous_state = state
    if state != '[playing]':
      lcd.set_color(0, 0, 0)
      lcd.clear()
      popen('i2cset -y 1 0x4b 0 0')
    else:
      lcd.set_color(1.0, 1.0, 1.0)
      previous_title = ''
      previous_volume = 0

  if state == '[playing]':
    mpc_proc = popen('mpc volume')
    volume = int(re_volume.match(mpc_proc.readline()).group(1))
    if volume != previous_volume:
      previous_volume = volume
      if volume == 0:
        popen('i2cset -y 1 0x4b 0 0')
      else:
        popen('i2cset -y 1 0x4b 0 ' + str((volume / 10) + 25))
   
    if title != previous_title:
      previous_title = title
      mpc_proc = popen('mpc -f "%artist%"')
      artist = mpc_proc.readline().rstrip()
      lcd.clear()
      lcd.message(artist)
      lcd.message('\n')
      lcd.message(title)
   
  sleep(1)
