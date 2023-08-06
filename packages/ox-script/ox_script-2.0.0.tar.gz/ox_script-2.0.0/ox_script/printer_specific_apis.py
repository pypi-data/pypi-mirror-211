# MIT License

# Copyright (c) 2023 Postek Electronics Co., Ltd

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# For the functions that only have pass in this file, please refer to the ox script development manual for details
# The functions are marked with pass only because they are meanted to be executed on the printer and will not function
# correctly on your device. Please run the script on Postek Printers for most accurate results
def debuglog(info: str):
    """
    Log the information to the debug log file stored inside the printer, the file can be 
        later acccessed through the file manager that comes with the free POSTEK companion app 

    Parameters:
        info (str): The information to be logged
    """
    pass

version = "V2.0.1"
def PTK_getVersion():
    """
    PTK_getVersion is used to get the version of the ox script runtime environment, if there is a mismatch
        between the version of the runtime environment and the version of this script when ran on your devices
        please consider updating the firmware of your printer or updating ox_script from pypi

    """
    return version


MM = 0
DOTS = 1

def PTK_SetUnit(unit=MM) -> None:
    """
    PTK_SetUnit is used to set the unit of measurement for the printer. The default unit is mm.
        After setting a unit, the conversin is automatically applied to all the values that are sent to the printer
        If float is passed in and the unit is dots, the value will be truncated to a integer value

    Parameters:
        unit (int): The unit of measurement to be used. 0 -> mm, 1 -> dots
    """
    pass


# def mmOrDots(value):
#     """
#     mmOrDots is used to convert the value to the unit of measurement that is currently being used

#     Parameters:
#         value (float): The value to be converted

#     Returns:
#         int: The converted value
#     """
#     return int(value)


def PTK_GetErrorInfo() -> str:
    """
    PTK_GetErrorInfo is used to get the error information from the printer

    Returns:
        str: The error information from the printer

    """
    return "Error will be displayed when the script is ran on the printer"


# ===========================================================#
# Functions related to ports of the printer
# ===========================================================#

PORT_SERIAL = 0
PORT_USBDEVICE = 1
PORT_ETHERNET = 2
PORT_BLUETOOTH = 3
PORT_WIFI = 4
PORT_PARALLEL = 5
PORT_WEBSOCK = 6
PORT_USBHOST = 7
PORT_SCRIPT = 8


def PTK_GetPortData(port, dataLen=1024, timeout=5000) -> str:
    """
    PTK_GetPortData is used to get the data from the printer

    Parameters:
        port: The port to get the data from
            PORT_SERIAL: Serial port
            PORT_USBDEVICE: USB Device port
            PORT_ETHERNET: Ethernet port
            PORT_BLUETOOTH: Bluetooth port
            PORT_WIFI: Wifi port
            PORT_PARALLEL: Parallel port
            PORT_WEBSOCK: Websocket port
            PORT_USBHOST: USB Host port
            PORT_SCRIPT: Script port
        dataLen (int): The length of the data to be read
        timeout (int): The timeout for the operation

    Returns:
        str: The data read from the printer or -1 if an error occured or time out is reached 
    """
    return "Data will be read when the script is ran on the printer"


def PTK_SendCmdToPrinter(cmd: str) -> bool or str:
    """
    PTK_SendCmdToPrinter is used to send commands loaded from Forms to the printer or any PPLE
        commands directly to the printer

    Parameters:
        cmd (str): The command to be sent to the printer

    Returns:
        bool/str: The command was sent successfully or the error message if the command was not sent successfully
    """
    return True

def PTK_WriteToSerial(dataSize, dataBuff) -> None:
    """
    PTK_WriteToSerial is used to write data to the serial port of the printer

    Parameters:
        dataSize (int): The size of the data to be written
        dataBuff (str): The data to be written
    
    """

# ===========================================================#
# Functions related to the printer settings
# ===========================================================#

BOTTOM_RIGHT = "T"
TOP_LEFT = "B"


def PTK_SetPrintDirection(direction: str) -> bool or str:
    """
    PTK_SetPrintDirection is used to set the print direction of the printer. The default direction starts at bottom right.

    Parameters:
        direction (string): The direction to be used. "T" -> Top Left, "B" -> Bottom Right

    Returns:
        bool/str: The command was sent successfully or the error message if the command was not sent successfully

    """
    return True


def PTK_CutPage(number_of_labels=1, save_in_flash=False) -> bool or str:
    """
    PTK_CutPage is used to cut the page after printing the number of labels specified

    Parameters:
        number_of_labels (int): The number of labels to be printed before cutting the page
        save_in_flash (bool): Save the command in flash so that the value can be restored when the printer powers up again

    Returns:
        bool/str: The command was sent successfully or the error message if the command was not sent successfully
    """
    return True


