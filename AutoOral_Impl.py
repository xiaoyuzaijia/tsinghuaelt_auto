
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from time import sleep
import time
import os
import random
import pyttsx3
#import load
#import speech_to_text
def randslp(i):
    time.sleep(random.random()*(1+random.random())*i)

def initialize():
    global driver
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    s = Service(r"C:\Users\1\Downloads\chromedriver_win32\chromedriver.exe")
    driver = webdriver.Chrome(service=s,options=options)
    driver.get('https://www.tsinghuaelt.com/')
    driver.maximize_window()
    print('initialized')




_debug=True


# Edit: set sleep to random_sleep for preventing being banned
def Click(element):  
    # js注入单击
    randslp(0.005)
    driver.execute_script("arguments[0].click();", element)
    randslp(0.005)
def PageNext():
    # 下一页
    randslp(2.5)
    Click(driver.find_elements(By.CSS_SELECTOR, ".page-next")[1])
    randslp(2.5)

# (prototype) Oral func for "Answers will vary" Questions
def Oral():
    # do temp oral
    buttons = driver.find_elements(By.CSS_SELECTOR, '.lib-oral-shadow .lib-oral-img img[src="assets/img/record.png"]')
    for button in buttons:
        Click(button)
        randslp(2)
        # try to stop the recording opening before
        stp = driver.find_elements(By.CSS_SELECTOR, '.lib-oral-container-top img[src="assets/img/recording.gif"]')
        for stpb in stp:
            Click(stpb)
            randslp(0.5)
        randslp(1)

# ralease ver: variable name changes
def Oral_opening():
    buttons_recording = driver.find_elements(By.CSS_SELECTOR, '.lib-oral-shadow .lib-oral-img img[src="assets/img/record.png"]')
    for begin_rec in buttons_recording:
        Click(begin_rec)
        randslp(2)
        # try to stop the recording opening before
        stop_buttons_rec = driver.find_elements(By.CSS_SELECTOR, '.lib-oral-container-top img[src="assets/img/recording.gif"]')
        for stop_rec in stop_buttons_rec:
            Click(stop_rec)
            randslp(0.5)
        randslp(1)

# Insert Oral() for answering "opening questions"
def Re():
    # 重写或提交
    if driver.find_elements(By.CSS_SELECTOR, ".lib-oral-container-top") != []:
        # indicates that there will be opening oral ques
        Oral()
    randslp(2)
    Click(driver.find_element(By.CSS_SELECTOR, ".wy-course-bottom .wy-course-btn-right .wy-btn"))
    randslp(2)

# engine for generating voice media via texts
engine=pyttsx3.init()
voices=engine.getProperty('voices')
print('voice: {}'.format(engine.getProperty('voice')))
for voice in voices:
    print(voice.id)
    if 'EN-US' in voice.id:
        # default voice util in Windows is 'Chinese Zh-cn'
        engine.setProperty('voice', voice.id)
# the default speed is too high for recognizing
# set the rate to rate - 75 may get highest score (in experiments)
rate = engine.getProperty('rate')
engine.setProperty('rate', rate-75)

# (prototype) common Oral Questions, it can be used in common
def Oral1():
    global engine
    statements=driver.find_elements(By.CSS_SELECTOR, '.lib-listen-item-right')
    all=[]
    for i in statements:
        all.append(i.text)
    # -------------------
    # used for testing role play ques, it is not needed
    count=0
    left=[]
    right=[]
    for i in all:
        if count % 2 == 0:
            left.append(i)
        else:
            right.append(i)
        count+=1
    # -------------------
    buttons = driver.find_elements(By.CSS_SELECTOR, '.lib-listen-item-right-img img[src="assets/img/record.png"]')
    count=0
    for button in buttons:
        # answering oral ques in index
        Click(button)
        time.sleep(0.5)
        engine.say(all[count])
        print('say: {}'.format(all[count]))
        count+=1
        engine.runAndWait()
        randslp(1)
        time.sleep(1)
        # try to stop this task, for it we should use loop
        stp = driver.find_elements(By.CSS_SELECTOR, '.lib-listen-item-right-img img[src="assets/img/recording.gif"]')
        for stpb in stp:
            Click(stpb)
            randslp(0.5)
        randslp(1)

