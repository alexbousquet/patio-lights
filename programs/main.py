#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
from rpi_ws281x import PixelStrip, Color
import argparse

# LED strip configuration:
LED_COUNT = 300        # Number of LED pixels.
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)


def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, color)
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)


def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)


def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)


def rainbowCycle(strip, wait_ms=20, iterations=100):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel(
                (int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)


def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, wheel((i + j) % 255))
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)

def pink(strip):
    "Simply pink"

    for i in range(0, strip.numPixels()):
        strip.setPixelColor(i, wheel(100))
        
    strip.show()
    
def america(strip, wait_ms=50):
    "Now with 5% more Bald Eagle!"
    
    start_num = 60
    num_pixels = strip.numPixels() - start_num
    
    split1 = start_num + (num_pixels // 3)
    split2 = start_num + ((num_pixels // 3) * 2)
    
    for i in range(start_num, split1):
        strip.setPixelColor(i, Color(255,0,0))
    
    for i in range(split1, split2):
        strip.setPixelColor(i, Color(100,100,100))
    
    for i in range(split2, strip.numPixels()):
        strip.setPixelColor(i, Color(0,0,255))
    
    strip.show()

def americaCycle(strip, wait_ms=500):
    "Now with 50% more Bald Eagle!"
    color_red = Color(255,0,0)
    color_white = Color(100,100,100)
    color_blue = Color(0,0,255)

    start_1 = 60
    # num_pixels = 300 - start_1 
    num_pixels = strip.numPixels() - start_1
    interval = (num_pixels // 3)
    start_2 = start_1 + interval # 140
    start_3 = start_2 + interval # 220

    for i in range(0,num_pixels):
        pixel_red = (start_1 + i) % strip.numPixels()
        pixel_white = (start_2 + i) % strip.numPixels()
        pixel_blue = (start_3 + i) % strip.numPixels()

        if pixel_red < start_1: pixel_red += start_1

        if pixel_white < start_2: pixel_white += start_1

        if pixel_blue < start_3: pixel_blue += start_1
        
        strip.setPixelColor(pixel_red, color_red)
        strip.setPixelColor(pixel_white, color_white)
        strip.setPixelColor(pixel_blue, color_blue)

        # print('i: '+ format(i) + '  red: ' + format(pixel_red) + '   white: ' + format(pixel_white) + '  blue: ' + format(pixel_blue))
        strip.show()
        time.sleep(wait_ms / 1000.0)

def colorCycle(strip, color1, color2, color3, wait_ms=200):
    "Distributed three color chase"

    start_1 = 60
    # num_pixels = 300 - start_1 
    num_pixels = strip.numPixels() - start_1
    interval = (num_pixels // 3)
    start_2 = start_1 + interval # 140
    start_3 = start_2 + interval # 220

    for i in range(0,num_pixels):
        pixel1 = (start_1 + i) % strip.numPixels()
        pixel2 = (start_2 + i) % strip.numPixels()
        pixel3 = (start_3 + i) % strip.numPixels()

        if pixel1 < start_1: pixel1 += start_1

        if pixel2 < start_2: pixel2 += start_1

        if pixel3 < start_3: pixel3 += start_1
        
        strip.setPixelColor(pixel1, color1)
        strip.setPixelColor(pixel2, color2)
        strip.setPixelColor(pixel3, color3)

        strip.show()
        time.sleep(wait_ms / 1000.0)

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    wait_time = input("Enter speed in milliseconds:")

    print('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:
        while True:
            # rainbowCycle(strip)
            # pink(strip)
            # america(strip)
            #americaCycle(strip)
            colorCycle(strip,wheel(100),wheel(190),wheel(40),wait_time)




    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0, 0, 0), 5)
