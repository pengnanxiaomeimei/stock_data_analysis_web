# encoding:utf-8
import requests

api_key = "LelWdpw6Agd5ksCKXcSs4mwd"
secret_key = "cbPPzOptyQkw8kyBwIyACnmZr1raSZxE"

# client_id 为官网获取的AK， client_secret 为官网获取的SK
host = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=" + api_key
+ "&client_secret=" + secret_key
response = requests.get(host)
if response:
    print(response.json())