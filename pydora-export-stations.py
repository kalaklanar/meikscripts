#!/usr/bin/env python3
import os
import sys
import logging
import argparse
import csv

from pandora import clientbuilder,client
from pydora import configure

def get_client():
    cfg_file = os.environ.get("PYDORA_CFG", "")
    builder = clientbuilder.PydoraConfigFileBuilder(cfg_file)
    if builder.file_exists:
        return builder.build()

    builder = clientbuilder.PianobarConfigFileBuilder()
    if builder.file_exists:
        return builder.build()

    if not client:
        try:
            configure()
        except Exception:
            sys.exit("Error loading config file. Unable to continue.")

def export_station(client,station,outputdir):
    station_list_file = outputdir + station.name
    if station.can_add_music:
        try:
            stationinfo = client.get_station(station.token)
            allseeds = stationinfo.seeds
            artistlist = allseeds.artists
            songlist = allseeds.songs
            genreslist = allseeds.genres
            # I can't figure out a better way to keep the types, so I go through this 3 times
            with open(station_list_file+".csv", "w", newline='') as csvfile:
                wr = csv.writer(csvfile, dialect='excel')
                csv_headers = f'artist_name,song_name,type'
                wr.writerow(csv_headers.split(","))
                for i in range(len(songlist)):
                    newrow = [songlist[i].artist_name,songlist[i].song_name,"song"]
                    wr.writerow(newrow)
                for i in range(len(artistlist)):
                    newrow = [artistlist[i].artist_name,artistlist[i].song_name,"artist"]
                    wr.writerow(newrow)
                for i in range(len(genreslist)):
                    newrow = [genreslist[i].genre_name,artistlist[i].song_name,"genre"]
                    wr.writerow(newrow)
        except Exception as e:
            print(f"Unable to export station {station.name} with Error:\n {e}")
    else:
        with open(station_list_file+".txt", "w") as f:
            f.write("Cannot add songs to this station\n")

    
def main():
    parser = argparse.ArgumentParser(
        description="Reads Stations from Pandora and writes them to insdividual .csv files in the outputdir directory !!MUST configure with pydora-configure first!!"
    )

    # Adding arguments
    parser.add_argument("-o", "--outputdir", help = "Directory to write station files", required = True)
    parser.add_argument("-v", "--verbose", help = "enable verbose logging", action = "store_true")
    # Read arguments from command line
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.ERROR)

    if args.outputdir:
        outputdir = args.outputdir
        if not os.path.exists(outputdir):
            sys.exit(f'The output directory '+args.outputdir+' does not exist, so exiting...')
        try:
            filename  = os.path.join(outputdir, 'write_test.txt')
            f = open(filename,"w")
            f.close()
            os.remove(filename)
        except:
            sys.exit(f'The output directory '+outputdir+' is not writable, so exiting...')
    
    client = get_client()
 
    stations = client.get_station_list()

    for station in stations:
        # print(station)
        export_station(client,station,outputdir)

main()