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
    'Accept-Ranges': bytes,
    'Access-Control-Allow-Headers': 'X-Requested-With',
    'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
    'Access-Control-Allow-Origin': '*',
    'Content-Length': 787344,
    'Content-Type': 'video/mp2t',
    'Date': 'Wed, 29 Dec 2021 12:01:40 GMT',
    'ETag': "613b6143-c0390",
    'Last-Modified': 'Fri, 10 Sep 2021 13:44:35 GMT',
    'Server': 'Tengine',
    'X-Cache': 'hit'
}

header3 = {
    # 'Accept': '*/*',
    # 'Accept-Encoding': 'gzip,deflate',
    # 'Accept-Language': 'zh-CN,zh;q=0.9,en;q = 0.8',
    # 'Connection': 'keep-alive',
    # 'Host': 'player.videoincloud.com',
    # 'Referer': 'http://player.videoincloud.com/vod/19723163?src=gkw&cc=1&wm=19e83e3534b449fac5c89bda89dbb9eb & t = 1661916645031 - f6a25e5536bd26d14fd2dd7ca5d75029',
    'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 104.0.0.0Safari / 537.36',
    # 'X-Requested-With': 'XMLHttpRequest'
}

'''下载ts视频文件'''


def downLoad_video_ts(url, path):
    # try:
    session = requests.session()
    resdata = session.get(url=url, headers=header3, timeout=10)
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
    if Vname is None:
        n = time.localtime(time.time())
        time_name = time.strftime("%Y-%m-%d_%H.%M.%S", n)
        Vname = time_name
    if '.' not in Vname:
        Vname = Vname + '.mp4'
    Vname = ts_path + '\\' + str(Vname)
    print('\n\n整合Video：', Vname)
    if os.path.exists(Vname):
        print('文件重名！是否继续？')
        x = input()
        if not(x==1 or x=='y' or x=='Y'): Vname=Vname+'_2'
    with open(Vname, 'wb') as ff:
        for i in range(1, sizes + 1):
            name = ts_path + '\\' + '%08d.ts' % i
            # print('\r {}/{} :{}'.format(i, sizes + 1, name), end='')
            try:
                with open(name, 'rb') as fr:
                    ff.write(fr.read())
                os.remove(name)
            except:
                pass
    print('\n\n整合完成Video：', Vname)
    pass


def grab_video_from_index_m3u8(url, path=None, Videoname=None, fmt='1', isload=True, num_worker=200):
    if url is None: return
    if path is None:
        path = r'F:\迅雷下载\video_grab'
    try:
        os.makedirs(path)
    except:
        pass
    print('视频保存路径：', path)
    session = requests.session()

    print('视频服务器索引：', url)

    resdata = session.get(url=url, headers=header, timeout=1000)
    if not isload: print('视频服务器索引：[data]\n', resdata.text)
    urls_ts = []
    if fmt == '1':
        video_ts_idx = resdata.text.split('\n')
        # for idx_url in video_ts_idx:
        #     if idx_url.startswith('https:'):
        #         urls_ts.append(idx_url)
        # print(urls_ts)
        urls_ts = video_ts_idx
        if not isload: print('视频ts文件索引：[data]\n', urls_ts)
        pass
    else:
        pass
    if not isload: return 0

    threadPool = ThreadPool(num_worker, reRun=True)
    path_root = path  ## r'G:\pythonFiles\00-files\grab_video'
    num = 0
    for i, ts_name in enumerate(urls_ts):
        # if not ts_name.endswith('.ts'): continue
        if '.ts' not in ts_name: continue
        url_video_ts = ts_name
        print('\n  {}:'.format(num), ts_name)
        num += 1
        name = path_root + '\\' + '%08d.ts' % num
        print('\r download {}/{}'.format(i, len(urls_ts)), end='')
        threadPool.run(target=downLoad_video_ts, args=(url_video_ts, name))
        # downLoad_video_ts(url_video_ts, name)
    print('\nfinish download! \t\ttemp path=', path_root, '\tnum_ts:', num)
    # print('\n')
    if threadPool.join(60 * 30, ishow=True):
        merge_ts_files(path_root, Vname=Videoname)
    pass


if __name__ == '__main__':
    # url = r'https://s1.zoubuting.com/20210727/KTgRXcJS/1200kb/hls/index.m3u8'
    # url = r'https://cdn.zoubuting.com/20210704/egBHfrPk/1200kb/hls/index.m3u8'
    url = r'http://v.videoincloud.com/hncsylfy/20220824/hEEgPK/hEEgPK.m3u8?auth_key=1661960849-0-0-b7b72f676d6da71e14b493f697a5882b&uid=edc672bc72d849fe9148704488b720e8&pid=0d94ef4ccf8b4691a51f7e7a918eb50d&t=2540cacd1317c615dd5d2a9fb64f8384'
    path = r'F:\迅雷下载\video_grab'
    grab_video_from_index_m3u8(url, path=path, Videoname='law04', fmt='1', isload=True, num_worker=500)
    # merge_ts_files(path, Vname='yiyuanqingdan')
    pass
