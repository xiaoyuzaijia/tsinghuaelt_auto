from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# 测试账号 s20210678

options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')    # 去掉webdriver痕迹
options.add_experimental_option(
    'excludeSwitches', ['enable-logging'])    #不打印日志
s = Service(r"C:\webdrivers\chromedriver.exe")
wd = webdriver.Chrome(service=s, options=options)
wd.get("https://www.tsinghuaelt.com/")
wd.implicitly_wait(5) #隐式等待5s



def Click(element) :#单击
    sleep(0.005) 
    wd.execute_script("arguments[0].click();",element)
    sleep(0.005)

def PageNext() :#下一页
    sleep(2.5)
    Click(wd.find_elements(By.CSS_SELECTOR, ".page-next")[1])
    sleep(2.5)

def Re() :#重写或提交
    sleep(2)
    Click(wd.find_element(By.CSS_SELECTOR, ".wy-course-bottom .wy-course-btn-right .wy-btn"))
    sleep(2)




#填空题
def FillBlank() :
    blanks = wd.find_elements(By.CSS_SELECTOR, ".lib-fill-blank-do-input-left")
    for blank in blanks :
        blank.send_keys("a")
    Re()
    keys = []
    for key in wd.find_elements(By.CSS_SELECTOR, '.lib-edit-score span[data-type="1"]') :
        
        keys.append(key.text)
    Re()
    blanks = wd.find_elements(By.CSS_SELECTOR, ".lib-fill-blank-do-input-left")#retry后再获取一次blanks
    if keys[0] == "Answers will vary." : #开放性答案
        for blank in blanks :
            blank.send_keys("Answers will vary.")
    else :
        for blank,key in zip(blanks,keys) :
            blank.send_keys(key)
    Re()

#多选题
def MutiChoice() :
    choices = wd.find_elements(By.CSS_SELECTOR, '.lib-single-item-img img[src="assets/exercise/no-choices.png"]')
    for choice in choices :
        Click(choice)
    Re()
    keys = []
    keyName = ['A','B','C','D','E','F','G','H','I','J','K']  #选项名对应索引
    for key in wd.find_elements(By.CSS_SELECTOR, ".lib-single-cs-answer>span") :
        keys.append(keyName.index(key.text))  #索引存入keys
    Re()
    choices = wd.find_elements(By.CSS_SELECTOR, '.lib-single-item-img img[src="assets/exercise/no-choices.png"]')
    for i in keys :
        Click(choices[i])
    Re()


#单选题
def SingleChoice() :
    choices = wd.find_elements(By.CSS_SELECTOR, ".lib-single-item-order")
    for choice in choices :
        Click(choice)
    Re()
    keys = []
    for key in wd.find_elements(By.CSS_SELECTOR, ".lib-single-cs-answer") : #如keys=["A","B"]
        keys.append(key.text)
    choiceOfOne = len(choices)/len(keys)#每一题的选项数
    Re()
    choices = wd.find_elements(By.CSS_SELECTOR, ".lib-single-item-order") #再找一遍选项
    for key,i in zip(keys,range(len(keys))) :
        for choice in choices[int(i * choiceOfOne):] :   #每做一题从此题的第一个选项开始寻找
            if choice.text == key + '.' :  #如 "A." == "A"+"."
                Click(choice)
                break
            else :
                continue
    Re()

#判断题
def Judge() : #支持 'T' 'F' 'NI' 三个选项的题
    choices = wd.find_elements(By.CSS_SELECTOR, ".lib-judge-radio")
    for choice in choices :
        Click(choice)
    Re()
    keys = []
    for key in wd.find_elements(By.CSS_SELECTOR, ".lib-judge-info-text") : #如keys=["T","F"]
        keys.append(key.text)
    choiceOfOne = len(choices)/len(keys)#每一题的选项数
    Re()
    choices = wd.find_elements(By.CSS_SELECTOR, ".lib-judge-radio")
    for key,i in zip(keys,range(len(keys))) :
        if key == 'T' :
            Click(choices[int(i * choiceOfOne):][0])
        elif key == 'F' :
            Click(choices[int(i * choiceOfOne):][1])
        elif key == 'NI' :
            Click(choices[int(i * choiceOfOne):][2])    
    Re()

#下拉选择题
def Drop() :
    choices = wd.find_elements(By.CSS_SELECTOR, ".ant-select-dropdown-menu-item")
    for choice in choices :
        Click(choice)
    Re()
    keys = []
    for key in wd.find_elements(By.CSS_SELECTOR, ".wy-lib-cs-key + span") :
        keys.append(key.text)
    choiceOfOne = len(choices)/len(keys)#每一题的选项数
    Re()
    choices = wd.find_elements(By.CSS_SELECTOR, ".ant-select-dropdown-menu-item")
    for key,i in zip(keys,range(len(keys))) :
        for choice in choices[int(i * choiceOfOne):] :
            if choice.get_attribute("innerText").strip() == key :
                Click(choice)
                break
            else :
                continue
    Re()








if __name__ == "__main__" :
    input("登陆后到答题界面，并最大化窗口，按任意键继续。")
    while True : 
        if wd.find_elements(By.CSS_SELECTOR, ".wy-course-bottom .wy-course-btn-right .wy-btn") == [] :
            PageNext()    #找不到提交按钮，为单元标题页
        elif wd.find_elements(By.CSS_SELECTOR, ".lib-oral-container-top") != []:
            PageNext()    #有录音题直接跳过
        else :
            Re()
            if  wd.find_elements(By.CSS_SELECTOR, ".lib-fill-blank-do-input-left") != [] :
                FillBlank()   #填空题
            elif wd.find_elements(By.CSS_SELECTOR, '.lib-single-item-img img[src="assets/exercise/no-choices.png"]') !=[] :
                MutiChoice()  #多选题
            elif wd.find_elements(By.CSS_SELECTOR, ".lib-single-item-order") != [] :
                SingleChoice()   #单选题
            elif wd.find_elements(By.CSS_SELECTOR, ".lib-judge-radio") != [] :
                Judge()    #判断题
            elif wd.find_elements(By.CSS_SELECTOR, ".ant-select-dropdown-menu-item") !=[] :
                Drop()    #下拉选择题
        
            else :
                PageNext()
            # sleep(120)
            PageNext()


