from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from time import sleep
import time
import os
#import load
#import speech_to_text


def initialize():
    global driver
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    s = Service(r"C:\webdrivers\chromedriver.exe")
    driver = webdriver.Chrome(service=s,options=options)
    driver.get('https://www.tsinghuaelt.com/')
    driver.maximize_window()

def voice():
    #将音频转换为文字
    del driver.requests
    loading(driver.find_element(By.CSS_SELECTOR, 'div .time'))
    speech_to_text.speech_to_text()

def loading(a):
    #此处读取音频请求进度
    print('音频加载中')
    while True:
        try:
            a.text
        except:print('加载成功');time.sleep(2);break
    url = []
    for i in driver.requests:
        if 'mp3' in str(i):
            url = i
    load.main(url,r'C:\Users\killout\tsinghuaelt\venv\video.mp3')
    print('下载完毕')

def log_in():
    print('如果脚本在输入密码后暂停了，说明密码错误,请重新启动并正确输入密码')
    account = input('请输入账号')
    password = input("请输入密码")
    driver.find_element(By.CSS_SELECTOR,'#account').send_keys(f'{account}')#账号
    driver.find_element(By.CSS_SELECTOR,'#password').send_keys(f'{password}')#密码
    time.sleep(2)
    #以下为滑块处理
    while True:
        time.sleep(1)
        huakuai = driver.find_element(By.CSS_SELECTOR,'#nc_1_n1z')
        action = ActionChains(driver)
        action.click_and_hold(huakuai).perform()
        action.drag_and_drop_by_offset(huakuai,500,0).perform()
        try:
            driver.find_element(By.CSS_SELECTOR, '.login-btn.point').click()
            break
        except:
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, '.nc_wrapper').click()


def entry_answer():
    driver.implicitly_wait(5)
    driver.find_element(By.CSS_SELECTOR,'.guide').click()
    time.sleep(2)
    ActionChains(driver).reset_actions()
    ActionChains(driver).move_by_offset(1330,137).click().perform()
    driver.find_element(By.CSS_SELECTOR,'#root > app-index > div > app-student-course > div.course-main > div > div.course-list-main.clearfix > div:nth-child(1) > div.course-title').click()
    #这里我水平有限只能这么定位，直接复制了一长串定位用的，有能力的朋友可以改进一些
    time.sleep(2)
    for i in range(2):
        ActionChains(driver).send_keys(Keys.ENTER).perform()
    driver.find_element(By.CSS_SELECTOR,'#root > app-index > div > app-course-basic-student > div:nth-child(3) > app-study > div > div.courseContent > div > div:nth-child(1) > div.unitItemOr.unitItem > div:nth-child(2) > div.goalTitle > span > strong').click()


def Click(element):  
    # js注入单击
    sleep(0.005)
    driver.execute_script("arguments[0].click();", element)
    sleep(0.005)

def PageNext():
    # 下一页
    sleep(2.5)
    Click(driver.find_elements(By.CSS_SELECTOR, ".page-next")[1])
    sleep(2.5)

def Re():  
    # 重写或提交
    sleep(2)
    Click(driver.find_element(By.CSS_SELECTOR, ".wy-course-bottom .wy-course-btn-right .wy-btn"))
    sleep(2)

def FillBlank():
    # 填空题
    blanks = driver.find_elements(By.CSS_SELECTOR, ".lib-fill-blank-do-input-left")
    for blank in blanks:
        blank.send_keys("a")
    Re()
    keys = []
    for key in driver.find_elements(By.CSS_SELECTOR, '.lib-edit-score span[data-type="1"]'):
        keys.append(key.text)
    Re()
    blanks = driver.find_elements(By.CSS_SELECTOR, ".lib-fill-blank-do-input-left")  # retry后再获取一次blanks
    if keys[0] == "Answers will vary.":  # 开放性答案
        for blank in blanks:
            blank.send_keys("Answers will vary.")
    else:
        for blank, key in zip(blanks, keys):
            blank.send_keys(key)
    Re()

def MutiChoice():
    # 多选题
    choices = driver.find_elements(By.CSS_SELECTOR, '.lib-single-item-img img[src="assets/exercise/no-choices.png"]')
    for choice in choices:
        Click(choice)
    Re()
    keys = []
    keyName = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']  # 选项名对应索引
    for key in driver.find_elements(By.CSS_SELECTOR, ".lib-single-cs-answer>span"):
        keys.append(keyName.index(key.text))  # 索引存入keys
    Re()
    choices = driver.find_elements(By.CSS_SELECTOR, '.lib-single-item-img img[src="assets/exercise/no-choices.png"]')
    for i in keys:
        Click(choices[i])
    Re()

