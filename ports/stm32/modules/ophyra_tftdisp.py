# MicroPython ST7735 TFT display driver
from machine import Pin
from machine import SPI
import font
import time
class CMD_TFT(object):
    # command definitions
    CMD_NOP     = const(0x00) # No Operation
    CMD_SWRESET = const(0x01) # Software reset
    CMD_RDDID   = const(0x04) # Read Display ID
    CMD_RDDST   = const(0x09) # Read Display Status

    CMD_SLPIN   = const(0x10) # Sleep in & booster off
    CMD_SLPOUT  = const(0x11) # Sleep out & booster on
    CMD_PTLON   = const(0x12) # Partial mode on
    CMD_NORON   = const(0x13) # Partial off (Normal)
        
    CMD_INVOFF  = const(0x20) # Display inversion off
    CMD_INVON   = const(0x21) # Display inversion on
    CMD_DISPOFF = const(0x28) # Display off
    CMD_DISPON  = const(0x29) # Display on
    CMD_CASET   = const(0x2A) # Column address set
    CMD_RASET   = const(0x2B) # Row address set
    CMD_RAMWR   = const(0x2C) # Memory write
    CMD_RAMRD   = const(0x2E) # Memory read
            
    CMD_PTLAR   = const(0x30) # Partial start/end address set
    CMD_COLMOD  = const(0x3A) # Interface pixel format
    CMD_MADCTL  = const(0x36) # Memory data access control
            
    CMD_RDID1   = const(0xDA) # Read ID1
    CMD_RDID2   = const(0xDB) # Read ID2
    CMD_RDID3   = const(0xDC) # Read ID3
    CMD_RDID4   = const(0xDD) # Read ID4
            
            # panel function commands
    CMD_FRMCTR1 = const(0xB1) # In normal mode (Full colors)
    CMD_FRMCTR2 = const(0xB2) # In Idle mode (8-colors)
    CMD_FRMCTR3 = const(0xB3) # In partial mode + Full colors
    CMD_INVCTR  = const(0xB4) # Display inversion control

    CMD_PWCTR1  = const(0xC0) # Power control settings
    CMD_PWCTR2  = const(0xC1) # Power control settings
    CMD_PWCTR3  = const(0xC2) # In normal mode (Full colors
    CMD_PWCTR4  = const(0xC3) # In Idle mode (8-colors)
    CMD_PWCTR5  = const(0xC4) # In partial mode + Full colors
    CMD_VMCTR1  = const(0xC5) # VCOM control

    CMD_GMCTRP1 = const(0xE0)
    CMD_GMCTRN1 = const(0xE1)
    def __init__(self):
        """
            SPI      - SPI Bus (CLK/MOSI/MISO)
            DC       - RS/DC data/command flag
            CS       - Chip Select, enable communication
            RST/RES  - Reset
            BL/Lite  - Backlight control
            """
        
        # self.tab = tab
        self.spi = SPI(1, baudrate=8000000, polarity=1, phase=0)
        self.dc  = Pin('D6', Pin.OUT, Pin.PULL_DOWN)
        self.cs  = Pin('A15', Pin.OUT, Pin.PULL_DOWN)
        self.rst = Pin('D7', Pin.OUT, Pin.PULL_DOWN)
        self.bl  = Pin('A7', Pin.OUT, Pin.PULL_DOWN)
        #self.spi, self.dc, self.cs, self.rst, self.bl
        super().__init__()
        
        # self.tab        = tab
        self.power_on     = True
        self.inverted     = False
        self.backlight_on = True
        
        # default margins, set yours in HAL init
        self.margin_row = 0
        self.margin_col = 0
    
    def _set_window(self, x0, y0, x1, y1):
        """
            Set window frame boundaries.
            Any pixels written to the display will start from this area.
        """
        # set row XSTART/XEND
        self.write_cmd(CMD_RASET)
        self.write_data(bytearray([0x00, y0 + self.margin_row, 0x00, y1 + self.margin_row]))

        # set column XSTART/XEND
        self.write_cmd(CMD_CASET)
        self.write_data(bytearray([0x00, x0 + self.margin_col, 0x00, x1 + self.margin_col]))
                        
                        # write addresses to RAM
        self.write_cmd(CMD_RAMWR)


