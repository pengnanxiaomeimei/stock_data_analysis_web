# 简书
import json
import random
import ssl
import time
import urllib.request
import urllib.parse

import js2py
import requests
from bs4 import BeautifulSoup

global false, null, true
false = null = true = ""

ssl._create_default_https_context = ssl._create_unverified_context

# 简书请求头
user_agent = r'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) ' \
             r'Chrome/88.0.4324.96 Safari/537.36 '
headers = {r'User-Agent': user_agent,
           r'Host': "www.jianshu.com",
           r'Origin': "https://www.jianshu.com",
           r'Sec-Fetch-Dest': "empty",
           r'Sec-Fetch-Mode': "cors",
           r'Sec-Fetch-Site': "same-origin",
           r'Connection': "keep-alive",
           r'Accept-Language': "zh-CN,zh;q=0.9",
           r'Accept-Encoding': "gzip, deflate, br"}

# 登录成功后的cookie
cookie_str = "__yadk_uid=I6rLZ9jXpSCvrt95oV2bojQzntCzQc6Y; locale=zh-CN; _ga=GA1.2.438895632.1610609736; " \
             "read_mode=day; default_font=font2; " \
             "remember_user_token" \
             "=W1syNTgyMDQ1Nl0sIiQyYSQxMSRYeWFJYmZQUVN5UWF6dzV2MG4yZEF1IiwiMTYxMjY5MDQ1Mi44NDc4NDc3Il0%3D" \
             "--8cc9f5c9d90dcf89049f50ca1f59c541fb0c5aab; " \
             "web_login_version=MTYxMjY5MDQ1Mg%3D%3D--b2cde55f5f93d0034944deae5e50f9bc36700044; " \
             "_m7e_session_core=b85d3bd7f1d129e61f52e4371f6f7efc; " \
             "sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2225820456%22%2C%22first_id%22%3A%22176ffd23926b1b" \
             "-047c657dc724e6-326e7006-2073600-176ffd23927c0f%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type" \
             "%22%3A%22%E7%A4%BE%E4%BA%A4%E7%BD%91%E7%AB%99%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A" \
             "%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fopen.weixin.qq" \
             ".com%2F%22%2C%22%24latest_utm_source%22%3A%22desktop%22%2C%22%24latest_utm_medium%22%3A%22search-recent" \
             "%22%7D%2C%22%24device_id%22%3A%22176ffd23926b1b-047c657dc724e6-326e7006-2073600-176ffd23927c0f%22%7D; " \
             "Hm_lvt_0c0e9d9b1e7d617b3e6842e85b9fb068=1611833590,1611833940,1612147838,1612690453; " \
             "Hm_lpvt_0c0e9d9b1e7d617b3e6842e85b9fb068="
cookie = {"Cookie": cookie_str}


