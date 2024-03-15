"""
VRChat OSC DRV2605L-Based Haptic Module
- cubee <['.'<]

Make sure OSC is enabled in VRChat settings and that your avatar has an appropriate contact receiver on it!
Send an INT to the parameter this module reads to activate the corresponding effect.
You can set a contact to drive the parameter directly, triggering "Strong Click", or use the contact and an FX layer state to drive the parameter for a specific effect.

See available effects here:
https://learn.adafruit.com/assets/72594
Send 255 to interrupt the playing effect and stop the motor immediately.

Made for Adafruit DRV2605L Haptic Motor Controller:
https://www.adafruit.com/product/2305

Library install and hardware details:
https://learn.adafruit.com/adafruit-drv2605-haptic-controller-breakout/python-circuitpython

Using PythonOSC:
https://github.com/attwad/python-osc
"""

## config
# you can pass in these values via arguments
# alternatively, you can just change these directly
defaultVRChatIP = "0.0.0.0" # set this to the IP of the device running VRChat
defaultVRChatPort = 9001
contactParameter = "pivibe/head" # the parameter that will control this module
outputVerbose = True


## imports
import argparse

# pythonOSC
try:
  from pythonosc.dispatcher import Dispatcher
  from pythonosc import osc_server
except:
  print("Failed to import PythonOSC. Is it installed?")
  print("See: https://github.com/attwad/python-osc")

# motor initialisation
try:
  import board
  import busio
  import adafruit_drv2605
  motorInitialised = True
  i2c = busio.I2C(board.SCL, board.SDA)
  drv = adafruit_drv2605.DRV2605(i2c)
except:
  motorInitialised = False


## functions
def Vibrate(address: str, args: list, effect: int):
  print("[{0}: {1}] ~ Playing effect {2}".format(address, args[0], effect))
  effect = int(effect)

  # return early if the motor isn't initialised
  if not motorInitialised:
    return


  # immediately stop motor if effect is 255
  if effect == 255:
    drv.stop()

  # do nothing if the parameter sends 0, so the motor can finish vibrating on its own
  elif effect == 0:
    pass

  # play effect on motor
  else:
    drv.sequence[0] = adafruit_drv2605.Effect(effect)
    drv.play()

def Debug(address: str, args: list, effect: int):
  print("[{0}: {1}] ~ Value {2}".format(address, args[0], effect))


## mainloop
if __name__ == "__main__":
  # header message
  if motorInitialised:
    print("Motor initialised.")
    print("Will vibrate the connected haptic motor.")
  else:
    print("Motor library not installed or failed to initialise.")
    print("See: https://learn.adafruit.com/adafruit-drv2605-haptic-controller-breakout/python-circuitpython")
    print("Will only print received messages to console.")

  # parse arguments
  parser = argparse.ArgumentParser()
  
  parser.add_argument("--ip",
      default=defaultVRChatIP, help="The IP of the device running VRChat. Current default: {}".format(defaultVRChatIP))
  parser.add_argument("--port",
      type=int, default=defaultVRChatPort, help="The port VRChat will broadcast OSC data out of. Current default: {}".format(defaultVRChatPort))

  parser.add_argument("--contact",
      default=contactParameter, help="The parameter name of the contact to read from. Current default: {}".format(contactParameter))

  parser.add_argument("--verbose",
      default=outputVerbose, help="Output ALL received OSC messages. Current default: {}".format(outputVerbose))

  args = parser.parse_args()

  # build the contact's full address
  contactParameter = "/avatar/parameters/{0}".format(args.contact)
  print("Reading from \"{0}\"".format(contactParameter))

  # map addresses to functions
  dispatcher = Dispatcher()
  # dispatcher.map( address, function, pretty name, ?? )
  if outputVerbose:
    print("Verbose mode enabled. EVERY detected message will be printed.")
    dispatcher.map("/*", Debug, "verbose")
  dispatcher.map(contactParameter, Vibrate, "contact")

  # set up udp server to receive osc from vrchat
  server = osc_server.ThreadingOSCUDPServer(
      (args.ip, args.port), dispatcher)
  print("Listening on {0}:{1}".format(args.ip, args.port))

  # run server
  server.serve_forever()
