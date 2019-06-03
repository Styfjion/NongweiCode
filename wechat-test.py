from urllib import request,parse

data = {'text':'Test','desp':'RT'}
url = r'https://sc.ftqq.com/SCU45342Tb4e29be9a89b07ec9e0d95dd16f42c625c74c780d63d3.send?'
data = parse.urlencode(data).encode('utf-8')
req = request.Request(url,data=data)
page = request.urlopen(req).read()
page = page.decode('utf-8')