def PTK_Reset() -> bool or str:
    """
    PTK_Reset can be used to reset the printer

    Returns:
        bool/str: The command was sent successfully or the error message if the command was not sent successfully
    """
    return True


# ===========================================================#
# Functions for print job related settings
# ===========================================================#

def PTK_SetDarkness(darkness: int) -> bool or str:
    """
    PTK_SetDarkness is used to set the darkness of the print. The default darkness is 8.

    Parameters:
        darkness (int): The darkness to be used. The range is 0 to 30.

    Returns:
        bool/str: The command was sent successfully or the error message if the command was not sent successfully
    """
    return True


GAP_MODE = 0
SPECIAL_MODE = 1
BLACK_LINE_MODE = 2


def PTK_SetLabelHeight(height, mode=GAP_MODE, gapH=3) -> bool or str:
    """
    PTK_SetLabelHeight is used to set the height of the label.

    Parameters:
        height (float): The height of the label in mm or dots(depending on PTK_SetUnit)
        gapH (float): The gap between the labels in mm or dots(depending on PTK_SetUnit)

    Returns:
        bool/str: The command was sent successfully or the error message if the command was not sent successfully
    """
    return True


def PTK_SetLabelWidth(width: int) -> bool or str:
    """
    PTK_SetLabelWidth is used to set the width of the label.

    Parameters:
        width (float): The width of the label in mm or dots(depending on PTK_SetUnit)

    Returns:
        bool/str: The command was sent successfully or the error message if the command was not sent successfully
    """
    return True


def PTK_SetCoordinateOrigin(x=0, y=0) -> bool or str:
    """
    PTK_SetCoordinateOrigin is used to set the origin of the coordinates. The default origin is (0,0)
        which is the topleft corner of the label.

    Parameters:
        x (float): The x coordinate of the origin in mm or dots(depending on PTK_SetUnit)
        y (float): The y coordinate of the origin in mm or dots(depending on PTK_SetUnit) 

    Returns:
        bool/str: The command was sent successfully or the error message if the command was not sent successfully
    """
    return True


def PTK_SetPrintSpeed(speed) -> bool or str:
    """
    PTK_SetPrintSpeed is used to set the print speed of the printer. The default speed and top speed depends on the
        model of the printer.

    Parameters:
        speed (float): The speed to be used in inches per second. The range depends upon the model of the printer.
            Please refer to the user manual of the specific model for more information.

    Returns:
        bool/str: The command was sent successfully or the error message if the command was not sent successfully
    """
    return True


# ===========================================================#
# Text related functions
# ===========================================================#

NORMAL = "N"
REVERSE = "R"
SDRAM = 0
FLASH = 1


def PTK_CreatFont(location, fontname, downloadfontname) -> bool or str:
    """
    PTK_CreatFont is used to create a font in the printer

    Parameters:
        location (int): The location to store the font. 0 -> SDRAM, 1 -> Flash
        fontname (str): The name of the font to be created, the name should be in a single capital letters between A to Z
        downloadfontname (str): The name of the font to be downloaded

    Returns:
        bool/str: The command was sent successfully or the error message if the command was not sent successfully
    """
    return True


def PTK_DrawText(
    x_coordinate: float,
    y_coordinate: float,
    data: str,
    fonts="1",
    font_size=3,
    text_style="N",
    rotation=0,
) -> bool or str:
    """
    PTK_DrawText is used to print text on the label

    Parameters:
        x_coordinate (float): The x coordinate of the text in mm or dots(depending on PTK_SetUnit)
        y_coordinate (float): The y coordinate of the text in mm or dots(depending on PTK_SetUnit) 
        data (string): The text to be printed
        fonts (string): The font to be used. i.e "Inter", the Font should be stored in the fonts folder on the printer
        font_size (int): The size of the font
        text_style (string): The style of the text. "N" -> Normal, "R" -> Reverse
        rotation (int): The rotation of the barcode. The range is 0 to 3 where
            0 = 0 degree, 1 = 90 degree, 2 = 180 degree, 3 = 270 degree

    Returns:
        bool/str: The command was sent successfully or the error message if the command was not sent successfully
    """
    return True

# ===========================================================#
# 2D Barcode related functions
# ===========================================================#


def PTK_DrawBar2D_DATAMATRIX(
    x_coordinate: float, y_coordinate: float, multiplier: int, data: str, rotation=0) -> bool or str:
    """
    PTK_DrawBar2D_DATAMATRIX is used to print a DataMatrix barcode on the label

    Parameters:
        x_coordinate (float): The x coordinate of the 2Dcode in mm or dots(depending on PTK_SetUnit)
        y_coordinate (float): The y coordinate of the 2Dcode in mm or dots(depending on PTK_SetUnit) 
        multiplier (int): The multiplier of the barcode. The range is 1 to 9
        data (string): The data to be printed in the barcode
        rotation (int): The rotation of the barcode. The range is 0 to 3 where
            0 = 0 degree, 1 = 90 degree, 2 = 180 degree, 3 = 270 degree

    Returns:
        bool/str: The command was sent successfully or the error message if the command was not sent successfully
    """
    return True