# (prototype) Answering Role Play Question, it is not fully implemented.
# It is not fully automatic now, for there is no method to find out the approach to select the role to play
# you can invoke this function after the role be chosen, and the countdown is end, and it works
def Oral2():
    global engine
    # rate-75 is too low to record; the recording will automatically end before the saying ends
    engine.setProperty('rate', rate-50)
    # there are bugs that can not find 'select_role' and 'select_start'
    select_role = driver.find_elements(By.CSS_SELECTOR, '.lib-role-select-item')
    select_start = driver.find_elements(By.CSS_SELECTOR, '.lib-role-select-start')
    # get all texts to be spoken
    statements=driver.find_elements(By.CSS_SELECTOR, '.lib-role-item-right')
    all=[]
    for i in statements:
        all.append(i.text)
    count=0
    # this prototype is based on the situation that only 2 roles exists, but the true situation may have 3 roles
    left=[]
    right=[]
    for i in all:
        if count % 2 == 0:
            left.append(i)
        else:
            right.append(i)
        count+=1
    # -----------------
    #Click(select_role[0])
    #Click(select_start[0])
    # -----------------
    timestart = time.time()
    print(left)
    for i in left:
        stp0=None
        while True:
            stp = driver.find_elements(By.CSS_SELECTOR, '.lib-listen-item-right-img img[src="assets/img/recording.gif"]')
            if time.time()-timestart > 60:
                # timeout
                break
            if stp == []:
                # no in the round
                continue
            else:
                stp0=stp[0]
                break
        time.sleep(0.75)
        engine.say(i)
        print('say: {}'.format(i))
        engine.runAndWait()
        print('say end')
        randslp(1)
        time.sleep(1)
        # try to end the task
        try:
            Click(stp0)
        except Exception as E:
            print(E)
        stp = driver.find_elements(By.CSS_SELECTOR, '.lib-listen-item-right-img img[src="assets/img/recording.gif"]')
        print(stp)
        if stp==[]:
            # the stopping may fail, for recording automatically stops before saying ends
            # so it is reasonable to continue for next text
            print('continue')
            continue
        for stpb in stp:
            # common stopping
            print('stop')
            Click(stpb)
            randslp(0.5)
        randslp(1)
    engine.setProperty('rate', rate-75)

# debug used only
def test():
    ip=input('inp:')
    statements=driver.find_elements(By.CSS_SELECTOR, ip)
    for i in statements:
        print(i)
        print(i.text)
def setp():
    ip=input('rate-:')
    engine.setProperty('rate', rate-int(ip))

# release ver: answering common Oral ques
def AutoOral():
    global engine
    text_elems=driver.find_elements(By.CSS_SELECTOR, '.lib-listen-item-right')
    all_texts=[]
    for i in text_elems:
        all_texts.append(i.text)
    buttons_recording = driver.find_elements(By.CSS_SELECTOR, '.lib-listen-item-right-img img[src="assets/img/record.png"]')
    idx=0
    for button_rec in buttons_recording:
        # answering oral ques in index
        Click(button_rec)
        time.sleep(0.5)
        engine.say(all_texts[idx])
        idx+=1
        engine.runAndWait()
        randslp(1)
        time.sleep(1)
        # try to stop this task, for it we should use loop
        stop_buttons_rec = driver.find_elements(By.CSS_SELECTOR, '.lib-listen-item-right-img img[src="assets/img/recording.gif"]')
        for stop_button in stop_buttons_rec:
            Click(stop_button)
            randslp(0.5)
        randslp(1)

# -------------------------------
# prototypes
def getRoleNum():
    # prototype
    # return role number
    pass
def SelectRole(roleindex: int):
    # prototype
    # roleindex: the index of the role to select
    pass
def StartRolePlay():
    # prototype
    pass
def collect_texts_for_selected(texts:list, roleNum:int):
    # prototype
    # texts: all texts colleced from the web
    # ---------------
    # debug used only
    if _debug:
        return [texts[0], texts[-1]]
    # ---------------
    pass
# -------------------------------

# release ver: to do role play task
def RolePlay():
    # prototype needs to be implemented
    roleNum = getRoleNum()
    # select the first role (should be the first role in role play dialog, not in role selection plane)
    SelectRole(0)
    StartRolePlay()
    # ---------------
    # debug used only
    if _debug:
        roleNum=3
    # ---------------
    role_play_impl(roleNum)

def role_play_impl(roleNum: int):
    global engine
    # rate-75 is too low to record; the recording will automatically end before the saying ends
    engine.setProperty('rate', rate-50)
    # get all texts to be spoken
    text_elems=driver.find_elements(By.CSS_SELECTOR, '.lib-role-item-right')
    all_texts=[]
    for i in text_elems:
        all_texts.append(i.text)
    # should implement this method to distribute texts for the selected role 
    text_to_say=collect_texts_for_selected(all_texts, roleNum)
    timestart = time.time()
    for i in text_to_say:
        _stop=None
        while True:
            try_stop = driver.find_elements(By.CSS_SELECTOR, '.lib-listen-item-right-img img[src="assets/img/recording.gif"]')
            if time.time()-timestart > 60:
                # timeout
                break
            if try_stop == []:
                # no in the round
                continue
            else:
                _stop=try_stop[0]
                break
        time.sleep(0.75)
        engine.say(i)
        engine.runAndWait()
        randslp(1)
        time.sleep(1)
        # try to end the task
        try:
            Click(_stop)
        except Exception as E:
            print(E)
        try_stop_after_speech = driver.find_elements(By.CSS_SELECTOR, '.lib-listen-item-right-img img[src="assets/img/recording.gif"]')
        if try_stop_after_speech ==[]:
            # the stopping may fail, for recording automatically stops before saying ends
            # so it is reasonable to continue for next text
            print('continue')
            continue
        for single_try in try_stop_after_speech:
            # common stopping
            Click(single_try)
            randslp(0.5)
        randslp(1)
    engine.setProperty('rate', rate-75)


def procedure():
    input("按任意键继续进行题目作答。")
    while True:
        ip = input()
        if ip == '1':
            Oral1()
        elif ip=='3':
            test()
        elif ip=='4':
            setp()
        elif ip=='role_play':
            RolePlay()
        elif ip=='Oral':
            AutoOral()
        else:
            Oral2()

if __name__ == "__main__" :
    initialize()
    procedure()
    input('任意键')
