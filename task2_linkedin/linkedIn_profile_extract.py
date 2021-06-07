import os, random,sys,time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv
import json
import time
from user_pwd import lpassword,lusername
def get_education(browser,education_tag,education):
    edu=[]
    list_ins=education_tag.find_all('li')
    
    for i in list_ins:
        temp=[]
        name_tag=i.find('div',{'class':'pv-entity__degree-info'})
        temp.append(name_tag.find('h3',{'class':'pv-entity__school-name t-16 t-black t-bold'}).text)
        temp.append(name_tag.find('span',{'class':'pv-entity__comma-item'}).text)
        edu.append(temp[:])
    education.append(edu)
def get_experience(browser,experience_tag,experience):
    exp=[]
    list_ins=experience_tag.find_all('li')
    for i in list_ins:
        temp=[]
        try:
            company=i.find('div',{'class':'pv-entity__company-summary-info'})

            if company is None:
                company=i.find('div',{'class':'pv-entity__summary-info pv-entity__summary-info--background-section mb2'})
                temp.append(company.find('p',{'class':'pv-entity__secondary-title t-14 t-black t-normal'}).text.replace('\n',''))
                exp.append(temp)
            else:
                temp.append(company.find('h3',{'class':'t-16 t-black t-bold'}).text.replace('\n',''))
                exp.append(temp)
            
        except:
            pass
                    
    experience.append(exp)
def get_contacts(browser,link):
    contacts_list=[]
    browser.get(link)
    time.sleep(3)
    browser.execute_script('window.scrollTo(0,2400)')
    time.sleep(2)
    next_button=browser.find_element_by_xpath("//button[@aria-label='Next']")
    print(next_button)
    while next_button.is_enabled():
        src=browser.execute_script('return document.documentElement.outerHTML')
        soup=BeautifulSoup(src,'lxml')
        ul_tag=soup.find('ul',{'class':'reusable-search__entity-results-list list-style-none'})
        for li in ul_tag.find_all('li'):
            link_co=li.find('a',{'class':'app-aware-link'})['href']
            contacts_list.append(link_co)
        browser.execute_script("arguments[0].click();", next_button)
        time.sleep(5)
        browser.execute_script('window.scrollTo(0,2400)')
        time.sleep(2)
        next_button=browser.find_element_by_xpath("//button[@aria-label='Next']")
        #next_button.click()
    return contacts_list



    
def extract(education,experience,bio_list,contact_list):
    chrome_driver_path = "C:/Users/DANIEL/Desktop/chromedriver.exe"
    browser = webdriver.Chrome(chrome_driver_path)
    # browser = webdriver.Chrome('C:/Users/DANIEL/Desktop/chromedriver.exe')

    browser.get('https://www.linkedin.com/uas/login')

    # file = open('urls.txt')
    # lines = file.readlines()
    username = lusername      #lines[0]
    password = lpassword  #lines[1]+'\n'
    # '\n' should be added for password, if we dont give \n chrome driver throw error.
    

    elementID = browser.find_element_by_id('username')
    elementID.send_keys(username)
    elementID = browser.find_element_by_id('password')
    elementID.send_keys(password)
    elementID.submit()

    file2=open('C://Users/DANIEL/Desktop/freelancing/tasks/task2_linkedin/links.txt')
    lines2=file2.readlines()
    data=[]
    temp=[]
    for i in range(len(lines2)):
        if lines2[i]!='\n':
            temp.append(lines2[i])
    lines2=temp
    for link in lines2:
    
        browser.get(link)
        #experience
        browser.execute_script("window.scrollTo(0,600);")
        time.sleep(3)
        src = browser.execute_script('return document.documentElement.outerHTML')
        soup = BeautifulSoup(src, 'lxml')
        experience_tag=soup.find('div',{'class':'pv-profile-section-pager ember-view'})
        get_experience(browser,experience_tag,experience)

        #education
        browser.execute_script("window.scrollTo(600,2400);")
        education_tag=soup.find('section',{'id':"education-section"})
        get_education(browser,education_tag,education)
        
        browser.execute_script("window.scrollTo(2400,0)")
        time.sleep(3)
        bio_tag=soup.find('div',{'class':'flex-1 mr5'})
        name=bio_tag.find('li',{'class':'inline t-24 t-black t-normal break-words'}).text.replace('\n','')
        professional_tag=bio_tag.find('h2',{'class':'mt1 t-18 t-black t-normal break-words'})
        if professional_tag==None:
            professional_tagline=None
        else:
            professional_tagline=professional_tag.text.replace('\n','')
        location_tag=bio_tag.find('li',{'class':'t-16 t-black t-normal inline-block'})
        if location_tag is None:
            location=None
        else:
            location=location_tag.text.replace('\n','')
        connection_tag=bio_tag.find('span',{'class':'t-16 t-black t-normal'})
        if connection_tag is None:
            connections=None
            connections=bio_tag.find('span',{'class':'t-16 t-bold link-without-visited-state'}).text
        else:
            connections=connection_tag.text.replace('\n','')
        bio_temp_list=[]
        bio_temp_list.append(name)
        bio_temp_list.append(professional_tagline)
        bio_temp_list.append(location)
        bio_temp_list.append(connections)
        bio_list.append(bio_temp_list)

        #contacts
        contact_web_link=soup.find('a',{'data-control-name':'topcard_view_all_connections'})
        if contact_web_link is None:
            contact_list.append()
        else:
            link=contact_web_link['href']
            contact_list.append(get_contacts(browser,'https://www.linkedin.com'+link))
        




if __name__=='__main__':
    education=[]
    experience=[]
    bio_list=[]
    contact_list=[]
    extract(education,experience,bio_list,contact_list)
    print(education)
    print(experience)
    print(bio_list)
    print(contact_list)
    data=[]
    connection_data=[]
    for i in range(len(bio_list)):
        temp_dic={}
        temp_dic['name']=bio_list[i][0]
        temp_dic['tagline']=bio_list[i][1]
        temp_dic['location']=bio_list[i][2]
        temp_dic['connections']=bio_list[i][3]
        temp_dic['education']=education[i]
        temp_dic['experience']=experience[i]

        data.append(temp_dic)
        connection_temp={bio_list[i][0]:contact_list[i]}
        connection_data.append(connection_temp)
    with open('result.json','w') as f:
        for i in data:
            json.dump(i,f,indent=2)
    with open('contacts.json','w') as contacts:
        for i in connection_data:
            json.dump(i,contacts,indent=2)
    





    