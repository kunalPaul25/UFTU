from selenium import webdriver
import time
from keyboard import press
from selenium.webdriver.support import ui
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import xlwt
from tempfile import TemporaryFile

#initialising Chrome Web Driver
driver = webdriver.Chrome("C:\WebDrivers\chromedriver.exe")
driver.get("https://instagram.com")

time.sleep(5)
userName = driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[2]/div/label/input')
userName.send_keys("feetoutside")

password = driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[3]/div/label/input')
password.send_keys("feetoutside@2019")

driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[4]').click()


ui.WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".aOOlW.HoLwm"))).click()
driver.find_element_by_xpath('//*[@id="react-root"]/section/main/section/div[3]/div[1]/div/div[2]/div[1]/a').click()

time.sleep(12)

def get_followers():
    driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a').click()
    time.sleep(5)
    scroll_box = driver.find_element_by_xpath('/html/body/div[4]/div/div[2]')
    last_ht, ht = 0, 1
    while last_ht != ht:
        last_ht = ht
        time.sleep(2)
        ht = driver.execute_script("""
        arguments[0].scrollTo(0, arguments[0].scrollHeight);
        return arguments[0].scrollHeight;
        """, scroll_box)
    links = scroll_box.find_elements_by_tag_name('a')
    global followers
    followers = [name.text for name in links if name.text != '']
    time.sleep(2)
    driver.find_element_by_xpath('/html/body/div[4]/div/div[1]/div/div[2]/button').click()
    return followers

def get_following():
    driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a').click()
    # sugs = driver.find_element_by_xpath()
    time.sleep(8)
    scroll_box = driver.find_element_by_xpath('//html/body/div[4]/div/div[2]')
    last_ht, ht = 0, 1
    while last_ht != ht:
        last_ht = ht
        time.sleep(3)
        ht = driver.execute_script("""
            arguments[0].scrollTo(0, arguments[0].scrollHeight);
            return arguments[0].scrollHeight;
            """, scroll_box)
    links = scroll_box.find_elements_by_tag_name('a')
    global following
    following = [name.text for name in links if name.text != '']
    return following
get_followers()
time.sleep(2)
get_following()
not_following_back = [user for user in following if user not in followers]
book = xlwt.Workbook()
sheet1 = book.add_sheet('sheet1')

for i,e in enumerate(not_following_back):
    sheet1.write(i,0,e)

name = "to_unfollow.xls"
book.save(name)
book.save(TemporaryFile())
from win10toast import ToastNotifier
toaster = ToastNotifier()
toaster.show_toast("Ready to Roll",
                   "Unfollow List is Ready",
                   duration=10)