def PTK_DrawBar2D_QR(
    x_coordinate: float,
    y_coordinate: float,
    qr_version=0,
    rotation=0,
    multiplier=1,
    encode_mode=0,
    correction_level=0,
    masking=8,
    data='string',
) -> bool or str:
    """
    PTK_DrawBar2D_QR is used to print a QR barcode on the label

    Parameters:
        x_coordinate (float): The x coordinate of the 2Dcode in mm or dots(depending on PTK_SetUnit)
        y_coordinate (float): The y coordinate of the 2Dcode in mm or dots(depending on PTK_SetUnit) 
        qr_version (int): The version of the QR code. The range is 0 to 40
        rotation (int): The rotation of the barcode. The range is 0 to 3 where
            0 = 0 degree, 1 = 90 degree, 2 = 180 degree, 3 = 270 degree
        multiplier (int): The multiplier of the barcode. The range is 1 to 99
        encode_mode (int): The encoding mode of the barcode. The range is 0 to 4 where
            0 = Numeric, 1 = Alphanumeric, 2 = Byte, 3 = chinese, 4 = auto
        correction_level (int): The correction level of the barcode. The range is 0 to 3
        masking (int): The masking of the barcode. The range is 0 to 8
        data (string): The data to be printed in the barcode

    Returns:
        bool/str: The command was sent successfully or the error message if the command was not sent successfully
    """
    return True


UPS = 1
NOT_UPS = 0


def PTK_DrawBar2D_MaxiCode(
    x_coordinate: float, y_coordinate: float, is_ups_data: int, data: str, mode=4
) -> bool or str:
    """
    PTK_DrawBar2D_MaxiCode is used to print a MaxiCode barcode on the label

    Parameters:
        x_coordinate (float): The x coordinate of the 2Dcode in mm or dots(depending on PTK_SetUnit)
        y_coordinate (float): The y coordinate of the 2Dcode in mm or dots(depending on PTK_SetUnit) 
        is_ups_data (int): The ups data of the barcode. 0 -> Not UPS, 1 -> UPS
        data (string): The data to be printed in the barcode
        mode (int): The mode of the barcode. The range is 2 to 4

    Returns:
        bool/str: The command was sent successfully or the error message if the command was not sent successfully
    """
    return True


def PTK_DrawBar2D_Pdf417(
    x_coordinate: float,
    y_coordinate: float,
    correction_level: int,
    px: int,
    py: int,
    encode_row: int,
    encode_column: int,
    t: int,
    data: str,
    rotation=0,
) -> bool or str:
    """
    PTK_DrawBar2D_Pdf417 is used to print a Pdf417 barcode on the label

    Parameters:
        x_coordinate (float): The x coordinate of the 2Dcode in mm or dots(depending on PTK_SetUnit)
        y_coordinate (float): The y coordinate of the 2Dcode in mm or dots(depending on PTK_SetUnit) 
        correction_level (int): The correction level of the barcode. The range is 0 to 8
        px (int): The px of the barcode. The range is 2 to 9
        py (int): The py of the barcode. The range is 4 to 99
        encode_row (int): The maxrow of the barcode. The range is 3 to 90
        encode_column (int): The maxcolumn of the barcode. The range is 1 to 30
        t (int): Truncation of the barcode. i.e 0 -> No truncation, 1 -> Truncation
        data (string): The data to be printed in the barcode
        rotation (int): The rotation of the barcode. The range is 0 to 3 where
            0 = 0 degree, 1 = 90 degree, 2 = 180 degree, 3 = 270 degree

    Returns:
        bool/str: The command was sent successfully or the error message if the command was not sent successfully
    """
    return True


def PTK_DrawBar2D_HANXIN(
    x_coordinate: float,
    y_coordinate: float,
    multiplier: int,
    data: str,
    encoding=0,
    correction_level=0,
    masking=0,
    rotation=0,
) -> bool or str:
    """
    PTK_DrawBar2D_HANXIN is used to print a Han Xin barcode on the label

    Parameters:
        x_coordinate (float): The x coordinate of the 2Dcode in mm or dots(depending on PTK_SetUnit)
        y_coordinate (float): The y coordinate of the 2Dcode in mm or dots(depending on PTK_SetUnit) 
        multiplier (int): The multiplier of the barcode. The range is 1 to 30
        data (string): The data to be printed in the barcode
        encoding (int): The encoding of the barcode. The range is 0 to 6 where
            0 = Auto, 1 = Text, 2 = Binary, 3 = Numeric, 4 = Alphanumeric, 5 = GB 18030 binary, 6 = GB 18030 numeric
        correction_level (int): The correction level of the barcode. The range is 0 to 3
        masking (int): The masking of the barcode. The range is 0 to 3
        rotation (int): The rotation of the barcode. The range is 0 to 3 where
            0 = 0 degree, 1 = 90 degree, 2 = 180 degree, 3 = 270 degree

    Returns:
        bool/str: The command was sent successfully or the error message if the command was not sent successfully
    """
    return True


