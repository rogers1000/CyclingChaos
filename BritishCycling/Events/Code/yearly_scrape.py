##### NOTES
# This didn't work properly and still needs amendments to be working properly.

##### Adjust the function below to adjust the year you want to scrape.
scrape_year = 2025

##### Copy and Paste below


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import numpy as np


setwd = # Set Working Directory

# Setup headless Chrome
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

# Main event search URL
url = "https://www.britishcycling.org.uk/events?keywords=&view=off&distance=&postcode=&fromdate=01%2F01%2F"+str(scrape_year)+"&todate=31%2F12%2F"+str(scrape_year)+"&gender=&day_of_week%5B%5D=1&day_of_week%5B%5D=2&day_of_week%5B%5D=3&day_of_week%5B%5D=4&day_of_week%5B%5D=5&day_of_week%5B%5D=6&day_of_week%5B%5D=7&race_duration_min=&race_duration_max=&resultsperpage=100&series_only=0&online_entry_only=0&zuv_bc_event_filter_id%5B%5D=4&zuv_bc_event_filter_id%5B%5D=7&zuv_bc_event_filter_item_id%5B%5D=9&zuv_bc_event_filter_item_id%5B%5D=43&zuv_bc_event_filter_item_id%5B%5D=53&zuv_bc_event_filter_item_id%5B%5D=8&zuv_bc_event_filter_item_id%5B%5D=10&zuv_bc_event_filter_item_id%5B%5D=13&zuv_bc_event_filter_item_id%5B%5D=16&zuv_bc_event_filter_item_id%5B%5D=21&zuv_bc_event_filter_item_id%5B%5D=41&zuv_bc_event_filter_item_id%5B%5D=23&zuv_bc_event_filter_item_id%5B%5D=24&zuv_bc_event_filter_item_id%5B%5D=25&zuv_bc_event_filter_item_id%5B%5D=27&zuv_bc_event_filter_id%5B%5D=29&zuv_bc_event_filter_item_id%5B%5D=30&zuv_bc_event_filter_item_id%5B%5D=31&zuv_bc_event_filter_id%5B%5D=37&zuv_bc_event_filter_item_id%5B%5D=51&save-filter-name="


driver.get(url)
time.sleep(5)

events_data = []
subtable_data = []
event_id_list = []


# print('test8')

count = 0
table_count_make_sure_random = 0
table_count = 0
page_num = 1

while True:
    time.sleep(2)

    # Get the list of events and toggle buttons
    events = driver.find_elements(By.CLASS_NAME, "events--desktop__row")
    try:
        accept_cookies_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        )
        accept_cookies_button.click()
        print("✅ Accepted cookies.")
    except:
        print("⚠️ No cookie banner appeared.")
    toggle_buttons = driver.find_elements(By.CSS_SELECTOR, "a.event--race__title")

    print('event total count: ' + str(len(events)))

    for i, event in enumerate(events):
        try:
            # ✅ Extract metadata
            event_id = event.find_element(By.CSS_SELECTOR, 'a[data-event-id]').get_attribute("data-event-id")
            title = event.find_element(By.CSS_SELECTOR, 'a.event--race__title').text.strip()
            date = event.find_element(By.CLASS_NAME, 'event--date__column').text.strip()
            type = event.find_element(By.CLASS_NAME, 'event--type__row').text.strip()

            print(f"🔎 Processing event {i+1}: {title} ({event_id})")

            # ✅ Scroll and click the toggle to expand subtable
            toggle = toggle_buttons[i-1]
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle)
            time.sleep(0.5)
            driver.execute_script("arguments[0].click();", toggle)
            time.sleep(4)

            # ✅ Locate subtable(s)
            tables = event.find_elements(By.CSS_SELECTOR, ".table__more-data--showing table")
            print(f"{len(tables)} tables found for event_id: {event_id}")

            for table_index, table in enumerate(tables):
                print(f"Processing table {table_index + 1} for event_id: {event_id}")
                rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")

                for row in rows:
                    cols = row.find_elements(By.TAG_NAME, "td")
                    try:
                        race_date = cols[0].text.strip()
                        race_time = cols[1].text.strip()
                        race_race_name = cols[2].text.strip()
                        race_classification = cols[3].text.strip()
                        race_band = cols[4].text.strip()
                        race_category = cols[5].text.strip()
                        # race_entry_fee = cols[6].text.strip()
                    except:
                        race_date = 'fail'
                        race_time = 'fail'
                        race_race_name = 'fail'
                        race_classification = 'fail'
                        race_band = 'fail'
                        race_category = 'fail'
                        # race_entry_fee = 'fail'
                    
                    # subtable_data.append({
                    #     "race_id":race_id[table_index],
                    #     "Event Date":race_date,
                    #     "Event Time":race_time,
                    #     "Event Race Name":race_race_name,
                    #     "Event Classification":race_classification,
                    #     "Event Band":race_band,
                    #     "Event Category":race_category,
                    #     "Event Entry Fee":race_entry_fee
                    # })

                    events_data.append({
                    "Event ID": event_id
                    ,"Title":title
                    ,'Date':date
                    ,'Type':type,
                    "Race Date":race_date,
                    "Race Time":race_time,
                    "Race Name":race_race_name,
                    "Race Classification":race_classification,
                    "Race Band":race_band,
                    "Race Category":race_category
                    ,# "Race Entry Fee":race_entry_fee
                    })  


        except Exception as e:
            # print(f"❌ Error processing event {i+1}: {e}")
            print('event process failed, think should be once a page')
            continue
                        
    try:
        # Find and click the "Next" button
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, "a.button.button--medium.button--secondary.next")
        except:
            print('next button function failed')

        # Check if button is disabled (optional safety check)
        if "disabled" in next_button.get_attribute("class"):
            print("🚫 No more pages.")
            break

        try:
            driver.execute_script("arguments[0].scrollIntoView();", next_button)
        except:
            print('finding next page button failed')
        time.sleep(1)
        try:
            driver.execute_script("arguments[0].click();", next_button)
        except:
            print('clicking next page button failed')
        time.sleep(5)  # wait for new content to load

        page_num += 1

    except Exception as e:
        # print(f"❌ No Next button found or failed to click: {e}")
        print('hit max page')
        break
            
driver.quit()

events_data = pd.DataFrame(events_data)
events_data = events_data[events_data['Race Date'] != 'fail']

print("Saved to british_cycling_events_with_sub_events_"+str(scrape_year)+".csv")
events_data.to_csv(setwd+"/british_cycling_events_"+str(scrape_year)+".csv")
print("Saved to british_cycling_events_"+str(scrape_year)+".csv")
print('main df')
print(events_data.head(10))
print('finished 38')
