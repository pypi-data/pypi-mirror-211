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



def log_name():
    current_debug_time = datetime.now()
    log_str = str(current_debug_time.hour) + '.' + str(current_debug_time.minute) + '.' + str(current_debug_time.second) + ' ' + str(current_debug_time.day) + '-' + str(current_debug_time.month)  + '-' + str(current_debug_time.year)
    logs_name = 'logs_' + log_str + '.log'
    return logs_name

def filelog(e):
    logs_name = log_name()
    with open(logs_name, 'a+') as file:
        contents = file.write(str(e))
        contents = file.write('\n')
    pass


def logg(msg, color):
    # debg('='*50)
    # debg(msg)
    # debg('='*50)
    pass


def proxies_plugin(username, proxypass, endpoint, port):
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Proxies",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
            },
            bypassList: ["localhost"]
            }
        };
    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }
    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (endpoint, port, username, proxypass)

    # extension_id = ''.join(random.choices(string.ascii_letters, k=8))
    extension = 'proxies_extension.zip' # + extension_id + '.zip'
    
    with zipfile.ZipFile(extension, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    return extension


def configure_chromedriver(proxy=None, user_agent=None, headless_mode=False, change_resolutions=False, undetected_chrome=False, detach=False):
    global pluginfile
    proxy_address = proxy
    if undetected_chrome == False:
        chrome_options = webdriver.ChromeOptions()
        
        if change_resolutions == True:
            resolutions = [[1366, 768], [1920, 1080], [1536, 864], [1440, 900], [1280, 720], [768, 1024], [1280, 800]]
            resolution = random.choice(resolutions)
                
            width = resolution[0]
            height = resolution[1]
            # debg('Chosen Dimensions Are:')
            # debg('Width: ' + str(width))
            # debg('Height: ' + str(height))
            window_size_param = 'window-size=' + str(width) + ', ' + str(height)
            chrome_options.add_argument(str(window_size_param))
        else:
            pass

        if headless_mode == True:
            chrome_options.add_argument("--headless=new")
        else:
            pass
        
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument('disable-infobars')
        chrome_options.add_argument("--lang=en")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        
        # Adding argument to disable the AutomationControlled flag 
        chrome_options.add_argument("--disable-blink-features=AutomationControlled") 
        
        # Exclude the collection of enable-automation switches 
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"]) 
        
        # Turn-off userAutomationExtension 
        chrome_options.add_experimental_option("useAutomationExtension", False)

        if proxy != None:
            proxy_full = proxy_address.strip('\n')
            proxy_full = proxy_full.split(':')
            # debg(proxy_full)
            if len(proxy_full) <= 2:
                PROXY_HOST = proxy_full[0]
                PROXY_PORT = proxy_full[1]
                no_authentication = True
            elif len(proxy_full) == 4:
                PROXY_HOST = proxy_full[0]
                PROXY_PORT = proxy_full[1]
                PROXY_USER = proxy_full[2]
                PROXY_PASS = proxy_full[3]
                no_authentication = False
        else:
            # debg('Not Using Proxy')
            pass
        

        if proxy and no_authentication == True:
            unauthenticated_proxy = str(PROXY_HOST.strip('\n')) + ':' + str(PROXY_PORT.strip('\n'))
            chrome_options.add_argument('--proxy-server=%s' % unauthenticated_proxy)
        elif proxy and no_authentication == False:
            pluginfile = proxies_plugin(PROXY_USER, PROXY_PASS, PROXY_HOST, PROXY_PORT)
            chrome_options.add_extension(pluginfile)
            
        if user_agent:
            user_agent = user_agent.strip('\n')
            chrome_options.add_argument('--user-agent=%s' % user_agent)


        if detach == True:
            chrome_options.add_experimental_option("detach", True)
        else:
            chrome_options.add_experimental_option("detach", False)

        
        try:
            # Open the file with the list of User Agents
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            # Changing the property of the navigator value for webdriver to undefined 
        except Exception as e:            
            # Pick emy
            # debg('Chrome Failed Loading With Error:')
            # debg(e)
            logg('Error Loading Chrome.', '#f9600f')

            # Open the file with the list of User Agents
            # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        
    else:
        chrome_options = uc.ChromeOptions()
        
        try:
            # Open the file with the list of User Agents
            if headless_mode == True:
                # debg('Using Headless Undetected Chromedriver!')
                driver = uc.Chrome(chrome_options=chrome_options, headless=True)
            else:
                # debg('Using Headfull Undetected Chromedriver!')
                driver = uc.Chrome(chrome_options=chrome_options)
            # Changing the property of the navigator value for webdriver to undefined 
        except Exception as e:            
            # Pick emy
            # debg('Chrome Failed Loading With Error:')
            # debg(e)
            logg('Error Loading Chrome.', '#f9600f')
            
        
    return driver
