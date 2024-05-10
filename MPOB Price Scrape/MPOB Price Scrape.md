# MPOB Price Scrape
A tool to scrape prices from [MPOB Website](https://bepi.mpob.gov.my/admin2/price_local_daily_view_cpo_msia.php?more=Y&jenis=1Y&tahun=2008) to csv file
## Chromedriver
This tool needs chromedriver installed for web scraping
- Install from [here](https://www.e-sentral.com/download_installer](https://chromedriver.chromium.org/downloads))
## Program Installation 
1. Download main.py and run
**NOTE**: This program only applies to Windows.
## Requirements
- Python 3.9.12
- selenium 4.3.0
## Key Features
- Control how many and which years to scrape
- Scrape daily prices for each years and output data in csv file
## Usage Guidelines
- open main.ini file
- copy chromedriver path and change in file 
- save main.ini
- open anaconda prompt
- change directory to folder where program is stored
- run "python main.py" 
- to specify year start and end input "python main.py 2020 2022" (this will scrape from year 2020 to 2022) 
- to specify year start "python main.py 2015" (this will scrape from year 2015 to the latest year)
- find csv file stored in folder 'data', different files for each years

