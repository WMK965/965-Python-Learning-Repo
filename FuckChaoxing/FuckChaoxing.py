import requests
import json
import os, sys
import urllib.request
import re
import time
import random
from bs4 import BeautifulSoup
import configparser


folder = ""  # 创建子目录文件夹名称

# headers_0 用于登录
headers_0 = {'Accept-Language': 'zh_CN',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': '62',
            'Host': 'passport2-api.chaoxing.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip'}
# headers_1用于打开任务点card页面
headers_1 = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Host': 'mooc1.chaoxing.com',
    'Upgrade-Insecure-Requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    'Pragma': 'no-cache',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1'}
# headers_2用于下载
headers_2 = {'Accept': '*/*'}
# headers3用于抓取任务点列表json
headers_3 = {
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9; Realme X MIUI/V11.0.3.0.PFJCNXM) com.chaoxing.mobile/ChaoXingStudy_3_4.5.1_android_phone_582_41 (@Kalimdor)_17efb19783494fdaa77aa853ce115c6a',
    'Host': 'mooc1-api.chaoxing.com'}
# headers_4用于获取目标下载文件json
headers_4 = {
    'Host': 'mooc1-api.chaoxing.com',
    'Connection': 'keep-alive',
    "User-Agent": 'Mozilla/5.0 (Linux; Android 9; SAMSUNG SM-G960U Build/PKQ1.190302.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/94.0.4606.102 Mobile Safari/537.36 (device:Realme X) Language/zh_CN com.chaoxing.mobile/ChaoXingStudy_3_5.1.4_android_phone_614_74 (@Kalimdor)_17efb19783494fdaa77aa853ce115c6a',
    'X-Requested-With': 'XMLHttpRequest',
    'Accept': '*/*',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'

}


# 在根目录下创建一个新文件夹
def create_folder(path):
    is_exist = os.path.exists(path)
    # 判断结果
    if not is_exist:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        print(path, '创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')
        return False


# 下载功能相关函数
def getfile(url, label, passname=None):
    opener = urllib.request.build_opener()
    opener.addheaders = [('Accept', '*/*'), ('Accept-Encoding', 'identity'), ('Accept-Language', 'zh-CN'), ('Accept-Charset', '*'), ('Referer', 'http://d0.ananas.chaoxing.com/download/')]
    urllib.request.install_opener(opener)
    if passname:
        fileName = passname
        urllib.request.urlretrieve(url, folder + '/' + fileName, Schedule)
    else:
        r = urllib.request.urlopen(url)
        if 'Content-Disposition' in r.info():
            filename = label + '_' + r.info()['Content-Disposition'].split('filename=')[1][
                                     :r.info()['Content-Disposition'].split('filename=')[1].find(';')].encode(
                'latin1').decode('utf-8')
            filename = filename.replace('"', '').replace("'", "")
            print(filename)

        elif r.url != url:
            # if we were redirected, the real file name we take from the final URL
            from os.path import basename
            from urllib.parse import urlsplit
            filename = basename(urlsplit(r.url)[2])
        else:
            filename = os.path.basename(url)
        urllib.request.urlretrieve(r.url, filename)


# 下载进度条
def Schedule(blocknum, blocksize, totalsize):
    speed = (blocknum * blocksize) / (time.time() - start_time)
    # speed_str = " Speed: %.2f" % speed
    speed_str = " Speed: %s" % format_size(speed)
    recv_size = blocknum * blocksize

    # 设置下载进度条
    f = sys.stdout
    percent = recv_size / totalsize
    percent_str = "%.2f%%" % (percent * 100)
    n = round(percent * 50)
    s = ('#' * n).ljust(50, '-')
    f.write(percent_str.ljust(8, ' ') + '[' + s + ']' + speed_str)
    f.flush()
    # time.sleep(0.1)
    f.write('\r')


# 字节bytes转化K\M\G
def format_size(bytes):
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except:
        print("传入的字节格式不对")
        return "Error"
    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            return "%.3fG" % (G)
        else:
            return "%.3fM" % (M)
    else:
        return "%.3fK" % (kb)


# 登录功能
def login(username, password):
    lgdata = {'uname': username,
              'code': password,
              'loginType': 1,
              'roleSelect': 'true'}
    lgresponse = seesion.post('https://passport2-api.chaoxing.com/v11/loginregister?cx_xxt_passport=json', lgdata,
                              headers=headers_0)
    print(lgresponse.text)


