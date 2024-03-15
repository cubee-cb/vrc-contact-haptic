# VRChat OSC Contact Haptic

A couple versions of a program that interfaces with VRChat's OSC system using "Small example OSC server" from https://github.com/attwad/python-osc.
Use it to feel when someone taps you on your shoulder or head or something. That's about all this is *intended* for, but feel free to expand on it.

The two versions have different setup and functionality:
- Haptic Module: For Raspberry Pi. Listens to OSC messages on the network, taking in an INT from a specified avatar parameter and playing the corresponding effect on an attached DRV2605L Haptic Motor controller. See the code for more details. It requires a server program; I plan to expand it to support multiple modules at some point.
- Contact Haptic: (Old) A haptic module server that takes input from a VRChat contact and forwards it to a specific device running an OSC client that can trigger a vibration.

You may be able to use the OLD Contact Haptic server to control the Haptic Module if you change the parameters they send/receive from each other to the same path, for example "pivibe/vibrate".

Latewarner is just a small thing I forgot was here, it basically just checks the time on certain days and sends a chatbox message to notify everyone of your current sleep schedule predicament. Set "Own Chatbox" to Shown and "Chatbox Position" to Forward so you can see it too.
