import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
from requests_ntlm import HttpNtlmAuth
import urllib
import random
from PIL import Image
import pytesseract
import time
imagePath='./code.png'
imagePath2='./code2.png'
url = 'http://localhost:8301/punchcardv3.aspx'
codeUrl = "http://localhost:8301/ValidationCode.aspx?" + str(random.random())
headers = {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}
postData = {
	'__VIEWSTATE': '',
	'__EVENTVALIDATION': '',
	'txtValCode': ''
}

mysession = requests.Session()
r = mysession.get(url, headers=headers, auth=HttpNtlmAuth('domain\\username', 'password!'), timeout=60 * 4)
r.encoding = r.apparent_encoding
c = r.content
cookies=r.cookies
soup = BeautifulSoup(c ,"html.parser")
# inputstring = mysoup.find_all('input', attrs={"name":"__VIEWSTATE"})
txtValCode = soup.find_all(id='txtValCode')
chkCodeImg = soup.find(id='chkCode')
hiddtxtValCodeFlag = soup.find(id='hiddtxtValCodeFlag')
__VIEWSTATE = soup.find(id='__VIEWSTATE')
__EVENTVALIDATION = soup.find(id='__EVENTVALIDATION')
# 设置post信息
postData['__VIEWSTATE'] = __VIEWSTATE.get('value')
postData['__EVENTVALIDATION'] = __EVENTVALIDATION.get('value')
capr = mysession.get(codeUrl, cookies=cookies,headers=headers,auth=HttpNtlmAuth('domain\\username', 'password!'), timeout=60 * 4)
with open(imagePath, 'wb') as f:
	f.write(capr.content)
	f.flush()
f.close()


#time.sleep(2)
###获取验证码字串 赋值cap_str
image = Image.open(imagePath)
#image = image.convert('1')
#print(image.size[0],image.size[1])
h=image.size[0]*3
w=image.size[1]*3
image.resize((w,h),Image.ANTIALIAS)
image.save(imagePath2)
image2 = Image.open(imagePath2)
image2.load()
image2.show()
code = pytesseract.image_to_string(image2,config='digits')
print(code)
code=input("输入验证码: ")
print("接收到验证码:",code)
postData['txtValCode'] = code
postData['hdfIPAddress']='1.1.1.1'
postData['hdfHostName']='1.1.1.1'
result = mysession.post(url,cookies=cookies, data=postData, headers=headers, auth=HttpNtlmAuth('domain\\username', 'password!'),
						timeout=60 * 4)

result.encoding = result.apparent_encoding
soup = BeautifulSoup(result.content,"html.parser")
print(soup.prettify())


def open_page(url):
	try:
		r = requests.get(url, headers=headers, auth=HttpNtlmAuth('domain\\username', 'password!'))
		r.encoding = r.apparent_encoding

		r.raise_for_status()
		return r.content
	except:
		print('打开页面失败')


def post_page(url):
	try:
		r = requests.post(url, data=postData, headers=headers, auth=HttpNtlmAuth('domain\\username', 'password!'))
		r.encoding = r.apparent_encoding

		r.raise_for_status()
		return r.content
	except:
		print('打开页面失败')


if 1 == 2:
	html = open_page(url)
	# html = open('page.html',encoding='utf-8')
	soup = BeautifulSoup(html, "html.parser")
	with open('./page.html', 'wb') as f:
		f.write(soup.prettify(encoding='utf-8'))
		f.close
	txtValCode = soup.find_all(id='txtValCode')
	chkCodeImg = soup.find(id='chkCode')
	hiddtxtValCodeFlag = soup.find(id='hiddtxtValCodeFlag')
	__VIEWSTATE = soup.find(id='__VIEWSTATE')
	__EVENTVALIDATION = soup.find(id='__EVENTVALIDATION')

	# 设置post信息
	postData['__VIEWSTATE'] = __VIEWSTATE.get('value')
	postData['__EVENTVALIDATION'] = __EVENTVALIDATION.get('value')
	post_html = post_page(url)
	soup = BeautifulSoup(post_html, "html.parser")
	with open('./post_page.html', 'wb') as f:
		f.write(soup.prettify(encoding='utf-8'))
		f.close
