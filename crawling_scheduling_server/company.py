#-*- coding:utf-8 -*-
import urllib.request
import bs4
import openpyxl # pip install openpyxl
import pymysql # pip install pymysql
import re
from datetime import datetime
from time import sleep

def get_bsobj(url):
    """
    bs_obj를 리턴
    """
    html = urllib.request.urlopen(url)
    bs_obj = bs4.BeautifulSoup(html, "html.parser") # url에 해당하는 html이 bsObj에 들어감

    return bs_obj

def make_connection(db_name):
    """
    DB GET CONNECTION
    """
    conn = pymysql.connect(host='13.125.213.221', user='root', password='TestAdmin1234!', db=db_name, charset='utf8')
    
    return conn

def select_query(conn):
    """
    DB SELECT
    """
    try:
        with conn.cursor() as cursor:
            sql = "select * from aa;" # hoho 여기엔 테이블 이름
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
    finally:
        pass

def insert_query(conn, recruit_name, company_id, company_occupation, company_category, recruitment_school, work_location, pay, position, start_day, finish_day, require_documents, status, require_how_many):
    """
    DB INSERT
    """
    try:
        with conn.cursor() as cursor:
            sql = "insert into recruitment (recruit_name, company_id, company_occupation, company_category, recruitment_school, work_location, pay, position, start_day, finish_day, require_documents, status, require_how_many) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (recruit_name, company_id, company_occupation, company_category, recruitment_school, work_location, pay, position, start_day, finish_day, require_documents, status, require_how_many))
        conn.commit()
        print(cursor.lastrowid)
    finally:
        pass
    #     conn.close()


def insert_query_company(conn, company_name, company_founded_date, company_scale, company_sector, company_url, company_location):
    """
    DB INSERT
    """
    try:
        with conn.cursor() as cursor:
            sql = "insert into Company (company_name, company_founded_date, company_scale, company_sector, company_url, company_location) values(%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (company_name, company_founded_date, company_scale, company_sector, company_url, company_location))
        conn.commit()
        print(cursor.lastrowid)
    finally:
        pass

def update_query(conn):
    """
    DB UPDATE
    """
    try:
        with conn.cursor() as cursor:
            sql = "update hoho set aa=%s where bb=%s"
            cursor.execute(sql, ("hihihi", "하하하"))
        conn.commit()
        print(cursor.rowcount) # affected rows
    finally:
        conn.close()

def delete_query(conn):
    """
    DB DELETE
    """
    try:
        with conn.cursor() as cursor:
            sql = "delete from hoho where aa=%s"
            cursor.execute(sql, ("히히히"))
        conn.commit()
        print(cursor.rowcount) # affected rows
    finally:
        conn.close()

