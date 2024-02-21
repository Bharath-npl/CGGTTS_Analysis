import streamlit as st

st.set_page_config(page_title="CGGTTS data format", page_icon=":newspaper:", layout="wide",initial_sidebar_state="collapsed")
st.title(":clipboard: CGGTTS data format")

# st.header("**Welcome to data format**")


# st.text("gzau0660.309")

# # File name text with tooltip
# tooltip_message = "This is the file name tooltip"
# file_name_text = f'<div class="file-name" title="{tooltip_message}">gzau0660.309</div>'

# st.set_page_config(initial_sidebar_state="collapsed")

st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)


# File name text with tooltip
file_name_text = '''
<div class="file-name">gmpt1060.312
    <span class="tooltip-text">
    The file name should be of the form: XFLLmodd.ddd where<br><br>
    <ul>
        <li><strong>X</strong> is the code character indicating the constellation, using the same convention as in the RINEX standard:
            <ul>
                <li>"G" for a GPS</li>
                <li>"R" for a GLONASS (R stands for Russia)</li>
                <li>"E" for Galileo (Europe)</li>
                <li>"C" for BeiDou (China)</li>
                <li>"J" for QZSS (Japan)</li>
            </ul>
        </li>
        <li><strong>F</strong> is the code character indicating the frequencies and channels:
            <ul>
                <li>"S" a Single-frequency single-channel observation file</li>
                <li>"M" for a single-frequency multi-channel observation file</li>
                <li>"Z" for a dual frequency observation file (always multi-channel)</li>
            </ul>
        </li>
        <li><strong>LL</strong> is the two alphabetical character code for the laboratory</li>
        <li><strong>m</strong> is the receiver identification first character (to be chosen by the laboratory), it can be "_" if not applicable or "0 to 9"</li>
        <li><strong>o</strong> is the receiver identification second character (to be chosen by the laboratory), it can be "_" if not applicable or "0 to 9"</li>
        <li><strong>dd.ddd</strong> is the MJD of the first observation in the file</li>
    </ul>
    </span>
</div>
'''



