import jieba.analyse
from html2text import html2text
import pymongo
import pandas as pd
from flask import Flask
import matplotlib.pyplot as plt
from PIL import Image , ImageSequence
from wordcloud import WordCloud,ImageColorGenerator
from flask import render_template , request
import numpy as np
import logging
import re
jieba.setLogLevel(logging.INFO)
import json
#创建一个Flask应用
app = Flask(__name__)

client = pymongo.MongoClient('localhost', 27017)
db = client['weibo']
Tweets = db['Tweets']
Information = db['Information']


#读取数据
userinfo = pd.DataFrame(list(Information.find()))


#选择需要显示的字段
userID =userinfo._id
gender = userinfo.gender
nickname = userinfo.NickName
num_tweets = userinfo.Num_Tweets
num_fans = userinfo.Num_Fans
num_follows = userinfo.Num_Follows

def wordcould(userID,data1):
    content ='\n'.join([html2text(i) for i in data1])
    result = jieba.analyse.textrank(content, topK=1000, withWeight=True)
    keywords = dict()
    for i in result:
        keywords[i[0]] = i[1]
    del keywords['大家']
    alice_mask = np.array(Image.open('201206061443468639.png'))
    alice_color = np.array(Image.open('alice_color.png'))
    wc = WordCloud(font_path='simhei.ttf', background_color='white',max_words=2000,mask=alice_mask,max_font_size=100,random_state=42)
    wc.generate_from_frequencies(keywords)
    image_colors = ImageColorGenerator(alice_color)
    plt.imshow(wc)
    plt.imshow(wc.recolor(color_func=image_colors))
    plt.axis("off")  # 关闭图像坐标系
    plt.savefig('./static/personas/{}.png'.format(userID))


@app.route('/',methods=['GET','POST'])
def index():
    INFO = {}
    image = ''
    if request.method == 'POST' and request.form.get('userID'):
        userID = request.form.get('userID')
        result = Information.find_one({'_id': int(userID)})
        data = pd.DataFrame(list(Tweets.find({'ID':str(userID)})))
        if data.empty ==True:
            all_data = pd.DataFrame(list(Tweets.find()))
            data1 = all_data.Content
        else:
            data1 = data.Content

        INFO = result
        INFO = str(INFO).replace("'",'"')
        dest_img =wordcould(userID,data1)
        image_local_path ='../static/personas/' + userID + '.png'
        image = image_local_path
    return render_template('index.html', INFO=INFO ,image=image)


if __name__=='__main__':
    app.run()
