#!/usr/bin/env python

import string
def main():
    infile = open('incidence_final_cleaned.csv', 'r')
    outfile = open('incidence_final_cleaned2.csv', 'w')
    for line in infile:
        fields = line.split(",")
        line = "%s,%s,%s" % (string.capwords(fields[0]), fields[1], fields[2])
        outfile.write(line)
    infile.close()
    outfile.close()

    
if __name__ == "__main__":
    main()
