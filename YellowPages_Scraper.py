#!/usr/bin/python
# -*- coding: utf-8 -*-

## Brian Kingery
## 3/29/2016
## YellowPages_Scraper.py

## This application is designed to:
##      1) Scrape the YellowPages.com searching for whatever the user desires
##      2) Export results to a CSV file
##      3) Use CSV file to geocode turning results into a point feature class

import requests, string, time, datetime, arcpy, os, sys, csv, geopy
from bs4 import BeautifulSoup
from arcpy import env
from geopy.geocoders import Nominatim
from glob import glob

## Target Locations
webscrapeFolder = "R:/Divisions/InfoTech/Private/GIS_Private/Kingery/Development/Web_Scraping/YellowPages/Searches"
env.workspace = webscrapeFolder
env.overwriteoutput = True

## Column Headers for the CSV file produced for Custom and State Searches
DATA = []
columnName      = "Name"
columnAddress   = "Address"
columnCity      = "City"
columnState     = "State"
columnZipcode   = "Zipcode"
columnPhone     = "Phone"
columnLat       = "Latitude"
columnLon       = "Longitude"
headers = columnName, columnAddress, columnCity, columnState, columnZipcode, columnPhone, columnLat, columnLon
DATA.append(headers)

################################################################################
## FUNCTIONS
################################################################################

def timestamp():
    global event
    timesnapshot = time.ctime()
    time_str = str(timesnapshot)
    time_list = string.split(time_str)
    month       = time_list[1]
    day         = time_list[2]
    year        = time_list[4]
    timestamp   = time_list[3]
    timestamp   = timestamp.replace(":", "")
    if timestamp[0:2] == '12':
        timestamp = timestamp[0:4] + 'pm'
    elif int(timestamp[0:2]) >= 13 and int(timestamp[0:2]) <= 24:
        x = str(int(timestamp[0:2]) - 12)
        timestamp = x + timestamp[2:4] + 'pm'
    elif timestamp[0:2] == '10' or timestamp[0:2] == '11':
        timestamp = timestamp[0:4] + 'am'
    else:
        timestamp = timestamp[1:4] + 'am'
    title = month+day+year +"_"+ timestamp
    event = str(title)
    return event

