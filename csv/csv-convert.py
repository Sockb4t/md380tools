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
 
def write_line(out_db, line):       # Write a given line (string) to the out_db file
    csv.writer(out_db, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL).writerow(line)
        
def ishomerepeater(callsign):       # Boolean: Whether the given call sign matches one of the home repeaters
    retval = False
    for rptcall in home_repeaters:
        if callsign.upper() == rptcall.upper():
            retval = True
    return retval

def addsimplex(out_db):

    # Analogue PMR uses sixteen FM channels separated by 12.5 kHz from each other. 
    for pmrchan in [(1,"446.006250"), ( 2,"446.018750"), ( 3,"446.031250"), ( 4,"446.043750"), ( 5,"446.056250"), ( 6,"446.068750"), ( 7,"446.081250"), ( 8,"446.093750"),                   (9,"446.106250"), (10,"446.118750"), (11,"446.131250"), (12,"446.143750"), (13,"446.156250"), (14,"446.168750"), (15,"446.181250"), (16,"446.193750")]:
        memname = "PMR446-"+str(pmrchan[0])+" FM Simplex"
        txfreq = pmrchan[1]
        rxfreq = txfreq
        #tg = "9"
        ts = "1"
        ccode = "1"
        write_line(out_db,[memname, "FM", "12.5", txfreq, rxfreq, "-NULL-", "NORMAL", "Always", "Low", "Low", "180", "0", "LOW", "No", "No", "No", "No", "No", "NONE", "NONE", "180", "Off", "Off", "YES", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NONE", "NONE", "NONE", ccode, "NONE", "1", ts])

    # Digital DMR Tier I uses eight digital voice channels separated by 12.5 kHz from each other with 4-level FSK modulation at 3.6 kbit/s.
    for dmrchan in [(1,"446.106250"), (2,"446.118750"), (3,"446.131250"), (4,"446.143750"), (5,"446.156250"), (6,"446.168750"), (7,"446.181250"), (8,"446.193750")]:
        memname = "DMR446-"+str(dmrchan[0])+" DV Simplex"
        txfreq = dmrchan[1]
        rxfreq = txfreq
        tg = "9"
        ts = "1"
        ccode = "1"
        write_line(out_db,[memname, "DMR", "12.5", txfreq, rxfreq, "-NULL-", "NORMAL", "Color Code Free", "Low", "Low", "180", "0", "LOW", "No", "No", "No", "No", "No", "NONE", "NONE", "180", "Off", "Off", "YES", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NONE", "TG"+tg, "NONE", ccode, "NONE", "1", ts])

    # UK Amateur Radio UHF 430-440 MHz

    for dmrchan in [(1,"438.587500"), (2,"438.600000"), (3,"438.612500"), (4,"438.625000"), (5,"438.637500"), (6,"438.650000"), (7,"438.662500"), (8,"438.675000")]:
        memname = "DMR"+str(dmrchan[0])+" DV Simplex"
        if dmrchan[0] == 3:
            memname = "DMR3 CALL DV Simplex"
        txfreq = dmrchan[1]
        rxfreq = txfreq
        tg = "9"
        ts = "1"
        ccode = "1"
        write_line(out_db,[memname, "DMR", "12.5", txfreq, rxfreq, "-NULL-", "NORMAL", "Color Code Free", "Low", "Low", "180", "0", "LOW", "No", "No", "No", "No", "No", "NONE", "NONE", "180", "Off", "Off", "YES", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NONE", "TG"+tg, "NONE", ccode, "NONE", "1", ts])

    for dmrchan in [("U272","433.400000"), ("U274","433.425000"),("U276","433.450000"),("U278","433.475000"),("U280","433.500000"),("U282","433.525000"),("U284","433.550000"),("U286","433.575000"), ("U288","433.600000")]:
        txfreq = dmrchan[1]
        rxfreq = txfreq
        tg = "9"
        ts = "1"
        ccode = "1"
        memname = dmrchan[0] + " DV Simplex"
        write_line(out_db,[memname, "DMR", "12.5", txfreq, rxfreq, "-NULL-", "NORMAL", "Color Code Free", "Low", "Low", "180", "0", "LOW", "No", "No", "No", "No", "No", "NONE", "NONE", "180", "Off", "Off", "YES", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NONE", "TG"+tg, "NONE", ccode, "NONE", "1", ts])
        memname = dmrchan[0] + " FM Simplex"
        write_line(out_db,[memname, "FM", "12.5", txfreq, rxfreq, "-NULL-", "NORMAL", "Always", "Low", "Low", "180", "0", "LOW", "No", "No", "No", "No", "No", "NONE", "NONE", "180", "Off", "Off", "YES", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NONE", "NONE", "NONE", ccode, "NONE", "1", ts])

    for dmrchan in ["432.625000", "432.650000","432.675000"]:
        txfreq = dmrchan
        rxfreq = txfreq
        tg = "9"
        ts = "1"
        ccode = "1"
        memname = dmrchan[:7] + " DV Simplex"
        write_line(out_db,[memname, "DMR", "12.5", txfreq, rxfreq, "-NULL-", "NORMAL", "Color Code Free", "Low", "Low", "180", "0", "LOW", "No", "No", "No", "No", "No", "NONE", "NONE", "180", "Off", "Off", "YES", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NONE", "TG"+tg, "NONE", ccode, "NONE", "1", ts])


# Check arguments handed to script
if len(sys.argv) > 1 and sys.argv[1].endswith(".csv"): # One filename handed to script OK
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
#count = len(infile) - 4
#outfile = infile[:count] + "_conv.csv"
outfile = "dmr-contacts.csv"
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
            write_line(out_db, av_format(record))
        
        elif band == "70CM" and ( mode == "DV" or mode == "MULTI" ):
            if ishomerepeater(callsign):
                talkgroups = [(1,1), (2,1), (9,1), (9,2), (13,1), (80,1), (81,1), (82,1), (83,1), (84,1), (113,1), (123,1), (129,1), (235,1), (801,2), (810,2), (820,2), (840,2), (850,2), (9990,2)]
            else:
                talkgroups = [(9,2)]
            for talkgroup in talkgroups:
                write_line(out_db, dv_format(record, str(talkgroup[0]), str(talkgroup[1]) ))

# Add Simplex frequencies
addsimplex(out_db)

# Close output file
out_db.close()
