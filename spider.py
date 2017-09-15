import requests
from bs4 import BeautifulSoup as BS
search_page_range=5
author=input('输入你想查询的作家：')
url="https://book.douban.com/subject_search"
payload={'search_text':author}
html=requests.get(url,params=payload)
bsObj=BS(html.content,"html.parser")
page_info=bsObj.find('div',class_='paginator')
page_range=int(page_info.select('a[href]')[-2].get_text())

for page_num in range(search_page_range):
	#print(bsObj.title)
	book_data=bsObj.find_all('li',class_='subject-item')
	#print(book_data[0])
	for i in range(len(book_data)):
		#print(i)
		temp=book_data[i].find_all('span',class_='rating_nums')		
		#print('temp:',type(temp))
		if len(temp)>0:
			rate_tag=temp[0]
			#print(rate_tag)
			rate=float(rate_tag.get_text())
			if rate > 8:
				title_tag=str(book_data[i].select('a[title]')[0])
				bs_title_tag=BS(title_tag,'html.parser')
				result_str=bs_title_tag.get_text().replace('\n','').replace('：',':').strip()
				pub_tag=book_data[i].find('div',class_='pub')
				pub=pub_tag.get_text().replace('\n','').strip()
				print('评分：',rate,'<<',result_str,'>>','\n',pub)
	#print(page_num,page_range)
	if(page_num+1>=page_range):
		#print(page_num+1,page_range)
		break
	page_next=page_info.select('a[href]')[page_num+1]['href']
	print(page_next)
	#input()
	url="https://book.douban.com"+page_next
	html=requests.get(url)
	bsObj=BS(html.content,"html.parser")


