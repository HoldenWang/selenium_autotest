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
import pdb, ddt, base64, os

__author__="Holden.W"

reload(sys)
sys.setdefaultencoding("utf-8")


testData=[{u"低危告警",u"出网","tcp sync flood",u"运营商级流量基线"},\
          {u"中危告警",u"入网","tcp sync flood",u"运营商级流量基线"},\
          {u"高危告警",u"出网","tcp sync flood",u"运营商级流量基线"}]

@ddt.ddt
class DdosAutoTest(unittest.TestCase):
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True

    def elementshot_base64(self, how, what):
        # 获取元素截图并输出base64格式打印到测试报告中
        now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
        item=self.driver.find_element(by=how, value=what)
        path='..\\result\\image\\tmp'+now+'.png'
        #item.screenshot(path)
        self.driver.save_screenshot(path)
        left=int(item.location['x']+250)
        top=int(item.location['y']+50)
        right=int(left+item.size['width'])
        bottom=int(top+item.size['height'])
        from PIL import Image
        im=Image.open(path)
        im=im.crop((left,top,right,bottom))
        im.save(path)
        f=open(path,'rb')
        ls_f=base64.b64encode(f.read())
        f.close()
        print "CODEBEGIN"+ls_f+"CODEEND"


    @classmethod
    def setUpClass(self):
        print "start suites "

    @classmethod
    def tearDownClass(self):
        time.sleep(3)
        print "\nend suites "

    def setUp(self):
        #self.driver = webdriver.PhantomJS()
        self.driver = webdriver.Chrome()
        # 智能等待
        self.driver.implicitly_wait(30)
        # 删除所有的cookie
        self.driver.delete_all_cookies()
        self.driver.maximize_window()
        print "now we are testing with "+ str(self.driver).split('.')[2]
        self.base_url = "http://*i.com:19000/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_forbiden_string(self):
        """页面没有undefine和null元素"""
        driver = self.driver
        driver.get(self.base_url + "/ddos/view/main.html#")
        driver.maximize_window()
        driver.switch_to_frame(0)
        self.assertFalse(re.search('undefined',driver.page_source))
        self.assertFalse(re.search('null',driver.page_source))

    def test_button_back_and_user(self):
        """收缩按钮和用户按钮"""
        driver = self.driver
        driver.get(self.base_url + "/ddos/view/main.html#")
        #self.assertFalse(re.search(u"今日事件",driver.page_source))
        driver.find_element_by_css_selector("span.icon-bar").click()
        #self.assertTrue(re.search(u"今日事件",driver.page_source))
        driver.find_element_by_css_selector("span.icon-bar").click()
        # 点击用户名Linda
        driver.find_element_by_xpath("//li/a/span").click()

    def test_today_event(self):
        u"""今日事件统计"""
        driver = self.driver
        driver.get(self.base_url + "/ddos/view/main.html#")
        driver.switch_to_frame(0)
        #time.sleep(5)
        counts=driver.find_elements_by_xpath("//span[@class='number']")
        try:
            for count in counts:
                print count.text,
        except StaleElementReferenceException as e: self.verificationErrors.append(str(e))
        self.assertTrue(len(counts)==6)

    def test_top_target(self):
        """攻击目标top5"""
        driver = self.driver
        driver.get(self.base_url + "/ddos/view/main.html#")
        driver.switch_to_frame(0)
        flows=driver.find_elements_by_xpath("//section/div[1]/div[2]/div[2]/ul/li[*]/span[1]")
        for flow in flows:
            print flow.text
        self.assertTrue(len(flows)==5)

        ips=driver.find_elements_by_xpath("//section/div[1]/div[2]/div[2]/ul/li[*]/span[2]")
        for ip in ips:
            print ip.text
        self.assertTrue(len(ips)==5)

    def test_top_source(self):
        """攻击来源top5"""
        driver = self.driver
        driver.get(self.base_url + "/ddos/view/main.html#")
        driver.switch_to_frame(0)
        flows=driver.find_elements_by_xpath("//section/div[1]/div[2]/div[3]/ul/li[*]/span[1]")
        for flow in flows:
            print flow.text
        self.assertTrue(len(flows)==5)

        ips=driver.find_elements_by_xpath("//section/div[1]/div[2]/div[3]/ul/li[*]/span[2]")
        for ip in ips:
            print ip.text
        self.assertTrue(len(ips)==5)
        
    def test_visible_map_show(self):
        u"""实时攻击可视化地图"""
        now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
        driver = self.driver
        driver.get(self.base_url + "/ddos/view/main.html#")
        #driver.find_element_by_css_selector("span.icon-bar").click()
        driver.switch_to_frame(0)
        self.assertTrue(self.is_element_present(By.XPATH, "//div[@id='map']/div[1]/canvas[3]"))
        time.sleep(5)
        self.elementshot_base64(By.XPATH,"//div[@id='map']/div[1]/canvas[3]")
        # now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
        # pic_path='..\\result\\image\\'+now+'.png'
        # print pic_path
        # driver.save_screenshot(pic_path)
        # item=driver.find_element_by_xpath("//div[@id='map']/div[1]/canvas[3]")
        # left=int(item.location['x'])
        # top=int(item.location['y']+50)
        # right=int(left+item.size['width'])
        # bottom=int(top+item.size['height'])
        # from PIL import Image
        # im=Image.open(pic_path)

        # im=im.crop((left,top,right,bottom))
        # #im.save(pic_path)
        # im.save('map_%s.png' % now)

    def test_attack_type(self):
        u"""右上角攻击类型饼状图"""
        driver = self.driver
        driver.get(self.base_url + "/ddos/view/main.html#")
        driver.switch_to_frame(0)
        #print "now we are testing with"+ str(driver).split('.')[2]
        self.assertTrue(self.is_element_present(By.CSS_SELECTOR,"#attackType > div > canvas"))
        # 点击饼状图块，测试联调
        j=driver.find_element_by_css_selector("#attackType > div > canvas")
        # 225和50分别是主框架导致的偏移
        x_O=j.location['x']+225
        y_O=j.location['y']+50
        ActionChains(driver).move_by_offset(x_O+100,y_O+80).click().move_by_offset(0,20).click().move_by_offset(-20,0).click().perform()
        time.sleep(5)
        #now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
        # t=driver.get_screenshot_as_file('%s.jpg' % now)
        # print (u"截图结果：%s" %t)
        self.elementshot_base64(By.XPATH,"//*[@id='attackType']/div[1]")

        # pic_path='..\\result\\image\\'+now+'.png'
        # item=driver.find_element_by_xpath("//*[@id='attackType']/div[1]")
        # item.screenshot(pic_path)
        # left=int(item.location['x']+250)
        # top=int(item.location['y']+50)
        # right=int(left+item.size['width'])
        # bottom=int(top+item.size['height'])
        # from PIL import Image
        # im=Image.open(pic_path)
        # im=im.crop((left,top,right,bottom))
        # im.save(pic_path)
        # f=open(pic_path,'rb')
        # ls_f=base64.b64encode(f.read())
        # f.close()
        # print "CODEBEGIN"+ls_f+"CODEEND"
        """
        j.screenshot('attacktype_%s.png' % now) 
        #code=j.screenshot_as_base64()
        # 下面的截图方法可以将截图放到测试报告中，其他的都是存为附件
        code=driver.get_screenshot_as_base64()
        #code=j.screenshot_as_base64()
        print "CODEBEGIN"+code+"CODEEND"
        """

    
    def test_flow_distribution(self):
        u"""右上角流向分布饼状图"""
        driver = self.driver
        driver.get(self.base_url + "/ddos/view/main.html#")
        driver.switch_to_frame(0)
        self.assertTrue(self.is_element_present(By.CSS_SELECTOR,"#flowDistribution > div > canvas"))

    def test_recent_statistic(self):
        u"""右侧24小时攻击趋势图"""
        driver = self.driver
        driver.get(self.base_url + "/ddos/view/main.html#")
        driver.switch_to_frame(0)
        self.assertTrue(self.is_element_present(By.ID,"alarm_trend_chart"))

    def test_event_list(self):
        u"""攻击事件实时滚屏窗口"""
        driver = self.driver
        driver.get(self.base_url + "/ddos/view/main.html#")
        driver.switch_to_frame(0)
        self.assertTrue(self.is_element_present(By.CSS_SELECTOR,"div.opacity-bg"))
        # section 标签中显示内容不能大于5行
        events=driver.find_elements_by_xpath("//span[@class='td time']")
        count=0
        for event in events:
            tmp=event.text
            if tmp:
                print tmp
                count=count+1
        print count
        self.assertTrue(count<=5)
        # 要根据时间排序
        self.assertEqual(driver.find_element_by_xpath("//span[@class='th time']").get_attribute("class"),"sort_esc")

    def test_board_countchart_left(self):
        u"""当前告警看板-告警次数统计(按攻击类型)"""
        driver = self.driver
        driver.get(self.base_url + "/ddos/view/main.html#")
        driver.find_element_by_link_text(u"告警管理").click()
        driver.find_element_by_link_text(u"当前告警看板").click()
        driver.switch_to_frame(0)
        self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "canvas"))

    def test_board_countchart_right(self):
        u"""当前告警看板-告警次数统计(按告警级别)"""
        driver = self.driver
        driver.get(self.base_url + "/ddos/view/main.html#")
        driver.find_element_by_link_text(u"告警管理").click()
        driver.find_element_by_link_text(u"当前告警看板").click()
        driver.switch_to_frame(0)
        self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "#alarm_count_level_chart > div > canvas"))

    def test_board_currentchart_left(self):
        u"""当前告警看板-告警流量统计(按攻击类型)"""
        driver = self.driver
        driver.get(self.base_url + "/ddos/view/main.html#")
        driver.find_element_by_link_text(u"告警管理").click()
        driver.find_element_by_link_text(u"当前告警看板").click()
        driver.switch_to_frame(0)
        self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "#flow_type_chart > div > canvas"))

    def test_board_currentchart_right(self):
        u"""当前告警看板-告警流量统计(按攻击类型)"""
        driver = self.driver
        driver.get(self.base_url + "/ddos/view/main.html#")
        driver.find_element_by_link_text(u"告警管理").click()
        driver.find_element_by_link_text(u"当前告警看板").click()
        driver.switch_to_frame(0)
        self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "#flow_level_chart > div > canvas"))

    def test_board_event_list(self):
        u"""当前告警看板-告警详情列表"""
        driver = self.driver
        driver.get(self.base_url + "/ddos/view/main.html#")
        driver.find_element_by_link_text(u"告警管理").click()
        driver.find_element_by_link_text(u"当前告警看板").click()
        driver.switch_to_frame(0)
        # 使用键盘下拉
        j=driver.find_element_by_xpath("//*[@id='flow_level_chart']")
        action=ActionChains(driver).move_to_element(j)
        j.click()
        action.send_keys(Keys.PAGE_DOWN)
        action.perform()
        warn_ids= driver.find_elements_by_xpath("//*[@id='attack_table']/tbody/tr[*]/td[1]/span")
        for warn_id in warn_ids:
            print warn_id.text.decode('UTF-8').encode('GBK')
        print "default length:",
        print len(warn_ids)
        # 改变分页的每页条数
        PAGE_NUM=75
        Select(driver.find_element_by_xpath("//*[@id='attack_table_length']/label/select")).select_by_visible_text("75")
        time.sleep(3)
        j=driver.find_element_by_xpath("//*[@id='attack_table']/tbody/tr[1]/td[3]/span")
        action=ActionChains(driver).move_to_element(j)
        j.click()
        action.send_keys(Keys.PAGE_DOWN)
        action.perform()
        # 第三列
        elapseds= driver.find_elements_by_xpath("//*[@id='attack_table']/tbody/tr[*]/td[3]/span")
        for elapsed in elapseds:
            print elapsed.text
        self.assertTrue(len(elapseds)==75)
        # 点击详情
        driver.find_element_by_xpath("//table[@id='attack_table']/tbody/tr/td[9]/i").click()
        # 另一个层次的canvas

    def test_AlarmDetail(self):
        u"""告警详情界面-由其他页面(告警详情)进入"""
        driver = self.driver
        driver.get(self.base_url + "/ddos/view/main.html#")
        driver.find_element_by_link_text(u"告警管理").click()
        driver.find_element_by_link_text(u"当前告警看板").click()
        driver.switch_to_frame(0)
        driver.find_element_by_xpath("//table[@id='attack_table']/tbody/tr/td[9]/i").click()
        self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "canvas"))
        driver.find_element_by_id("btn_open_route").click()
        time.sleep(10)
        driver.find_element_by_css_selector("button.ui-dialog-close").click()
        time.sleep(10)

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

    def test_query_traverse(self):
        u"""告警查询-遍历"""
        driver = self.driver
        driver.get(self.base_url + "/ddos/view/main.html#")
        #driver.find_element_by_css_selector("li.treeview > a > span").click()
        driver.find_element_by_link_text(u"告警管理").click()
        driver.find_element_by_link_text(u"告警查询").click()
        driver.switch_to_frame(0)
        driver.find_element_by_xpath("//div[1]/form/div[1]/div[1]/ins").click()
        driver.find_element_by_xpath("//div[1]/form/div[1]/div[2]/ins").click()
        driver.find_element_by_xpath("//div[1]/form/div[1]/div[3]/ins").click()
        driver.find_element_by_xpath("//div[1]/form/div[1]/div[4]/ins").click()
        # 选择日期区间
        driver.find_element_by_xpath("//div[1]/form/div[1]/input[2]").click()
        driver.find_element_by_xpath("//div[2]/div[2]/div/div[2]/div/span[17]").click()
        driver.find_element_by_xpath("//div[1]/form/div[1]/input[4]").click()
        # driver.find_element_by_xpath("//div[1]/form/div[1]/input[4]").click()
        # #两次是模拟操作第一次取消上次的下拉框，第二次才能真正点中目标元素
        # driver.find_element_by_xpath("//div[3]/div[2]/div/div[2]/div/span[19]").click()
        # driver.find_element_by_xpath("//div[1]/form/div[1]/input[4]").click()
        # 选择下拉选项
        Select(driver.find_element_by_id("alarm_level")).select_by_visible_text(u"高危告警")
        Select(driver.find_element_by_id("attack_direction")).select_by_visible_text(u"入网")
        Select(driver.find_element_by_id("attack_type")).select_by_visible_text("HTTP")
        Select(driver.find_element_by_id("granularity")).select_by_visible_text(u"运营商级流量基线")
        
        # 拖动进度条元素
        # 持续时间
        end_button_t=driver.find_element_by_xpath("//div[1]/form/div[3]/div[1]/span/span[7]")
        action=ActionChains(driver).move_to_element(end_button_t)
        #action.context_click(flag).perform()#右键
        end_button_t.click()
        for i in range(11):
            action.send_keys(Keys.ARROW_RIGHT)
            #pdb.set_trace()
        action.perform()
        #time.sleep(10)
        # 若是把perform()放到循环体内，无法准确控制刻度，不知为何

        from_button_t=driver.find_element_by_xpath("//div[1]/form/div[3]/div[1]/span/span[6]")
        action=ActionChains(driver).move_to_element(from_button_t)
        driver.find_element_by_xpath("//div[1]/form/div[3]/div[2]/label").click()
        from_button_t.click()
        for i in range(6):
            action.send_keys(Keys.ARROW_RIGHT)
        action.perform()

        # 峰值速率
        end_button_v=driver.find_element_by_xpath("//div[1]/form/div[3]/div[2]/span/span[7]")
        action=ActionChains(driver).move_to_element(end_button_v)
        end_button_v.click()
        for i in range(300):
            action.send_keys(Keys.ARROW_RIGHT)
        action.perform()

        from_button_v=driver.find_element_by_xpath("//div[1]/form/div[3]/div[2]/span/span[6]")
        action=ActionChains(driver).move_to_element(from_button_v)
        from_button_v.click()
        for i in range(100):
            action.send_keys(Keys.ARROW_RIGHT)
        action.perform()

        #time.sleep(20)
        driver.find_element_by_id("btn_query").click()
        driver.find_element_by_id("btn_export").click()
        Select(driver.find_element_by_id("fileFormat")).select_by_visible_text("TXT")
        driver.find_element_by_xpath("(//input[@name='zipOrNot'])[1]").click()
        driver.find_element_by_css_selector("button.ui-dialog-autofocus").click()
        time.sleep(15)

    def test_ddos_home(self):
        u"""首页"""
        driver = self.driver
        driver.get(self.base_url + "/ddos/view/main.html#")
        # driver.find_element_by_link_text("DDOS").click()
        #driver.back()
        driver.maximize_window()
        driver.find_element_by_css_selector("span.icon-bar").click()
        driver.find_element_by_css_selector("span.icon-bar").click()
        # 点击用户名Linda
        driver.find_element_by_xpath("//li/a/span").click()
        # 显示中国地图
        # 切换frame
        driver.switch_to_frame(0)
        count_1= driver.find_element_by_css_selector("span.number").text
        time.sleep(4)
        count_2= driver.find_element_by_xpath("//span[2]/span[2]").text
        count_3= driver.find_element_by_xpath("//span[2]/span[3]").text
        count_4= driver.find_element_by_xpath("//span[4]").text
        # 为了在windows下展示中文方面了解测试进度，使用chcp 65001命令将控制台编码方式变为utf-8
        # 但python的print默认打印的是GBK，不识别utf-8,只得进行如下转换方便展示
        current_event_count= count_1.decode('UTF-8').encode('GBK')+count_2.decode('UTF-8').encode('GBK')+count_3.decode('UTF-8').encode('GBK')+count_4.decode('UTF-8').encode('GBK')
        print "Today Event:"+current_event_count
        time.sleep(3)
        target_content='null'
        # 使用xpath查看页面中是否含有指定字符
        try: 
            driver.find_element_by_xpath("//*[contains(.,'" + target_content + "')]")
            print target_content+'exit'
        except NoSuchElementException as e: self.verificationErrors.append(str(e))
        self.assertTrue(self.is_element_present(By.XPATH, "//div[@id='map']/div[1]/canvas[3]"))
        #print "value:"+ driver.find_element_by_xpath("//div[@id='map']/div[1]/canvas[3]").text
        #try: self.assertEqual("", driver.find_element_by_xpath("//div[@id='map']/div[1]/canvas[3]").text)
        #except AssertionError as e: self.verificationErrors.append(str(e))
        # 判断攻击类型饼状图
        try: self.assertEqual("", driver.find_element_by_css_selector("#attackType > div > canvas").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        except NoSuchElementException as e:
            self.verificationErrors.append(str(e))
            print 'cant find geography map',e
        # finally:
        #     print 'finished checking map displaying'
        # 判断饼状图控件canvas存在否
        try: self.assertEqual("", driver.find_element_by_css_selector("#flowDistribution > div > canvas").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        # 最近统计 趋势图
        try: self.assertEqual("", driver.find_element_by_id("alarm_trend_chart").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        # 告警事件表数据
        try: self.assertEqual("", driver.find_element_by_css_selector("li > div.opacity-bg").text)
        except AssertionError as e: 
            self.verificationErrors.append(str(e))
            print 'lack data！'
        except NoSuchElementException as e:
            self.verificationErrors.append(str(e))
            print 'cant locate element',e
        # finally:
        #     print 'finished checking data exiting'
        # top攻击目标 ip与归属
        self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "span.ip"))
        self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "li > span"))
        # top攻击来源 ip与归属
        self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "div.source-top > ul > li > span"))
        self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "div.source-top > ul > li > span.ip"))

    def test_ddos_alarm_trend(self):
        u"""告警管理-告警趋势分析"""
        driver = self.driver
        driver.get(self.base_url + "/ddos/view/main.html#")
        driver.maximize_window()
        driver.find_element_by_css_selector("li.treeview > a > span").click()
        driver.find_element_by_link_text(u"告警趋势分析").click()
        driver.switch_to_frame(0)
        driver.find_element_by_xpath("//div[1]/form/div[1]/div[1]/ins").click()
        driver.find_element_by_xpath("//div[1]/form/div[1]/div[2]/ins").click()
        driver.find_element_by_xpath("//div[1]/form/div[1]/div[3]/ins").click()
        driver.find_element_by_xpath("//div[1]/form/div[1]/div[4]/ins").click()
        # 设置开始时间
        driver.find_element_by_xpath("//div[1]/form/div[1]/input[2]").click()
        driver.find_element_by_xpath("//div[2]/div[2]/div/div[2]/div/span[16]").click()
        driver.find_element_by_xpath("//div[2]/div[3]/div[1]/input").send_keys("17")
        driver.find_element_by_xpath("//div[2]/div[3]/div[2]/input").send_keys("13")
        driver.find_element_by_xpath("//div[2]/div[3]/div[3]/input").send_keys("45")
        # 设置结束时间
        driver.find_element_by_xpath("//div[1]/form/div[1]/input[4]").click()
        driver.find_element_by_xpath("//div[1]/form/div[1]/input[4]").click()
        driver.find_element_by_xpath("//div[3]/div[2]/div/div[2]/div/span[19]").click()
        Select(driver.find_element_by_id("attack_granularity")).select_by_visible_text(u"路由器级流量基线")
        driver.find_element_by_css_selector("option[value=\"4\"]").click()
        Select(driver.find_element_by_id("router")).select_by_visible_text("192.169.128.70")
        driver.find_element_by_id("btn_query").click()
        try: self.assertEqual("",driver.find_element_by_css_selector("By.CSS_SELECTOR, \"canvas\"").text)
        except AssertionError as e: 
            self.verificationErrors.append(str(e))
        except InvalidSelectorException as e:
            self.verificationErrors.append(str(e))
            print "cant get chart",e
        #self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "canvas"))
        try: 
            self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "#flow_by_attack_level > div > canvas"))
        except AssertionError as e: 
            self.verificationErrors.append(str(e))
        #time.sleep(5)

    def test_ddos_current_alarm(self):
        u"""告警管理-当前告警看板"""
        driver = self.driver
        driver.get(self.base_url + "/ddos/view/main.html#")
        driver.maximize_window()
        driver.find_element_by_link_text(u"告警管理").click()
        driver.find_element_by_link_text(u"当前告警看板").click()
        driver.switch_to_frame(0)
        # 从左到右，从上到下匹配canvas画板存在否
        self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "canvas"))
        self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "#alarm_count_level_chart > div > canvas"))
        self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "#flow_type_chart > div > canvas"))
        #self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "#flow_level_chart > div > canvas"))
        # 匹配下方table的第一行第一列数据
        self.assertTrue(self.is_element_present(By.XPATH, "//*[@id='attack_table']/tbody/tr[1]/td[1]/span"))
        # 使用键盘下拉
        j=driver.find_element_by_xpath("//*[@id='flow_level_chart']")
        action=ActionChains(driver).move_to_element(j)
        j.click()
        action.send_keys(Keys.PAGE_DOWN)
        action.perform()
        # js="var q=document.documentElement.scrollTop=10000"
        # driver.execute_script(js)
        # 我们在iframe下，且iframe 的scrolling设置为yes，并不同于简单的只有body的html

        # 判断表中某一列元素合法性
        # 第一列
        warn_ids= driver.find_elements_by_xpath("//*[@id='attack_table']/tbody/tr[*]/td[1]/span")
        for warn_id in warn_ids:
            print warn_id.text.decode('UTF-8').encode('GBK')
        print "default length:"+len(warn_ids)

        # 改变分页的每页条数
        Select(driver.find_element_by_xpath("//*[@id='attack_table_length']/label/select")).select_by_visible_text("25")
        time.sleep(3)
        j=driver.find_element_by_xpath("//*[@id='attack_table']/tbody/tr[1]/td[3]/span")
        action=ActionChains(driver).move_to_element(j)
        j.click()
        action.send_keys(Keys.PAGE_DOWN)
        action.perform()

        # 第三列
        elapseds= driver.find_elements_by_xpath("//*[@id='attack_table']/tbody/tr[*]/td[3]/span")
        for elapsed in elapseds:
            print elapsed.text
        print len(elapseds)
        time.sleep(10)

        # 点击详情
        driver.find_element_by_xpath("//table[@id='attack_table']/tbody/tr/td[9]/i").click()
        # 另一个层次的canvas
        self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "canvas"))
        driver.find_element_by_id("btn_open_route").click()
        time.sleep(10)
        driver.find_element_by_css_selector("button.ui-dialog-close").click()
    
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
        # self.assertEqual([], self.verificationErrors)