# Header text split into lines
header_lines = [
    '''<div class="header-line header-line-1">
            <pre>CGGTTS     GENERIC DATA FORMAT VERSION = 2E</pre>
            <span class="tooltip-text">
                <ul>
                    <li>
                        <strong>CGGTTS Version Title</strong>
                        <ul>
                            <li>CGGTTS: Common format for reporting GNSS time transfer data</li>
                            <li>Generic Data Format: Standardized format for compatibility and ease of analysis</li>
                            <li>Version 2E: Indicates the specific version of the CGGTTS format being used</li>
                        </ul>
                    </li>
                </ul>
            </span>
        </div>'''
    '''<div class="header-line header-line-2">
            <pre>REV DATE = 2022-06-22</pre>
            <span class="tooltip-text">
                <ul>
                    <li>
                        <strong>Revision Date Details</strong>
                        <ul>
                            <li>Date of last revision of the header data</li>
                            <li>Changed whenever any parameter in the header is modified</li>
                            <li>Format: YYYY-MM-DD (Year, Month, Day)</li>
                        </ul>
                    </li>
                </ul>
            </span>
        </div>'''
    '''<div class="header-line header-line-3">
            <pre>RCVR = GTR51 1309042 1.9.0</pre>
            <span class="tooltip-text">
                <ul>
                    <li>
                        <strong>Receiver Information</strong>
                        <ul>
                            <li>Maker acronym: Sep</li>
                            <li>Type: GTR51</li>
                            <li>Serial Number: 1309042</li>
                            <li>Software Number: 1.9.0</li>
                            <li>Additional Details: First year of operation and other relevant information</li>
                        </ul>
                    </li>
                </ul>
            </span>
        </div>'''
    '''<div class="header-line header-line-4">
            <pre>CH = 20</pre>
            <span class="tooltip-text">
                <ul>
                    <li>
                        <strong>Channel Information</strong>
                        <ul>
                            <li>Total number of receiver channels: 20</li>
                            <li>Channel distribution for different systems:
                                <ul>
                                    <li>GPS</li>
                                    <li>GLONASS</li>
                                    <li>GALILEO</li>
                                    <li>BEIDOU</li>
                                    <li>Others as applicable</li>
                                </ul>
                            </li>
                        </ul>
                    </li>
                </ul>
            </span>
        </div>'''
    '''<div class="header-line header-line-5">
            <pre>IMS = GTR51 1309042 1.9.0</pre>
            <span class="tooltip-text">
                <ul>
                    <li>
                        <strong>Ionospheric Measurement System (if any):</strong>
                        <ul>
                            <li>Maker acronym, type, serial number, first year of operation, and eventually software number.</li>
                            <li>IMS = 99999 if none.</li>
                            <li>Similar to line 3 if included in the time receiver.</li>
                        </ul>
                    </li>
                </ul>
            </span>
        </div>'''
    '''<div class="header-line header-line-6">
            <pre>LAB = PTB Germany</pre>
            <span class="tooltip-text">
                <ul>
                    <li>
                        <strong>Laboratory Information</strong>
                        <ul>
                            <li>LAB acronym: PTB</li>
                            <li>Country: Germany</li>
                            <li>Facility where satellite observations are conducted and analyzed</li>
                            <li>Key focus on geospatial and astronomical research</li>
                        </ul>
                    </li>
                </ul>
            </span>
        </div>'''
    '''<div class="header-line header-line-7">
            <pre>X = -1432891.86 m</pre>
            <span class="tooltip-text">
                <ul>
                    <li>
                        <strong>X Coordinate Information</strong>
                        <ul>
                            <li>Coordinate in the ITRF (International Terrestrial Reference Frame)</li>
                            <li>Represents the X-axis position of the antenna phase center</li>
                            <li>Accuracy: Provided with at least 2 decimal places</li>
                        </ul>
                    </li>
                </ul>
            </span>
        </div>'''

    '''<div class="header-line header-line-8">
            <pre>Y = +6050260.21 m</pre>
            <span class="tooltip-text">
                <ul>
                    <li>
                        <strong>Y Coordinate Information</strong>
                        <ul>
                            <li>Coordinate in the ITRF (International Terrestrial Reference Frame)</li>
                            <li>Represents the Y-axis position of the antenna phase center</li>
                            <li>Accuracy: Provided with at least 2 decimal places</li>
                        </ul>
                    </li>
                </ul>
            </span>
        </div>'''

    '''<div class="header-line header-line-9">
            <pre>Z = -5739698.67 m</pre>
            <span class="tooltip-text">
                <ul>
                    <li>
                        <strong>Z Coordinate Information</strong>
                        <ul>
                            <li>Coordinate in the ITRF (International Terrestrial Reference Frame)</li>
                            <li>Represents the Z-axis position of the antenna phase center</li>
                            <li>Accuracy: Provided with at least 2 decimal places</li>
                        </ul>
                    </li>
                </ul>
            </span>
        </div>'''
    '''<div class="header-line header-line-10">
            <pre>FRAME = ITRF</pre>
            <span class="tooltip-text">
                <ul>
                    <li>
                        <strong>Reference Frame Information</strong>
                        <ul>
                            <li>Designation: ITRF (International Terrestrial Reference Frame)</li>
                            <li>Purpose: Defines the reference frame used for GNSS data</li>
                            <li>Additional Information: Includes transformation parameters between different GNSS frames if necessary</li>
                        </ul>
                    </li>
                </ul>
            </span>
        </div>'''

    '''<div class="header-line header-line-11">
            <pre>COMMENTS = AUSPOS ITRF2014 2020-11-23</pre>
            <span class="tooltip-text">
                <ul>
                    <li>
                        <strong>Comments Section</strong>
                        <ul>
                            <li>Comments regarding the coordinates, such as methods used for determination or estimated uncertainty</li>
                            <li>Details on corrections applied, like the identification of specific Ccode/P-code biases</li>
                            <li>Example: Comments include details related to AUSPOS ITRF2014 data as of 2020-11-23</li>
                            <li> There can be multiple comment lines in the header</li>
                        </ul>
                    </li>
                </ul>
            </span>
        </div>'''

    '''<div class="header-line header-line-12">
            <pre>INT DLY = 33.2 ns (GPS C1),  31.4 ns (GPS P1),  24.8 ns (GPS P2), CAL_ID = 1001-2020</pre>
            <span class="tooltip-text">
                <ul>
                    <strong>Internal delays of the receiver:</strong>
                    <li>
                        <strong>For single-frequency CGGTTS:</strong>
                        <br>"INT DLY = DDD.D ns (cons code1) CAL_ID = cccccccccccc",
                    </li>
                    <li>
                        <strong>For dual-frequency CGGTTS:</strong>
                        <br>"INT DLY = DDD.D ns (cons code1), DDD.D ns (cons code2) CAL_ID = cccccccccccc",
                    </li>
                    <li>
                        The Internal delays (receiver + antenna) should be entered in ns and given with 1 decimal, only for the constellation and the code(s) used in the file. The parameter 'cons' will be <strong>GPS, GLO, GAL, BDS or QZS</strong>, and 'code1' and 'code2' will follow the convention provided in the third column of Table 1. The parameter <strong>"CAL_ID"</strong> is the reference to the calibration report where the internal delays are provided; its expression is detailed in the BIPM guidelines for calibration.
                    </li>
                </ul>
            </span>
        </div>'''
    '''<div class="header-line header-line-13">
        <pre>CAB DLY = 250.0 ns</pre>
        <span class="tooltip-text">
            <ul>
                <strong>Antenna cable delay of the receiver:</strong>
                <li>
                    <strong>"CAB DLY = DDD.D ns"</strong>
                    <ul>
                        <li>Delays from the antenna to the main unit including delays in the filters, electronics, and cable length.</li>
                        <li>Entered in the receiver and corresponding to the constellation of the file (GPS, GLONASS, GALILEO, QZSS, BDS).</li>
                        <li>In ns and given with 1 decimal.</li>
                    </ul>
                </li>
            </ul>
        </span>
    </div>'''
    '''<div class="header-line header-line-14">
            <pre>REF DLY = 36.6 ns</pre>
            <span class="tooltip-text">
                <ul>
                    <strong>Reference delay :</strong>
                    <li>
                        <strong>"REF DLY = DDD.D ns"</strong>
                        <ul>
                            <li>Time delay between the local clock (or realization of UTC) and the receiver internal clock.</li>
                            <li>Or its conventional realization by an external signal.</li>
                            <li>In ns and given with 1 decimal.</li>
                        </ul>
                    </li>
                </ul>
            </span>
        </div>'''
    '''<div class="header-line header-line-15">
            <pre>REF = UTC(PTB)</pre>
            <span class="tooltip-text">
                <ul>
                    <li>
                        <strong>Time Reference Information</strong>
                        <ul>
                            <li>Reference: Indicates the time reference used</li>
                            <li>Identifier: For time synchronization, GNSS time receivers use specific reference codes</li>
                            <li>TAI Contribution: For labs contributing to TAI (International Atomic Time), a 7-digit clock code or a 5-digit local UTC code is used, as assigned by the BIPM (Bureau International des Poids et Mesures)</li>
                        </ul>
                    </li>
                </ul>
            </span>
        </div>'''

    '''<div class="header-line header-line-16">
            <pre>CKSUM = DA</pre>
            <span class="tooltip-text">
                <ul>
                    <li>
                        <strong>"CKSUM = XX"</strong>
                        <ul>
                            <li>Header check-sum: hexadecimal representation of the sum, modulo 256.</li>
                            <li>Includes the ASCII values of the characters constituting the complete header.</li>
                            <li>Begins with the first letter "C" of line 1.</li>
                            <li>Includes all spaces indicated as "˽" (ASCII value 20 in hexadecimal).</li>
                            <li>Ends with the space after "=" of line 20 just preceding the actual check sum value.</li>
                            <li>Excludes all carriage returns or line feeds.</li>
                        </ul>
                    </li>
                </ul>
            </span>
        </div>'''
    '''<div class="header-line header-line-17"> <span class="tooltip-text">Blank line.</span></div>''']


