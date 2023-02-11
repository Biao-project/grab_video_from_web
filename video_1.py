from sys import exit
import requests
import os
import time
import threading

from bs4 import BeautifulSoup

from buildThread import ThreadPool_alone as ThreadPool
header = {
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        # 'Content-Length': 6042,
        'Content-Type': 'text/html;charset=utf-8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'from=undefined; from=undefined; errortime=0; JSESSIONID=E017A07DD228275CDBD9B2176DBA1D60',
        'Referer': 'http://116.57.72.197:9099/index.html',  # /login/pre.html
        'User-Agent': 'Mozilla/5.0 (Windows NT 11.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.182 Safari/537.36'
    }

header2 = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'istips=1; __tins__21076419=%7B%22sid%22%3A%201636613704517%2C%20%22vd%22%3A%201%2C%20%22expires%22%3A%201636615504517%7D; __51cke__=; __51laig__=1',
        'Host': 'www.mmhse5.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }

header3 = {
        # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        # 'Accept-Encoding': 'gzip, deflate',
        # 'Accept-Language': 'zh-CN,zh;q=0.9',
        # 'Cache-Control': 'max-age=0',
        # 'Connection': 'keep-alive',
        'Cookie': '__tins__21076419=%7B%22sid%22%3A%201636613704517%2C%20%22vd%22%3A%201%2C%20%22expires%22%3A%201636615504517%7D',
        'Host': 'www.mmhse5.com',
        # 'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }

'''下载ts视频文件'''
def downLoad_video_ts(url, path):
    # try:
    session = requests.session()
    resdata = session.get(url=url, headers=header, timeout=10)
    resdata.raise_for_status()
    resdata.encoding = 'utf-8'
    with open(path, 'wb') as f:
        f.write(resdata.content)
    return True
    # except:
    #     print('请求失败！', url, path)
    #     return url, path

'''将下载的多个ts视频文件，合并成一个文件'''
def merge_ts_files(ts_path, Vname: str = None):
    ts_files = os.listdir(ts_path)
    sizes = len(ts_files)
    # ts_files.sort()
    # print(ts_files)
    # return 0
    if Vname is None or '.' not in Vname:
        n = time.localtime(time.time())
        time_name = time.strftime("%Y-%m-%d_%H.%M.%S", n)
        Vname = time_name + '.mp4'
    Vname = ts_path + '\\' + str(Vname)
    print('整合Video：', Vname)
    with open(Vname, 'wb') as ff:
        for i in range(1, sizes + 1):
            name = ts_path + '\\' + '%04d.ts' % i
            # print('\r {}/{} :{}'.format(i, sizes + 1, name), end='')
            with open(name, 'rb') as fr:
                ff.write(fr.read())
            os.remove(name)

    pass

def grab_mmhse_player(url, path=None, Videoname=None, fmt='1', isload=True):
    # url = r'http://www.mmhse5.com/Public/player/player5.html?url=\x68\x74\x74\x70\x73\x3a\x2f\x2f\x76\x69\x64\x65\x6f\x7a\x6d\x2e\x77\x68\x71\x68\x79\x67\x2e\x63\x6f\x6d\x3a\x38\x30\x39\x31\x2f\x32\x30\x32\x30\x30\x37\x31\x36\x2f\x6d\x39\x5a\x55\x48\x78\x46\x43\x2f\x69\x6e\x64\x65\x78\x2e\x6d\x33\x75\x38'
    if url is None: return
    if path is None:
        path = r'F:\迅雷下载\video_grab'
    try:
        os.makedirs(path)
    except: pass
    print('视频保存路径：', path)
    session = requests.session()

    ss_index = url.find('=') + 1
    ss = url[ss_index:].split('\\x')
    ss_url = ''
    for sc in ss:
        if sc == '': continue
        ss_url += chr(int(sc, 16))
    # ss_url = r'https://videozm.whqhyg.com:8091/20200716/m9ZUHxFC/index.m3u8'
    print('视频服务器索引：', ss_url)

    resdata = session.get(url=ss_url, headers=header, timeout=1000)
    if not isload: print('视频服务器索引：[data]\n', resdata.text)
    if fmt == '2':
        video_ts_idx = resdata.text.split('\n')[2]
        url_video_ts_idx = ss_url[:ss_url.rfind('/') + 1] + video_ts_idx
        print('url_video_ts_idx:', url_video_ts_idx)
        resdata = session.get(url=url_video_ts_idx, headers=header, timeout=1000)
        if not isload: print('视频ts文件索引：[data]\n', resdata.text)
    else : url_video_ts_idx = ss_url[:ss_url.rfind('/') + 1]
    if not isload: return 0


    video_ts_data = resdata.text.split('\n')
    threadPool = ThreadPool(200, reRun=True)
    path_root = path   ## r'G:\pythonFiles\00-files\grab_video'
    num = 0
    for i, ts_name in enumerate(video_ts_data):
        if not ts_name.endswith('.ts'): continue
        url_video_ts = url_video_ts_idx[:url_video_ts_idx.rfind('/') + 1] + ts_name
        # print(url_video_ts)
        num += 1
        name = path_root + '\\' + '%04d.ts' % num
        print('\r download {}/{}'.format(i, len(video_ts_data)), end='')
        threadPool.run(target=downLoad_video_ts, args=(url_video_ts, name))
        # downLoad_video_ts(url_video_ts, name)
    print('\nfinish download! \t\ttemp path=', path_root)
    # print('\n')
    threadPool.join(60 * 5, ishow=True)
    merge_ts_files(path_root, Vname=Videoname)
    pass


def grap_video():

    url = r'http://www.mmhse5.com/Public/player/player5.html?url=\x68\x74\x74\x70\x73\x3a\x2f\x2f\x76\x69\x64\x65\x6f\x7a\x6d\x2e\x77\x68\x71\x68\x79\x67\x2e\x63\x6f\x6d\x3a\x38\x30\x39\x31\x2f\x32\x30\x32\x30\x30\x37\x31\x36\x2f\x6d\x39\x5a\x55\x48\x78\x46\x43\x2f\x69\x6e\x64\x65\x78\x2e\x6d\x33\x75\x38'
    url2 = r'http://www.mmhse5.com/play/256038-3-1.html'
    url3 = 'https://videozm.whqhyg.com:8091/20200716/m9ZUHxFC/1000kb/hls/tvULPs8J.ts'
    url4 = 'https://videozm.whqhyg.com:8091/20200716/m9ZUHxFC/index.m3u8'
    url5 = 'https://hao.youaima.com/down.html'
    url6= r'https://b1.cdn.mh3666.com/Public/js/jquery.index.js?t='+str(time.time())
    path_root = r'G:\pythonFiles\00-files\grab_video'
    # grab_mmhse(url, path_root)


    ss = r'%2f%50%75%62%6c%69%63%2f%70%6c%61%79%65%72%2f%70%6c%61%79%65%72%35%2e%68%74%6d%6c%3f%75%72%6c%3d%5c%78%36%38%5c%78%37%34%5c%78%37%34%5c%78%37%30%5c%78%37%33%5c%78%33%61%5c%78%32%66%5c%78%32%66%5c%78%36%33%5c%78%33%32%5c%78%33%32%5c%78%32%65%5c%78%36%33%5c%78%36%34%5c%78%36%65%5c%78%32%65%5c%78%36%34%5c%78%37%39%5c%78%36%33%5c%78%37%30%5c%78%33%34%5c%78%33%34%5c%78%33%34%5c%78%32%65%5c%78%36%33%5c%78%36%66%5c%78%36%64%5c%78%32%66%5c%78%33%32%5c%78%33%30%5c%78%33%31%5c%78%33%39%5c%78%33%31%5c%78%33%30%5c%78%32%66%5c%78%33%30%5c%78%33%36%5c%78%32%66%5c%78%36%34%5c%78%33%36%5c%78%37%30%5c%78%33%31%5c%78%35%31%5c%78%33%39%5c%78%34%62%5c%78%35%37%5c%78%32%66%5c%78%33%35%5c%78%33%30%5c%78%33%30%5c%78%36%62%5c%78%36%32%5c%78%32%66%5c%78%36%38%5c%78%36%63%5c%78%37%33%5c%78%32%66%5c%78%36%39%5c%78%36%65%5c%78%36%34%5c%78%36%35%5c%78%37%38%5c%78%32%65%5c%78%36%64%5c%78%33%33%5c%78%37%35%5c%78%33%38%5c%78%33%66%5c%78%37%33%5c%78%36%39%5c%78%36%37%5c%78%36%65%5c%78%33%64%5c%78%37%31%5c%78%35%66%5c%78%36%66%5c%78%35%39%5c%78%36%64%5c%78%35%66%5c%78%35%33%5c%78%37%32%5c%78%36%31%5c%78%34%39%5c%78%34%63%5c%78%35%61%5c%78%34%61%5c%78%33%33%5c%78%34%33%5c%78%37%35%5c%78%37%31%5c%78%35%34%5c%78%34%63%5c%78%37%33%5c%78%35%35%5c%78%36%37%5c%78%32%36%5c%78%37%34%5c%78%33%64%5c%78%33%31%5c%78%33%36%5c%78%33%33%5c%78%33%36%5c%78%33%37%5c%78%33%30%5c%78%33%35%5c%78%33%34%5c%78%33%37%5c%78%33%34'
    '# '
    ss = ss.split('%')
    ss_url = ''
    for sc in ss:
        if sc == '': continue
        ss_url += chr(int(sc, 16))
    ss_url = r'http://www.mmhse5.com' + ss_url
    print('ss_url=', ss_url)
    grab_mmhse_player(ss_url, None, Videoname=None, fmt='2', isload=True)




    exit()
    session = requests.session()
    resdata = session.get(url=url5, headers=header2, timeout=1000)
    print(resdata.text)






if __name__ == '__main__':
    grap_video()
    exit()