# ===========================================================#
# 1D Barcodes
# ===========================================================#

NO_TEXT = "N"
TEXT = "B"

def PTK_DrawBarcode(
    x_coordinate: float,
    y_coordinate: float,
    barcode_type: str,
    wide_unit_width: float,
    barcode_height: float,
    data: str,
    human_readable=TEXT,
    narrow_unit_width=0.1,
    rotation=0,
) -> bool or str:
    """
    PTK_DrawBarcode is used to print a 1D barcode on the label

    Parameters:
        x_coordinate (float): The x coordinate of the barcode in mm or dots(depending on PTK_SetUnit)
        y_coordinate (float): The y coordinate of the barcode in mm or dots(depending on PTK_SetUnit) 
        barcode_type (string): The type of the barcode.
            0 = Code 128 UCC(shipping container code)
            1 = Code 128 auto
            1A = Code 128 subset A
            1B = Code 128 subset B
            1C = Code 128 subset C
            1E = UCC/EAN128
            2 = Interleaved 2 of 5 (wide_unit_width adjustable)
            2C = Interleaved 2 of 5 check sum digit (wide_unit_width adjustable)
            2D = Interleaved 2 of 5 with human readable check digit (wide_unit_width adjustable)
            2M = Matrix 2 of 5 (wide_unit_width adjustable)
            3 = Code 3 of 9 (wide_unit_width adjustable)
            3C = Code 3 of 9 check sum digit (wide_unit_width adjustable)
            3E = Extended Code 3 of 9 (wide_unit_width adjustable)
            3F = Extended Code 3 of 9 check sum digit (wide_unit_width adjustable)
            9 = Code 93
            E30 = EAN 13
            E32 = EAN 13 2 digit add on
            E35 = EAN 13 5 digit add on
            E80 = EAN 8
            E82 = EAN 8 2 digit add on
            E85 = EAN 8 5 digit add on
            K = Codabar (wide_unit_width adjustable)
            P = Postnet
            UA0 = UPC-A
            UA2 = UPC-A 2 digit add on
            UA5 = UPC-A 5 digit add on
            UE0 = UPC-E
            UE2 = UPC-E 2 digit add on
            UE5 = UPC-E 5 digit add on


            The range is 0 to 8 where
            0 = UPC-A, 1 = UPC-E, 2 = EAN13, 3 = EAN8, 4 = CODE39, 5 = ITF, 6 = CODABAR, 7 = CODE93, 8 = CODE128

        narrow_unit_width (float): The bar width of the narrow unit width of the barcode in mm or
            dots(depending on PTK_SetUnit) 
        wide_unit_width (float): The bar width of the narrow unit width of the barcode in mm or 
            dots(depending on PTK_SetUnit). Not applicable for all barcode types
        data (string): The data to be printed in the barcode
        human_readable (string): The human readable of the barcode. The range is "N" or "B" where
            "N" = No text, "B" = Text
        bar_height (int): The bar height of the barcode. The range is 1 to 9999
        rotation (int): The rotation of the barcode. The range is 0 to 3 where
            0 = 0 degree, 1 = 90 degree, 2 = 180 degree, 3 = 270 degree

    Returns:
        bool/str: The command was sent successfully or the error message if the command was not sent successfully
    """
    return True


# ===========================================================#
# Printing graphics
# ===========================================================#

def PTK_DrawGraphics(x_coordinate, y_coordinate, graphic_name) -> bool or str:
    """
    PTK_DrawGraphics is used to print a graphic on the label

    Parameters:
        x_coordinate (float): The x coordinate of the graphic in mm or dots(depending on PTK_SetUnit)
        y_coordinate (float): The y coordinate of the graphic in mm or dots(depending on PTK_SetUnit) 
        graphic_name (string): The name of the graphic that is stored in the printer

    Returns:
        bool/str: The command was sent successfully or the error message if the command was not sent successfully
    """
    return True


def PTK_DrawGraphicsFromBytes(x_coordinate, y_coordinate, graphic_data, isbase64=False) -> bool or str:
    """
    PTK_DrawGraphicsFromBytes is used to print a graphic on the label

    Parameters:
        x (float): The x coordinate of the graphic in mm or dots(depending on PTK_SetUnit)
        y (float): The y coordinate of the graphic in mm or dots(depending on PTK_SetUnit) 
        isbase64 (bool): If the Data is base64 encoded, is it is the function will
            perform a base64 decode on the data before sending it to the printer
        graphic_data (string): The data of the graphic

    Returns:
        bool/str: The command was sent successfully or the error message if the command was not sent successfully
    """
    return True

