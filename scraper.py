from selenium import webdriver # allow launching browser
from selenium.webdriver.common.by import By # allow search with parameters
from selenium.webdriver.support.ui import WebDriverWait # allow waiting for page to load
from selenium.webdriver.support import expected_conditions as EC # determine whether the web page has loaded
from selenium.common.exceptions import TimeoutException # handling timeout situation
from selenium.webdriver.chrome.service import Service
import pandas as pd

driver_option = webdriver.ChromeOptions()
driver_option.add_argument(" — incognito")


chromedriver_path = 'chromedriver-win64\chromedriver-win64\chromedriver.exe'

def create_webdriver():
    service = Service(chromedriver_path)
    return webdriver.Chrome(service=service, options=driver_option)


# Open the website
browser = create_webdriver()
browser.get("https://github.com/collections/machine-learning")

try:
    projects = browser.find_elements(By.XPATH, "//h1[@class='h3 lh-condensed']")
    project_list = {}

    for proj in projects:
        proj_name = proj.text  # Extract project name
        proj_url = proj.find_element(By.TAG_NAME, "a").get_attribute("href")  # Extract project URL
        project_list[proj_name] = proj_url

    project_df = pd.DataFrame.from_dict(project_list, orient="index")

    # Fix column names
    project_df["project_name"] = project_df.index
    project_df.columns = ["project_url", "project_name"]
    project_df = project_df.reset_index(drop=True)

    # ✅ Save DataFrame to CSV
    project_df.to_csv("project_list.csv", index=False)
    print("\n✅ Data saved to 'project_list.csv'!")
except TimeoutException:
    print("❌ Timed out while loading page!")

# ✅ Step 4: Close the browser
browser.quit()