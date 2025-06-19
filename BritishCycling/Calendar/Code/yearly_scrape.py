##### ADDING QUICK ADJUSTMENT FOR CODE THAT MEANS THE REST IS COPY AND PASTE
scrape_year = 2024


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


setwd = ### Your Working Directory 

### Setup headless Chrome (or not depending on if testing or not)
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

page_num = 1
month = 1

for month in range(1,13):
    if month < 10:
        month_str = '0'+str(month)
    else:
        month_str = str(month)
    events_data = []
    page_num = 1
    url = "https://www.britishcycling.org.uk/events?keywords=&view=off&distance=&postcode=&fromdate=01/"+month_str+"/"+str(scrape_year)+"&todate=31/"+month_str+"/"+str(scrape_year)+"&gender=&day_of_week[]=1&day_of_week[]=2&day_of_week[]=3&day_of_week[]=4&day_of_week[]=5&day_of_week[]=6&day_of_week[]=7&race_duration_min=&race_duration_max=&resultsperpage=100&series_only=0&online_entry_only=0&zuv_bc_event_filter_id[]=4&zuv_bc_event_filter_item_id[]=9&zuv_bc_event_filter_item_id[]=43&zuv_bc_event_filter_item_id[]=53&zuv_bc_event_filter_item_id[]=8&zuv_bc_event_filter_item_id[]=10&zuv_bc_event_filter_item_id[]=12&zuv_bc_event_filter_item_id[]=21&zuv_bc_event_filter_item_id[]=41&zuv_bc_event_filter_item_id[]=23&zuv_bc_event_filter_item_id[]=24&zuv_bc_event_filter_item_id[]=25&zuv_bc_event_filter_id[]=29&zuv_bc_event_filter_item_id[]=30&zuv_bc_event_filter_item_id[]=31&zuv_bc_event_filter_id[]=37&zuv_bc_event_filter_item_id[]=51&save-filter-name="
   
    driver.get(url)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "events--desktop__row")))

    while True:
        WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "events--desktop__row")))

        ### Get the list of events and toggle buttons
        events = driver.find_elements(By.CLASS_NAME, "events--desktop__row")
        ### Accept Cookies Toggle
        try:
            accept_cookies_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            )
            accept_cookies_button.click()
            print("✅ Accepted cookies.")
        except:
            print("⚠️ No cookie banner appeared.")

        ### Locate toggle button to unhide nested tables
        toggle_buttons = driver.find_elements(By.CSS_SELECTOR, "a.event--race__title")

        ### Terminal commentary so can understand how far through the code is

        print(f'month: {month_str} event page: {page_num} event total count: ' + str(len(events)))

        ####

        for i in range(len(events)):
            try:
                # Re-fetch the list of event rows and toggle buttons each time
                events = driver.find_elements(By.CLASS_NAME, "events--desktop__row")
                toggle_buttons = driver.find_elements(By.CSS_SELECTOR, "a.event--race__title")
                event = events[i]

            ### Main table data
                event_id = event.find_element(By.CSS_SELECTOR, 'a[data-event-id]').get_attribute("data-event-id")
                event_title = event.find_element(By.CSS_SELECTOR, 'a.event--race__title').text.strip()
                event_date = event.find_element(By.CLASS_NAME, 'event--date__column').text.strip().rsplit(' ')[-1]
                event_day = event.find_element(By.CLASS_NAME, 'event--date__column').text.strip().rsplit(' ')[0]
                event_type = event.find_element(By.CLASS_NAME, 'event--type__row').text.strip()
            ### Provide commentary on code update
                print(f"🔎 Processing page {page_num} event {i+1}: {event_title} ({event_id})")

                ### interactive button usage
                toggle = toggle_buttons[i-1]
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle)
                time.sleep(0.5)
                driver.execute_script("arguments[0].click();", toggle)
                time.sleep(4.5)

                ### scrape nested table
                tables = event.find_elements(By.CSS_SELECTOR, ".table__more-data--showing table")
                print(f"{len(tables)} tables found for event_id: {event_id}")

                for table_index, table in enumerate(tables):
                    print(f"Processing table {table_index + 1} for month {month_str} event_id: {event_id} on page {page_num}")
                    rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")

                    for row in rows:
                        cols = row.find_elements(By.TAG_NAME, "td")
                        try:
                            race_date = cols[0].text.strip()
                        except:
                            race_date = 'fail'
                        try:
                            race_time = cols[1].text.strip()
                        except:
                            race_time = 'fail'
                        try:
                            race_name = cols[2].text.strip()
                        except:
                            race_name = 'fail'
                        try:
                            race_classification = cols[3].text.strip()
                        except:
                            race_classification = 'fail'
                        try:
                            race_band = cols[4].text.strip()
                        except:
                            race_band = 'fail'
                        try:
                            race_category = cols[5].text.strip()
                        except:
                            race_category = 'fail'
                        
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
                        "Event_ID": event_id
                        ,"Event_Title":event_title
                        ,'Event_Date':event_date
                        ,'Event_Day':event_day
                        ,'Event_Type':event_type,
                        "Race_Date":race_date,
                        "Race_Time":race_time,
                        "Race_Name":race_name,
                        "Race_Classification":race_classification,
                        "Race_Band":race_band,
                        "Race_Category":race_category
                        ,# "Race Entry Fee":race_entry_fee
                        })  


            except Exception as e:
                # print(f"❌ Error processing event {i+1}: {e}")
                print('event process failed, think should be once a page')
                print('The failed event month: '+str(month_str)+' page: '+str(page_num)+' event total count: ' + str(len(events)))
                continue
                            
        try:
            # if page_num > 1:
            #     break
            ### Use "Next" page button to load next 100 events
            try:
                next_button = driver.find_element(By.CSS_SELECTOR, "a.button.button--medium.button--secondary.next")
            except:
                print('next button function failed')

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
                
            WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "events--desktop__row"))) 

            page_num += 1

        except Exception as e:
            print('hit max page')
            break

    events_data = pd.DataFrame(events_data)
    print(events_data)
    # events_data = events_data[events_data['Race_Date'] != 'fail']
    print("Saved to british_cycling_events_with_sub_events_"+str(scrape_year)+"_"+str(month_str)+".csv")
    events_data.to_csv(setwd+"/british_cycling_events_"+str(scrape_year)+"_"+str(month_str)+".csv")
            
