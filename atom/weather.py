import requests


weater_apiKey = 'd4vbvu6zpcxfqqnh'
weater_apiId = 'U92A957B08'
city = '北京'

weater_url = 'https://api.seniverse.com/v3/weather/now.json?key=%s&location=%s&language=zh-Hans&unit=c' % (weater_apiKey,city)

req = requests.get(weater_url)
weatertext = req.json()['results'][0]['now']['text']
temperature = req.json()['results'][0]['now']['temperature']
lastupdate = req.json()['results'][0]['last_update']
content = '''
{0} --- {1}
温度：{2}℃
更新时间：{3}
'''.format(city,weatertext,temperature,lastupdate)

print (content)