labels = [[
    "SAT", "CL", "MJD", "STTIME", "TRKL", "ELV", "AZTH", "REFSV", "SRSV", 
    "REFSYS", "SRSYS", "DSG", "IOE", "MDTR", "SMDT", "MDIO", "SMDI", 
    "MSIO", "SMSI", "ISG", "FR", "HC", "FRC", "CK"], [
    "", "", "", "hhmmss", "s", ".1dg", ".1dg", ".1ns", ".1ps/s",
    ".1ns", ".1ps/s", ".1ns","", ".1ns", ".1ps/s", ".1ns", ".1ps/s",
    ".1ns", ".1ps/s", ".1ns", "", "", "", ""]]

raw_data = """
G02 FF 60312 000200  780 811 2954    +5065571    -65         -17     -9    3 061   82   -2   50   -1   26  +10   5  0  0 L1C AA
G03 FF 60312 000200  780 374 2333     -994025   -281         -64    -16    4 095  133  -22   77  -10   67   -1   9  0  0 L1C F3
G08 FF 60312 000200  780 410 1811    +1601523     +5         -36    -14    5 014  123  +19   72  +10   61   +9  19  0  0 L1C CC
G10 FF 60312 000200  780 191  589     +677818     +7        -188     -8    8 036  246  +82  111  +16   52  -33  19  0  0 L1C 02
G14 FF 60312 000200  780 211 2864    -2881624    -79         -76    +25    9 160  223  +23  106   +5   42  +28  30  0  0 L1C 0E
G17 FF 60312 000200  780 192 3153    -7207717     +9        -103     +1    8 046  243  -75  111  -15   28   -8  28  0  0 L1C 00
G21 FF 60312 000200  780 831 1062    -1396356     +7         -14     -5    4 047   81   +1   50   +0   14  +26   7  0  0 L1C 8F
G22 FF 60312 000200  780 206 3084     -549647    +78         -81    +12    9 040  228   -4  108   -1    6  +39  43  0  0 L1C DE
G32 FF 60312 000200  780 421  728    +6019645    +28         -81     -3    5 055  120   +4   71   +2   44  -24   8  0  0 L1C AB
G02 FF 60312 001800  780 883 2851    +5065514    -60         -21     -4    3 061   81   +0   50   +0   24  -12   4  0  0 L1C 9D
G03 FF 60312 001800  780 446 2373     -994281   -259         -66     +6    5 095  115  -15   68   -8   62   +1   8  0  0 L1C E8
G08 FF 60312 001800  780 335 1800    +1601526     +3         -52    -17    7 014  146  +30   83  +12   81  +25  11  0  0 L1C E5
G14 FF 60312 001800  780 184 2796    -2881731   -108         -83     -5   10 160  255  +43  113   +8   73   +5  31  0  0 L1C 18
G17 FF 60312 001800  780 252 3134    -7207690    +23         -83    +15    7 046  189  -42   98  -12   47   +6  19  0  0 L1C 15
G21 FF 60312 001800  780 761 1158    -1396348    +18         -17     +7    4 047   83   +3   51   +1   24  -13   8  0  0 L1C BA
G22 FF 60312 001800  780 203 3016     -549584    +52         -81    -14   10 040  231   +9  108   +2   40  +17  31  0  0 L1C E4
G32 FF 60312 001800  780 397  641    +6019669    +23         -88     -9    5 055  126   +8   74   +4   29  +22   9  0  0 L1C D5
"""


# Split the string into lines and then each line into columns
data_lines = raw_data.strip().split('\n')
formatted_data = [line.split() for line in data_lines]
# Prepend labels to the formatted data
data = labels + formatted_data




# Tool tip text for the Data 

