import sys
import csv

# Define functions
def av_format(record):      # Analog Voice Format
    callsign = record[0]
    # band = record[1]
    # chan = record[2]
    rxfreq = record[3]
    txfreq = record[4]
    # mode = record[5]
    # locator = record[6]
    location = record[7]
    # ngr = record[8]
    # region = record[9]
    ccode = record[10]
    # keeper = record[11]
    # lat = record[12]
    # lon = record[13]
    if ccode != "" and ccode[0].isnumeric() and float(ccode) > 66 and float(ccode) < 255:    # CTCSS Tone Freq
        fcode = '{:05.1f}'.format(float(ccode))
    elif ccode != "" and ccode[0] == "D":                                           # DCS Code
        fcode = ccode
    else:
        fcode = "NONE"
    return [callsign+" "+location, "FM", "12.5", txfreq, rxfreq, "-NULL-", "NORMAL", "Always", "Low", "Low", "Infinite", "0", "LOW", "No", "No", "No", "No", "No", fcode, fcode, "180", "Off", "Off", "YES", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NONE", "NONE", "NONE", "0", "NONE", "1", "0"] 
 
def dv_format(record,tg,ts):      # Digital Voice Format
    callsign = record[0]
    # band = record[1]
    # chan = record[2]
    rxfreq = record[3]
    txfreq = record[4]
    # mode = record[5]
    # locator = record[6]
    location = record[7]
    # ngr = record[8]
    # region = record[9]
    ccode = record[10]
    # keeper = record[11]
    # lat = record[12]
    # lon = record[13]
    return [callsign+" "+tg+"/"+ts+" "+location, "DMR", "12.5", txfreq, rxfreq, "-NULL-", "NORMAL", "Color Code Free", "Low", "Low", "180", "0", "LOW", "No", "No", "No", "No", "No", "000.0", "000.0", "180", "Off", "Off", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NONE", "TG"+tg, "NONE", ccode, "NONE", "1", ts]
 
# Check arguments handed to script
if len(sys.argv) > 1 and sys.argv[1].endswith(".csv"):          # One filename handed to script OK
        infile = sys.argv[1]
        if len(sys.argv) > 2 :
            home_repeaters = sys.argv                   # Create a list of home_repeater callsigns
            home_repeaters.pop(0)                       # Remove script name from list
            home_repeaters.pop(0)                       # Remove csv file name from list
        else:
            home_repeaters = []
        print("\nRepeater call signs provided: "+str(home_repeaters))
else:							        # No filenames handed to script NOT OK
    sys.exit("\nUsage: "+sys.argv[0]+" import_file.csv [optional: home_repeater]")

# Generate output file name
count = len(infile) - 4
outfile = infile[:count] + "_conv.csv"
print("\nRunning conversion of "+infile+ " to "+outfile)

# Open input and output files
in_db = csv.reader(open(infile, 'r', errors='replace'))
out_db = open(outfile, 'w', newline ='')

# Process input file line by line
for record in in_db:
        callsign = record[0]
        band = record[1]
        mode = record[5]

        if band == "70CM" and mode == "AV":
            csv.writer(out_db, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL).writerow(av_format(record))
        
        elif band == "70CM" and ( mode == "DV" or mode == "MULTI" ):
            
            ishomerepeater = False
            for rptcall in home_repeaters:
                if callsign.upper() == rptcall.upper():
                    ishomerepeater = True

            if ishomerepeater:
                talkgroups = [(1,1), (2,1), (9,1), (9,2), (13,1), (80,1), (81,1), (82,1), (83,1), (84,1), (113,1), (123,1), (129,1), (235,1), (801,2), (810,2), (820,2), (840,2), (850,2), (9990,2)]
            else:
                talkgroups = [(9,2)]
            for talkgroup in talkgroups:
                csv.writer(out_db, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL).writerow(dv_format(record, str(talkgroup[0]), str(talkgroup[1]) ))

# Close output file
out_db.close()
