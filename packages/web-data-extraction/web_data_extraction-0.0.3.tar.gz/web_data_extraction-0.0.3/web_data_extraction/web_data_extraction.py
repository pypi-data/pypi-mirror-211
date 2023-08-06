# A collection of functions 
# Links exctraction
# Data extraction
# 
import requests #to send HTTP requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import re

# Modules to connect with postgress
import psycopg2
import psycopg2.extras
import csv

# Modules to run automatically
import schedule # To handle scheduling tasks.
import time as tm # For time-related operations


run_count = 0  # Counter for tracking the number of times the script has run
def scrape_and_clean_data_appart4sale(filename):
    global run_count
    run_count += 1
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    

    def get_real_estate_data(filename):
        """ function to extract links

        Params:
        .......
        filename: links

        Usage:
        ......
        >>> from Apartment4sale_web_scraper import get_get_real_estate_data
        get_get_real_estate_data(filename = "Any link to the apartment for sale")
        
        """
        # Empty list to store links
        Links = []
        #Looping through the pages
        for page in range(1,2):
            # Headers used to specify how the HTTP request should be processed by the server. 
            # i.e - User-Agent header specifying the user agent string that should be sent with the request,
            # - Accept header specifying the types of content that the client can handle.
            headers = {'Accept-Encoding': 'gzip, deflate, sdch','Accept-Language': 'en-US,en;q=0.8','Upgrade-Insecure-Requests': '1',
                       'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                       'Cache-Control': 'max-age=0','Connection': 'keep-alive',}      
        
            # Requesting desired URL
            try:
                response_text = requests.get(filename + str(page), headers=headers, allow_redirects=False).text
                # Parse the HTML content
                soup = BeautifulSoup(response_text, 'html.parser')

                # Loop through every house's link
                for div in soup.findAll('div', {'class': 'item-list'}):
                    # Find the link for the current apartment
                    link = div.find('a').attrs['href']
                    # Keep the links in the Links list
                    Links.append("https://imali.biz" + link)  
            except requests.exceptions.RequestException as e:
                print(f"An error occurred while fetching data: {e}")
        # Create a DataFrame from the list
        imali_data = pd.DataFrame({'IMALI_Apartment4sale_links': Links})         
        imali_data.to_csv("IMALI_Apartment4sale_links.csv")
    

    # Function to extract apartment for sale data
    #............................................
    def extract_appart4sale_data():
        apartment_for_sale_links = pd.read_csv('IMALI_Apartment4sale_links.csv', usecols=[1])
        # List to store extracted data from all the houses for sale
        all_appart_list = []
        # Iterating through links in the df
        for i in apartment_for_sale_links['IMALI_Apartment4sale_links']:
            headers = {'accept': 'application/json',}
            # Requesting desired URL
            response_text = requests.get(i,headers=headers, allow_redirects=False).text 
            # Parsing the response text
            soup = BeautifulSoup(response_text, 'html.parser')

            # List to keep extracted data for each appartment
            each_appart_list = []
            # Iterating through each div with class "media-body"
            for div in soup.findAll('div', {'class': "media-body"}):
                # Find the specifications of the appartment
                specifications = div.find('span', {'class': "media-heading"}).text.strip()
                # Keep the specifications of the appartment
                each_appart_list.append(specifications)

            # Loop through each div with class "col-md-4" (Price & Location)
            for i in soup.findAll('div', {'class':"col-md-4"}):
                # Find the price of the appartment
                price = i.find('p').text.replace("\t","").strip()
                # Keep the price of the appartment
                each_appart_list.append(price)
                # Find the district of the appartment
                district = i.findAll('p')
                # Keep the district name of the appartment
                each_appart_list.append(district)
                # Find the sector of the appartment
                sector = i.findAll('p')
                # Keep the sector name of the appartment
                each_appart_list.append(sector)

            # Loop through each span with class "date" (Date) & to find date posted
            for div in soup.findAll('span', {"class":"date"}):
                Date = div
                # Keep the date posted
                each_appart_list.append(Date.text.strip())
            # Keep details of all appartments     
            all_appart_list.append(each_appart_list)

        #Create dataframe to keep appartments details
        columns = ["Ref_number","Build_Year","Floors","Sitting_Rooms","Dining_Rooms","Bedrooms","Wardrobes","Bathrooms","Car_Parking","Ancillary","Plot_number","LandSize", "Price", "District","Sector","Date"]
        all_appart_df = pd.DataFrame(all_appart_list, columns = columns)
        # Save the dataframe to csv file
        all_appart_df.to_csv("IMALI_appart4sale_Details.csv") 
    

    # Function to clean and save the apartment for sale data
    #.......................................................
    def clean_and_save_appart4sale_data():
        apartment4sale = pd.read_csv("IMALI_appart4sale_Details.csv")
        # Set the 'Date' column as the index & convert it to datetime format
        apartment4sale = apartment4sale.set_index(pd.to_datetime(apartment4sale['Date'], format="%a, %d %b %Y %H:%M:%S"))

        # Drop unwanted cols from the df
        apartment4sale = apartment4sale.drop(['Ref_number', 'Plot_number', "Unnamed: 0", "Date"], axis =1)
        
        # Clean respective columns accordingy
        apartment4sale['LandSize'] = [int(area.replace("m2","").replace(",","")) for area in apartment4sale['LandSize']]
        apartment4sale['District'] = apartment4sale['District'].str.split('District:</strong>').str[1].str.split('<').str[0]
        apartment4sale['Sector'] = apartment4sale['Sector'].str.split('Sector:</strong>').str[1].str.split('<').str[0]
        apartment4sale['Price'] = apartment4sale['Price'].str.replace(r'[^0-9]', '', regex=True)

        # Save the clean df to a CSV file named "IMALI_House4sale_Data.csv"
        apartment4sale.to_csv("IMALI_apartment4sale_Clean_data.csv")
        
        
    # Function to create BD to postgres
    #..................................
    def infer_column_types(csv_file_path):
        # Read data from CSV file and infer column types
        with open(csv_file_path, 'r') as csv_file:
            reader = csv.reader(csv_file)
            header = next(reader)  # Get the header row
            data_sample = next(reader)  # Get a sample row of data

        column_types = []
        for value in data_sample:
            # Check for specific data types
            if value.isdigit():
                if int(value) > 2147483647:  # Check for big integer values
                    column_types.append('BIGINT')
                else:
                    column_types.append('INTEGER')
            elif value.replace('.', '', 1).isdigit():
                column_types.append('DECIMAL')
            elif value.strip():
                try:
                    datetime.strptime(value, '%Y-%m-%d')  # Check for date values
                    column_types.append('DATE')
                except ValueError:
                    column_types.append('VARCHAR(100)')
            else:
                column_types.append('VARCHAR(100)')

        return header, column_types


    def insert_data_from_csv_to_imali_table(csv_file_path):
        # Establish a connection to the PostgreSQL database
        conn = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="Inyange"
        )

        # Create a cursor object to interact with the database
        cur = conn.cursor()

        # Create the database if it doesn't exist
        cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname='IMALI_Properties'")
        database_exists = cur.fetchone()

        if not database_exists:
            cur.execute("CREATE DATABASE IMALI_Properties")
            conn.commit()
            print("Database 'IMALI_Properties' created successfully.")

        # Close the cursor and current connection
        cur.close()
        conn.close()

        # Connect to the Trial database
        conn = psycopg2.connect(
            host="localhost",
            database="IMALI_Properties",
            user="postgres",
            password="Inyange"
        )

        # Create a new cursor object to interact with the Trial database
        cur = conn.cursor()

        # Check if the table exists
        cur.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'apartment_for_sale')")
        table_exists = cur.fetchone()[0]

        # Create the table if it doesn't exist
        if not table_exists:
            header, column_types = infer_column_types(csv_file_path)

            # Construct the CREATE TABLE query
            create_table_query = 'CREATE TABLE apartment_for_sale ('
            for column_name, column_type in zip(header, column_types):
                create_table_query += f'{column_name} {column_type}, '
            create_table_query = create_table_query.rstrip(', ') + ')'

            cur.execute(create_table_query)
            conn.commit()
            print("Table 'apartment_for_sale' created successfully.")
        else:
            # Update the table if it exists
            update_table_query = '''
                ALTER TABLE apartment_for_sale
                ADD COLUMN IF NOT EXISTS department VARCHAR(100)
            '''
            cur.execute(update_table_query)
            conn.commit()
            print("Table 'apartment_for_sale' updated successfully.")

        # Read data from CSV file
        with open(csv_file_path, 'r') as csv_file:
            reader = csv.reader(csv_file)
            next(reader)  # Skip header row
            imali_data = list(reader)
        # Sort the data by date
        sorted_data = sorted(imali_data, key=lambda x: x[0], reverse=True)

        # Insert new rows into the table if they don't already exist
        insert_query = '''
            INSERT INTO apartment_for_sale (Date, Build_Year, Floors, Sitting_Rooms, Dining_Rooms, Bedrooms, Wardrobes, Bathrooms, Car_Parking, Ancillary, LandSize, Price, District, Sector)
            SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            WHERE NOT EXISTS (
                SELECT 1 FROM apartment_for_sale WHERE Date = %s AND Build_Year = %s AND Floors = %s AND Sitting_Rooms = %s
                AND Dining_Rooms = %s AND Bedrooms = %s AND Wardrobes = %s AND Bathrooms = %s
                AND Car_Parking = %s AND Ancillary = %s AND LandSize = %s AND Price = %s
                AND District = %s AND Sector = %s
            )
        '''
        data_inserted = False  # Flag variable to track new row insertion
        for data in sorted_data:
            cur.execute(insert_query, [*data, *data])
            if cur.rowcount > 0:
                conn.commit()
                if not data_inserted:
                    print("New row(s) inserted:")
                    data_inserted = True
                print(data)
        if not data_inserted:
            print("No new data was inserted.")


        # Close the cursor and connection
        cur.close()
        conn.close()


    # Function to combine all the functions into one
    #...............................................
    def combined_function():
        # URL of the real estate listings page on 'imali.biz', with the page number left blank 
        imali_data = get_real_estate_data(filename)
        extract_appart4sale_data()
        clean_and_save_appart4sale_data()
        # Specify the path to the CSV file
        csv_file_path = 'C:\\Users\\yinyange\\Documents\\BNR\\Imali_properties\\House&Appart(all)\\Appart4sale(all)\\IMALI_apartment4sale_Clean_data.csv'
        # Insert data from the CSV file to the table
#         insert_data_from_csv_to_imali_table(csv_file_path)

    # Call the combined function
    combined_function()
    print(f"Script has run {run_count} times. Current time: {current_time}\n\n")
# scrape_and_clean_data_appart4sale('https://imali.biz/category/1/125/search?pg=')   


    
# Automation
# ..........
# # ..........
# schedule.every(5).minutes.do(scrape_and_clean_data_appart4sale)

# while True:
#     schedule.run_pending()
#     tm.sleep(30) # Optional