tooltip_texts = [
    '''<div class="data-column col-1">
            <span class="tooltip-text">
                <ul>
                    <li><strong>Satellite ID (SAT)</strong>: 
                        <ul>
                            <li> This column represents the constellation code and satellite number.</li>
                            <li><strong>GPS</strong>: "G" followed by satellite PRN number, ranging from 01 to 38.</li>
                            <li><strong>GLONASS</strong>: "R" followed by almanac slot number, ranging from 01 to 24.</li>
                            <li><strong>GALILEO</strong>: "E" followed by satellite PRN number, ranging from 01 to 30.</li>
                            <li><strong>QZSS</strong>: "J" followed by broadcast satellite PRN minus 192, ranging from 01 to 05.</li>
                            <li><strong>BEIDOU</strong>: "C" followed by satellite PRN number, ranging from 01 to 40.</li>
                        </ul>
                    </li>
                </ul>
            </span>
        </div>''',
    '''<div class="data-column col-2" >
            <span class="tooltip-text">
                <ul>
                    <li><strong>Common-view Hexadecimal Class Byte (CL)</strong>: 
                        <ul>
                            <li>Indicates the type of data file.</li>
                            <li>For multi-channel files, the value "FF" is used to represent the common-view class byte.</li>
                        </ul>
                    </li>
                </ul>
            </span>
        </div>''',

    '''<div class="data-column col-3" >
            <span class="tooltip-text">
                <ul>
                    <li><strong>Modified Julian Date (MJD)</strong>: 
                    <ul> 
                        <li>Represents the start time of the 13-minute track.</li>
                    </ul>
            </span>
        </div>''',

    '''<div class="data-column col-4" >
        <span class="tooltip-text">
            <ul>
                <li><strong>STTIME: Represents the start time of the 13-minute track </strong>
                <ul>
                    <li>The date is indicated in the format of hour (2 characters), minute (2 characters), and second (2 characters).</li>
                    <li>Time is referenced to Coordinated Universal Time (UTC).</li>
                </ul>
            </ul>
        </span>
    </div>''',

   '''<div class="data-column col-5" >
        <span class="tooltip-text">
            <ul>
                <li>
                    <strong>TRKL (Track Length):</strong> 
                    <ul>
                        <li>Represents the duration of the satellite track. </li>
                        <li>The value is typically 780, corresponding to full 13-minute tracks.</li>
                        <li>Unit of measure: seconds.</li>
                    </ul>
                </li>
            </ul>
        </span>
    </div>''',
    '''<div class="data-column col-6">
            <span class="tooltip-text">
                <ul>
                    <li><strong>ELV (Elevation angle of the satellite)</strong>: 
                        <ul>
                            <li>Measured at the date and time corresponding to the midpoint of the track.</li>
                            <li>Unit of measure: 0.1 degree.</li>
                        </ul>
                    </li>
                </ul>
            </span>
        </div>''',
    '''<div class="data-column col-7" > 
            <span class="tooltip-text">
                <ul>
                    <li><strong>Azimuth angle of the satellite (AZTH)</strong>: 
                        <ul>
                            <li>Measured at the date and time corresponding to the midpoint of the track.</li>
                            <li>Unit of measure: 0.1 degree.</li>
                        </ul>
                    </li>
                </ul>
            </span>
        </div>''',
    '''<div class="data-column col-8" >
            <span class="tooltip-text">
                <ul>
                    <li><strong>Satellite Clock Offset (REFSV) </strong>: 
                        <ul>
                            <li>As mentioned in Solution A, Section 2.3.3 of CGGTTS V2E.</li>
                            <li>Represents the offset of the satellite clock relative to the receiver clock.</li>
                            <li>Unit of measure: 0.1 nanoseconds (ns).</li>
                        </ul>
                    </li>
                </ul>
            </span>
        </div>''',
    '''<div class="data-column col-9" >
            <span class="tooltip-text">
                <ul>
                    <li><strong>Slope of Satellite Clock Offset (SRSV)</strong>: 
                        <ul>
                            <li>Rate of change of the satellite clock offset.</li>
                            <li>As mentioned in Solution A, Section 2.3.3 of CGGTTS V2E.</li>
                            <li>Indicates the variation in satellite clock offset over time.</li>
                            <li>Unit of measure: 0.1 picoseconds per second (ps/s).</li>
                        </ul>
                    </li>
                </ul>
            </span>
        </div>''',
    '''<div class="data-column col-10" >
            <span class="tooltip-text">
                <ul>
                    <li><strong>GNSS Time Difference (REFSYS) </strong>: 
                        <ul>
                            <li>Difference between receiver clock and GNSS time.</li>
                            <li>As mentioned in Solution B, Section 2.3.3 of CGGTTS V2E.</li>
                            <li>Measures the time difference between the receiver clock and the corresponding GNSS system.</li>
                            <li>Unit of measure: 0.1 nanoseconds (ns).</li>
                        </ul>
                    </li>
                </ul>
            </span>
        </div>''',
    '''<div class="data-column col-11" >
            <span class="tooltip-text">
                <ul>
                    <li><strong>Slope of GNSS Time Difference (SRSYS)</strong>: 
                        <ul>
                            <li>Rate of change of the time difference between receiver clock and GNSS time.</li>
                            <li>As mentioned in Solution B, Section 2.3.3 of CGGTTS V2E.</li>
                            <li>Indicates how the time difference varies over time.</li>
                            <li>Unit of measure: 0.1 picoseconds per second (ps/s).</li>
                        </ul>
                    </li>
                </ul>
            </span>
        </div>''',

    '''<div class="data-column col-12" >
            <span class="tooltip-text">
                <ul>
                    <li><strong>Root-Mean-Square of Residuals: Data Sigma (DSG)</strong>: 
                        <ul>
                            <li>Measure of the residuals in the linear fit from Solution B.</li>
                            <li>As described in Section 2.3.3 of CGGTTS V2E.</li>
                            <li>Represents the variation or spread of residuals in the time difference data.</li>
                            <li>Unit of measure: 0.1 nanoseconds (ns).</li>
                        </ul>
                    </li>
                </ul>
            </span>
        </div>''',

    '''<div class="data-column col-13" >
            <span class="tooltip-text">
                <ul>
                    <li><strong>Issue of Ephemeris (IOE)</strong>: 
                        <ul>
                            <li> A three-digit decimal code indicating the ephemeris data used for computations.</li>
                            <li>For GLONASS, as there's no direct IOE, values from 1 to 96 indicate the quarter-hour slot of the day <br>when the ephemeris was used. The numbering starts at 1 for 00h00m00s.</li>
                            <li>For BeiDou, IOE reports the integer hour of the ephemeris date, corresponding to the Time of Clock.</li>
                            <li>This code is essential for understanding the specific ephemeris data utilized in the GNSS measurements <br> and computations.</li>
                        </ul>
                    </li>
                </ul>
            </span>
        </div>''',

    '''<div class="data-column col-14" >
            <span class="tooltip-text">
                <ul>
                    <li><strong>Modeled Tropospheric Delay (MDTR) </strong>: 
                        <ul>
                            <li> Delay due to the troposphere, modeled as per solution C in CGGTTS V2E Section 2.3.3.</li>
                            <li>Unit: 0.1 nanoseconds (ns).</li>
                            <li>Crucial for adjusting satellite signal delays caused by the troposphere.</li>
                        </ul>
                    </li>
                </ul>
            </span>
        </div>''',

    '''<div class="data-column col-15" >
            <span class="tooltip-text">
                <ul>
                    <li><strong>Slope of Modeled Tropospheric Delay (SMDT)</strong>: 
                        <ul>
                            <li>Slope associated with the modeled tropospheric delay as per solution C in CGGTTS V2E Section 2.3.3.</li>
                            <li>Unit: 0.1 picoseconds per second (ps/s).</li>
                            <li>Indicates the rate of change of the tropospheric delay over time.</li>
                        </ul>
                    </li>
                </ul>
            </span>
        </div>''',

    '''<div class="data-column col-16" >
            <span class="tooltip-text">
                <ul>
                    <li><strong>Modelled Ionospheric Delay (MDIO)</strong>: 
                        <ul>
                            <li>Delay attributed to the ionosphere, modeled according to solution D in CGGTTS V2E Section 2.3.3.</li>
                            <li>Unit: 0.1 nanoseconds (ns).</li>
                            <li>Essential for accounting for signal delays caused by the ionosphere.</li>
                        </ul>
                    </li>
                </ul>
            </span>
        </div>''',

    '''<div class="data-column col-17" >
            <span class="tooltip-text">
                <ul>
                    <li><strong>Slope of Modelled Ionospheric Delay (SMDI)</strong>: 
                        <ul>
                            <li>The rate of change of the ionospheric delay, modelled as per solution D in CGGTTS V2E Section 2.3.3.</li>
                            <li>Unit: 0.1 picoseconds per second (ps/s).</li>
                            <li>Indicates variation of ionospheric delay over time.</li>
                        </ul>
                    </li>
                </ul>
            </span>
        </div>''',

    '''<div class="data-column col-18" >
            <span class="tooltip-text">
                <ul>
                    <li><strong>Measured Ionospheric Delay (MSIO)</strong>: 
                        <ul>
                            <li>Actual ionospheric delay measurements, available for single or dual-frequency results,<br> as per solution E in CGGTTS V2E Section 2.3.3.</li>
                            <li>Unit: 0.1 nanoseconds (ns).</li>
                            <li>Provided when measured ionospheric delays are available.</li>
                        </ul>
                    </li>
                </ul>
            </span>
        </div>''',

    '''<div class="data-column col-19" >
            <span class="tooltip-text">
                <ul>
                    <li><strong>Slope of Measured Ionospheric Delay (SMSI)</strong>: 
                        <ul>
                            <li>Rate of change of the measured ionospheric delay, for cases when such data is available,<br> as per solution E in CGGTTS V2E Section 2.3.3.</li>
                            <li>Unit: 0.1 picoseconds per second (ps/s).</li>
                            <li>Applicable only when measured ionospheric delays are available.</li>
                        </ul>
                    </li>
                </ul>
            </span>
        </div>''',

    '''<div class="data-column col-20" >
            <span class="tooltip-text">
                <ul>
                    <li><strong>Ionospheric Sigma (ISG)</strong>: 
                        <ul>
                            <li>Root-mean-square of the residuals for measured ionospheric delays, <br> as per solution E in CGGTTS V2E Section 2.3.3.</li>
                            <li>Unit: 0.1 nanoseconds (ns).</li>
                            <li>Calculated only when measured ionospheric delays are available.</li>
                        </ul>
                    </li>
                </ul>
            </span>
        </div>''',

    '''<div class="data-column col-21" >
            <span class="tooltip-text">
                <ul>
                    <li><strong>GLONASS Transmission Frequency Channel Number (FR)</strong>: 
                        <ul>
                            <li>Indicates the channel number for GLONASS transmissions.</li>
                            <li>Range: 1 to 24 for GLONASS satellites.</li>
                            <li>Set to 0 for other GNSS systems.</li>
                        </ul>
                    </li>
                </ul>
            </span>
        </div>''',

    '''<div class="data-column col-22" >
            <span class="tooltip-text">
                <ul>
                    <li><strong>Receiver Hardware Channel Number (HC)</strong>: 
                        <ul>
                            <li>Identifies the hardware channel number used by the receiver.</li>
                            <li>Range: 0 to 99.</li>
                            <li>Set to 0 if the channel number is unknown.</li>
                        </ul>
                    </li>
                </ul>
            </span>
        </div>''',

    '''<div class="data-column col-23" >
            <span class="tooltip-text">
                <ul>
                    <li><strong>GNSS Observation Code (FRC)</strong>: 
                        <ul>
                            <li>The specific observation code used for GNSS data collection.</li>
                            <li>Denoted by a unique code for each type of observation.</li>
                            <li>Varies based on the GNSS system and the specific observation technique used.</li>
                        </ul>
                    </li>
                </ul>
            </span>
        </div>''',

    '''<div class="data-column col-24" >
            <span class="tooltip-text">
                <ul>
                    <li><strong>Data Line Check-sum (CK)</strong>: 
                        <ul>
                            <li>A checksum for validating the integrity of data in the line.</li>
                            <li>Calculated as the hexadecimal sum modulo 256 of the ASCII values of characters from column 1 to 125.</li>
                            <li>Ensures data accuracy and integrity by detecting any alterations or errors in the data line.</li>
                        </ul>
                    </li>
                </ul>
            </span>
        </div>'''

]

