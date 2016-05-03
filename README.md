# YellowPages
1. Download YellowPages_Scraper.py
2. All modules used in this script are standard except the following modules. Ensure that you have the following modules installed.
 - BeautifulSoup (https://pypi.python.org/pypi/beautifulsoup4)
 - geopy (https://pypi.python.org/pypi/geopy/1.11.0)
3. Change the webscrapeFolder variable to your own workspace

# Output
1. CSV file
2. File geodatabase (depending on option selected)

# Note
- If user chooses option to geocode the results, the geocoder only allows X items per month before the service is deactivated. I believe the service cuts off at 10,000 items.
- If user chooses to not geocode results, the program can be ran without limit.
- The program is designed to walk the user through the process. See below...

# Interface Example
- Search for all Starbucks Coffee in the state of VA without geocoding.
- Output - A single CSV of all Starbucks Coffee locations

Started: Tuesday, May 03, 2016 11:43:52 AM
Processing

Yellow Pages Geocoder

This application is designed to:
   - Scrape the YellowPages website given specific search criteria
   - Export results to a CSV file
   - Geocodes the CSV file resulting in a point feature class

What are you looking for?
Keyword: Starbucks Coffee

Choose location of interest...

   - Type 2 letter state abbreviation to return all entries within that state.

---OR---

   - Type NATIONAL if you want all entries across the entire nation.

---OR---

   - All other entries will be treated as a custom search.
     Example: Newport News, VA

Location: VA
Geocode Results? (Yes or No): n

Ended: Tuesday, May 03, 2016 11:46:01 AM

Elapsed Time: 0:02:09
Press 'Enter' to exit program
