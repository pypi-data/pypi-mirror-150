import time,os

from selenium import webdriver
import allure
from .utils.handle_loguru import log
from time import strftime

class Exec:
    def __init__(self,data):
        self.data = data
        if 'browser' in self.data[0]:
            if self.data[0]['browser'] == 'chrome':
                self.driver = webdriver.Chrome()
            elif self.data[0]['browser'] == 'firefox':
                self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)
        os.makedirs('screenshot')


    def goto(self):
        for one in self.data:
            if one.get('goto'):
                goto_data = one.pop('goto')
                step,step_text = list(one.items())[0]
                with allure.step(f'步骤{step}:{step_text}'):
                    self.driver.get(goto_data)
                    log.info(f'步骤{step}:{step_text}')
                    file_name = f'screenshot/{strftime("%Y%m%d%H%M%S")}{step_text}.png'
                    self.driver.save_screenshot(file_name)
                    with open(file_name,'rb') as f:
                        file = f.read()
                    allure.attach(file,attachment_type=allure.attachment_type.PNG)
                    break
        return self

    def input(self):
        for one in self.data:
            if one.get('input'):
                input_ele = one.pop('input')
                step,step_text = list(one.items())[0]
                with allure.step(f'步骤{step}:{step_text}'):
                    ele =self.driver.find_element(*input_ele[:-1])
                    ele.clear()
                    time.sleep(1)
                    ele.send_keys(input_ele[-1])
                    log.info(f'步骤{step}:{step_text}')
                    log.info(f'定位方式by={input_ele[:-1][0]},定位的值{input_ele[:-1][-1]}')
                    log.info(f'输入的值{input_ele[-1]}')
                    file_name = f'screenshot/{strftime("%Y%m%d%H%M%S")}{step_text}.png'
                    self.driver.save_screenshot(file_name)
                    with open(file_name, 'rb') as f:
                        file = f.read()
                    allure.attach(file, attachment_type=allure.attachment_type.PNG)
                    break
        return self

    def click(self):
        for one in self.data:
            if one.get('click'):
                click_data = one.pop('click')
                step, step_text = list(one.items())[0]
                with allure.step(f'步骤{step}:{step_text}'):
                    self.driver.find_element(*click_data).click()
                    log.info(f'步骤{step}:{step_text}')
                    log.info(f'定位方式by={click_data[0]},定位的值{click_data[-1]}')
                    log.info('点击元素')
                    file_name = f'screenshot/{strftime("%Y%m%d%H%M%S")}{step_text}.png'
                    self.driver.save_screenshot(file_name)
                    with open(file_name, 'rb') as f:
                        file = f.read()
                    allure.attach(file, attachment_type=allure.attachment_type.PNG)
                    break
        return self


    def def_assert(self,save_data):
        var = save_data[0]
        result = save_data[1]
        for one in self.data:
            if one.get('assert'):
                assert_data = one.pop('assert')
                step, step_text = list(one.items())[0]
                with allure.step(f'步骤{step}:{step_text}'):
                    if var in assert_data[-1]:
                        assert_data[-1] = result
                        try:
                            if isinstance(result,list):
                                log.info(f'步骤{step}:{step_text}')
                                log.info(f'期望值{assert_data[0]},实际值{result}')
                                assert assert_data[0] in result
                            else:
                                log.info(f'步骤{step}:{step_text}')
                                log.info(f'期望值{assert_data[0]},实际值{result}')
                                assert assert_data[0] == result
                        except Exception as error:
                            log.info(f'步骤{step}:{step_text}')
                            log.error(f'断言失败，期望值{assert_data[0]},实际值{result}')
                            file_name = f'screenshot/{strftime("%Y%m%d%H%M%S")}{step_text}断言失败.png'
                            self.driver.save_screenshot(file_name)
                            with open(file_name, 'rb') as f:
                                file = f.read()
                            allure.attach(file, attachment_type=allure.attachment_type.PNG)
                            raise error
                    else:
                        log.info(f'没有找到变量{assert_data[-1]}')
                        raise Exception('变量填写错误')



    def save_text(self):
        for one in self.data:
            if one.get('save_text'):
                text_ele = one.pop('save_text')
                step, step_text = list(one.items())[0]
                with allure.step(f'步骤{step}:{step_text}'):
                    text_msg = self.driver.find_element(*text_ele[:-1]).text
                    var = text_ele[-1]
                    log.info(f'步骤{step}:{step_text}')
                    log.info(f'保存变量{var},变量值为{text_msg}')
                    file_name = f'screenshot/{strftime("%Y%m%d%H%M%S")}{step_text}.png'
                    self.driver.save_screenshot(file_name)
                    with open(file_name, 'rb') as f:
                        file = f.read()
                    allure.attach(file, attachment_type=allure.attachment_type.PNG)
        return var,text_msg


    def save_texts(self):
        for one in self.data:
            if one.get('save_texts'):
                text_ele = one.pop('save_texts')
                step, step_text = list(one.items())[0]
                with allure.step(f'步骤{step}:{step_text}'):
                    text_msg = [ele.text for ele in self.driver.find_elements(*text_ele[:-1])]
                    var = text_ele[-1]
                    log.info(f'步骤{step}:{step_text}')
                    log.info(f'保存变量{var},变量值为{text_msg}')
                    file_name = f'screenshot/{strftime("%Y%m%d%H%M%S")}{step_text}.png'
                    self.driver.save_screenshot(file_name)
                    with open(file_name, 'rb') as f:
                        file = f.read()
                    allure.attach(file, attachment_type=allure.attachment_type.PNG)
        return var, text_msg
