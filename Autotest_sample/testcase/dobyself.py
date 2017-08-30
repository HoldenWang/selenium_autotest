# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

browser=webdriver.Firefox()
print str(browser).split('.')[2]
# print browser.title
# browser2=webdriver.Firefox()
# print str(browser2).split('.')[2]
# browser3=webdriver.PhantomJS()
# print str(browser3).split('.')[2]

browser.implicitly_wait(30)

base_url = "http://ci.haohanheifei.com:19000/"
browser.get("http://gitlab.haohandata.local/TopLevel/Department_HeFei/wikis/daily_record_wangxing_201708")
# c1={'token':'4a33f6f4523db2b3e3389373aaf4a2df'}
cookie1={u'domain': u'gitlab.haohandata.local', 
u'secure': False, 
u'value': u'W1s0ODldLCIkMmEkMTAkM0hkWS56blMwWjJ4M2E1Mk5CLzFSdSIsIjE1MDM4ODQ2ODkuMTcxMzAxIl0%3D--6cea94147eea569532d26dfdee01317c31dfad90', 
u'expiry': None, 
u'path': u'/', 
u'httpOnly': True, 
u'name': u'remember_user_token'}

cookie2={u'domain': u'gitlab.haohandata.local', 
u'secure': False, 
u'value': u'7b78ba48531ce3f7dddb12db97911183', 
u'expiry': None, 
u'path': u'/', 
u'httpOnly': True, 
u'name': u'_gitlab_session'}

browser.add_cookie(cookie1)
browser.add_cookie(cookie2)

time.sleep(3)
browser.refresh()
# #browser.maximize_window()
# print browser
# browser.find_element_by_css_selector("li.treeview > a > span").click()
# time.sleep(3)
# browser.find_element_by_link_text(u"告警查询").click()
# time.sleep(5)
# browser.switch_to_frame(0)
# #inputs=browser.find_element_by_css_selector('input[type=radio]')
# print "browser"
# input=browser.find_element_by_xpath("//div[1]/form/div[1]/div[2]/ins")
# # for input in inputs:
# #     input.click()
# #     time.sleep(2)
# input.click()
# #print len(inputs)
# time.sleep(2)
#browser.quit()
