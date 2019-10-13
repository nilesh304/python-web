#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  1 00:09:54 2018

@author: nilesh
"""
#from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords

#for opening and browsing through web
from selenium import webdriver

#time is required to stop pyhton process for required amount of time
import time

#importing for web scrapping
import requests
from bs4 import BeautifulSoup 


news=input("Enter News to be tested: ")
news=news.lower()



dictionary={'toi':0, 'reut':0, 'fake':2}

#set of all non-keywords
s=set(stopwords.words('english'))


#Create new file for TOI and Reuters
file_toi= open("toi.txt","w")
file_reu=open("reu.txt","w")


#opeing a new firefox browser
driver=webdriver.Firefox()


def newscount():
    
    count_news=0
    
#    vectorizer = CountVectorizer()
#    print( vectorizer.fit_transform(news).todense() )
#    print( vectorizer.vocabulary_ )
    
    #closing files
    closefiles()
    
    
    k= filter(lambda w: not w in s,news.split())
    
    
    #opening files for reading
    file_reu=open("reu.txt","r")
    file_toi= open("toi.txt","r")
    
#    print(k)
    for line in file_toi:
        line=line.lower()
        
        #removing all non-keywords
        filter_toi = (filter(lambda w: not w in s,line.split()))
        
        #print(filter_toi)
        
        for word in k:
            if word in filter_toi:
                count_news=count_news+1
        
        dictionary['toi']=count_news
        
    count_news=0
    
    for line in file_reu:
        
        line=line.lower()
        
        #removing all non-keywords
        filter_toi = (filter(lambda w: not w in s,line.split()))
        
#        print(filter_toi)
        
        for word in k:
            if word in filter_toi:
                count_news=count_news+1
        dictionary['reut']=count_news
    
                
#    print(count_news)
    
    #closing files
    closefiles()
    
    

def timesofIndia(news):
    
    quote_page = 'https://timesofindia.indiatimes.com/'
    
    #browsing to Times of India web site
    driver.get(quote_page)
    
    #waiting for Ad to get over
    time.sleep(10)
    
    #finding search Lens
    src_btn=driver.find_element_by_class_name("jSearchLens")
    src_btn.click()
    
    #entering news to be confirmed
    search=driver.find_element_by_id("query")
    search.send_keys(news)
    
    #submiting the news for search
    search_btn=driver.find_element_by_class_name("jSearchSubmit")
    search_btn.submit()
    
    time.sleep(10)
    
    driver.forward()
#    print(driver.current_url)
    toiNewsClick(driver.current_url)
    
    
    for i in range(1,6):
        driver.switch_to.window(driver.window_handles[i])
        try:
            toiscraper(driver.current_url)
        except:
            continue
    


def reuters(news):
    quote_page = 'https://in.reuters.com/'
    
    #browsing to Times of India web site
    driver.get(quote_page)
    
    #finding search Lens
    src_btn=driver.find_element_by_class_name("search-icon")
    src_btn.click()
    
    #entering news to be confirmed
    search=driver.find_element_by_id("searchfield")
    search.send_keys(news)
    
    #submiting the news for search
    search_btn=driver.find_element_by_class_name("search-submit-button")
    search_btn.submit()
    
    time.sleep(10)
    
    driver.forward()
    print(driver.current_url)
    reuNewsCLick(driver.current_url)

#function to go to different news link of TOI
def toiNewsClick(URL):

    driver.get(URL)
    time.sleep(10)
    
    li=driver.find_elements_by_class_name("title")
    for i in range(5):
        li[i].click()
        time.sleep(10)

#function to scrape site and save text in file
def toiscraper(URL):
	r = requests.get(URL) 
	soup = BeautifulSoup(r.content, 'html5lib') 
	table = soup.find('div', attrs = {'class':'Normal'})
	file_toi.write(table.text)
    
 #function to go to different news link of Reuters   
def reuNewsCLick(URL):
    driver.get(URL)
    time.sleep(10)
    
    for i in range(1,6):
        li=driver.find_elements_by_class_name("search-result-title")
#        print(li[i])
        li[i].click()
        driver.forward()
        reutersscraper(driver.current_url)
        driver.back()
        time.sleep(5)
        
#function to scrape site and save text in file
def reutersscraper(URL):
    r = requests.get(URL) 
    soup = BeautifulSoup(r.content, 'html5lib') 
    table = soup.find('div', attrs = {'class':'StandardArticleBody_body'})
#    print(table)
    text=(table.text).encode('ascii','ignore')
    file_reu.write(text)
    file_reu.write('\n')   
    
#news="The Kite Runner is the first novel by Afghan-American author Khaled Hosseini.[1] Published in 2003 by Riverhead Books, it tells the story of Amir, a young boy from the Wazir Akbar Khan district of Kabul, whose closest friend is Hassan. The story is set against a backdrop of tumultuous events, from the fall of Afghanistan's monarchy through the Soviet military intervention, the exodus of refugees to Pakistan and the United States, and the rise of the Taliban regime."


def scorer(dictionary):
	toi_flag=0
	reut_flag=0
	fake_flag=0
	prob_news=0
	score_news_toi=0
	score_news_reut=0
	score_news_fake=0
	for i in dictionary:
		if (i == 'toi'):
			score_news_toi=0.075*dictionary[i]
			if (dictionary[i]>15):
				toi_flag=1
		elif (i == 'reut'):
			score_news_reut=0.098*dictionary[i]
			if(dictionary[i]>10):
				reut_flag=1
		elif (i == 'fake'):
			score_news_fake=0.07*dictionary[i]
			if (dictionary[i]>5):
				fake_flag=1
	tot_news_score=score_news_reut+score_news_toi-score_news_fake
	if (reut_flag==0 and toi_flag==0 and fake_flag==0):
		prob_news=0.2
	if (reut_flag==0 and toi_flag==0 and fake_flag==1):
		prob_news=0
	if (reut_flag==0 and toi_flag==1 and fake_flag==0):
		prob_news=2.4
	if (reut_flag==0 and toi_flag==1 and fake_flag==1):
		prob_news=1.6
	if (reut_flag==1 and toi_flag==0 and fake_flag==0):
		prob_news=3
	if (reut_flag==1 and toi_flag==0 and fake_flag==1):
		prob_news=1.75
	if (reut_flag==1 and toi_flag==1 and fake_flag==0):
		prob_news=4
	if (reut_flag==1 and toi_flag==1 and fake_flag==1):
		prob_news=2.8
	if (prob_news==0.2):
		print("The news has just 5% accuracy or it may be a latest news")
	if (prob_news==0):
		print("The news is 100% fake")
	if (tot_news_score>2.5):
		print("The news is 98% correct")
	if (tot_news_score<0.3):
		print("The news is 99% fake")
	else:
		prob_news_per=(prob_news/4)*0.25+tot_news_score*0.75
		prob_news_per=(prob_news_per/2.2)*100
		print("The accuracy of the news is: ") 
		print("%.2f" % prob_news_per)
	return()



def closefiles():
    file_reu.close()
    file_toi.close()

# calling function to check on TOI
timesofIndia(news)


# calling function to check on REUTERS
reuters(news)

newscount()
scorer(dictionary)
#print(dictionary)

#closing browser
driver.quit()