def writeCSV(workarea,x,y):
    with open(workarea + '/' + x + '.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile)
        for item in y:
            try:
                writer.writerow(item)
            except UnicodeEncodeError:
                pass
    csvfile.close()

def scrapeNOGeocode(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    g_data = soup.find_all("div", {"class": "info"})
    global state
    for item in g_data:
        try:
            name    = item.contents[0].find_all("a", {"class": "business-name"})[0].text
        except:
            pass
        try:
            street  = item.contents[1].find_all("span", {"itemprop": "streetAddress"})[0].text
        except:
            pass
        try:
            city    = item.contents[1].find_all("span", {"itemprop": "addressLocality"})[0].text.replace(',', '').strip()
        except:
            pass
        try:
            state   = item.contents[1].find_all("span", {"itemprop": "addressRegion"})[0].text
        except:
            pass
        try:
            zipcode = item.contents[1].find_all("span", {"itemprop": "postalCode"})[0].text
        except:
            pass
        try:
            phone   = item.contents[1].find_all("div",  {"class": "phones phone primary"})[0].text
        except:
            pass

        try:
            entry = name, street, city, state, zipcode, phone
            DATA.append(entry)
        except:
            pass

def scrape(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    g_data = soup.find_all("div", {"class": "info"})
    global state
    for item in g_data:
        try:
            name    = item.contents[0].find_all("a", {"class": "business-name"})[0].text
        except:
            pass
        try:
            street  = item.contents[1].find_all("span", {"itemprop": "streetAddress"})[0].text
        except:
            pass
        try:
            city    = item.contents[1].find_all("span", {"itemprop": "addressLocality"})[0].text.replace(',', '').strip()
        except:
            pass
        try:
            state   = item.contents[1].find_all("span", {"itemprop": "addressRegion"})[0].text
        except:
            pass
        try:
            zipcode = item.contents[1].find_all("span", {"itemprop": "postalCode"})[0].text
        except:
            pass
        try:
            phone   = item.contents[1].find_all("div",  {"class": "phones phone primary"})[0].text
        except:
            pass

        try:
            geolocator  = Nominatim()
            location    = geolocator.geocode(street + ' ' + city + ' ' + state + ' ' + zipcode)
            latitude    = location.latitude      # Y
            longitude   = location.longitude     # X
            entry = name, street, city, state, zipcode, phone, latitude, longitude
            DATA.append(entry)
        except:
            pass

def nationalScrapeNOGeocode(url,x):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    g_data = soup.find_all("div", {"class": "info"})
    global state
    
    for item in g_data:
        try:
            name    = item.contents[0].find_all("a", {"class": "business-name"})[0].text
        except:
            pass
        try:
            street  = item.contents[1].find_all("span", {"itemprop": "streetAddress"})[0].text
        except:
            pass
        try:
            city    = item.contents[1].find_all("span", {"itemprop": "addressLocality"})[0].text.replace(',', '').strip()
        except:
            pass
        try:
            state   = item.contents[1].find_all("span", {"itemprop": "addressRegion"})[0].text
        except:
            pass
        try:
            zipcode = item.contents[1].find_all("span", {"itemprop": "postalCode"})[0].text
        except:
            pass
        try:
            phone   = item.contents[1].find_all("div",  {"class": "phones phone primary"})[0].text
        except:
            pass

        try:
            entry = name, street, city, state, zipcode, phone
            x.append(entry)
        except:
            pass

def nationalScrape(url,x):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    g_data = soup.find_all("div", {"class": "info"})
    global state
    
    for item in g_data:
        try:
            name    = item.contents[0].find_all("a", {"class": "business-name"})[0].text
        except:
            pass
        try:
            street  = item.contents[1].find_all("span", {"itemprop": "streetAddress"})[0].text
        except:
            pass
        try:
            city    = item.contents[1].find_all("span", {"itemprop": "addressLocality"})[0].text.replace(',', '').strip()
        except:
            pass
        try:
            state   = item.contents[1].find_all("span", {"itemprop": "addressRegion"})[0].text
        except:
            pass
        try:
            zipcode = item.contents[1].find_all("span", {"itemprop": "postalCode"})[0].text
        except:
            pass
        try:
            phone   = item.contents[1].find_all("div",  {"class": "phones phone primary"})[0].text
        except:
            pass

        try:
            geolocator  = Nominatim()
            location    = geolocator.geocode(street + ' ' + city + ' ' + state + ' ' + zipcode)
            latitude    = location.latitude      # Y
            longitude   = location.longitude     # X
        
            entry = name, street, city, state, zipcode, phone, latitude, longitude
            x.append(entry)
        except:
            pass

def fGDB(name):
    ## Create New File GDB
    global fgdb
    fgdb = name
    arcpy.CreateFileGDB_management(env.workspace, fgdb)

def fGDBnational(x, name):
    ## Create New File GDB
    global fgdb
    fgdb = name + "_National"
    arcpy.CreateFileGDB_management(x, fgdb)

def customCreatePoints(x,y):
    input_table  = x + "/" + y + '_Custom.csv'
    output_points  = y + "_Custom.gdb/" + y + '_Custom'
    x_field  = columnLon
    y_field  = columnLat
    input_format = 'DD_2'
    output_format = 'DD_2'
    id_field = ''
    spatial_ref = arcpy.SpatialReference('WGS 1984')
    arcpy.ConvertCoordinateNotation_management(input_table, output_points, x_field, y_field, input_format, output_format, id_field, spatial_ref)

def stateCreatePoints(x,y,z):
    input_table  = x + "/" + y + '_' + z + '.csv'
    output_points  = y + "_" + z + ".gdb/" + y + '_' + z
    x_field  = columnLon
    y_field  = columnLat
    input_format = 'DD_2'
    output_format = 'DD_2'
    id_field = ''
    spatial_ref = arcpy.SpatialReference('WGS 1984')
    arcpy.ConvertCoordinateNotation_management(input_table, output_points, x_field, y_field, input_format, output_format, id_field, spatial_ref)
    
def nationalCreatePoints(x,y,z,w):                  # (tempFolder,stateX,projectFolder,csvName)
    input_table    = x + "/" + y + '.csv'
    output_points  = z + "/" + w + "_National.gdb/" + y
    x_field  = columnLon
    y_field  = columnLat
    input_format = 'DD_2'
    output_format = 'DD_2'
    id_field = ''
    spatial_ref = arcpy.SpatialReference('WGS 1984')
    arcpy.ConvertCoordinateNotation_management(input_table, output_points, x_field, y_field, input_format, output_format, id_field, spatial_ref)

def ProjectWebscrape():
    url_1    = "http://www.yellowpages.com/search?search_terms="
    url_2    = "&geo_location_terms="

    print "Yellow Pages Geocoder\n"
    print "This application is designed to:"
    print "   - Scrape the YellowPages website given specific search criteria"
    print "   - Export results to a CSV file"
    print "   - Geocodes the CSV file resulting in a point feature class\n"
    
    # What are you searching for?
    what     = raw_input("What are you looking for?\nKeyword: ")

    # Saves search criteria as file name
    global csvName
    csvName  = None
    csv_name = string.split(what)
    Search   = []
    for name in csv_name:
        Search.append(name.lower().capitalize())
    csvName  = ''.join(map(str, Search))
    what     = string.replace(what, ' ', '+').lower()
    # How many pages will be looked at
    pages    = 25
    # User selects which state or all
    global national
    global stateList
    national  = 'NATIONAL'
    stateList = ['AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY']
    
    choice = raw_input("\nChoose location of interest...\n\n   - Type 2 letter state abbreviation to return all entries within that state.\n\n---OR---\n\n   - Type NATIONAL if you want all entries across the entire nation.\n\n---OR---\n\n   - All other entries will be treated as a custom search.\n     Example: Newport News, VA\n\nLocation: ").upper()
    
#####
#####
  ###
  ###
  ###
#######
#######

    # Custom search
    
    if choice not in stateList and choice != national:
        timestamp()
        projectFolder = webscrapeFolder + "/" + csvName + "_Custom_" + event
        os.makedirs(projectFolder)
        del env.workspace
        env.workspace = projectFolder        
        if choice.find(',') != -1:
            choice   = string.replace(choice, ',', '%2c').lower()
            choice   = string.replace(choice, ' ', '+')
            http    = url_1 + what + url_2 + choice
        else:
            choice   = string.replace(choice,' ', '+').lower()
            http    = url_1 + what + url_2 + choice
        def goCustom():
            geocodeOption = raw_input("Geocode Results? (Yes or No): ")
            if geocodeOption.lower() == 'n' or geocodeOption.lower() == 'no':
                url = http
                scrapeNOGeocode(url)
                page_number = 2
                while page_number < (pages + 1):
                    url = http + "&page=" + str(page_number)
                    scrapeNOGeocode(url)
                    page_number += 1
                writeCSV(projectFolder,csvName + '_Custom',DATA)
            elif geocodeOption.lower() == 'y' or geocodeOption.lower() == 'yes':
                url = http
                scrape(url)
                page_number = 2
                while page_number < (pages + 1):
                    url = http + "&page=" + str(page_number)
                    scrape(url)
                    page_number += 1
                writeCSV(projectFolder,csvName + '_Custom',DATA)
                fGDB(csvName + "_Custom")
                customCreatePoints(projectFolder,csvName)
            else:
                print '\nPlease answer with Yes or No if you would like the results to be geocoded.\n'
                goCustom()
                
        goCustom()

######
######
   ###
######
###
######
######

    # Searches entire state of choice
    
    if choice in stateList:
        timestamp()
        projectFolder = webscrapeFolder + "/" + csvName + "_" + choice + "_" + event
        os.makedirs(projectFolder)
        del env.workspace
        env.workspace = projectFolder
        http = url_1 + what + url_2 + choice
        def goState():
            geocodeOption = raw_input("Geocode Results? (Yes or No): ")
            if geocodeOption.lower() == 'n' or geocodeOption.lower() == 'no':
                url = http
                scrapeNOGeocode(url)
                page_number = 2
                while page_number < (pages + 1):
                    url = http + "&page=" + str(page_number)
                    scrapeNOGeocode(url)
                    page_number += 1
                writeCSV(projectFolder,csvName + "_" + choice,DATA)
            elif geocodeOption.lower() == 'y' or geocodeOption.lower() == 'yes':
                url = http
                scrape(url)
                page_number = 2
                while page_number < (pages + 1):
                    url = http + "&page=" + str(page_number)
                    scrape(url)
                    page_number += 1
                writeCSV(projectFolder,csvName + "_" + choice,DATA)
                fGDB(csvName + "_" + choice)
                stateCreatePoints(projectFolder,csvName,choice)
            else:
                print '\nPlease answer with Yes or No if you would like the results to be geocoded.\n'
                goState()
                
        goState()

######
######
   ###
 #####
 #####
   ###
######  
######

    # Searches entire nation

    if choice == national:
        timestamp()
        projectFolder = webscrapeFolder + "/" + csvName + "_National" + "_" + event
        os.makedirs(projectFolder)
        del env.workspace
        env.workspace = projectFolder

        global tempFolder
        tempFolder = projectFolder + '/' + csvName + '_StateFolder'
        os.makedirs(tempFolder)

        def goNational():
            geocodeOption = raw_input("Geocode Results? (Yes or No): ")
            if geocodeOption.lower() == 'n' or geocodeOption.lower() == 'no':
                fGDBnational(projectFolder,csvName)
                for stateX in stateList:
                    listX = []
                    http = url_1 + what + url_2 + stateX
                    url = http
                    nationalScrapeNOGeocode(url,listX)
                    page_number = 2
                    while page_number < (pages + 1):
                        url = http + "&page=" + str(page_number)
                        nationalScrapeNOGeocode(url,listX)
                        page_number += 1
                    writeCSV(tempFolder, stateX, listX)
                # All CSVs added to fgdb as a table
                for stateX in stateList:
                    arcpy.TableToGeodatabase_conversion(tempFolder + '/' + stateX + '.csv', projectFolder + '/' + csvName + '_National.gdb')
                del env.workspace
                env.workspace = projectFolder + '/' + csvName + "_National.gdb"

                tableList = arcpy.ListTables()
                tableMerge = []
                for table in tableList:
                    tableMerge.append(table)
                arcpy.Merge_management(tableMerge,csvName + "_National")

                inTable = csvName + "_National"
                out_xls = projectFolder + '/' + csvName + "_National.xls"
                arcpy.TableToExcel_conversion(inTable, out_xls)

            elif geocodeOption.lower() == 'y' or geocodeOption.lower() == 'yes':
                fGDBnational(projectFolder,csvName)
                for stateX in stateList:
                    listX = []
                    http = url_1 + what + url_2 + stateX
                    url = http
                    nationalScrape(url,listX)
                    page_number = 2
                    while page_number < (pages + 1):
                        url = http + "&page=" + str(page_number)
                        nationalScrape(url,listX)
                        page_number += 1
                    writeCSV(tempFolder, stateX, listX)

                for stateX in stateList:
                    nationalCreatePoints(tempFolder,stateX,projectFolder,csvName)

                del env.workspace
                env.workspace = projectFolder + '/' + csvName + "_National.gdb"

                fcList = arcpy.ListFeatureClasses()
                fcMerge = []
                for fc in fcList:
                    fcMerge.append(fc)
                arcpy.Merge_management(fcMerge,csvName)
            else:
                print '\nPlease answer with Yes or No if you would like the results to be geocoded.\n'
                goNational()
                
        goNational()

################################################################################
################################################################################

                                ####  #  #  #  #
                ############### #  #  #  #  #  # ###############
                ############### ###   #  #  ## # ###############
                ############### #  #  #  #  # ## ###############
                                #  #  ####  #  #

################################################################################
################################################################################

## Start
ExecutionStartTime = datetime.datetime.now()
print "Started: %s" % ExecutionStartTime.strftime('%A, %B %d, %Y %I:%M:%S %p')
print "Processing\n"

ProjectWebscrape()

ExecutionEndTime = datetime.datetime.now()
ElapsedTime = ExecutionEndTime - ExecutionStartTime
print "\nEnded: %s\n" % ExecutionEndTime.strftime('%A, %B %d, %Y %I:%M:%S %p')
print "Elapsed Time: %s" % str(ElapsedTime).split('.')[0]

choice = raw_input("Press 'Enter' to exit program")


################################################################################
################################################################################

