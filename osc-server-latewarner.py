"""Small example OSC server
+ client to randomise style

https://github.com/attwad/python-osc
"""
# import
import time
from datetime import datetime as dt
import argparse
import math
import random

from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
from pythonosc import udp_client

# variables
# change these to match your setup
defaultVRChatIP = "127.0.0.1" # leave this unless running on a different device
defaultVRChatPort = 9001

defaultModuleIP = "127.0.0.1" # set this to the ip of the vibration module
defaultModulePort = 9000

# change this to "/avatar/parameters/<contact parameter>"
toggleAddress = "/avatar/parameters/toggle/latewarning"

forceEnable = False
loopcount = 0

# functions
def ping_time():
  hour = dt.now().hour

  #hour = loopcount % 24

  end = "AM"
  late = False

  daystring = dt.today().strftime("%A")
  disabledays = ["Friday", "Saturday"]

  # enable latewarning
  if daystring in disabledays:
    print("disabled {}".format(daystring))
  elif hour < 23 and hour > 4:
    print("disabled {}".format(hour))
  else:
    late = True

  if late or forceEnable:
    if hour > 12:
      hour -= 12
      end = "PM"

    if hour == 0:
      hour = 12

    string = "[{0} {1} {2}]".format(hour, end, daystring)

    print(string)

    # send a chatbox message to the game
    client.send_message("/chatbox/input", [string, True, False])

    # toggle the latewarning parameter on the avatar
    client.send_message(toggleAddress, True)

# mainloop
if __name__ == "__main__":

  # parse arguments
  parser = argparse.ArgumentParser()
  
  parser.add_argument("--sendip",
      default=defaultModuleIP, help="The ip of the module to send vibration info to")
  parser.add_argument("--sendport",
      type=int, default=defaultModulePort, help="The port of the module to send vibration info to")

  args = parser.parse_args()

  # set up udp client for sending data to the vibration module
  client = udp_client.SimpleUDPClient(args.sendip, args.sendport)

  running = True
  while running:
    ping_time()
    time.sleep(10)
    loopcount += 1

