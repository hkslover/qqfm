import requests
import time
import json
from subprocess import call
def get_info(id):
    headers = {'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1'}
    html_content = requests.get('https://fm.qq.com/show/' + id + '__', '',headers=headers).text
    json_str = html_content[html_content.index('__INITIAL_STATE__=')+18:]
    json_str = json_str[:json_str.index('</script>')]
    json_data = json.loads(json_str)
    return json_data
def get_vkey(showmapid):
    headers = {
    'referer': 'https://fm.qq.com/show/' + showmapid + '__',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}
    url = 'https://fm.qq.com/webapp/json/fm_vkey/GetVkey?&guid=10000&inCharset=utf-8&outCharset=utf-8&_=' + str(time.time())
    response = requests.get(url,headers = headers)
    json_data = json.loads(response.text)
    return json_data['data']['vkey']
def get_showidlist(albumid):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
    url = 'https://fm.qq.com/album/' + albumid
    html_content = requests.get(url,headers = headers).text
    data_str = html_content[html_content.index('showIdList: ')+12:].replace(' ','').replace('\n','').replace('\t','')
    data_str = data_str[:data_str.index(',displayPageNum')]
    showidlist = eval(data_str)
    return showidlist
def deal(albumid):
    IDM = r'D:\Internet Download Manager\IDMan.exe'
    DownPath = r'D:\audio'
    #f = open('data.txt','w')
    showidlist = get_showidlist(albumid)
    #map_num = len(json_data['syncData']['showMap'])
    for showid in showidlist:
        json_data = get_info(showid)
        name = json_data['syncData']['showMap'][showid]['show']['name'].replace(' ','') + '.m4a'
        _url = json_data['syncData']['showMap'][showid]['show']['audioURL']['urls']['0']['url']
        vkey = get_vkey(showid)
        play_url = _url + '&vkey=' + vkey + '&guid=10000'
        #f.write(str(name + '|' + play_url) + '\n')
        call([IDM, '/d',play_url, '/p',DownPath, '/f', name, '/n', '/a'])
        #print(name,play_url)
if __name__ == "__main__":
    deal('rd000ykAOz1jIKCK')