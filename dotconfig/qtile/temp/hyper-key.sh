#!/bin/sh
#
# This file contains commands designed to modify an ANSI keyboard
# layout to be more ergonomic and allow a greater range of user-defined
# keybindings by levraging the archaic Hyper key orginally found on
# Symbolics "Space Cadet" keyboards and functionally vestigial in Linux.
# The script can be run standalone to test or set to automatically on
# user login, eg. in $HOME/.config/autostart/hyper-key.desktop

# Start with a clean ANSI US QWERTY layout. This can also be used to
# unset the rest of the configuration commands.
pkill xcape
setxkbmap -layout us

# Abolish CapsLock and replace with Control
setxkbmap -option ctrl:nocaps

# Some Linux distributions like Ubuntu have Hyper set to the same mappings
# as Super (Mod4), so we need to unset those
xmodmap -e "remove Mod4 = Hyper_L"
# Set Escape to be the left Hyper key
# xmodmap -e "keycode 9 = Hyper_L"
# Set Hyper_L to use the normally unused Mod3
xmodmap -e "add Mod3 = Hyper_L"

# Set left Control to Escape
xmodmap -e "keycode 37 = Hyper_L"
# Old Escape / new Hyper_L sends Escape when pressed alone
xcape -e '#9=Escape'
# Old CapsLock / new Control_L sends Escape when pressed alone
xcape -e '#66=Escape'
