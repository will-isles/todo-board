import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

def take_screenshot():
    options = ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    # Set the dimensions of the window
    driver.set_window_size(800, 480)  # width, height

    driver.get('http://localhost:8501')

    # Wait until the page has finished loading
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'p')))

    screenshot = driver.save_screenshot('static/screenshot.png')
    driver.quit()
    return screenshot

st.write("# Screenshotting")
st.markdown("[![Click me](app/static/screenshot.png)](https://streamlit.io)")

take_screenshot()