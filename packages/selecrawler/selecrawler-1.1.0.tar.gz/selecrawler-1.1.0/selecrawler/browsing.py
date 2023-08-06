import os
import csv
import glob
import json
import time
import random
import string
import tkinter
import zipfile
import logging
import requests
import threading
import multiprocessing
from datetime import datetime
from selenium import webdriver
from multiprocessing import Process
import undetected_chromedriver as uc
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC


def human_delay():
    global driver
    mean_delay = random.choice(range(2,7))
    delay = random.normalvariate(mean_delay, mean_delay/4)
    time.sleep(delay)


def human_typing(text, typing_area):
    global driver
    for char in text:
        start = 0.1 
        stop = 0.3
        step = 0.2
        precision = 0.1
        f = 1 / precision
        n = random.randrange(1, 3, 2) / f
        typo_chance = random.choice(range(0, 99))
        if typo_chance >= random.choice(range(80,95)):
            typo_keys = random.choice(range(1, 4))
            letters = list(string.ascii_lowercase)
            for _ in range(typo_keys):
                letter = random.choice(letters)
                typing_area.send_keys(letter)
                time.sleep(n)

            for removal in range(typo_keys):
                typing_area.send_keys(Keys.BACKSPACE)
                time.sleep(n)

        time.sleep(n)
        typing_area.send_keys(char)


def wait_for_element(driver, time, by_attribute, attribute_value):
    """
    Wait for an element to be present in the DOM using the specified WebDriver By attribute and attribute value.
    
    Args:
        driver: a Selenium WebDriver object
        time (int): the time in seconds to wait for the element to be present
        by_attribute (str): the By attribute to search for the element by (e.g. By.ID, By.XPATH)
        attribute_value (str): the value of the attribute to search for
        
    Returns:
        A WebDriverWait object that can be used in a Selenium WebDriver statement
    """
    by_method = getattr(By, by_attribute)
    return WebDriverWait(driver, time).until(EC.presence_of_element_located((by_method, attribute_value)))