# 文章列表关键词查询
def note_search(key_word, page):
    url = "https://www.jianshu.com/search?q=" + str(key_word) + "&page=" + str(page) + "&type=note"
    headers[r'Accept'] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng," \
                         "*/*;q=0.8,application/signed-exchange;v=b3;q=0.9 "

    resp = requests.get(url, headers=headers)
    print(resp.content.decode(encoding="utf-8"))
    soup = BeautifulSoup(resp.content.decode(encoding="utf-8"), 'lxml')
    # 提取csrf-token值
    csrf_token = soup.find("meta", {"name": "csrf-token"})["content"]
    print(csrf_token)
    return do_note_search(key_word, page, url, csrf_token)


# 文章列表关键词搜索
def do_note_search(key_word, page, refer_url, csrf_token):
    url = "https://www.jianshu.com/search/do?q=" + str(key_word) + "&page=" + str(page) + "&type=note&order_by=default"
    headers[r'Referer'] = refer_url
    headers[r'X-CSRF-Token'] = csrf_token
    headers[r'Accept'] = "application/json"
    headers[r'Content-Length'] = "0"
    cookie_str01 = cookie_str + str(int(time.time())) + " "
    cookie["Cookie"] = cookie_str01
    # time.sleep(10)
    resp = requests.post(url, headers=headers, cookies=cookie)
    # time.sleep(10)
    # response = urllib.request.urlopen(req)
    search_result = resp.content.decode(encoding="utf-8")
    print(search_result)
    dict_result = eval(search_result)
    print(dict_result)
    # 接口返回的总页数
    total_pages = dict_result["total_pages"]
    # 如果总页数不存在或总页数为0或总页数小于传参页数
    if total_pages is None or total_pages == 0 or total_pages < page:
        return None

    entries = dict_result["entries"]
    entry_ids = []
    for entry in entries:
        entry_ids.append(entry["id"])
    result = {"page": dict_result["page"],
              "total_pages": dict_result["total_pages"],
              "entry_ids": entry_ids}
    return result


# 文章点赞
def do_note_like(entry_ids):
    headers[r'Accept'] = "application/json"
    for entry_id in entry_ids:
        url = "https://www.jianshu.com/shakespeare/notes/" + str(entry_id) + "/like"
        data = {"energy_point": 3, "note_id": entry_id}

        # data = urllib.parse.urlencode(data).encode("utf-8")
        # req = urllib.request.Request(url, data=data, headers=headers)

        # req.add_header('cookie', cookie)  # 将cookie加入以后的请求头，保证多次请求属于一个session
        # req.get_method = lambda: 'DELETE'  # 设置HTTP的访问方式
        resp = requests.post(url, data, headers=headers, cookies=cookie)
        # response = urllib.request.urlopen(req)
        print(resp.content.decode(encoding="utf-8"))


# 根据关键词查询文章并点赞
def note_like(keyword):
    # 关键词转义
    keyword = urllib.parse.quote(keyword)
    # 初始化页数
    page = 9
    # 初始化总页数
    total_pages = 9

    # 循环获取文章id并点赞
    while total_pages is not None and page <= total_pages:
        # search_result = note_search("strings", page)
        search_result = note_search(keyword, page)
        if search_result is None:
            break
        entry_ids = search_result["entry_ids"]
        # 进行批量点赞
        do_note_like(entry_ids)
        # 更新最新的total_pages
        total_pages = int(search_result["total_pages"])
        page = page + 1
        # 请求间隔
        time.sleep(random.randrange(1, 20, 3))
        # print(int(time.time()))


# 简书钻文章排行
# 获取文章编号集合
def note_sort_list_by_diamond():
    url = "https://www.jianshu.com/fp/notice/now?read_mode=night"
    # 排行榜页面
    resp = requests.get(url, headers=headers, cookies=cookie)
    soup = BeautifulSoup(resp.content.decode(encoding="utf-8"), 'lxml')
    # 提取sort_list值
    scripts = soup.find_all("script")
    script = scripts.pop(3)
    script_str = str(script.contents[0])
    str_splits_01 = script_str.replace("\n", "").replace(" ", "").split(";")
    sort_dict_str_01 = ""
    count = len(str_splits_01)
    for i in range(count):
        sort_dict_str_01 = sort_dict_str_01 + ";" + str_splits_01[i]
        count = count - 1
        if count <= 4:
            break

    sort_dict_str = sort_dict_str_01.split("=", 1)[1]
    sort_dict = eval(sort_dict_str)
    print(sort_dict)
    # script_content = soup.find("script").contents
    # sort_dict = js2py.eval_js(script_content)
    sort_list = sort_dict["ruby"]["voter"]
    if sort_list is None:
        return None
    # 文章编号
    slug_list = []
    for note_info in sort_list:
        slug_list.append(note_info["slug"])
    return slug_list


# 获取文章id
def get_note_id(slug):
    url = "https://www.jianshu.com/p/" + str(slug)
    resp = requests.get(url, headers=headers, cookies=cookie)
    soup = BeautifulSoup(resp.content.decode(encoding="utf-8"), 'lxml')
    note_dict_str = str(soup.find("script", {"id": "__NEXT_DATA__"}).contents[0])
    note_dict = eval(note_dict_str)
    print(type(note_dict))
    note_id = note_dict["props"]["initialState"]["note"]["data"]["id"]
    return note_id


# 对简书钻排行的数据进行点赞
def note_like_4_diamond_sort():
    slug_list = note_sort_list_by_diamond()
    if slug_list is None:
        return None
    for slug in slug_list:
        note_id = get_note_id(slug)
        do_note_like([note_id])
        # 请求间隔
        time.sleep(random.randrange(1, 10, 3))


# note_like("热")

# for i in range(10):
#     print(random.randrange(1, 20, 3))

note_like_4_diamond_sort()


