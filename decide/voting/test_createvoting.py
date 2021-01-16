from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from base.tests import BaseTestCase

class TestCreatevoting(StaticLiveServerTestCase):
  def setUp(self):
    #Load base test functionality for decide
    self.base = BaseTestCase()
    self.base.setUp()

    options = webdriver.ChromeOptions()
    options.headless = True
    self.driver = webdriver.Chrome(options=options)

    super().setUp()
  
  def tearDown(self):
    super().tearDown()
    self.driver.quit()

    self.base.tearDown()
  
  def test_createvoting(self):
    self.driver.get(f'{self.live_server_url}/admin/')
    self.driver.find_element_by_id('id_username').send_keys("admin")
    self.driver.find_element_by_id('id_password').send_keys("qwerty",Keys.ENTER)
    self.driver.find_element(By.XPATH, "//form[@id=\'login-form\']/div[3]/input").click()
    self.driver.find_element(By.XPATH, "//a[contains(@href, \'/admin/voting/voting/\')]").click()
    self.driver.find_element(By.XPATH, "//a[contains(text(),'Add voting')]").click()
    self.driver.find_element(By.XPATH, "//input[@id='id_name']").click()
    self.driver.find_element(By.XPATH, "//input[@id='id_name']").send_keys("Voting prueba selenium")
    self.driver.find_element(By.XPATH, "//textarea[@id='id_desc']").click()
    self.driver.find_element(By.XPATH, "//textarea[@id='id_desc']").send_keys("Voting prueba selenium description")
    self.driver.find_element(By.XPATH, "//select[@id='id_question']").click()
    dropdown = self.driver.find_element(By.ID, "id_question")
    dropdown.find_element(By.XPATH, "//option[. = 'elige uno']").click()
    self.driver.find_element(By.XPATH, "//select[@id='id_question']").click()
    self.driver.find_element(By.XPATH, "//select[@id='id_tipo']").click()
    dropdown = self.driver.find_element(By.ID, "id_tipo")
    dropdown.find_element(By.XPATH, "//option[. = 'IMPERIALI']").click()
    self.driver.find_element(By.XPATH, "//select[@id='id_tipo']").click()
    self.driver.find_element(By.XPATH, "//input[@id='id_numEscanos']").click()
    self.driver.find_element(By.XPATH, "//input[@id='id_numEscanos']").send_keys("10")
    dropdown = self.driver.find_element(By.XPATH, "//select[@id='id_auths']")
    dropdown.find_element(By.XPATH, "//option[. = "+f'{self.live_server_url}'+"]").click()
    self.driver.find_element(By.XPATH, "//input[@name='_save']").click()
    self.driver.find_element(By.XPATH, "(//a[contains(text(),'Voting prueba selenium')])[2]").click()
    value = self.driver.find_element(By.XPATH, "//select[@id='id_tipo']").get_attribute("value")
    assert value == "IMPERIALI"
    value = self.driver.find_element(By.XPATH, "//input[@id='id_numEscanos']").get_attribute("value")
    assert value == "10"