Empty_line_tooltip = '''
<span class="tooltiptext">
    <ul>
        <li><strong>Blank line</strong>: 
            <ul>
                <li>Blank Line indicates the end of the header</li>
            </ul>
        </li>
    </ul>
</span>
'''

# HTML for the empty line with tooltip
empty_line_html = '''
<div class="tooltip" style="background-color: #DCDCDC; height: 20px;">
    {tooltip_content}
</div>
'''.format(tooltip_content=Empty_line_tooltip)

            
# Define custom CSS for colored columns with 24 different colors
custom_css = '''
    <style> 

        .file-name {
            color: #00008B; /* Font color, e.g., Dark blue */
            background-color: #b0becc; /* Background color, e.g., BLACKISH */
            font-family: Georgia, sans-serif; /* Optional: font family */
            padding: 5px; /* Optional: padding around the text */
            border-radius: 5px; /* Optional: rounded corners */
            position: relative; /* Needed for absolute positioning of tooltip */
            display: block; /* Ensures the tooltip aligns correctly with the text */
            font-size: 25px;
            font-weight: bold;
        }

        .file-name .tooltip-text {
            visibility: hidden;
            width: 1200px;
            /*height: 1000px;*/
            background-color: #ADD8E6;
            color: #000000;
            text-align: left;
            border-radius: 6px;
            padding: 5px;
            font-family: "Source Sans Pro", sans-serif;
            position: absolute;
            z-index: 1;
            top: 100%;
            left: 10%;
            /*transform: translateX(-50%);*/
            margin-left: 0px;
            opacity: 0;
            transition: opacity 0.3s;
        }

        .file-name:hover .tooltip-text {
            visibility: visible;
            opacity: 1;
        }


        .stMarkdown div.header-line {
        position: relative; /* Needed for absolute positioning of the tooltip */
        display: block; /* Keeps the tooltip aligned with the text */
        cursor: pointer; /* Changes the cursor to indicate hoverable text */
        margin: 0; /* Remove margin */
        padding: 0; /* Remove padding */
        line-height: normal; /* Adjust line height */
        font-size: 14px; /* Adjust font size as needed */
        }

        .stMarkdown div.header-line pre {
        margin: 0; /* Remove margin for pre tag */
        padding: 0; /* Remove padding for pre tag */
        white-space: pre-wrap; /* Wrap text in pre tag */
        }


        .stMarkdown div.header-line .tooltip-text {
            visibility: hidden;
            width: 800px; /* Adjust the width as needed */
            background-color: #ADD8E6; /* Tooltip background color light blue */
            color: #000000; /* Tooltip text color */
            text-align: left;
            border-radius: 6px;
            padding: 5px;
            position: absolute;
            z-index: 1;
            font-family: "Source Sans Pro", sans-serif;
            top: 100%; /* Position the tooltip below the text */
            left: 10%; /* Align the tooltip with the start of the text */
            opacity: 0;
            transition: opacity 0.3s;
            display: block;
        }

        .stMarkdown div.header-line:hover .tooltip-text {
            visibility: visible;  
            opacity: 1;
        }
        
        /* Background color for header */
        .header-bg {
            padding: 5px; /* Optional: padding around the text */
            background-color: #E9F1F0; /* Light blue background for header */
            border-radius: 5px; /* Optional: rounded corners */
            /*gap:0px;*/
            /*display: flex;*/
        }

        .st-emotion-cache-1347cmu {
            position: relative;
            margin: 0px 0px 0.5rem;
        }
        
        .st-emotion-cache-5rimss {
            # font-family: "Source Sans Pro", sans-serif;
            margin-bottom: -1.5rem;
        }
        .data-table {
            display: table;
            width: 100%;
        }
        .data-row {
            white-space: nowrap; /* Prevents wrapping of text within cells */
        }
        .data-cell {
            display: inline-block;
            padding: 1px;
            text-align: center;
            position: relative;
            border: 1px solid transparent; /* Hide cell borders */
            margin-right: 5px; /* Negative margin to reduce space between cells */
        }

        .data-cell:hover {
            background-color: #ADD8E6; /* Highlight color */
            border: 1px solid #000000; /* Optional: show border on hover */
        }

        .tooltip {
            position: relative;
            display: inline-block;
            width: 100%;
        }
        .tooltip .tooltiptext {
            visibility: hidden;
            width: 800px;
            background-color: #ADD8E6;
            color: #000000;
            text-align: left;
            border-radius: 6px;
            # padding: 5px;
            position: absolute;
            z-index: 1000;
            bottom: 5%;
            left: 15%;
            transform: translateY(25%);
            opacity: 0;
            transition: opacity 0.3s;
            display: inline-block;
            margin-right: 0;
        }

        /* Left aligned tooltips for columns on the left side */
        .tooltip-text-left {
            position: absolute;
            left: 100%; /* Align tooltip to the left of the cell */
            top: 100%;
            # transform: translateY(-5%);
            visibility: hidden;
            width: 800px;
            background-color: #ADD8E6;
            color: #000000;
            text-align: left;
            border-radius: 6px;
            # padding: 5px;
            position: absolute;
            z-index: 1000;
            top: 100%;
            # left: 90%;
            # transform: translateX(-50%);
            opacity: 0;
            transition: opacity 0.3s;
            display: inline-block;
            margin-right: 0;
        }

        /* Right aligned tooltips for columns on the right side */
        .tooltip-text-right {
            position: absolute;
            right: 100%; /* Align tooltip to the right of the cell */
            top: 100%;
            transform: translateX(150px);
            visibility: hidden;
            width: 800px;
            background-color: #ADD8E6;
            color: #000000;
            text-align: left;
            border-radius: 6px;
            # padding: 5px;
            position: absolute;
            z-index: 1000;
            top: 100%;
            opacity: 0;
            transition: opacity 0.3s;
            display: inline-block;
            margin-right: 0;
        }

        .data-cell:hover .tooltip-text {
            visibility: visible;
            opacity: 1;
        }

         /* Ensure tooltips are not clipped */
        .data-table {
            overflow: visible;
        }
        # @media screen and (max-width: 1200px) { /* Adjust the breakpoint as needed */
        #     .tooltip-text-right {
        #         left: auto;
        #         right: 100%;
        #     }
        # }

        # .tooltip-text ul {
        #     margin: 0; /* Remove default margin */
        #     padding: 0; /* Remove default padding */
        #     list-style-type: none; /* Remove bullet points */
        #     # padding-inline-start: 0 px;
        # }

        # .tooltip-text ul li {
        #     padding: 0; /* Adjust padding for list items */
        #     text-align: left; /* Align text to the left */
        # }

        # .data-cell:hover .tooltip-text {
        #     visibility: visible;
        #     opacity: 1;
        # }


        .tooltip:hover .tooltiptext {
            visibility: visible;
            opacity: 1;
        }

         /* Show tooltips on hover */
        .data-cell:hover .tooltip-text-right,
        .data-cell:hover .tooltip-text-left {
            visibility: visible;
            opacity: 1;
        }

        /* Background color for labels */
        .labels-bg {
            /*padding: 5px;  Optional: padding around the text */
            background-color: #FFDDDD; /* Light red background for labels */
            border-radius: 5px; /* Optional: rounded corners */
        }

        /* Background color for units */
        .units-bg {
           /* padding: 5px;  Optional: padding around the text */
            background-color: #FFDDDD; /* Light green background for units */
            border-radius: 5px; /* Optional: rounded corners */
        }

        /* Background color for data */
        .data-bg {
            /*padding: 5px;  Optional: padding around the text */
            background-color: #DDFFFF; /* Light yellow background for data */
            border-radius: 5px; /* Optional: rounded corners */
        }
        
        
        /* ... Define classes for data header ... */
        # .header-line-1 { color: #FF69B4; } /* HotPink */
        # .header-line-3 { color: #008000; } /* Green */
        # .header-line-5 { color: #FFA500; } /* Orange */
        # .header-line-6 { color: #0000FF; } /* Blue */        
        # .header-line-7 { color: #008000; } /* Green */
        # .header-line-8 { color: #008000; } /* Green */
        # .header-line-9 { color: #008000; } /* Green */
        # .header-line-11 { color: #00008B; } /* DarkBlue */
        # .header-line-12 { color: #4B0082; } /* Indigo */
        # .header-line-13 { color: #D2691E; } /* Chocolate */
        # .header-line-14 { color: #DC143C; } /* Crimson */
        # .header-line-16 { color: #8B4513; } /* SaddleBrown */
        
        /* ... Define classes for data widths ... */
        .col-width-1 { display: inline-block; width: 30px; } /* column_widths[0] = 3 */
        .col-width-2 { display: inline-block; width: 30px; } /* column_widths[1] = 3 */
        .col-width-3 { display: inline-block; width: 60px; } /* column_widths[2] = 6 */
        .col-width-4 { display: inline-block; width: 70px; } /* column_widths[3] = 7 */
        .col-width-5 { display: inline-block; width: 50px; } /* column_widths[4] = 5 */
        .col-width-6 { display: inline-block; width: 40px; } /* column_widths[5] = 4 */
        .col-width-7 { display: inline-block; width: 50px; } /* column_widths[6] = 5 */
        .col-width-8 { display: inline-block; width: 100px; } /* column_widths[7] = 10 */
        .col-width-9 { display: inline-block; width: 50px; } /* column_widths[8] = 5 */
        .col-width-10 { display: inline-block; width: 60px; } /* column_widths[9] = 6 */
        .col-width-11 { display: inline-block; width: 50px; } /* column_widths[10] = 5 */
        .col-width-12 { display: inline-block; width: 40px; } /* column_widths[11] = 4 */
        .col-width-13 { display: inline-block; width: 40px; } /* column_widths[12] = 4 */
        .col-width-14 { display: inline-block; width: 50px; } /* column_widths[13] = 5 */
        .col-width-15 { display: inline-block; width: 50px; } /* column_widths[14] = 5 */
        .col-width-16 { display: inline-block; width: 50px; } /* column_widths[15] = 5 */
        .col-width-17 { display: inline-block; width: 50px; } /* column_widths[16] = 5 */
        .col-width-18 { display: inline-block; width: 50px; } /* column_widths[17] = 5 */
        .col-width-19 { display: inline-block; width: 50px; } /* column_widths[18] = 5 */
        .col-width-20 { display: inline-block; width: 30px; } /* column_widths[19] = 3 */
        .col-width-21 { display: inline-block; width: 30px; } /* column_widths[20] = 3 */
        .col-width-22 { display: inline-block; width: 30px; } /* column_widths[21] = 3 */
        .col-width-23 { display: inline-block; width: 40px; } /* column_widths[22] = 4 */
        .col-width-24 { display: inline-block; width: 30px; } /* column_widths[23] = 3 */
        /* ... Define classes for color ... */
        # .col-1 { color: red; }
        # .col-2 { color: blue; }
        # .col-3 { color: green; }
        # .col-4 { color: orange; }
        # .col-5 { color: purple; }
        # .col-6 { color: brown; }
        # .col-7 { color: magenta; }
        # .col-8 { color: teal; }
        # .col-9 { color: olive; }
        # .col-10 { color: navy; }
        # .col-11 { color: maroon; }
        # .col-12 { color: coral; }
        # .col-13 { color: chocolate; }
        # .col-14 { color: darkgreen; }
        # .col-15 { color: darkblue; }
        # .col-16 { color: darkred; }
        # .col-17 { color: darkorchid; }
        # .col-18 { color: darkgoldenrod; }
        # .col-19 { color: crimson; }
        # .col-20 { color: green; }
        # .col-21 { color: darkslateblue; }
        # .col-22 { color: deepskyblue; }
        # .col-23 { color: dodgerblue; }
        # .col-24 { color: firebrick; }

        
         /* Font style for file name  */
        .file-name {
            font-family: Georgia, sans-serif;
            font-size: 18px;
            font-weight: bold;
        }

        /* Font style for header */
        .header-line {
            font-family: 'Lucida Console', monospace;
            font-size: 14px;
            # white-space: pre; /* Preserves whitespace and line breaks */
            # font-weight: bold;
        }


        /* Font style for labels */
        .label-font {
            font-family: Georgia, sans-serif;
            font-size: 14px;
            font-weight: bold;
        }

        /* Font style for units */
        .units-font {
            font-family: Georgia, sans-serif;
            font-size: 14px;
            font-weight: bold;
            /*font-style: italic;*/
        }

        /* Font style for data */
        .data-font {
            font-family: 'Lucida Console', monospace;
            font-size: 14px;
            font-weight: bold;
        }
   
    </style>
'''


