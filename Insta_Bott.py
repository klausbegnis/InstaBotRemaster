from selenium import webdriver
from time import sleep
from secrets import pw  # Document that contains your password
from selenium.webdriver.common.keys import Keys
import pandas as pd

user_name = ""  # Your username


class InstaBot:
    def __init__(self, username, password, followers, following):
        self.username = username
        self.followers = followers
        self.following = following
        self.driver = webdriver.Chrome("C:\wedriver\chromedriver")  # PATH TO WEBDRIVER check README
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
        df = pd.Series(data=data)
        df.to_csv('df.csv', sep=';')

    def get_names(self):
        local = self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]/ul/div')
        local.click() 
        if self._estate == '1':
            n = self.following  # N for following
        else:  
            n = self.followers  # N for followed        
        links = []
        while len(links) <= (n):
            sleep(0.5)
            local.click()
            html = self.driver.find_element_by_tag_name('html')
            html.send_keys(Keys.PAGE_DOWN)
            links = local.find_elements_by_tag_name('a')
        names = [name.text for name in links if name != '']
        self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div/div[2]/button').click()
        return names


    def unfollowing(self):  # Only call if a csv file exists
        data_u = pd.read_csv('df01.csv', sep=';')
        stay = []  # List of people u want to still follow
        for i in range(len(stay)):
            rmv = stay[i]
            data_u = data_u.drop(rmv)
        data_u = data_u.values.tolist()
        #for i in range(n): # In case the scripts stops by not finding an xpath
        #  del(data_u[0]) the n value is the amount of people you have already unfollowed in the loop
        # might not be necessaire, but sometimes it glitches
        for i in range(len(data_u)):
            name_u = str(data_u[i])
            index = name_u.find('\'')
            name_u = name_u[index + 1:]
            index = name_u.find('\'')
            name_u = name_u[:index]
            sleep(3)
            self.driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input').send_keys(name_u)
            sleep(1)
            self.driver.find_element_by_xpath(f"//a[contains(@href,'/{name_u}/')]").click()
            sleep(1.5)
            self.driver.find_element_by_class_name('_5f5mN').click()
            self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[1]').click()



bot = InstaBot(user_name, pw)
#bot.get_unfollowers()
#bot.unfollowing()
#bot.driver.close()