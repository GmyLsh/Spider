from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from lxml import etree
import csv
import re
import time
class TaoBaoSpider(object):
    def __init__(self,keyword):
        self.url="https://www.taobao.com/"
        self.driver=webdriver.Chrome()
        self.driver.maximize_window()
        self.keyword=keyword

    def search_and_click(self):
        #访问淘宝网首页
        self.driver.get(self.url)
        #查找输入框，然后传入要查找的关键字
        WebDriverWait(self.driver,10).until(lambda driver:self.driver.find_element_by_id("q")).send_keys(self.keyword)
        #查找搜索按钮，点击按钮
        WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_class_name("btn-search")).click()

    def get_page_code(self):
        #从1开始循环，每隔两次循环一次，x的值(1,3,5,7,9)
        for x in range(1,9,2):
            i=x/10
            print("i的值是%s"%i)
            #document.documentElement.scrollHeight:获取整个页面的高度
            #document.documentElement.scrollTop：每次滚动距离最上边的高度
            js="document.documentElement.scrollTop=document.documentElement.scrollHeight*%f"%i
            self.driver.execute_script(js)
            time.sleep(2)
        self.parse_html(self.driver.page_source)
        #找到下一页标签进行点击
        try:
            WebDriverWait(self.driver, 30).until(lambda driver: self.driver.find_element_by_link_text("下一页")).click()
        except Exception as  e:
            print("没有下一页了")
        else:
            self.get_page_code()
    def parse_html(self,page_source):
        html_obj = etree.HTML(page_source)
        div_list = html_obj.cssselect(".info-cont")
        for div in div_list:
            shop_name = div.cssselect(".product-title")[0].get("title")
            try:
                shop_price = div.cssselect("strong")[0]
            except Exception as e:
                shop_price = "未知"
            else:
                shop_price = shop_price.text
            try:
                pay_num = div.cssselect(".num")[0]
            except Exception as e:
                pay_num="0"
            else:
                pay_num=pay_num.text
            sale_num = div.cssselect(".seller>a")[0].text
            pattern_obj=re.compile("(\d+)")
            sale_num=re.search(pattern_obj,sale_num)[1]
            print(shop_name, shop_price, pay_num, sale_num)
            dict_info={"商品名称":shop_name,"商品价格":shop_price,"付款人数":pay_num,"在售商家数量":sale_num}
            writer.writerow(dict_info)

if __name__ == '__main__':
   key_word=input("请输入要爬取的商品名称:")
   with open("%s.csv"%key_word,"w",encoding="utf-8",newline="") as f:
       writer=csv.DictWriter(f,["商品名称","商品价格","付款人数","在售商家数量"])
       writer.writeheader()
       taobao=TaoBaoSpider(key_word)
       taobao.search_and_click()
       taobao.get_page_code()