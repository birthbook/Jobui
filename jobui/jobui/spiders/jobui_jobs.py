import scrapy,bs4
from ..items import JobuiItem

class JobuiSpider(scrapy.Spider):
	#定义一个爬虫类JobuiSpider

	#定义爬虫的名字为jobui
	name = 'jobui'

	#定义允许爬虫爬取网址的域名——职友集网站的域名
	allowed_domains = ['www.jobui.com']

	#定义起始网址——职友集企业排行榜的公司的网址
	start_urls = ['https://www.jobui.com/rank/company/']


	#parse是默认处理response的方法
	def parse(self,response):
		bs = bs4.BeautifulSoup(response.text,'lxml')
		ul_list = bs.find_all('ul',class_="textList flsty cfix")

		for ul in ul_list:
			a_list = ul.find_all('a')

			for a in a_list:
				company_id = a['href']

				real_url = 'https://www.jobui.com{id}jobs/'.format(id=company_id)
				#用yield语句把构造好的request对象传递给引擎。用scrapy.Request构造request对象。callback参数设置调用parsejob方法。
				yield scrapy.Request(real_url,callback=self.parse_job)

	##定义新的处理response的方法parse_job（方法的名字可以自己起）
	def parse_job(self,response):
		bs = bs4.BeautifulSoup(response.text,'lxml')

		#公司名称
		company = bs.find('div',class_="company-banner-mb20").find('a').text

		datas = bs.find_all('div',class_="job-simple-content")

		for data in datas:

			#实例化一个类
			item = JobuiItem()

			#公司
			item['company'] = company

			#职位
			item['position'] = data.find('a').text#可能有空格，准确：data.find('a').find('h3').text

			#工作地点
			address = data.find('div',class_="job-desc").find('span').text
			#或：data.find_all('span')[0]['title']

			#招聘要求
			detail = data.find_all('span')[1]['title']

			yield item
			#用yield语句把item传递给引擎








