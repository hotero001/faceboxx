from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import time
import os
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def fbupload(files, email, pword):
	# launch headless PhantomJS browser pointed at facebook
	# https://stackoverflow.com/a/23872305

	# creates a new Firefox process
	#driver = webdriver.PhantomJS()
	driver = webdriver.Firefox()
	
	driver.get('https://www.facebook.com')
	assert 'Facebook' in driver.title

	#https://stackoverflow.com/questions/25569426/unable-to-login-to-quora-using-selenium-webdriver-in-python
	form = driver.find_element_by_class_name("menu_login_container")
	username = form.find_element_by_name("email")
	username.send_keys(email)

	password = form.find_element_by_name("pass")
	password.send_keys(pword)
	password.send_keys(Keys.RETURN)
	time.sleep(2)

        # Open a Facebook 404 page to grab the username because it loads faster
        # than the newsfeed
        driver.get('https://www.facebook.com/aksdjsandkjasndjknandjsakndkjsads/')
        assert 'Page Not Found' in driver.title

        # get user ID from profile button
        ID = (driver.find_element_by_class_name('_2dpe').get_attribute('href')
                .split('/')[-1])

	driver.get('https://www.facebook.com/messages/' + ID)
	time.sleep(2)
	assert 'Messages' in driver.title
	time.sleep(2)
	#driver.save_screenshot('screenshot.jpg')

	#tag = 'a._59hn'
	#btns = driver.find_elements_by_css_selector(tag)
	#links=open('links.txt','w')
	#for btn in btns:
	#        links.write(btn.get_attribute('href')+'\n')
	#links.close()
	
	for fileDir in files:
		print 'sending file dir ' + os.path.join(os.getcwd(),
			fileDir.split(os.path.sep)[-2], fileDir.split(os.path.sep)[-1])
		input = driver.find_element_by_class_name("_3jk")
		attach = input.find_element_by_name("attachment[]")
		time.sleep(2)
		attach.send_keys(os.path.join(os.getcwd(),
			fileDir.split(os.path.sep)[-2], fileDir.split(os.path.sep)[-1]))
		time.sleep(2)
		message = driver.find_element_by_class_name("_1rt")
		m = message.find_element_by_name("message_body")
		m.send_keys(Keys.ENTER)
		time.sleep(3)
	return driver
        
def fbdownload(fileName, email, pword, driver=None):
	# launch headless PhantomJS browser pointed at facebook
	# https://stackoverflow.com/a/23872305

	if not driver:
	    # creates a new PhantomJS process
	    driver = webdriver.PhantomJS()
	    #driver = webdriver.Firefox()
		
	    driver.get('https://www.facebook.com')
	    assert 'Facebook' in driver.title

	    #https://stackoverflow.com/questions/25569426/unable-to-login-to-quora-using-selenium-webdriver-in-python
	    form = driver.find_element_by_class_name("menu_login_container")
	    username = form.find_element_by_name("email")
	    username.send_keys(email)

	    password = form.find_element_by_name("pass")
	    password.send_keys(pword)
	    password.send_keys(Keys.RETURN)

	    assert 'Facebook' in driver.title

            # Open a Facebook 404 page to grab the username because it loads faster
            # than the newsfeed
            driver.get('https://www.facebook.com/aksdjsandkjasndjknandjsakndkjsads/')
            assert 'Page Not Found' in driver.title

            # get user ID from profile button
            ID = (driver.find_element_by_class_name('_2dpe').get_attribute('href')
                    .split('/')[-1])
	    driver.get('https://www.facebook.com/messages/' + ID)
		
	assert 'Messages' in driver.title

	tag = 'a._59hn'
	btns = driver.find_elements_by_css_selector(tag)
	urls = []
	
	time.sleep(2)
	
	# Append all result URLs to results
	for btn in btns:
		urls.append(btn.get_attribute('href'))

	print 'scraped', str(len(urls)), 'urls'
	#print urls[0]
	print 'pursuing matches for ', fileName

	# If URL matches filename, keep it in results
	results = filter(lambda match: fileName in match, urls)

	#print results[0]
	print 'scraped', str(len(results)), 'urls for', fileName
	
        f = open('links.txt', 'a')
        for link in results:
            f.write(link)
            f.write('\n')
        f.close()
	return sorted(results,
			key=lambda numerical: re.search(r'\/([^?/]+)\?oh=', numerical).group(1))
