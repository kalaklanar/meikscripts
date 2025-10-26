#!/usr/bin/env python3
# Read HTML content from a the web page for a Pandora Station's "Show All" page
# Extract the artists in the station and print to stdout with one artist per line
import os
import argparse
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(
    description="Reads the save HTML file from a Pandora station seeds file (My Collection > [Station Name] > See All > Save the HTML in your browser)",
)

# Adding arguments
parser.add_argument("-s", "--station", help = "HTML file to process", required = True)
# Read arguments from command line
args = parser.parse_args()

# Check if the input file exists
if args.station:
    station_file = args.station
    if not os.path.exists(station_file):
        sys.exit(f'The station HTML file '+args.station+' does not exist, so exiting...')

with open (station_file, 'r', encoding='utf-8') as file:
    html_cont = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_cont, 'html.parser')
artists = soup.find_all("a",class_="RowItemText")

#print the atrists found, one per line
for artist in artists:
    print(artist.get_text())
