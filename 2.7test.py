import sys
import socket
from datetime import datetime
sys.path.insert(1, "./lib")

import netifaces as ni
import epd2in7b
from PIL import Image, ImageDraw, ImageFont

epd = epd2in7b.EPD()  # get the display
epd.init()  # initialize the display
print("Clear...")  # prints to console, not the display, for debugging
epd.Clear()  # clear the display

hostname = socket.gethostname()

local_ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']

def printToDisplay(string):

    now = datetime.now()
    dt_string = now.strftime("%Y/%m/%d %H:%M:%S")

    HBlackImage = Image.new('1', (epd2in7b.EPD_HEIGHT, epd2in7b.EPD_WIDTH), 255)
    HRedImage = Image.new('1', (epd2in7b.EPD_HEIGHT, epd2in7b.EPD_WIDTH), 255)

    draw = ImageDraw.Draw(HBlackImage)  # Create draw object and pass in the image layer we want to work with (HBlackImage)
    font = ImageFont.truetype('Font.ttc', 18) # Create our font, passing in the font file and font size
    fontsmall = ImageFont.truetype('Font.ttc', 14) # Create our font, passing in the font file and font size
    draw.line((0, 22, 264, 22), fill = 0) # Draw top line
    draw.line((0, 23, 264, 23), fill = 0) # Draw top line
    draw.line((0, 24, 264, 24), fill = 0) # Draw top line
    draw.text((0, 2), string, font=font, fill=0)
    draw.line((0, 157, 264, 157), fill = 0) # Draw bottom line
    draw.line((0, 158, 264, 158), fill = 0) # Draw bottom line
    draw.line((0, 159, 264, 159), fill = 0) # Draw bottom line
    draw.text((0, 160), f"Last Updated: {dt_string}     ", font=fontsmall, fill=0)

    epd.display(epd.getbuffer(HBlackImage), epd.getbuffer(HRedImage))

printToDisplay(f"""NAME: {hostname}
         ETH0         
MAC: {ni.ifaddresses('eth0')[ni.AF_LINK][0]['addr']}
IP: {ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']}



""")
