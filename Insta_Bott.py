from selenium import webdriver
from time import sleep
from secrets import pw  # Document that contains your password
from selenium.webdriver.common.keys import Keys
import pandas as pd

user_name = ""  # Your username


class InstaBot:
    def __init__(self, username, password):
        self.username = username
        self.driver = webdriver.Chrome("")  # PATH TO WEBDRIVER check README
        self._estate = '1'
        self.driver.get("https://www.instagram.com/")
        sleep(2)
        self.driver.find_element_by_xpath("//input[@name=\"username\"]")\
            .send_keys(username)
        self.driver.find_element_by_xpath("//input[@name=\"password\"]")\
            .send_keys(password)
        self.driver.find_element_by_xpath("//button[@type=\"submit\"]")\
            .click()
        sleep(5)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Agora não')]")\
            .click()
        sleep(1)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Agora não')]") \
            .click()

    @property
    def estate(self):
        return self._estate
    
    @estate.setter
    def estate(self, new_estate):
        self._estate = new_estate

    def get_unfollowers(self):
        self.driver.find_element_by_xpath(f"//a[contains(@href,'/{self.username}')]").click()
        sleep(1)
        self.driver.find_element_by_xpath(f"//a[contains(@href,'/{self.username}/following/')]")\
            .click()
        sleep(1)
        following = self.get_names()
        self._estate = '2'
        sleep(5)
        self.driver.find_element_by_xpath(f"//a[contains(@href,'/{self.username}/followers/')]") \
            .click()
        sleep(1)
        followers = self.get_names()
        not_following_back = [user for user in following if user not in followers]
        data = not_following_back
        index = [1 + int(i) for i in range(len(data))]
        columns = ['Usuário']
        df = pd.DataFrame(data=data, index=index, columns=columns)
        df.to_csv('df.csv', sep=';')

    def get_names(self):
        local = self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]/ul/div')
        local.click() 
        if self._estate == '1':
            n = 150  # N for following
        else:  # Tip, 150 is a good reference for 500 following users, calculate 'n' by considering //
               # the amount of following/followers you got on your account
            n = 90  # N for followed         
        for i in range(n):
            sleep(0.5)
            local.click()
            html = self.driver.find_element_by_tag_name('html')
            html.send_keys(Keys.PAGE_DOWN)
            print(i) 
        links = local.find_elements_by_tag_name('a')
        names = [name.text for name in links if name != '']
        self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div/div[2]/button').click()
        return names


bot = InstaBot(user_name, pw)
bot.get_unfollowers()
bot.driver.close()
