import time
import Adafruit_SSD1306   # This is the driver chip for the Adafruit PiOLED
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import subprocess
#libraries for the GPS
import time
import board
import busio
import adafruit_gps
import serial
#uart = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=10)
uart = serial.Serial("/dev/ttyTHS1", baudrate=9600, timeout=10)
gps = adafruit_gps.GPS(uart)  # Use UART/pyserial
# Return a float representing the percentage of GPU in use.
# On the Jetson Nano, the GPU is GPU0
def get_gpu_usage():
    GPU = 0.0
    with open("/sys/devices/gpu.0/load", encoding="utf-8") as gpu_file:
        GPU = gpu_file.readline()
        GPU = int(GPU)/10
    return GPU
# 128x64 display with hardware I2C:
# setting gpio to 1 is hack to avoid platform detection
disp = Adafruit_SSD1306.SSD1306_128_64(rst=None, i2c_bus=1, gpio=1)
# Initialize library.
disp.begin()
# Clear display.
disp.clear()
disp.display()
# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Load default font.
font = ImageFont.load_default()



gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
gps.send_command(b"PMTK220,1000")
timestamp = time.monotonic()


while True:
    #data read from the GPS
    data = gps.read(32)  # read up to 32 bytes
    if data is not None:
        # convert bytearray to string
        data_string = "".join([chr(b) for b in data])
        print(data_string, end="")

    if time.monotonic() - timestamp > 5:
        # every 5 seconds...
        gps.send_command(b"PMTK605")  # request firmware version
        timestamp = time.monotonic()


    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "free -m | awk 'NR==2{printf \"Mem:  %.0f%% %s/%s M\", $3*100/$2, $3,$2 }'"
    MemUsage = subprocess.check_output(cmd, shell=True)
    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
    Disk = subprocess.check_output(cmd, shell=True)
    # Alternate solution: Draw the GPU usage as text
    # draw.text((x, top+8),     "GPU:  " +"{:3.1f}".format(GPU)+" %", font=font, fill=255)
    # We draw the GPU usage as a bar graph
    string_width, string_height = font.getsize("GPU:  ")
    # Figure out the width of the bar
    full_bar_width = width-(x+string_width)-1
    gpu_usage = get_gpu_usage()
    # Avoid divide by zero ...
    if gpu_usage == 0.0:
        gpu_usage = 0.001
    draw_bar_width = int(full_bar_width*(gpu_usage/100))
    draw.text((x, top),     "GPU:  ", font=font, fill=255)
    draw.rectangle((x+string_width, top, x+string_width +
                    draw_bar_width, top), outline=1, fill=1)
    #draw.text((x, top+8),"current GPS location", font=font, fill=255)
    draw.text((x, top+8),data_string, font=font, fill=255)
    #draw.text((x, top+28),"longitude: :v :v", font=font, fill=255)
    # Display image.
    # Set the SSD1306 image to the PIL image we have made, then dispaly
    disp.image(image)
    disp.display()
    # 1.0 = 1 second; The divisor is the desired updates (frames) per second
    time.sleep(1.0/4)