driver.quit()

### Basic pandas manipulation

jan = pd.read_csv(setwd+"british_cycling_events_"+str(scrape_year)+"_01.csv")
feb = pd.read_csv(setwd+"british_cycling_events_"+str(scrape_year)+"_02.csv")
mar = pd.read_csv(setwd+"british_cycling_events_"+str(scrape_year)+"_03.csv")
apr = pd.read_csv(setwd+"british_cycling_events_"+str(scrape_year)+"_04.csv")
may = pd.read_csv(setwd+"british_cycling_events_"+str(scrape_year)+"_05.csv")
jun = pd.read_csv(setwd+"british_cycling_events_"+str(scrape_year)+"_06.csv")
jul = pd.read_csv(setwd+"british_cycling_events_"+str(scrape_year)+"_07.csv")
aug = pd.read_csv(setwd+"british_cycling_events_"+str(scrape_year)+"_08.csv")
sep = pd.read_csv(setwd+"british_cycling_events_"+str(scrape_year)+"_09.csv")
oct = pd.read_csv(setwd+"british_cycling_events_"+str(scrape_year)+"_10.csv")
nov = pd.read_csv(setwd+"british_cycling_events_"+str(scrape_year)+"_11.csv")
dec = pd.read_csv(setwd+"british_cycling_events_"+str(scrape_year)+"_12.csv")

events_full_year = pd.concat([jan,feb,mar,apr,may,jun,jul,aug,sep,oct,nov,dec])

events_full_year = events_full_year[events_full_year['Race_Name'] != 'fail']

print("Saved to british_cycling_events_"+str(scrape_year)+".csv")
events_full_year.to_csv(setwd+"/british_cycling_events_"+str(scrape_year)+".csv")

print(events_full_year)

print('finished code!')
