from urllib import parse
from urllib import request
import base64
import json
import cv2 as cv
import numpy as np

# client_id 为官网获取的AK， client_secret 为官网获取的SK
client_id = "PdGZt2zGGEYS02brWlzprc9Y"  # AK
client_secret = "v1Y3ws0QW8bBClxyleFxzSejdlscbfi0"  # SK


# 获取token
def get_token():
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + client_id + '&client_secret=' + client_secret
    req = request.Request(host)
    req.add_header('Content-Type', 'application/json; charset=UTF-8')
    response = request.urlopen(req)
    token_content = response.read()
    if token_content:
        token_info = json.loads(token_content)
        token_key = token_info['access_token']
    return token_key


# 手写文字
# filename:图片名（本地存储包括路径）
def handwriting(filename):
    word = []
    loc = []
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/handwriting"

    # 二进制方式打开图片文件
    f = open(filename, 'rb')
    img = base64.b64encode(f.read())

    params = dict()
    params['image'] = img
    params = parse.urlencode(params).encode("utf-8")
    # params = json.dumps(params).encode('utf-8')

    access_token = get_token()
    request_url = request_url + "?access_token=" + access_token
    req = request.Request(url=request_url, data=params)
    req.add_header('Content-Type', 'application/x-www-form-urlencoded')
    response = request.urlopen(req)
    content = response.read()
    if content:
        # index = 1
        # print(content)
        content = content.decode('utf-8')
        # print(content)
        data = json.loads(content)
        # print(data)
        words_result = data['words_result']
        print(words_result)

        for item in words_result:
            word = item['words']
            loc = item['location']
            print("word:", word, "loc:", loc, "len:", len(word))

            if len(word) > 11:
                word, loc = adjustRes(word, loc)
                break
            elif len(word) == 11:
                break

    return word, loc


def adjustRes(word, loc):
    new_word = ""
    delta = 11
    for index, item in enumerate(word):
        if item.isdigit():
            new_word += item
        elif index < 5:
            loc['left'] = loc['left'] + int(delta * 1.35)
            loc['width'] = loc['width'] - delta
        else:
            loc['width'] = loc['width'] - delta
    return new_word, loc


# 绘制识别后的矩形框
def drwaRect(image_file, loc):
    image = cv.imread(image_file)
    left_top_point = (loc['left'], loc['top'])
    right_down_point = (loc['left'] + loc['width'], loc['top'] + loc['height'])
    cv.rectangle(image, left_top_point, right_down_point, (255, 0, 0), 1)
    image_file = image_file.split('.')[0] + "_rect.jpg"
    cv.imwrite(image_file, image)
    return image_file


# 绘制识别后的矩形框
def drwaRect2(image_file, loc, origin_left_up_point):
    image = cv.imread(image_file)
    delta = 5
    left_top_point = (loc['left'] + origin_left_up_point[0] - delta, loc['top'] + origin_left_up_point[1] - delta)
    right_down_point = (loc['left'] + loc['width'] + origin_left_up_point[0] + delta,
                        loc['top'] + loc['height'] + origin_left_up_point[1] + delta)
    cv.rectangle(image, left_top_point, right_down_point, (0, 0, 255), 3)
    image_file = image_file.split('images')[0] + "/images/temp" + image_file.split('images')[1].split('.')[
        0] + "_rect.jpg"
    cv.imwrite(image_file, image)
    return image_file


# 裁剪预处理
def preprocess(path):
    img = cv.imread(path)
    height, width, _ = img.shape
    height_start = height // 3 + 50
    width_start = width // 2 + 80
    left_up_point = (width_start, height_start)
    img_copy = img[height_start:height * 2 // 3 - 60, width_start:width * 3 // 4 + 150]
    crop_path = path.split('images')[0] + "/images/temp" + path.split('images')[1].split('.')[0] + "_crop.jpg"
    cv.imwrite(crop_path, img_copy)
    return crop_path, left_up_point
