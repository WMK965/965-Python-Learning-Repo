# Script made by 965
import requests
import json
import ast
import time
import os

#Bing_24-09-07_23
console_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
json_url = 'https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1'
url_suffix = '_UHD.jpg&rf=LaDigue_UHD.jpg&pid=hp&w=3840&h=2160&rs=1&c=4'
folder_name = 'image'
filename = 'Bing_' + time.strftime("%Y-%m-%d_%H", time.localtime())[2:] + '.jpg'
filename_reg = str(filename)

if os.path.exists(f'./{folder_name}') is False:
    os.popen('mkdir image')
    print(f'[{console_time}]Making directory <image>')
else:
    print(f'[{console_time}]Directory exist, Downloading image...')
try:
    response = requests.get(json_url)
    response = json.loads(response.text)
    response = str(response['images'])[1:-1]
    response = ast.literal_eval(response)
    url = json_url[:20] + response['urlbase'] + url_suffix
except:
    print(f'[{console_time}]Url processing failure')
try:
    open(f'./{folder_name}/{filename_reg}', 'wb').write(requests.get(url).content)
    print(f'[{console_time}]Image download successful')
except:
    print(f'[{console_time}]Image download failure')
