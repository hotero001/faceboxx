from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#from selenium.common.exceptions import TimeoutException
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC

# launch headless PhantomJS browser pointed at facebook
# https://stackoverflow.com/a/23872305

# creates a new PhantomJS process
driver = webdriver.PhantomJS()
email = "johaxworthless@gmail.com"
pword = "sbhacks15"

driver.get('https://www.facebook.com')
assert 'Facebook' in driver.title

#https://stackoverflow.com/questions/25569426/unable-to-login-to-quora-using-selenium-webdriver-in-python
form = driver.find_element_by_class_name("menu_login_container")
username = form.find_element_by_name("email")
username.send_keys(email)

password = form.find_element_by_name("pass")
password.send_keys(pword)
password.send_keys(Keys.RETURN)

driver.get('https://www.facebook.com/messages/' + '100009014106177')
f = open('messages.txt', 'w')
f.write(driver.page_source.encode('utf-8'))
f.close()
driver.save_screenshot('screenshot.jpg')