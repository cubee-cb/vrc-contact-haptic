"""Small example OSC server

module tester

https://github.com/attwad/python-osc
"""
# import
import time
import argparse
import math
import random

from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
from pythonosc import udp_client

# variables
#defaultVRChatIP = "127.0.0.1"
#defaultVRChatPort = 9001

defaultModuleIP = "192.168.0.113"
#defaultModuleIP = "192.168.0.195"
defaultModulePort = 9002

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

  print("Forwarding to {0}:{1}".format(args.sendip, args.sendport))

  # run server
  #server.serve_forever()
  running = True
  while running:
    string = input()
    if string == "":
      # send duration in milliseconds
      # send amplitude in range from 0-255
      client.send_message("/vibration/amplitude", 1)
      client.send_message("/vibration/duration", 200)
      time.sleep(1)
      client.send_message("/vibration/amplitude", 0)
      client.send_message("/vibration/duration", 0)
    else:
      running = False
    

