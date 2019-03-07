from selenium import webdriver
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
# chromedriver
# 下面是chromedrive的绝对路径
chromepath = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
#微博的账号密码，如果爬取数量较大，可以适当的增多
myWeiBo = [
    {'account':'15673291724','password':'gjci4f2j0s'}
]


'''
登陆账号获取cookies
使用selenium，先调用chrome浏览器
最后改成PhantomJS
'''
def getCookies(weibo):
    url = 'https://passport.weibo.cn/signin/login'
    print("Start crawl cookies!!!!")
    cookies = []
    for ele in weibo:
        account = ele['account']
        password = ele['password']
        try:
            options = webdriver.ChromeOptions()
            options.add_experimental_option("excludeSwitches", ["--ignore-certificate-errors"])
            driver = webdriver.Chrome(executable_path=chromepath,chrome_options=options)
            driver.get(url=url)
            driver.wait = WebDriverWait(driver, 20)
            time.sleep(2)
#通过多次输入账号密码来获取多个cookie值
            failure = 0
            while "登录 - 新浪微博" in driver.title and failure < 5:
                failure+=1
                # #loginName
                username = driver.find_element_by_id("loginName")
                username.clear()
                username.send_keys(account)
                # loginPassword
                psd = driver.find_element_by_id("loginPassword")
                psd.clear()
                psd.send_keys(password)

                commit = driver.find_element_by_id('loginAction')
                commit.click()
                def get_geetest_button():
                    button = driver.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_radar_tip')))
                    return button
# 下面是针对出现的点击验证
                button = get_geetest_button() #寻找点击验证按钮
                button.click()
                time.sleep(10) #等待10s，足够我们处理选字的验证码
                cookie = {}
                if "微博" in driver.title:
                    for elem in driver.get_cookies():
                        cookie[elem['name']] = elem['value']
                        if len(cookie) > 0:
                            cookies.append(cookie)
                            print("Get Cookie Successful: %s!!!!!!" % account)
        except Exception as e:
            print("%s Failure!!!!!" % account)
            print(e)
            pass
        finally:
            try:
                driver.quit()
            except Exception as e:
                pass
    return cookies



cookies = getCookies(myWeiBo)