# 获取任务点dict
def get_data(class_id):
    response = seesion.get('https://mooc1-api.chaoxing.com/gas/clazz?id=' + str(
        class_id) + '&personid=110701074&fields=id,bbsid,classscore,isstart,allowdownload,chatid,name,state,isthirdaq,isfiled,information,discuss,visiblescore,begindate,coursesetting.fields(id,courseid,hiddencoursecover,hiddenwrongset),course.fields(id,name,infocontent,objectid,app,bulletformat,mappingcourseid,imageurl,teacherfactor,knowledge.fields(id,name,indexOrder,parentnodeid,status,layer,label,begintime,endtime,attachment.fields(id,type,objectid,extension).type(video)))&view=json',
                           headers=headers_3)
    print(response.text)
    return json.loads(response.text)


def getclass_id(courseid):
    response = seesion.get('https://mooc1-api.chaoxing.com/gas/course?id=' + str(
        courseid) + '&userid=119709934&personid=129170339&fields=role%2Cbbsid%2Cbulletformat%2Cteacherfactor%2Cobjectid%2Cid%2Cinfocontent%2Cschools%2Cname%2Cmappingcourseid%2Cclassscore%2Cimageurl%2Cisfiled%2Ccreaterid%2Ccoursestate%2Cclazz.fields(id%2Cname%2Cchatid%2Cbbsid%2Cstudentcount%2Cinvitecode).rankid(2)%2Ccoursesetting.fields(id%2Ccourseid%2Chiddencoursecover)&isteachcourse=true&view=json',
                           headers=headers_3)
    data = json.loads(response.text)
    clazz = data["data"][0]["clazz"]["data"]

    # 判断是否为空值，没有班级
    if clazz:
        cls_list = []
        i = 0
        for cls_info in clazz:
            class_id = cls_info["id"]
            classname = cls_info["name"]
            stunum = cls_info["studentcount"]
            print(i, class_id, classname, stunum)
            cls_list.append(cls_info["id"])
            i += 1
        i = int(input('选择班级：'))
        class_id = cls_list[i]
    return class_id


def file_downloader(downloaddata):
    filelink = downloaddata['download']
    filename = label + '-' + downloaddata['filename']
    # 文件下载归类
    if not os.path.exists(folder + '/' + filename):
        print(filename, filelink)
        try:
            getfile(filelink, '', passname=filename)
        except:
            print(filename, object_id, "下载失败")
    else:
        print(filename, '已存在')


def ppt_downloader(downloaddata):
    if 'ppt' in downloaddata['filename'] or 'pdf' in downloaddata['filename']:
        # 下载一般文件的办法
        filelink = downloaddata['download']
        filename = label + '-' + downloaddata['filename']
        # 文件下载归类
        if not os.path.exists(folder + '/' + filename):
            print(filename, filelink)
            try:
                getfile(filelink, '', passname=filename)
            except:
                print(filename, object_id, "下载失败")
        else:
            print(filename, '已存在')


def video_downloader(downloaddata):
    if 'rmvb' in downloaddata['filename'] or '3gp' in downloaddata['filename'] or 'mpg' in downloaddata[
        'filename'] or 'mpeg' in downloaddata['filename'] or 'mov' in downloaddata['filename'] or 'wmv' in downloaddata[
        'filename'] or 'avi' in downloaddata['filename'] or 'mkv' in downloaddata['filename'] or 'mp4' in downloaddata[
        'filename'] or 'flv' in downloaddata['filename'] or 'vob' in downloaddata['filename'] or 'f4v' in downloaddata[
        'filename']:
        # 下载一般文件的办法
        filelink = downloaddata['download']
        filename = label + '-' + downloaddata['filename']
        # 文件下载归类
        if not os.path.exists(folder + '/' + filename):
            print(filename, filelink)
            try:
                getfile(filelink, '', passname=filename)
            except:
                print(filename, object_id, "下载失败")
        else:
            print(filename, '已存在')


def read_credentials(config_file):
    """从配置文件读取账号和密码"""
    config = configparser.ConfigParser()
    config.read(config_file, encoding='utf-8')  # 读取配置文件
    try:
        username = config['login']['username']
        password = config['login']['password']
        return username, password
    except KeyError as e:
        print(f"配置文件错误：{e}")
        return None, None


