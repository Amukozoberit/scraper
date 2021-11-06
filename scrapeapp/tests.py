from django.test import TestCase
from selenium import webdriver
# Create your tests here.



class seleniumTestCase(TestCase):
    def setUp(self):
        self.driver=webdriver.Chrome(executable_path='/home/mwashe/Downloads/chromedriver_linux64/chromedriver')
    

    