# ===========================================================#
# Printing lines
# ===========================================================#


def PTK_DrawDiagonal(
    x_coordinate: float,
    y_coordinate: float,
    thickness: int,
    end_point_x: float,
    end_point_y: float,
) -> bool or str:
    """
     PTK_DrawDiagonal is used to draw lines on the label

     Parameters:
        x_coordinate (float): The x coordinate of the line in mm or dots(depending on PTK_SetUnit)
        y_coordinate (float): The y coordinate of the line in mm or dots(depending on PTK_SetUnit) 
        thickness (int): The thickness of the line in mm
        end_point_x (float): The x coordinate of the end point of the line
        end_point_y (float): The y coordinate of the end point of the line

     Returns:
         bool/str: The command was sent successfully or the error message if the command was not sent successfully
     """
    return True


def PTK_DrawRectangle(
    x_coordinate: float,
    y_coordinate: float,
    thickness: int,
    end_point_x: float,
    end_point_y: float,
) -> bool or str:
    """
    PTK_DrawRectangle is used to draw a rectangle on the label

    Parameters:
        x_coordinate (float): The x coordinate of the rectangle in mm or dots(depending on PTK_SetUnit)
        y_coordinate (float): The y coordinate of the rectangle in mm or dots(depending on PTK_SetUnit) 
        thickness (int): The thickness of the rectangle in mm
        end_point_x (float): The x coordinate of the end point of the rectangle in mm 
            or dots(depending on PTK_SetUnit)
        end_point_y (float): The y coordinate of the end point of the rectangle in mm 
            or dots(depending on PTK_SetUnit) 

    Returns:
        bool/str: The command was sent successfully or the error message if the command was not sent successfully
    """
    return True

# ===========================================================#
# Printjob settings
# ===========================================================#


def PTK_PrintLabel(number_of_label=1, number_of_copy=1) -> bool or str:
    """
    PTK_PrintLabel is used to print the label

    Parameters:
        number_of_label (int): The number of label to be printed.
        number_of_copy (int): The number of copies to be printed.

    Returns:
        bool/str: The function will return the error message in string format if an error occurred or true when the printjob
            finished successfully or false when the printjob failed. The function will block until the printjob is finished
    """
    return True


def PTK_PrintConfigunation() -> bool or str:
    """
    PTK_PrintConfigunation is used to print the current configuration of the printer onto the label.
    Usually only used for debugging purposes

    Returns:
        bool/str: The command was sent successfully or the error message if the command was not sent successfully
    """
    return True


def PTK_FeedMedia() -> bool or str:
    """
    PTK_FeedMedia is used to feed one label

    Returns:
        bool/str: The command was sent successfully or the error message if the command was not sent successfully
    """
    return True


def PTK_MediaCalibration() -> bool or str:
    """
    PTK_MediaCalibration is used to calibrate the media. If the calibration is successful the
        media size information will be stored and used for the next printjob unless specificed through
        PTK_SetLabelHeight or specificed through print job configuration

    Returns:
        bool/str: The command was sent successfully or the error message if the command was not sent successfully
    """
    return True

# ===========================================================#
# RFID打印标签
# ===========================================================#


# def PTK_RFIDCalibrate() -> bool or str:
#     """
#     PTK_RFIDCalibrate is used to calibrate the RFID tag. If the calibration is successful the
#     RFID tag information will be stored and used for the next printjob unless specificed through
#     print job configuration

#     Returns:
#         bool/str: The command was sent successfully or the error message if the command was not sent successfully
#     """
#     return True


# def PTK_RWRFIDLabel(RWMode, WForm, StartBlock, WDataNum, WArea, data) -> bool or str:
#     """
#     PTK_RWRFIDLabel is used to read and write data to the RFID tag

#     Parameters:
#         RWMode (int): 0 = read, 1 = write
#         WForm (int): 0 = ASCII, 1 = HEX
#         StartBlock (int): The start block to read or write
#         WDataNum (int): The number of blocks to read or write
#         WArea (int): 0 = EPC, 1 = TID, 2 = USER
#         data (string): The data to be written to the RFID tag

#     Returns:
#         bool/str: The command was sent successfully or the error message if the command was not sent successfully
#     """
#     return True


# def PTK_SetRFLabelPWAndLockRFLabel(OperationMode, OperationArea, data) -> bool or str:
#     """
#     PTK_SetRFLabelPWAndLockRFLabel is used to set the password and lock the RFID tag

#     Parameters:
#         OperationMode (int): 0 = set password, 1 = lock
#         OperationArea (int): 0 = EPC, 1 = TID, 2 = USER
#         data (string): The password to be set

#     Returns:
#         bool/str: The command was sent successfully or the error message if the command was not sent successfully
#     """
#     return True


