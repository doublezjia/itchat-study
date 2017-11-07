#!/usr/local/bin/env python3
# python3 
# weater_api: www.seniverse.com

'''
itchat.content中的内容

TEXT       = 'Text'
MAP        = 'Map'
CARD       = 'Card'
NOTE       = 'Note'
SHARING    = 'Sharing'
PICTURE    = 'Picture'
RECORDING  = VOICE = 'Recording'
ATTACHMENT = 'Attachment'
VIDEO      = 'Video'
FRIENDS    = 'Friends'
SYSTEM     = 'System'
INCOME_MSG = [TEXT, MAP, CARD, NOTE, SHARING, PICTURE,RECORDING, VOICE, ATTACHMENT, VIDEO, FRIENDS, SYSTEM]

itchat.send方法：send(msg="Text Message", toUserName=None)
参数：
msg : 文本消息内容
@fil@path_to_file : 发送文件
@img@path_to_img : 发送图片
@vid@path_to_video : 发送视频
toUserName : 发送对象, 如果留空, 将发送给自己.

下载文件的方法是：msg['Text'](msg['FileName'])
'''

import itchat,os,requests
from itchat.content import *


# weater key
weater_apiKey = 'd4vbvu6zpcxfqqnh'
weater_apiId = 'U92A957B08'

# tuling key
tuling_key = 'dc47ce10cfd24347a6e0baf08401d2d8'

#图灵机器人API
def tulingapi(msg):
	tulingUrl = 'http://www.tuling123.com/openapi/api'
	data = {
	    'key'    : tuling_key, # 如果这个Tuling Key不能用，那就换一个
	    'info'   : msg, # 这是我们发出去的消息
	    'userid' : 'Atom', # 这里你想改什么都可以
	}
	# 我们通过如下命令发送一个post请求
	try:
		req = requests.post(tulingUrl, data=data).json()
		if req.get('code') == 200000 :
			return req.get('text')+'\n'+req.get('url')
		elif req.get('code') == 302000:
			new = ''
			for i in range(len(req.get('list'))):
				new =new+'\n标题：'+req.get('list')[i].get('article')+'\n地址：'+req.get('list')[i].get('detailurl')+'\n来源：'+req.get('list')[i].get('source')+'\n'
			return req.get('text')+'\n'+new
		else:
			return req.get('text')
	except:
		return 'QAQ Error'


# 天气API  注意：图灵机器人已经包括有这个功能呢，这个可以不用
def weaterapi(city):
	city = city
	weater_url = 'https://api.seniverse.com/v3/weather/now.json?key=%s&location=%s&language=zh-Hans&unit=c' % (weater_apiKey,city)
	req = requests.get(weater_url)
	# 判断api获取的状态码
	if req.status_code == 200 :
		weatertext = req.json()['results'][0]['now']['text']
		temperature = req.json()['results'][0]['now']['temperature']
		lastupdate = req.json()['results'][0]['last_update']
		wechatmsg = '''
		{0} --- {1}
		温度：{2}℃
		更新时间：{3}
		'''.format(city,weatertext,temperature,lastupdate)
	elif req.status_code == 403:
		wechatmsg = '暂时只能查看国内各大城市天气'
	elif req.status_code == 404 :
		wechatmsg = '请正确输入城市名'	
	return wechatmsg


# itchat.content中的内容
msgtype=[TEXT, MAP, CARD, NOTE, SHARING, PICTURE,RECORDING, VOICE, ATTACHMENT, VIDEO, FRIENDS, SYSTEM]
# itchat使用
@itchat.msg_register(msgtype)
def conText(msg):
	# 判断是否为文件传输助手
	if msg['ToUserName'] != 'filehelper':return
	# 判断是否为文字，这里要注意emoji表情也是属于Text类型的
	if msg['Type'] == 'Text':
		# 通过判断Text中是否包含'天气+'的字符来判断是否为查询天气
		if '天气+' in msg['Text']:
			try:
				# 获取城市名,通过+进行截取
				city = msg['Text'].split('+')[1]
				wechatmsg = weaterapi(city)
			except:
				wechatmsg = '查询出错！！！'
		else:
			wechatmsg = tulingapi(msg['Text'])  
		itchat.send('%s' % wechatmsg,'filehelper')
	# 判断图片
	elif msg['Type'] == 'Picture':
		fname = './file/images'+msg['FileName']
		wechatmsg = msg['Text'](fname)
		itchat.send('@img@%s' % fname,'filehelper')	 
	# 判断语音
	elif msg['Type'] == 'Recording':
		# 下载语音文件
		# fname = './file/recording'+msg['FileName']
		# wechatmsg = msg['Text'](fname)
		itchat.send('暂时我还不会说语音','filehelper')
 
if __name__ == '__main__':

	# 短时间内登陆重连hotReload=True,命令行二维码enableCmdQR=2 
	# 命令行二维码前提要Linux安装pillow 安装命令 pip install pillow

	itchat.auto_login(hotReload=True,enableCmdQR=2)
	itchat.send('查看天气可以输入：天气+城市名','filehelper')
	itchat.send('也可以直接天气城市名查询','filehelper')
	itchat.run()