# # Insert label rows 
# data.insert(0, unit_labels)  # Insert the units as the first row

# # Insert the units after the labels row
# data.insert(1, units)  # Insert the units as the second row


transposed_data = list(zip(*data))

# # Updated function to include font_class
# def colored_text_with_tooltip(text, color_class, width_class, font_class, tooltip):
#     if tooltip:
#         return f'<span class="{color_class} {width_class} {font_class}" title="{tooltip}">{text}</span>'
#     else:
#         return f'<span class="{color_class} {width_class} {font_class}">{text}</span>'


# Function to add a specific number of non-breaking spaces
def add_nbsp(num):
    return '&nbsp;' * num

# Define width classes for each column
width_classes = [
    "col-width-1", "col-width-2", "col-width-3", "col-width-4",
    "col-width-5", "col-width-6", "col-width-7", "col-width-8",
    "col-width-9", "col-width-10", "col-width-11", "col-width-12",
    "col-width-13", "col-width-14", "col-width-15", "col-width-16",
    "col-width-17", "col-width-18", "col-width-19", "col-width-20",
    "col-width-21", "col-width-22", "col-width-23", "col-width-24"
]

# # Create the formatted data display
# formatted_data = ""
# rightmost_column_start = 12
# # Generate HTML table with tooltips
# html = "<div class='data-table'>"
# for row_index, row in enumerate(data):
#     bg_class = "labels-bg" if row_index == 0 else "units-bg" if row_index == 1 else "data-bg"
#     html += f"<div class='data-row {bg_class}'>"