# def PTK_SetRFID(
#     ReservationParameters,
#     ReadWriteLocation,
#     ReadWriteArea,
#     MaxErrNum,
#     ErrProcessingMethod,
# ) -> bool or str:
#     """
#     PTK_SetRFID is used to set the RFID tag parameters

#     Parameters:
#         ReservationParameters (int): 0 = no reservation, 1 = reservation
#         ReadWriteLocation (int): 0 = read and write, 1 = read only
#         ReadWriteArea (int): 0 = EPC, 1 = TID, 2 = USER
#         MaxErrNum (int): The maximum number of errors allowed
#         ErrProcessingMethod (int): 0 = stop printing, 1 = continue printing

#     Returns:
#         bool/str: The command was sent successfully or the error message if the command was not sent successfully
#     """
#     return True


# def PTK_SetRFIDCmdMode(flag) -> bool or str:
#     """
#     PTK_SetRFIDCmdMode is used to set the RFID command mode

#     Parameters:
#         flag (int): 0 = normal mode, 1 = command mode

#     Returns:
#         bool/str: The command was sent successfully or the error message if the command was not sent successfully
#     """
#     return True

def PTK_GetPrinterStatus() -> bool:
    """
    PTK_GetPrinterStatus is used to get the printer status. Currently only supports getting the status
        of the last printjob. 

    Returns:
        bool: The command returns true if the last printjob completed or false if the last printjob failed
    """
    return True

TID = 0
EPC = 1
TID_EPC = 2
USER = 3
TID_USER = 4
RESERVED = 5
TID_RESERVED = 6
PORT_SCRIPT = 3

def PTK_ReadRFID(block=TID, comm_mode=3, auto_foward=False, len=10):
    """
    PTK_ReadRFID is used to read the RFID tag

    Parameters:
        block (int): 0 = TID, 1 = EPC, 2 = USER
        comm_mode (int): 0 = 9600, 1 = 19200, 2 = 38400, 3 = 57600, 4 = 115200
        auto_foward (bool): 0 = no auto forward, 1 = auto forward
        len (int): The length of the data to be read
    """
    return "RFID Data will be read on printer"


# def PTK_SetEPCBlock(allnum, p1, p2, p3, p4, p5, p6):
#     """
#     PTK_SetEPCBlock is used to set the EPC block

#     Parameters:
#         allnum (int): The total number of blocks
#         p1 (int): The first block
#         p2 (int): The second block
#         p3 (int): The third block
#         p4 (int): The fourth block
#         p5 (int): The fifth block
#         p6 (int): The sixth block

#     Returns:
#         bool: The function executed successfully

#     """
#     return True


# def PTK_WriteRFID(data_mode, start_addr, len, block, data):
#     """
#     PTK_WriteRFID is used to write data to the RFID tag

#     Parameters:
#         data_mode (int): 0 = ASCII, 1 = HEX
#         start_addr (int): The start address to write
#         len (int): The length of the data to be written
#         block (int): 0 = TID, 1 = EPC, 2 = USER
#         data (string): The data to be written to the RFID tag

#     Returns:
#         bool: The function executed successfully
#         String: The error message in string if an error occured

#     """
#     return True

# ===========================================================#
# Functions to display information on the printer screen
# ===========================================================#

# Parent class of all UI elements
# This shouldn't be used directly

class UIWidgets:
    def __init__(self, name, value, Onpressed):
        self.value = value
        self.name = name
        self.Onpressed = Onpressed
        self.id = 0
        self.enabled = True


    def update(self, value):
        """
        update is used to update the value of the UI element on the printer screen

        Parameters:
            value (string): The value to be updated
        
        """
        self.value = value

    def enable(self):
        """
        enable is used to enable the UI element on the printer screen. A disabled UI element 
            is still visible but can't be interacted with on the printer screen

        """
        self.enabled = True

    def disable(self):
        """
        disable is used to disable the UI element on the printer screen. A disabled UI element 
            is still visible but can't be interacted with on the printer screen

        """
        self.enabled = False

# Button class used for creating a button on the printer screen
# To create UI Elements use UIInit and UIPage
class PTK_UIButton(UIWidgets):
    def __init__(self, Onpressed, title="button", visible=True, enabled=True, name=""):
        """
        Parameters:
            Onpressed (function): The function to be called when the button is pressed
            title (string): The title of the button that will be displayed on screen
            visible (bool): Whether the button is visible on the printer screen
            enabled (bool): Whether the button is enabled on the printer screen, a disabled
                widget is grey and can't be interacted with
            name (string): A custom name for button that can be used to identify the button
        """

        self.type = "button"
        self.Onpressed = Onpressed
        self.title = title
        self.name = name
        self.value = "0"
        self.visible = visible
        self.enabled = enabled
        self.id = 0
    
    def return_json(self):
        return {
            "type": self.type,
            "id": self.id,
            "name": self.title,
            "visible": self.visible,
            "enabled": self.enabled,
        }


