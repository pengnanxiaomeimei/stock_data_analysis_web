import json
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from PIL import Image

# webdriver配置信息
caps = {
    'browserName': 'chrome',
    'loggingPrefs': {
        'browser': 'ALL',
        'driver': 'ALL',
        'performance': 'ALL',
    },
    'goog:chromeOptions': {
        'perfLoggingPrefs': {
            'enableNetwork': True,
        },
        'w3c': False,
    },
}

driver = webdriver.Chrome(desired_capabilities=caps)
driver.get('https://jywg.18.cn/Login/Login')  # 进入东方财富登录页
time.sleep(3)
driver.find_element_by_id("txtZjzh").send_keys("540350286928")
driver.find_element_by_id("txtPwd").send_keys("cdd15225115906")
imageElement = driver.find_element_by_id("imgValidCode")
locations = imageElement.location
print(locations)
sizes = imageElement.size
print(sizes)

save_path = "test.png"
driver.save_screenshot(save_path)

# 构造指数的位置
rangle = (int(locations['x']),int(locations['y']),int(locations['x'] + sizes['width']),int(locations['y'] + sizes['height']))
print(rangle)


# 打开截图切割
img = Image.open(save_path)
jpg = img.convert('RGB')
jpg = img.crop(rangle)
save_path2 = "test2.png"
jpg.save(save_path2)


driver.find_element_by_id("btnConfirm").click()
request_log = driver.get_log('performance')
print(request_log)

for i in range(len(request_log)):
    message = json.loads(request_log[i]['message'])
    message = message['message']['params']
    # .get() 方式获取是了避免字段不存在时报错
    request = message.get('request')
    if (request is None):
        continue

    url = request.get('url')
    if (url == "https://jywg.18.cn/Login/Authentication?validatekey="):
        # 得到requestId
        print(message['requestId'])
        # 通过requestId获取接口内容
        content = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': message['requestId']})
        print(content)
        break
driver.close()
