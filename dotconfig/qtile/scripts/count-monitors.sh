#!/bin/bash

xrandr -q | grep -o ' connected' | wc -l