def main():

    conn = make_connection('hanium')

    # driver = webdriver.Chrome("./chromedriver.exe")
    url = "http://job.incruit.com/jobdb_list/searchjob.asp"
    query = "?ct=1&ty=1&cd=150&page={}"
    
    all_urls = [] # http://job.incruit.com/jobdb_list/searchjob.asp?ct=1&ty=1&cd=150&page=58
    links= []
    result_dic = {}
    

    for i in range(1,2): # 1 ~ 58 url 모두 담기
        query.format(i)
        uri = url + query.format(i)
        all_urls.append(uri)
        print(uri)

    print("=================")

    for i in range(0,len(all_urls)):
        print(all_urls[i])
        bs_obj = get_bsobj(all_urls[i])
        div = bs_obj.find("div",{"class":"n_job_list_default"})
        
        table = div.find("div",{"class":"n_job_list_table_a"})
        
        a_tags = table.findAll("a",{"class":"links"})

        for j in range(0,len(a_tags)):
            links.append(a_tags[j]["href"])
            
        print(len(links))
    for i in range(0,len(links)):
        print(links[i])

    for i in range(0,len(links)):
        print("=================")

        reuslt_value_list = [] # 공고 내용을 담는 list

        job_link = get_bsobj(links[i])

        # p = re.findall('\d', links[i])

        # link_key = ""

        # for i in p:
        #     link_key += i

        # print(p)
        # print(link_key)
        # print(len(result_dic))

        title = job_link.find("div",{"class":"jobview_top_title"})
        job_title = title.find("strong").text
        company_name = title.find("span").text
        
        reuslt_value_list.append(links[i])

        print(job_title.strip().strip()) # 공고 제목
        reuslt_value_list.append(job_title)
        print(company_name.strip().strip()) # 회사 이름
        reuslt_value_list.append(company_name.strip())

        div_left = job_link.find("div",{"class":"jobpost_sider_cpinfo_table"})
        
        try:
            left_dls = div_left.findAll("dl")
        except:
            left_dls = "None"
            
        try:
            born_date = left_dls[0].find("p").text # 설립일
        except:
            born_date = "None"

        try:
            company_size = left_dls[1].find("a").text # 기업 규모(중소, 대)
        except:
            company_size = "None"

        try:
            company_category = left_dls[2].find("p").text # 업종
        except:
            company_category = "None"

        try:
            company_url = left_dls[3].find("a")["href"] # 회사 홈페이지
        except:
            company_url = "None" # 회사 홈페이지

        try:
            div_right = job_link.find("div",{"class":"jobpost_sider_jbinfo"})
            divs = div_right.findAll("div",{"class":"jobpost_sider_jbinfo_inlay"})

            if(len(divs)>1):

                right_dls = divs[0].findAll("dl")
                
                try:
                    recruitment_work = right_dls[0].find("div",{"class":"inset_ely_lay"}).text # 모집 직종
                except:
                    recruitment_work = "None"

                try:
                    recruitment_how_many = right_dls[1].find("div",{"class":"inset_ely_lay"}).text # 모집 인원
                except:
                    recruitment_how_many = "None"
                
                try:
                    right_dls = divs[1].findAll("dl")
                except:
                    right_dls = "None"
                
                try:
                    recruitment_condition = right_dls[0].find("em",{"class":"pt_txt"}).text # 신입, 경력
                except:
                    recruitment_condition = "None"
                
                try:
                    recruitment_school = right_dls[1].find("em",{"class":"pt_txt"}).text # 학력
                except:
                    recruitment_school = "None"

                try:
                    right_dls = divs[2].findAll("dl")
                    recruitment_form = right_dls[0].find("em",{"class":"pt_txt"}).text # 고용형태(정규직, 인턴)
                except:
                    recruitment_form = "None"
                
                try:
                    work_location = right_dls[1].find("div",{"class":"inset_ely_lay"}).text # 근무지역
                except:
                    work_location = "None"
                
                try:    
                    pay = right_dls[2].find("div",{"class":"inset_ely_lay"}).text # 급여
                except:
                    pay = "None"
                    
                try:
                    position = right_dls[3].find("div",{"class":"inset_ely_lay"}).text # 직급
                except:
                    position = "None"

            else:
                right_dls = divs[0].findAll("dl")
                try:
                    born_date = right_dls[0].find("div",{"class":"inset_ely_lay"}).text # 설립일
                except:
                    born_date = "None"
                try:
                    company_size_div = right_dls[2].find("div",{"class":"inset_ely_lay"}) # 기업 규모
                    company_size = company_size_div.find("a").text
                except:
                    company_size = "None"
                try:
                    company_category_div = right_dls[4].find("div",{"class":"inset_ely_lay"}) # 업종
                    company_category = company_size_div.find("a").text
                except:
                    company_category = "None"
                try:
                    company_url_div = right_dls[5].find("div",{"class":"inset_ely_lay"}) # 회사 홈페이지
                    company_url = company_size_div.find("a")["href"]
                except:
                    company_url = "None"

        except:
            recruitment_work = "None"
            recruitment_how_many = "None"
            recruitment_condition = "None"
            recruitment_school = "None"
            recruitment_form = "None"
            work_location = "None"
            pay = "None"
            position = "None"

        print(born_date.strip())
        reuslt_value_list.append(born_date.strip())
        print(company_size.strip())
        reuslt_value_list.append(company_size.strip())
        print(company_category.strip())
        reuslt_value_list.append(company_category.strip())
        print(company_url.strip())
        reuslt_value_list.append(company_url.strip())

        print(recruitment_work.strip())
        reuslt_value_list.append(recruitment_work.strip())
        print(recruitment_how_many.strip())
        reuslt_value_list.append(recruitment_how_many.strip())
        print(recruitment_condition.strip())
        reuslt_value_list.append(recruitment_condition.strip())
        print(recruitment_school.strip())
        reuslt_value_list.append(recruitment_school.strip())
        print(recruitment_form.strip())
        reuslt_value_list.append(recruitment_form.strip())
        print(work_location.strip())
        reuslt_value_list.append(work_location.strip())
        print(pay.strip())
        reuslt_value_list.append(pay.strip())
        print(position.strip())
        reuslt_value_list.append(position.strip())

        try:    
            jobview_receipt_layout1 = job_link.find("div",{"class":"jobview_receipt_layout1"})
        
            jobview_receipt_daybox = jobview_receipt_layout1.find("div",{"class":"jobview_receipt_daybox"})
        except:
            pass

        try:
            dds = jobview_receipt_daybox.findAll("dd")
            start_day = dds[0].find("strong").text

            # datetime으로 변경하는 코드
            # p = re.findall('[\d.\d.\d]', start_day)
            # day =""
            # for j in p:
            #     day += j
            # # print(day)

            # start_day = datetime.strptime(day, '%Y.%m.%d')

            finish_day = dds[1].find("strong").text
            
            # datetime으로 변경하는 코드
            # p1 = re.findall('[\d.\d.\d]', finish_day)
            # p2 = re.findall('[\d:\d]', finish_day)

            # finish_day = ""

            # for k in range(0,10):
            #     finish_day += p1[k]

            # finish_hour = ""

            # for l in range(8,len(p2)):
            #     finish_hour += p2[l]

            # finish_day = finish_day + " " + finish_hour
            # finish_day = datetime.strptime(finish_day, '%Y.%m.%d %H:%M')

        except:
            start_day = "None"
            finish_day = "None"
        
        print(start_day) # 모집 시작일
        reuslt_value_list.append(start_day)
        print(finish_day) # 모집 마감일
        reuslt_value_list.append(finish_day)

        jobview_receipt_layout2 = job_link.find("div",{"class":"jobview_receipt_layout2"})
        try:
            require_documents = jobview_receipt_layout2.find("td").text
        except:
            require_documents = "인크루트 이력서"

        print(require_documents.strip()) # 필요 서류
        reuslt_value_list.append(require_documents.strip())

        print(reuslt_value_list)

        # sleep(0.5)

        print(links[i])

        p = re.findall('\d', links[i])

        link_key = ""

        for m in p:
            link_key += m

        result_dic[link_key] = reuslt_value_list
        # insert_query(conn, link_key, links[i], title, company_name, born_date, company_size, company_category, company_url, recruitment_work, recruitment_how_many, recruitment_condition, recruitment_school, recruitment_form, work_location, pay, position, start_day, finish_day, require_documents, 0)
        insert_query_company(conn, company_name, born_date, company_size, company_category, company_url, "")
    print(result_dic)

    print(len(links))

    # save_excel(result_dic)
    conn.close()

if __name__ == "__main__":
    main()