#     for i, cell in enumerate(row):
#         tooltip = tooltip_texts[i] if i < len(tooltip_texts) else ""
#         # Determine the tooltip position based on column index
#         tooltip_position_class = "tooltip-text-right" if i >= rightmost_column_start else "tooltip-text-left"
#         width_class = width_classes[i]  # Use the width class for the current column
#         html += f"<div class='data-cell {width_class}'>{cell}<span class='{tooltip_position_class}'>{tooltip}</span></div>"
#     html += "</div>"
# html += "</div>"

# # Render the table in Streamlit
# st.markdown(custom_css + html, unsafe_allow_html=True)


def CGGTTS_data_format():
    

    st.header(" CGGTTS data format: Version 2E ")
    st.subheader ("File name")

    # Render the file name using st.markdown
    st.markdown(file_name_text, unsafe_allow_html=True)

    st.subheader("File content")

    header_html = '<div class="header-bg">' + '<br>'.join(header_lines) + '</div>' 
    st.markdown(custom_css + header_html, unsafe_allow_html=True)
    
    # #Insert an empty line with background color
    # empty_line_html = '''
    # <div style="background-color: #DCDCDC; height: 20px;">
    # <span class= "tooltiptext"> Empty line indicates the end of the header </span>
    # </div>'''  # Adjust the color and height as needed

    st.markdown(custom_css + empty_line_html, unsafe_allow_html=True)

    transposed_data = list(zip(*data))

    # Create the formatted data display
    formatted_data = ""
    rightmost_column_start = 13
    # Generate HTML table with tooltips
    html = "<div class='data-table'>"
    for row_index, row in enumerate(data):
        bg_class = "labels-bg" if row_index == 0 else "units-bg" if row_index == 1 else "data-bg"
        html += f"<div class='data-row {bg_class}'>"

        for i, cell in enumerate(row):
            tooltip = tooltip_texts[i] if i < len(tooltip_texts) else ""
            tooltip_position_class = "tooltip-text-right" if i >= rightmost_column_start else "tooltip-text-left"
            width_class = width_classes[i]  # Use the width class for the current column
            html += f"<div class='data-cell {width_class}'>{cell}<span class='{tooltip_position_class}'>{tooltip}</span></div>"
        html += "</div>"
    html += "</div>"

    st.markdown(custom_css + html, unsafe_allow_html=True)

CGGTTS_data_format()