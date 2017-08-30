# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.common.exceptions import NoAlertPresentException, InvalidSelectorException
#import unittest, time,sys, re, HTMLTestRunner
import sys, time, re, unittest
import pdb, ddt

reload(sys)
sys.setdefaultencoding("utf-8")


testData=[{"warn_level":u"低危告警","warn_io":u"出网","warn_type":"TCP","warn_base":u"运营商级流量基线"},\
          {"warn_level":u"中危告警","warn_io":u"入网","warn_type":"TCP Sync Flood","warn_base":u"出入网总流量基线"},\
          {"warn_level":"高危告警","warn_io":"出网","warn_type":"HTTP","warn_base":"出入网总流量基线"}]

@ddt.ddt
class DdosAutoTest(unittest.TestCase):
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True

    def setUp(self):
        self.driver = webdriver.Chrome()
        # 智能等待
        self.driver.implicitly_wait(30)
        # 删除所有的cookie
        #self.driver.delete_all_cookies()
        self.driver.maximize_window()
        self.base_url = "http://*:19000/"
        self.verificationErrors = []
        self.accept_next_alert = True

    @ddt.data(*testData)
    def test_DDT(self,data):
        u"""测试数据驱动ddt"""
        print data
        self.query_forddt(data["warn_level"],data["warn_io"],data["warn_type"],data["warn_base"])
        time.sleep(5)

    def query_forddt(self,warn_level,warn_io,warn_type,warn_base):
        u"""数据驱动"""
        driver = self.driver
        driver.get(self.base_url + "/ddos/view/main.html#")
        #driver.find_element_by_css_selector("li.treeview > a > span").click()
        driver.find_element_by_link_text(u"告警管理").click()
        driver.find_element_by_link_text(u"告警查询").click()
        driver.switch_to_frame(0)
        Select(driver.find_element_by_id("alarm_level")).select_by_visible_text(warn_level)
        Select(driver.find_element_by_id("attack_direction")).select_by_visible_text(warn_io)
        Select(driver.find_element_by_id("attack_type")).select_by_visible_text(warn_type)
        Select(driver.find_element_by_id("granularity")).select_by_visible_text(warn_base)
        driver.find_element_by_id("btn_query").click()

    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        #self.driver.close()
        self.driver.quit()

if __name__ =="__main__":
    # 全部执行当前测试项
    #unittest.main()
    # 定制执行某个类中的测试项
    # suite=unittest.TestSuite()
    # suite.addTest(DdosAutoTest("test_DDT(data)"))
    # runner=unittest.TextTestRunner()
    # runner.run(suite)
    # 载入多个类
    suite=unittest.TestLoader().loadTestsFromTestCase(DdosAutoTest)
    unittest.TextTestRunner(verbosity=2).run(suite)