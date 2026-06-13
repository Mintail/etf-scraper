"""
User Configuration

Edit these settings to control input/output files and default parameters.
All values here can be safely customized.

Sections
---------
1. MAIN INPUTS: file paths and overwrite behavior
2. DEFAULT PARAMETERS: settings for data extraction and file handling
"""

########## MAIN INPUTS ##########
path             = "examples/"          # Path to the folder containing input files
input_file       = "input_test.txt"     # Name of the input file
output_file      = "output.xlsx"        # Name of the output file
use_input_format = False                # If input_file and output_file are excel,
                                        # True = use input_file format into the output_file
override_input   = False                # If input_file == output_file: False = create a backup copy

########## DEFAULT PARAMETERS ##########
# Website to scrap (see config for the list of websites)
WEBSITE = "justETF"

# SoupDataExtractor defaults (see soup_extractor.py)
BROWSER       = "Safari"            # Browser to use for scraping
HEADLESS      = True                # Run browser in headless mode (not available for Safari)
LOAD_TIMEOUT  = 10                  # Max seconds to wait for page load
LOAD_WAIT     = 2                   # Seconds to wait after page load
RETRY_DELAYS  = ( 60, 120, 180, 240, 300 ) # Retry delays in seconds

# FileReader defaults (see file_utils.py)
CSV_SEP = ","                       # Use ";" for French locale

# FileWriter defaults (see file_utils.py)
LINE_HEIGHT    = 14                 # Row height in Excel output
MAX_LINE_WIDTH = 40                 # Maximum width before splitting line
