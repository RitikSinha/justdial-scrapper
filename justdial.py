from selenium import webdriver
driver = webdriver.Chrome('./chromedriver')
import pandas as pd
import time
import os

    
def justdial(url):
    def strings_to_num(argument): 
    
        switcher = { 
            'dc': '+',
            'fe': '(',
            'hg': ')',
            'ba': '-',
            'acb': '0', 
            'yz': '1', 
            'wx': '2',
            'vu': '3',
            'ts': '4',
            'rq': '5',
            'po': '6',
            'nm': '7',
            'lk': '8',
            'ji': '9'
        } 
        
        return switcher.get(argument, "nothing")
    def scrool():
        SCROLL_PAUSE_TIME = 0.5
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
            print('scrooling page')
            # Wait to load page
            print('waiting....')
            time.sleep(SCROLL_PAUSE_TIME)
            print('scrooling page')
            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            print('scrooled full..')
            print('extracting data')
    while True:
        pages = 0
        if pages == 0:
            time.sleep(10)
            scrool()
            driver.get(url)
        else:
            driver.get(f'{url}/page-{pages}')
            scrool()
            pages = pages + 1
        
        storeDetails = driver.find_elements_by_class_name('store-details')


        nameList = []
        addressList = []
        numbersList = []

        for i in range(len(storeDetails)):
            
            name = storeDetails[i].find_element_by_class_name('lng_cont_name').text
            address = storeDetails[i].find_element_by_class_name('cont_fl_addr').get_attribute('innerHTML')
            contactList = storeDetails[i].find_elements_by_class_name('mobilesv')
            
            myList = []
            
            for j in range(len(contactList)):
                
                myString = contactList[j].get_attribute('class').split("-")[1]
            
                myList.append(strings_to_num(myString))

            nameList.append(name)
            addressList.append(address)
            numbersList.append("".join(myList))


            
        # intialise data of lists.
        data = {'Company Name':nameList,
                'Address': addressList,
                'Phone':numbersList}

        # Create DataFrame
        df = pd.DataFrame(data)
        df.to_csv('f{profession}-{city}.csv', mode='a', header=False)

print("enter city")
city = input()
print("enter profession")
profession = input()

justdial(f"https://www.justdial.com/{city}/search?q={profession}")
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