def main(object_id):
    global start_time
    jdownloaddata = seesion.get("https://mooc1.chaoxing.com/ananas/status/" + object_id, headers=headers_4)
    print(jdownloaddata.text)
    if jdownloaddata.status_code == 404:
        print(404)
        return
    downloaddata = json.loads(jdownloaddata.text)
    start_time = time.time()
    # 根据下载模式选择函数
    if down_method == 1:
        ppt_downloader(downloaddata)
    elif down_method == 2:
        video_downloader(downloaddata)
    elif down_method == 0 or down_method == 4:
        file_downloader(downloaddata)

    # 开始pdf下载
    # 判断有无pdf文件
    # 下载pdf文件的
    '''
    print(str(knowledgeid)+"有pdf文件")
    pdflink=downloaddata['pdf']
    re2=r'"filename":"(.*?)\.'
    print(re.findall(re2, jdownloaddata))
    pdffilename=re.findall(re2, jdownloaddata)[0]+".pdf"
    '''


start_time = 0
seesion = requests.session()
config_file = "account.ini"
username, password = read_credentials(config_file)
login(username, password)  # 登录
course_id = int(input('输入courseid:'))
class_id = getclass_id(course_id)
data = get_data(class_id)  # 获取任务点dict
folder = data['data'][0]["course"]['data'][0]["name"]
create_folder(folder)
i = 0
knowledge = data['data'][0]["course"]['data'][0]["knowledge"]['data']  # 取出知识点列表
print("请选择下载模式")
print(0, "下载所有文件")
print(1, "下载PPT+PDF")
print(2, "下载视频文件")
print(3, "下载所有文档（PDF格式）")
print(4, "下载指定knowledgeid资源")
down_method = int(input('下载模式：'))
kid_list = []
for i in range(len(knowledge)):
    knowledgeid = knowledge[i]['id']
    kid_list.append(knowledgeid)
print(kid_list)
down_list = []
if down_method == 4:
    knowledge_id = int(input('输入knowledgeid：'))
    down_list.append(knowledge_id)
else:
    down_list = kid_list
for i in range(len(down_list)):
    knowledgeid = down_list[i]
    print(knowledgeid)
    if down_method == 4:
        u = kid_list.index(down_list[i])
        label = knowledge[u]['label']
    else:
        label = knowledge[i]['label']
    num = 0
    rs = seesion.get(
        'https://mooc1-api.chaoxing.com/gas/knowledge?id={}&fields=id%2Cparentnodeid%2Cindexorder%2Clabel%2Clayer%2Cname%2Cbegintime%2Ccreatetime%2Clastmodifytime%2Cstatus%2CjobUnfinishedCount%2Cclickcount%2Copenlock%2Ccard.fields(id%2Cknowledgeid%2Ctitle%2CknowledgeTitile%2Cdescription%2Ccardorder).contentcard(all)&view=json'.format(
            knowledgeid), headers=headers_3)
    tab_num = len(json.loads(rs.text)['data'][0]['card']['data'])
    if tab_num == 0:
        continue
    while num <= tab_num:
        response = seesion.get(
            "https://mooc1.chaoxing.com/knowledge/cards?courseid={}&clazzid={}&knowledgeid={}&num={}".format(
                str(course_id), str(
                    class_id), str(knowledgeid), str(num)), headers=headers_1)
        card_html = response.text
        # 开始匹配附件
        if "objectid" in card_html:  # 判断有无附件
            print(knowledgeid, "有附件")
            # re1 = r'mArg = {(.*?);'  # 抓attachment数据（json）
            soup = BeautifulSoup(card_html, 'lxml')
            iframe_list = soup.find_all('iframe')
            object_id_list = []
            for iframe in iframe_list:
                if "data" in iframe.attrs.keys() and "objectid" in iframe.get('data'):
                    object_data = json.loads(iframe.get('data'))
                    try:
                        object_id = object_data['objectid']  # 拿到objectid
                        object_id_list.append(object_id)
                    except:
                        continue
            print(object_id_list)
            for object_id in object_id_list:
                main(object_id)
        elif "验证码" in card_html:
            # 处理反爬虫验证码：清除cookie，重新登录
            print("出现反爬虫验证码，正在重试")
            seesion.close()
            seesion.cookies.clear()
            login(username, password)
            continue
        num = num + 1
        time.sleep(random.randint(1, 3))
    time.sleep(random.randint(1, 3))