class ST7735(CMD_TFT):
    # colors
    COLOR_BLACK   = const(0x0000)
    COLOR_BLUE    = const(0x001F)
    COLOR_RED     = const(0xF800)
    COLOR_GREEN   = const(0x07E0)
    COLOR_CYAN    = const(0x07FF)
    COLOR_MAGENTA = const(0xF81F)
    COLOR_YELLOW  = const(0xFFE0)
    COLOR_WHITE   = const(0xFFFF)

    
    def init(self, orient=None):

        # hard reset first
        self.reset()
        
        self.write_cmd(CMD_SWRESET)
        time.sleep_ms(150)
        self.write_cmd(CMD_SLPOUT)
        time.sleep_ms(255)
        
        # TODO: optimize data streams and delays
        self.write_cmd(CMD_FRMCTR1)
        self.write_data(bytearray([0x01, 0x2C, 0x2D]))
        self.write_cmd(CMD_FRMCTR2)
        self.write_data(bytearray([0x01, 0x2C, 0x2D, 0x01, 0x2C, 0x2D]))
        time.sleep_ms(10)
        
        self.write_cmd(CMD_INVCTR)
        self.write_data(bytearray([0x07]))
        
        self.write_cmd(CMD_PWCTR1)
        self.write_data(bytearray([0xA2, 0x02, 0x84]))
        self.write_cmd(CMD_PWCTR2)
        self.write_data(bytearray([0xC5]))
        self.write_cmd(CMD_PWCTR3)
        self.write_data(bytearray([0x8A, 0x00]))
        self.write_cmd(CMD_PWCTR4)
        self.write_data(bytearray([0x8A, 0x2A]))
        self.write_cmd(CMD_PWCTR5)
        self.write_data(bytearray([0x8A, 0xEE]))
        
        self.write_cmd(CMD_VMCTR1)
        self.write_data(bytearray([0x0E]))
        
        self.write_cmd(CMD_INVOFF)
        self.write_cmd(CMD_MADCTL)
        
        if orient == None:                      #Si es cero la orientacion es horizontal
            self.write_data(bytearray([0xA0]))  # RGB Cambio de Posicion a Horizontal MV=1 MX=0 MY=1
            self.width = 160                    #Tamaño de la pantalla para el controlador
            self.height = 128
        else:
            self.write_data(bytearray([0x00]))
            self.width = 128
            self.height = 160
    
        self.write_cmd(CMD_COLMOD)
        self.write_data(bytearray([0x05]))
        
        self.write_cmd(CMD_CASET)
        self.write_data(bytearray([0x00, 0x01, 0x00, 127]))
        
        self.write_cmd(CMD_RASET)
        self.write_data(bytearray([0x00, 0x01, 0x00, 159]))
        
        self.write_cmd(CMD_GMCTRP1)
        self.write_data(bytearray([0x02, 0x1c, 0x07, 0x12, 0x37, 0x32,
            0x29, 0x2d, 0x29, 0x25, 0x2b, 0x39, 0x00, 0x01, 0x03, 0x10]))
            
        self.write_cmd(CMD_GMCTRN1)
        self.write_data(bytearray([0x03, 0x1d, 0x07, 0x06, 0x2e, 0x2c,
            0x29, 0x2d, 0x2e, 0x2e, 0x37, 0x3f, 0x00, 0x00, 0x02, 0x10]))
                                   
        self.write_cmd(CMD_NORON)
        time.sleep_ms(10)
                                   
        self.write_cmd(CMD_DISPON)
        time.sleep_ms(100)
            
    def show_image(self, path, x, y):
        imgbmp = open(path)
        
        # set row XSTART/XEND
        self.write_cmd(CMD_RASET)
        self.write_data(bytearray([0x00, y0 + self.margin_row, 0x00, y1 + self.margin_row]))
        
        # set column XSTART/XEND
        self.write_cmd(CMD_CASET)
        self.write_data(bytearray([0x00, x0 + self.margin_col, 0x00, x1 + self.margin_col]))
        
        # write addresses to RAM
        self.write_cmd(CMD_RAMWR)
        
        
        
        self.dc.value(1)
        self.cs.value(0)
        for _ in range(count):
            self.spi.write(color)
        self.cs.value(1)

    def power(self, state=None):
        """
        Get/set display power.
        """
        if state is None:
            return self.power_on
        self.write_cmd(CMD_DISPON if state else CMD_DISPOFF)
        self.power_on = state

    def clear(self, color):
        """
        Clear the display filling it with color.
        """
        self.rect(0, 0, self.width, self.height, color)

    def invert(self, state=None):
        """
        Get/set display color inversion.
        """
        if state is None:
            return self.inverted
        self.write_cmd(CMD_INVON if state else CMD_INVOFF)
        self.inverted = state

    def rgbcolor(self, r, g, b):
        """
        Pack 24-bit RGB into 16-bit value.
        """
        return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)

    def pixel(self, x, y, color):
        """
        Draw a single pixel on the display with given color.
        """
        self._set_window(x, y, x + 1, y + 1)
        self.write_pixels(1, bytearray([color >> 8, color]))

    def rect(self, x, y, w, h, color):
        """
        Draw a rectangle with specified coordinates/size and fill with color.
        """
        # check the coordinates and trim if necessary
        if (x >= self.width) or (y >= self.height):
            return
        if (x + w - 1) >= self.width:
            w = self.width - x
        if (y + h - 1) >= self.height:
            h = self.height - y

        self._set_window(x, y, x + w - 1, y + h - 1)
        self.write_pixels((w*h), bytearray([color >> 8, color]))

    def line(self, x0, y0, x1, y1, color):
        # line is vertical
        if x0 == x1:
            # use the smallest y
            start, end = (x1, y1) if y1 < y0 else (x0, y0)
            self.vline(start, end, abs(y1 - y0) + 1, color)

        # line is horizontal
        elif y0 == y1:
            # use the smallest x
            start, end = (x1, y1) if x1 < x0 else (x0, y0)
            self.hline(start, end, abs(x1 - x0) + 1, color)

        else:
            # Bresenham's algorithm
            dx = abs(x1 - x0)
            dy = abs(y1 - y0)
            inx = 1 if x1 - x0 > 0 else -1
            iny = 1 if y1 - y0 > 0 else -1

            # steep line
            if (dx >= dy):
                dy <<= 1
                e = dy - dx
                dx <<= 1
                while (x0 != x1):
                    # draw pixels
                    self.pixel(x0, y0, color)
                    if (e >= 0):
                        y0 += iny
                        e -= dx
                    e += dy
                    x0 += inx

            # not steep line
            else:
                dx <<= 1
                e = dx - dy
                dy <<= 1
                while(y0 != y1):
                    # draw pixels
                    self.pixel(x0, y0, color)
                    if (e >= 0):
                        x0 += inx
                        e -= dy
                    e += dx
                    y0 += iny

    def hline(self, x, y, w, color):
        if (x >= self.width) or (y >= self.height):
            return
        if (x + w - 1) >= self.width:
            w = self.width - x

        self._set_window(x, y, x + w - 1, y)
        self.write_pixels(x+w-1, bytearray([color >> 8, color]))

    def vline(self, x, y, h, color):
        if (x >= self.width) or (y >= self.height):
            return
        if (y + h -1) >= self.height:
            h = self.height - y

        self._set_window(x, y, x, y + h - 1)
        self.write_pixels(y+h-1, bytearray([color >> 8, color]))

    def text(self, x, y, string, color):
        """
        Draw text at a given position using the user font.
        Font can be scaled with the size parameter.
        """
        z=font.terminalfont
       
        width = z['width'] + 1

        px = x
        for c in string:
            self.char(px, y, c, z, color, 1, 1)
            px += width

            # wrap the text to the next line if it reaches the end
            if px + width > self.width:
                y += z['height'] + 1
                px = x

    def char(self, x, y, char, font, color, sizex=1, sizey=1):
        """
        Draw a character at a given position using the user font.
        Font is a data dictionary, can be scaled with sizex and sizey.
        """
        if font is None:
            return

        startchar = font['start']
        endchar = font['end']
        ci = ord(char)

        if (startchar <= ci <= endchar):
            width = font['width']
            height = font['height']
            ci = (ci - startchar) * width

            ch = font['data'][ci:ci + width]

            # no font scaling
            px = x
            if (sizex <= 1 and sizey <= 1):
                for c in ch:
                    py = y
                    for _ in range(height):
                        if c & 0x01:
                            self.pixel(px, py, color)
                        py += 1
                        c >>= 1
                    px += 1

            # scale to given sizes
            else:
                for c in ch:
                    py = y
                    for _ in range(height):
                        if c & 0x01:
                            self.rect(px, py, sizex, sizey, color)
                        py += sizey
                        c >>= 1
                    px += sizex
        else:
            # character not found in this font
            return

    def reset(self):
        """
        Hard reset the display.
        """
        self.dc.value(0)
        self.rst.value(1)
        time.sleep_ms(500)
        self.rst.value(0)
        time.sleep_ms(500)
        self.rst.value(1)
        time.sleep_ms(500)

    def backlight(self, state=None):
        """
        Get or set the backlight status if the pin is available.
        """
        if self.bl is None:
            return None
        else:
            if state is None:
                return self.backlight_on
            self.bl.value(1 if state else 0)
            self.backlight_on = state

    def write_pixels(self, count, color):
        """
        Write pixels to the display.
        count - total number of pixels
        color - 16-bit RGB value
        """
        self.dc.value(1)
        self.cs.value(0)
        for _ in range(count):
            self.spi.write(color)
        self.cs.value(1)

    def write_cmd(self, cmd):
        """
        Display command write implementation using SPI.
        """
        self.dc.value(0)
        self.cs.value(0)
        self.spi.write(bytearray([cmd]))
        self.cs.value(1)
                    
    def write_data(self, data):
        """
        Display data write implementation using SPI.
        """
        self.dc.value(1)
        self.cs.value(0)
        self.spi.write(data)
        self.cs.value(1)