# Text class used for just displaying text on the printer screen
# To create UI Elements use UIInit and UIPage
class PTK_UIText(UIWidgets):
    def __init__(self, title="text", visible=True, enabled=True, name=""):
        """
        Parameters:
            title (string): The title of the button that will be displayed on screen
            visible (bool): Whether the button is visible on the printer screen
            enabled (bool): Whether the widget is enabled on the printer screen, a disabled
                widget is grey and can't be interacted with
            name (string): A custom name for button that can be used to identify the button
        """
                
        self.type = "text"
        self.title = title
        self.name = name
        self.visible = visible
        self.enabled = enabled
        self.id = 0
    
    def return_json(self):
        return {
            "type": "text",
            "id": self.id,
            "name": self.title,
            "visible": self.visible,
            "enabled": self.enabled,
        }


class PTK_UITextBox(UIWidgets):
    def __init__(self, value="--", title="Textbox", visible=True, enabled=True, name=""):
        """
        Parameters:
            value (string): The value of the textbox that will be displayed on screen, can be 
                updated using the update function
            title (string): The title of the button that will be displayed on screen
            visible (bool): Whether the button is visible on the printer screen
            enabled (bool): Whether the textbox is enabled on the printer screen, a disabled
                widget is grey and can't be interacted with
            name (string): A custom name for button that can be used to identify the button
        """
        self.type = "text"
        self.value = value
        self.title = title
        self.name = name
        self.visible = visible
        self.enabled = enabled
        self.id = 0

    def return_json(self):
        return {
            "type": "text",
            "id": self.id,
            "name": self.title,
            "value": self.value,
            "visible": self.visible,
            "enabled": self.enabled,
        }

# List class that can be used to create a drop down list on the printer screen
# To create UI Elements use UIInit and UIPage
class PTK_UIList(UIWidgets):
    def __init__(
        self,
        Onpressed,
        items=['Add Custom List Items', '0', '1'],
        title="list",
        value=["Add Custom List Items"],
        valueType="int",
        valueMax="1",
        valueMin="0",
        visible=True,
        enabled=True,
        name="",
    ):        
        """
        Parameters:
            Onpressed (function): The function to be called when the button is pressed
            items (list): The list of items to be displayed in the drop down list
            title (string): The title of the button that will be displayed on screen
            value (list): The default value of the drop down list
            valueType (string): The type of the value of the drop down list
            valueMax (string): The maximum value of the drop down list
            valueMin (string): The minimum value of the drop down list
            visible (bool): Whether the list is visible on the printer screen
            enabled (bool): Whether the list is enabled on the printer screen, a disabled
                widget is grey and can't be interacted with
            name (string): A custom name for button that can be used to identify the button
        """
        self.type = "list"
        self.Onpressed = Onpressed
        self.items = items
        self.title = title
        self.name = name
        self.value = value
        self.valueType = valueType
        self.valueMax = valueMax
        self.valueMin = valueMin
        self.visible = visible
        self.enabled = enabled
        self.id = 0

    def return_json(self):
        return {
            "type": "list",
            "id": self.id,
            "items": self.items,
            "value": self.value,
            "visible": self.visible,
            "name": self.title,
            "valueType": self.valueType,
            "valueMax": self.valueMax,
            "valueMin": self.valueMin,
            "enabled": self.enabled,
        }
    
# Input class that can be used to create a input box on the printer screen
# To create UI Elements use UIInit and UIPage
class PTK_UIInput(UIWidgets):
    def __init__(
        self,
        Onsubmit,
        Onchange="",
        title="input",
        value="0",
        valueType="double",
        valueMax="10.0",
        valueMin="-10.0",
        dotNum=1,
        visible=True,
        enabled=True,
        name="",
    ):
        """
        Parameters:
            Onsubmit (function): The function to be called when the button is pressed
            ONchange (function): The function to be called when the value of the input box is changed
            title (string): The title of the button that will be displayed on screen
            value (list): The default value of the drop down list
            valueType (string): The type of the value of the drop down list
            valueMax (string): The maximum value of the drop down list
            valueMin (string): The minimum value of the drop down list
            visible (bool): Whether the inputbox is visible on the printer screen
            enabled (bool): Whether the inputbox is enabled on the printer screen, a disabled
                widget is grey and can't be interacted with
            name (string): A custom name for button that can be used to identify the button
        """
        self.type = "input"
        self.Onsubmit = Onsubmit
        self.Onchange = Onchange
        self.title = title
        self.name = name
        self.value = value
        self.valueType = valueType
        self.valueMax = valueMax
        self.valueMin = valueMin
        self.visible = visible
        self.dotNum = dotNum
        self.id = 0
        self.enabled = enabled

    def return_json(self):
        return {
            "type": "input",
            "id": self.id,
            "name": self.title,
            "value": self.value,
            "visible": self.visible,
            "valueType": self.valueType,
            "valueMax": self.valueMax,
            "valueMin": self.valueMin,
            "dotNum": self.dotNum,
            "enabled": self.enabled,
        }
    
