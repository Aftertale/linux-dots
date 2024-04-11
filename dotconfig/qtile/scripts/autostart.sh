#!/bin/sh

picom --backend glx --fade-exclude 'class_g = "xsecurelock"' --daemon
