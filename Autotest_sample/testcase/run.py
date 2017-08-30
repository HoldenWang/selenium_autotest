# -*- coding: utf-8 -*-
#!/usr/bin/env/ python

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import sys, os, unittest, time, re, HTMLTestRunner
from sample_webdriver import DdosAutoTest,testData

reload(sys)
sys.setdefaultencoding("utf-8")

if __name__ == "__main__":
    run_type="default"
    now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    # 仅支持载入全部类
    #unittest.main()
    # 构造测试集，不支持ddt
    suite=unittest.TestSuite()
    #suite.addTest(DdosAutoTest("test_ddos_home"))
    # suite.addTest(DdosAutoTest("test_ddos_alarm_trend"))
    # suite.addTest(DdosAutoTest("test_ddos_alarm_history"))
    # suite.addTest(DdosAutoTest("test_ddos_current_alarm"))
    # 细化测试用例
    # suite.addTest(DdosAutoTest("test_forbiden_string"))
    # suite.addTest(DdosAutoTest("test_button_back_and_user"))
    #suite.addTest(DdosAutoTest("test_today_event"))
    # suite.addTest(DdosAutoTest("test_top_target"))
    # suite.addTest(DdosAutoTest("test_top_source"))
    #suite.addTest(DdosAutoTest("test_visible_map_show"))
    #suite.addTest(DdosAutoTest("test_attack_type"))
    #suite.addTest(DdosAutoTest("test_flow_distribution"))
    # suite.addTest(DdosAutoTest("test_recent_statistic"))
    #suite.addTest(DdosAutoTest("test_event_list"))
    # suite.addTest(DdosAutoTest("test_board_countchart_left"))
    # suite.addTest(DdosAutoTest("test_board_countchart_right"))
    # suite.addTest(DdosAutoTest("test_board_currentchart_left"))
    # suite.addTest(DdosAutoTest("test_board_currentchart_right"))
    suite.addTest(DdosAutoTest("test_board_event_list"))
    # suite.addTest(DdosAutoTest("test_AlarmDetail"))
    #suite.addTest(DdosAutoTest("test_query_traverse"))
    #suite.addTest(DdosAutoTest("test_DDT"))
    # suite.addTest(DdosAutoTest(""))
    # suite.addTest(DdosAutoTest(""))
    # 实施测试
    HtmlFile="..\\result\\"+now+"result.html"
    print HtmlFile
    fp=file(HtmlFile,"wb")
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u"Ddos攻击溯源-测试报告", description=u"测试结果详情")
    #runner=unittest.TextTestRunner()
    runner.run(suite)
    fp.close()
    # 显示测试报告,要操作文件必须先关闭文件fp.close()
    browser=webdriver.Chrome()
    file_path='file:///' + os.path.abspath(HtmlFile)
    browser.get(file_path)
    browser.maximize_window()

    #最终建议使用方案，可载入多个类的测试项且支持ddt
    if run_type == "Loader":
        suite=unittest.TestLoader().loadTestsFromTestCase(DdosAutoTest)
        #suite=unittest.TestLoader().loadTestsFromTestCase(DdosAutoTest1)
        HtmlFile="..\\result\\"+now+"result.html"
        print HtmlFile
        fp=file(HtmlFile,"wb")
        runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u"Ddos攻击溯源-测试报告", description=u"测试结果详情")
        runner.run(suite)
        fp.close()
        # 显示测试报告,要操作文件必须先关闭文件fp.close()
        browser=webdriver.Chrome()
        file_path='file:///' + os.path.abspath(HtmlFile)
        browser.get(file_path)