class PTK_UICheckbox(UIWidgets):
    def __init__(
        self,
        Onpressed,
        title="checkbox",
        value="0",
        visible=True,
        enabled=True,
        name="",
    ):
        """
        Parameters:
            Onpressed (function): The function to be called when the button is pressed
            title (string): The title of the widget that will be displayed on screen
            value (int): The default value of the checkbox, 0 for unchecked and 1 for checked
            visible (bool): Whether the checkbox is visible on the printer screen
            enabled (bool): Whether the checkbox is enabled on the printer screen, a disabled
                widget is grey and can't be interacted with
            name (string): A custom name for the widget that can be used to retrieve the widget
                controller from the UIPage
        """

        self.type = "checkbox"
        self.Onpressed = Onpressed
        self.title = title
        self.name = name
        self.value = value
        self.valueType = "bool"
        self.valueMax = "1"
        self.valueMin = "0"
        self.visible = visible
        self.id = 0
        self.enabled = enabled

    def return_json(self):
        return {
            "type": "checkbox",
            "id": self.id,
            "name": self.title,
            "value": self.value,
            "visible": self.visible,
            "valueType": self.valueType,
            "valueMax": self.valueMax,
            "valueMin": self.valueMin,
            "enabled": self.enabled,
        }

def PTK_UIchangePage(pagenum):
    """
    UIchangePage can be used to change the page on the printer screen as
        a ox script can be used to create multiple pages

    Parameters:
        pagenum (int): The page number to be displayed
    """
    pass

controllers = {}
requestId = 0
total_page_num = 0
pages = []
currentPage = ""
startFlag = 0
onlyOnePageFlag = 0
def PTK_UIPage(*args) -> dict:
    """
    UIPage is used to create a page on the printer screen. A page is used to
        group UI elements together. UI elements have to be added to a page to be displayed
        on the printer screen. UI elements needs to be added in the following way

    controller = PTK_UIInit(
        PTK_UIPage(
            UITextbox(name="Barcode One:", value="--"),
            UITextbox(name="Barcode Two:", value="--"),
        ),
    )

    Parameters:
        *args (UIWidgets): The UI elements to be added to the page

    Returns:
        dict: The page in dictionary format, it is meanted to be used with PTK_UIInit and not
            used directly by the user

    """
    global total_page_num
    flag = 0
    if type(args[0]) is str:
        page_num = args[0]
    else:
        page_num = "page_" + str(total_page_num)
        flag = 1
    total_page_num += 1
    temp = {page_num: []}
    if flag == 1:
        temp[page_num].append(" ")
    for arg in args:
        if type(arg) is not str:
            index = args.index(arg)
            arg.id = index + flag
            temp[page_num].append(arg)
    return temp

def PTK_UIInit(*params, require_execute_confirmation=True) -> dict:
    """
    PTK_UIInit is used to initialize the UI elements on the printer screen. 

    Parameters:
        *params (dict): The pages to be displayed on the printer screen, it should be used in the
            way shown below. The user can create multiple pages and add UI elements to each page
        require_execute_confirmation (bool, optional): If the printer screen should require
            confirmation before executing the script. Defaults to True which requires the user to press 
            the run script button on the bottom right of the pop up window

    controller = PTK_UIInit(
        PTK_UIPage(
            UITextbox(name="Barcode One:", value="--"),
            UITextbox(name="Barcode Two:", value="--"),
        ),
        PTK_UIPage(
            UITextbox(name="Barcode Three:", value="--"),
            UITextbox(name="Barcode Four:", value="--"),
        ),
    )

    Returns:
        controller (dict): The controller for the UI elements. The user can use the controllers
            to change the values of the UI elements on the printer screen
    """
    global requestId
    global controllers
    global pages
    global currentPage
    global onlyOnePageFlag
    
    if type(params) == tuple and params.__len__() == 1:
        params = params[0]
        onlyOnePageFlag = 1
        for page in params.keys():
            pages.append({page: []})
            for element in params[page]:
                if element != " ":
                    pages[0][page].append(element.return_json())
                    if element.name != "":
                        controllers[element.name] = element
                    controllers["Widget_" + str(element.id)] = element
    else:
        onlyOnePageFlag = 0
        for param in params:
            for page_num in param.keys():
                pages.append({page_num: []})
                controllers[page_num] = {}
                for element in param[page_num]:
                    if element != " ":
                        pages[params.index(param)][page_num].append(
                            element.return_json()
                        )
                        if element.name != "":
                            controllers[element.name] = element
                        controllers[page_num]["Widget_" + str(element.id)] = element

    currentPage = list(pages[0].keys())[0]
    requestId += 1
    return controllers