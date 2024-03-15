"""Small example OSC server

by default this reads from a contact assigned with the parameter "detector/head", but any arbitrary contact/parameter can be defined with the --contact argument

https://github.com/attwad/python-osc
"""
# import
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

defaultModuleIP = "192.168.0.113" # set this to the ip of the vibration module
#defaultModuleIP = "192.168.0.195" # set this to the ip of the vibration module
defaultModulePort = 9002

contactAddress = "detector/head"

# functions
def vibration_handler(unused_addr, args, contactOn):
  print("[{0}] ~ {1}".format(args[0], contactOn))

  # forward vibration message to the vibration module
  if (contactOn):
    client.send_message("/vibration/amplitude", 100)
    client.send_message("/vibration/duration", 200)
  else:
    client.send_message("/vibration/amplitude", 0)
    client.send_message("/vibration/duration", 0)

  #client.send_message("/vibration", strength)

# mainloop
if __name__ == "__main__":

  # parse arguments
  parser = argparse.ArgumentParser()
  
  parser.add_argument("--ip",
      default=defaultVRChatIP, help="The ip of the device running vrchat")
  parser.add_argument("--port",
      type=int, default=defaultVRChatPort, help="The port vrchat will broadcast osc data out of, normally 9001")

  parser.add_argument("--sendip",
      default=defaultModuleIP, help="The ip of the module to send vibration info to")
  parser.add_argument("--sendport",
      type=int, default=defaultModulePort, help="The port of the module to send vibration info to")
      
  parser.add_argument("--contact",
      default=contactAddress, help="The parameter name of the contact to read from")

  args = parser.parse_args()

  # build the contact's full address
  contactAddress = "/avatar/parameters/{0}".format(args.contact)
  print("Reading from \"{0}\"".format(contactAddress))

  # set up udp client for sending data to the vibration module
  client = udp_client.SimpleUDPClient(args.sendip, args.sendport)

  # map adresses to functions
  dispatcher = Dispatcher()
  dispatcher.map(contactAddress, vibration_handler, "contact")
  # dispatcher.map( address, function, pretty name, ?? )

  # set up udp server to receive osc from vrchat
  server = osc_server.ThreadingOSCUDPServer(
      (args.ip, args.port), dispatcher)
  print("Listening on {0}:{1}".format(args.ip, args.port))
  print("Forwarding to {0}:{1}".format(args.sendip, args.sendport))

  # run server
  server.serve_forever()

