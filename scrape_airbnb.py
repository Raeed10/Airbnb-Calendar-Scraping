from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from datetime import datetime
import time
import pandas as pd 
import re
import string
import random


class ScrapeAirbnb:
    
    def __init__(self, file_path) -> None:
        # Read DataFrame
        self.data = self.read_data(file_path)
        # Setup WebDriver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.table_class = "_cvkwaj"
        self.sleep_time = random.randint(5, 25)

    def read_data (self, file_path) -> pd.DataFrame:
        data = pd.read_excel(file_path)
        return data 

    def merge_dataframes(self, df1, df2):
        merged_df = pd.concat([df1, df2], ignore_index=True)
        return merged_df

    def convert_to_dataframe(self, data):
        """
        Converts a list of dictionaries to a pandas DataFrame.
        Parameters:
        data (list): List of dictionaries to convert.
        Returns:
        pd.DataFrame: DataFrame created from the list of dictionaries.
        """
        df = pd.DataFrame(data)
        return df

    def save_results(self, data: pd.DataFrame):
        data.to_csv("results.csv", index=False)
        
    def remove_punctuation(self, text) -> str:
        # Create a translation table that maps each punctuation character to None
        translation_table = str.maketrans('', '', string.punctuation)
        # Use the translate method to remove all punctuation characters
        cleaned_text = text.translate(translation_table)
        return cleaned_text

    def extract_and_format_date(self, text) -> str:
        # Use regular expression to find the date in the text
        if text:
            date_info = text.split(".")[0]
            date_info = self.remove_punctuation(date_info)
            date_info = date_info.split(" ")
            day = date_info[0]
            month = date_info[2]
            year = date_info[3]

            # Convert the date parts into a single string
            date_str = f'{day} {month} {year}'
            # Parse the date string into a datetime object
            date_obj = datetime.strptime(date_str, '%d %B %Y')

            # Format date to DD/MM/YYYY
            formatted_date = date_obj.strftime('%d/%m/%Y')
            return formatted_date
        else:
            return None

    def extract_day_name(self, text):
        # Use regular expression to find the day name in the text
        if text :
            day_name_match = re.search(r'\d+, (\w+),', text)
            if day_name_match:
                return day_name_match.group(1)
            else:
                return None

    def is_date_greater_than_today(self, date_str):
        # Define the date format
        date_format = "%d/%m/%Y"
        # Parse the input date string to a datetime object
        input_date = datetime.strptime(date_str, date_format)
        # Get today's date
        today = datetime.today()
        # Compare the input date with today's date
        return input_date >= today
        
    def read_page(self, URL):
        self.driver.get(URL)
        time.sleep(self.sleep_time)
        # Get the page source and parse it with BeautifulSoup
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        return soup

    def extract_days_data(self, tables, page_id):
        # Function to extract days data from tables
        days = []
        for idx, table in enumerate(tables):
            for tr_element in table.find_all('tr'):
                for td_element in tr_element.find_all('td'):
                    label = td_element.get('aria-label')
                    day_date = self.extract_and_format_date(label)
                    day_name = self.extract_day_name(label)
                    div_element = td_element.find('div')
                    if div_element:
                        day_data = {
                            "Id": page_id,
                            "date": day_date,
                            "blocked": div_element.get('data-is-day-blocked'),
                            "day_number": div_element.text.strip(),
                            "day_name": day_name
                        }
                        if day_data["blocked"] == "true" and self.is_date_greater_than_today(day_date):
                            days.append(day_data)
        return days

    def collect_booked_days(self,):
        
        print("Data is being collected ...")
        results = pd.DataFrame()
        for index, row in self.data.iterrows():
            id = row["id"]
            soup = self.read_page(row["url"])
            tables = soup.find_all('table', {'class': self.table_class})
            days = self.extract_days_data(tables, page_id=id)
            results = self.merge_dataframes(results, self.convert_to_dataframe(days))
        self.save_results(results)
        self.driver.quit()
        print("Data Collected Successfully.")
    
obj_scrape_airbnb = ScrapeAirbnb("data.xlsx")
obj_scrape_airbnb.collect_booked_days()