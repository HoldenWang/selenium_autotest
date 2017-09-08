# selenium_autotest
使用selenium3+pyhon2.7进行ui自动化测试
提供完整环境安装包和指导文档方便直接部署测试环境

## 关于chromedriver版本
本项目中包含的是2.3版本的chromedriver，对于最新的稳定版chrome有效（60以下）
具体版本对应关系请自行百度

## 关于测试报告
本项目使用了修改了的HTMLTestRunner.py作为测试执行器（test runner)，使其能嵌入截图
在测试中打印截图的base64位编码，并打印在`CODEBEGIN` `CODEEND`中间，测试报告会打印除这部分编码的信息的其他测试中出现的提示信息并展示截图。