def SingleChoice():
    # 单选题
    choices = driver.find_elements(By.CSS_SELECTOR, ".lib-single-item-order")
    for choice in choices:
        Click(choice)
    Re()
    keys = []
    for key in driver.find_elements(By.CSS_SELECTOR, ".lib-single-cs-answer"):  # 如keys=["A","B"]
        keys.append(key.text)
    choiceOfOne = len(choices) / len(keys)  # 每一题的选项数
    Re()
    choices = driver.find_elements(By.CSS_SELECTOR, ".lib-single-item-order")  # 再找一遍选项
    for key, i in zip(keys, range(len(keys))):
        for choice in choices[int(i * choiceOfOne):]:  # 每做一题从此题的第一个选项开始寻找
            if choice.text == key + '.':  # 如 "A." == "A"+"."
                Click(choice)
                break
            else:
                continue
    Re()


def Judge():  
    # 判断题
    # 支持 'T' 'F' 'NI' 三个选项的题
    choices = driver.find_elements(By.CSS_SELECTOR, ".lib-judge-radio")
    for choice in choices:
        Click(choice)
    Re()
    keys = []
    for key in driver.find_elements(By.CSS_SELECTOR, ".lib-judge-info-text"):  # 如keys=["T","F"]
        keys.append(key.text)
    choiceOfOne = len(choices) / len(keys)  # 每一题的选项数
    Re()
    choices = driver.find_elements(By.CSS_SELECTOR, ".lib-judge-radio")
    for key, i in zip(keys, range(len(keys))):
        if key == 'T':
            Click(choices[int(i * choiceOfOne):][0])
        elif key == 'F':
            Click(choices[int(i * choiceOfOne):][1])
        elif key == 'NI':
            Click(choices[int(i * choiceOfOne):][2])
    Re()


def Drop():
    # 下拉选择题
    choices = driver.find_elements(By.CSS_SELECTOR, ".ant-select-dropdown-menu-item")
    for choice in choices:
        Click(choice)
    Re()
    keys = []
    for key in driver.find_elements(By.CSS_SELECTOR, ".wy-lib-cs-key + span"):
        keys.append(key.text)
    choiceOfOne = len(choices) / len(keys)  # 每一题的选项数
    Re()
    choices = driver.find_elements(By.CSS_SELECTOR, ".ant-select-dropdown-menu-item")
    for key, i in zip(keys, range(len(keys))):
        for choice in choices[int(i * choiceOfOne):]:
            if choice.get_attribute("innerText").strip() == key:
                Click(choice)
                break
            else:
                continue
    Re()


def procedure():
    input("按任意键继续进行题目作答。")
    while True:
        if driver.find_elements(By.CSS_SELECTOR, ".wy-course-bottom .wy-course-btn-right .wy-btn") == []:
            PageNext()  # 找不到提交按钮，为单元标题页
        elif driver.find_elements(By.CSS_SELECTOR, ".lib-oral-container-top") != []:
            PageNext()  # 有录音题直接跳过
        else:
            Re()
            if driver.find_elements(By.CSS_SELECTOR, ".lib-fill-blank-do-input-left") != []:
                FillBlank()  # 填空题
            elif driver.find_elements(By.CSS_SELECTOR, '.lib-single-item-img img[src="assets/exercise/no-choices.png"]') != []:
                MutiChoice()  # 多选题
            elif driver.find_elements(By.CSS_SELECTOR, ".lib-single-item-order") != []:
                SingleChoice()  # 单选题
            elif driver.find_elements(By.CSS_SELECTOR, ".lib-judge-radio") != []:
                Judge()  # 判断题
            elif driver.find_elements(By.CSS_SELECTOR, ".ant-select-dropdown-menu-item") != []:
                Drop()  # 下拉选择题

            else:
                PageNext()
            # sleep(120)
            PageNext()

if __name__ == "__main__" :
    initialize()
    driver.find_element(By.CSS_SELECTOR, '.login.ng-star-inserted').click()
    while True:
        try:log_in();break
        except:print('密码错误');continue
    entry_answer()
#以下部分为录音题，进入答题界面后
    procedure()
    input('任意键')
