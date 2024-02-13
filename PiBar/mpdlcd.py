#!/usr/bin/python
from time import sleep
from os import popen
from mpd import MPDClient

import board
import digitalio
import pwmio
import adafruit_character_lcd.character_lcd as characterlcd

# Raspberry Pi configuration:
lcd_rs = digitalio.DigitalInOut(board.D27)
lcd_en = digitalio.DigitalInOut(board.D22)
lcd_d7 = digitalio.DigitalInOut(board.D18)
lcd_d6 = digitalio.DigitalInOut(board.D23)
lcd_d5 = digitalio.DigitalInOut(board.D24)
lcd_d4 = digitalio.DigitalInOut(board.D25)
red = pwmio.PWMOut(board.D4)
green = pwmio.PWMOut(board.D17)
blue = pwmio.PWMOut(board.D7)
lcd_columns = 16
lcd_rows = 2

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows    = 2

# Initialize the LCD using the pins above.
lcd = characterlcd.Character_LCD_RGB(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, red, green, blue)

previous_title = ""
previous_volume = 0
previous_state = ""

mpdClient = MPDClient()
mpdClient.connect("localhost", 6600)

while True:
  status = mpdClient.status()
  song = mpdClient.playlistid(status["songid"])[0]
  title = song["title"]
  state = status["state"]
  if state != previous_state:
    previous_state = state
    if state != "play":
      lcd.color = [0, 0, 0]
      lcd.clear()
      popen("i2cset -y 1 0x4b 0 0")
    else:
      lcd.color = [100, 100, 100]
      previous_title = ""
      previous_volume = 0

  if state == "play":
    volume = int(status["volume"])
    if volume != previous_volume:
      previous_volume = volume
      if volume == 0:
        popen("i2cset -y 1 0x4b 0 0")
      else:
        popen("i2cset -y 1 0x4b 0 " + str(round(volume / 4) + 10))

    if title != previous_title:
      previous_title = title
      artist = song["artist"]
      lcd.clear()
      lcd.message = artist + "\n" + title

  sleep(1)
