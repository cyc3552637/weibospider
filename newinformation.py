from urllib import request
from urllib import parse
from urllib.request import urlopen
from http import cookiejar
from lxml import etree
from bs4 import  BeautifulSoup
import  re
import datetime
#from myfunction import ntoc
#from myfunction import dict_freq_sort
import xlwt
import random




user_agent_list = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]

def getday(y,m,d,n):
    the_date = datetime.datetime(y,m,d)
    result_date = the_date + datetime.timedelta(days=n)
    d = result_date.strftime('%Y-%m-%d')
    return d


def get_ip():
	ip_list = []
	with open ('ip_list.txt') as f:
		for line in f.readlines():
			ip_list.append(line.replace("\n",""))
	ip = random.choice(ip_list)
	return ip

def spider(keyword,y,m,d,days):
    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet('sheet 1')
    url_keyword=parse.quote(keyword)

    #提交准备
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763'
    headers = { 'User-Agent' : user_agent ,'Referer':'' }
    #cookie构建opener
    cookie=cookiejar.CookieJar()#cookie = cookiejar.MozillaCookieJar(filename) 可保存读取的cookie初始化方法
    #cookie.load(filename, ignore_discard=True, ignore_expires=True)读取已保存cookie
    handler = request.HTTPCookieProcessor(cookie)
    opener = request.build_opener(handler)


    #pattern_newline= re.compile(r'，|？|。|！|……|：|；')#每一句进行换行
    #pattern_del_blank=re.compile(r' ||的秒拍视频|“|”|、|网页链接|《|》|收起全文d|@|【|】|"|"')#删空格去和微博符号
    #pattern_del=re.compile(r'#.*#')#删掉微博中的主题名
    pattern_chinese =re.compile(u"[\u4e00-\u9fa5]+")
    end_str='抱歉，未找到“'+keyword+'”相关结果。'
    pattern_endweibo=re.compile(end_str)
    pattern1=re.compile('展开全文c')
    pattern_del_sentence=re.compile('的微博视频')
    pattern_save=re.compile(r'【.*?】|《.*?》')
    patterb_firstsen=re.compile(r'[\u4e00-\u9fa5](.*?)。|[\u4e00-\u9fa5](.*?)？|[\u4e00-\u9fa5](.*?)！')
    pattern_time=re.compile(r'..:..')

    sum=0
    spiderip=get_ip()
    for i in range(days):
        data=getday(y,m,d,-i)
        print(data)
        for j in range(24):
            if j==23:
                data_add_hour = data + '-' + str(j) + ':' +getday(y,m,d,-(i-1)) + '-' + str(0)
            else:
                data_add_hour = data + '-' + str(j) + ':' + data + '-' + str(j + 1)
            print(data_add_hour+':')
            for k in range(2):
                url = 'https://s.weibo.com/weibo?q='+url_keyword+'&typeall=1&suball=1&timescope=custom:'+data_add_hour+'&Refer=g&page='+str(k+1)
                user_agent = random.choice(user_agent_list)
                headerscheck = {'User-Agent': user_agent}
                proxy_temp = {"https": spiderip}
                httpproxy_handler = request.ProxyHandler(proxy_temp)
                opener = request.build_opener(httpproxy_handler)
                requ = request.Request(url=url, headers=headerscheck)  # data,#headers
                try:
                    respones = opener.open(requ,timeout=60)  # timeout=10 使用自己建的opener处理requests
                    # cookie.save(ignore_discard=True, ignore_expires=True)  保存cookie
                    web_data = respones.read().decode("utf-8", "ignore")
                    if pattern_endweibo.findall(web_data)!=[]:
                        #print('该时段没有更多结果')
                        break
                    page = etree.HTML(web_data)
                    weibo_list = page.xpath("//div[@mid]")
                    for p in weibo_list:
                        rowNum = sum
                        #print('=============')
                        mid = p.attrib.get('mid')
                        #print(mid)
                        p_time = p.xpath(".//div[@class='content'and @node-type='like']/p[@class='from']/a[@suda-data]")
                        time=p_time[0].xpath('string(.)')

                        sheet.write(rowNum,0,str(data))
                        sheet.write(rowNum,1,pattern_time.findall(time))


                        p_name = p.xpath(".//div[not(@node-type)]/a[@class]")
                        name=p_name[0].xpath('string(.)')

                        sheet.write(rowNum, 2, mid)
                        sheet.write(rowNum, 3, name)

                        p_vip = p.xpath(".//div[not(@node-type)]/a[@title]")
                        if p_vip == []:
                            sheet.write(rowNum, 4, "无")
                        else:
                            vip=p_vip[0].attrib.get('title')
                            sheet.write(rowNum, 4, vip)

                        p_content = p.xpath(".//p[@node-type='feed_list_content']")
                        content=p_content[0].xpath('string(.)')
                        sheet.write(rowNum, 5, content)

                        p_trans = p.xpath(".//p[not(@nick-name )and @node-type='feed_list_content']")
                        if (p_trans == []):
                            sheet.write(rowNum, 6, "无")
                        else:
                            p_trans_herf = p_trans[0].xpath(".//a")
                            #transherf=p_trans_herf[0].attrib.get('href')
                            transcontent=p_trans[0].xpath('string(.)')
                            p_trans_count = p.xpath(".//ul[@class='act s-fr']/li[1]/a")
                            trans_count=p_trans_count[0].xpath('string(.)')
                            p_com_count = p.xpath(".//ul[@class='act s-fr']/li[2]/a")
                            trans_comm=p_com_count[0].xpath('string(.)')
                            sheet.write(rowNum, 6, transcontent)
                            sheet.write(rowNum, 7, trans_count)
                            sheet.write(rowNum, 8, trans_comm)
                            #sheet.write(rowNum, 9, transherf)

                        """
                        if pattern_save.search(content)==None:
                            subject=patterb_firstsen.search(content).group(0)
                        else:
                            subject=pattern_save.search(content)
                            subject=subject.group(0)[1:-1]
                        print(subject)
                        if subject in top_n_dict:
                            top_n_dict[subject] += 1
                        else:
                            top_n_dict[subject] = 1
                        #file.write(str(txt) + '\n')
                        """
                        sum+=1
                except Exception as e:
                    spiderip=get_ip()
                    continue
                    print('error')
                    print(e.code)
        wbk.save('./'+datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d%H%M%S')+'.xls')
        print('save_today')
        #sheet.write(i, 1, str(sum))

def main():
    spider('食品安全',2019,3,1,1)
if __name__ == '__main__':
    main()

