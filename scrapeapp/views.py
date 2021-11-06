from tqdm import tqdm
from django.shortcuts import redirect, render
import time
from django.http import HttpResponse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from scrapeapp.forms import UserForm

def scrapwithselenium(request,query,drop):
    
  
    '''options defines whether the window of the website to be scraped to remain closed or opens '''
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")


    '''am using the chrome webdriver to scrape the site.it has argments 
    namely:options,executable_path where options has metadata defining whether the window runs in the background or opens up.
    while executable_path provides the path to the chromedriver used by selanium for scraping.
    not defining options means the window should display'''


    driver = webdriver.Chrome(executable_path='/home/mwashe/Downloads/chromedriver_linux64/chromedriver')
    
    '''we access the site to be scraped by get'''
    driver.get('https://www.tred.com/buy?body_style=&distance=50&exterior_color_id=&make=&miles_max=100000&miles_min=0&model=&page_size=24&price_max=100000&price_min=0&query=&requestingPage=buy&sort=desc&sort_field=updated&status=active&year_end=2022&year_start=1998&zip=')
    

    '''select element where here we select element 5 in the select options.we use select from selanium select'''
    rad=Select(driver.find_element(By.XPATH,'/html/body/section/div/div/div[3]/div/section/div/div[1]/div/section/form/div[1]/div[2]/div[1]/select'))
    rad.select_by_value(drop)
    print(rad.options)



    '''we then access search button and pass in the search value here we use ziocode 77494 by default we then send the value and press enter key'''  
    search=driver.find_element_by_xpath('/html/body/section/div/div/div[3]/div/section/div/div[1]/div/section/form/div[1]/div[2]/div[2]/input')
    search.clear()
    search.send_keys(query+ Keys.ENTER)
    search.submit()
    '''this is a pause.it allows the thread to relax for a while for instance for 5 seconds in our case'''
    time.sleep(5)

    '''here we are scrolling the page we first read the page height and save it to pervious_height variable'''
    pervious_height=driver.execute_script('return document.body.scrollHeight')

    while True:
        '''when there is previous height we can the scroll.we pause for 5 miliseconds ater every load to allow the page to load'''
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
        time.sleep(5)
        newHeight=driver.execute_script('return document.body.scrollHeight')
        if newHeight==pervious_height:
            '''we break when the scroll is at the end'''
            break
        '''assign previous height to newheight because condition is while true so that the while goes false'''
        pervious_height=newHeight


    '''get the cars list from all the loaded cars'''
    cars = driver.find_elements_by_class_name('grid-box-container')
    individualcarlinks=[]
    for car in cars:
        '''iterate through the cars list'''
        try:
            '''from each car object get the link and save to individuallinks ist'''
            linkcars=car.find_element_by_tag_name('a')
            link=linkcars.get_property('href')
            individualcarlinks.append(link)
        except:
            pass
    print(len(individualcarlinks))
    alldetails=[]
    for link in tqdm(individualcarlinks):
        '''access each link tqdm helps keep track of progress sor far and the remaining'''
        driver.get(link)
        try:
            '''access the link ,get the nme,price,summary,options with waits to ensure it gets data beore continuing'''
            
            
            carName=WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.XPATH,'//*[@id="react"]/div/div/div[2]/div[5]/div[2]/div/h1[1]'))
        )
            
            price=WebDriverWait(driver,10).until(
                EC.presence_of_element_located(
                    (By.XPATH,'/html/body/section/div/div/div[2]/div[4]/div/div/div[2]/div/div/h2'))
                    )
            summary=WebDriverWait(driver,10).until(
                EC.presence_of_element_located((By.XPATH,'/html/body/section/div/div/div[2]/div[5]/div[2]/div/div[5]/div/div/div[3]/div[1]/table'))
                )
           
            
            
           
            '''trim the name'''
            
            carName=carName.text,
            carName=str(list(carName))
            carName=carName.split()
            carName=carName[1:]
            carName=carName[:-2]
            carName=(' '.join(carName))
            print(carName)
            try:
                '''get the options'''
                op=[]
                options=driver.find_element_by_xpath('/html/body/section/div/div/div[2]/div[5]/div[2]/div/div[5]/div/div/div[3]/div[2]/table/tbody/tr[4]') 
                
                option2=driver.find_element_by_xpath('/html/body/section/div/div/div[2]/div[5]/div[2]/div/div[5]/div/div/div[3]/div[2]/table/tbody/tr[5]/td')
                    
                
                op.append(options.text)
                op.append(option2.text)
                
                
            except:
                op='none'
            
            temporarydetails={
                'carName':carName,
                'price':price.text,
                'summary':summary.text[7:],
                'options':op,
            }
            print(temporarydetails)
            alldetails.append(temporarydetails)
           
            
           
        
            
        except:
            print('oops')
       

   
        
    print(alldetails)
    
    '''convert the data to a dataframe with pandas'''
    df=pd.DataFrame(alldetails)

    '''convert the dataframe to csv file caled datas.csv'''
    df.to_csv('datas.csv')
  
       
  
    '''exit'''    
    driver.quit()
    '''render the dataframe'''
    return HttpResponse('done')
    

def home(request):
    '''get the zipcode and selected value and redirect to indexpage'''
    query = request.GET.get('q')
    drop = request.GET.get('selected')
    print(drop)
    print(query)
    if query and drop:
        return redirect('indexpage',query=query,drop=drop,)
    else:
        return render(request,'home.html')