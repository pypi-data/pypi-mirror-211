import sys
import time
from bs4 import BeautifulSoup
import re
import requests
from soupsieve import select
import m3u8
import os
import warnings
from concurrent.futures import thread


warnings.filterwarnings('ignore')


def view_list(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'
    }
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'lxml')
    title_text = soup.head.title.text

    # 从标题中获取视频的名和集数
    name, index_name = '-'.join(''.join(title_text.split('《')).split('》')).split('-')[:2]

    current_dir = '{}'.format(name)
    cache_dir = os.path.join('caches', name)
    if not os.path.exists(current_dir):
        # 创建保存目录
        os.mkdir(current_dir)

    if not os.path.exists(cache_dir):
        os.mkdir(cache_dir)

    absolute_urls = []
    # 保存已经下载的列表文件
    play_list_filename = os.path.join(cache_dir, 'play_list.txt')
    if os.path.exists(play_list_filename):
        # 从缓存文件中读取
        with open(play_list_filename, 'r') as play_list_fd:
            absolute_urls = [item.replace('\n', '') for item in play_list_fd.readlines()]
        return name, absolute_urls

    # 取得base url
    base_url = '/'.join(url.split('/')[:3])
    # print(base_url)

    # 这里可能获取到多个平台提供的连接，目前仅使用第一个平台
    all_videolist = soup.select('#mod_videolist')
    # 从a标签中获取相对url
    all_url = list(map(lambda item: item.attrs.get('href', None), select('a', all_videolist[1])))

    # 生成全部的绝对url
    for video_url in all_url:
        if video_url.startswith('javascript:'):
            absolute_urls.append(url)
        else:
            absolute_urls.append(base_url + video_url)

    absolute_urls.reverse()
    # 缓存到文件中
    with open(play_list_filename, 'w') as play_list_fd:
        for item in absolute_urls:
            play_list_fd.write(item + '\n')

    return name, absolute_urls


def get_a3u8(cache_dir, *urls):
    absolute_urls = []
    # 保存已经下载的列表文件
    play_list_filename = os.path.join(cache_dir, 'real_play_list.txt')
    if os.path.exists(play_list_filename):
        # 从缓存文件中读取
        with open(play_list_filename, 'r', encoding='utf-8') as play_list_fd:
            absolute_urls = [item.replace('\n', '').split(',', 1) for item in play_list_fd.readlines()]
        return absolute_urls

    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'
    }

    for index, url in enumerate(urls):
        html = requests.get(url, headers=headers).text
        soup = BeautifulSoup(html, 'lxml')

        # 从标题中获取视频的名和集数
        # title_text = soup.head.title.text
        # name, index_name = '-'.join(''.join(title_text.split('《')).split('》')).split('-')[:2]
        index_name = '第{}集'.format(index + 1)

        # 从javascript中获取真正的视频地址
        all_scripts = soup.select('body script')

        # [print(item) for item in all_scripts]
        # 取得包含视频链接的javascript内容
        script_context = all_scripts[3].text
        # [print(item) for item in script_context.split(';')]
        result = re.search(r'siteLink:"([^,"]*)"', script_context, re.M)
        if result:
            site_link = result.groups()[0]

        result = re.search(r'ec:"([^,"]*)"', script_context, re.M)
        if result:
            ec = result.groups()[0]

        try_max = 3
        while try_max > 0:
            response = requests.get(
                url='https://r.tvkanba.com/analysis/index',
                params={'eurl': site_link, 'ec': ec},
                #url='https://r.tvkanba.com/analysis/index?eurl=T248wrvHWsISDy4Rwky8r2Kzq2nNq8kTttkq7UMj9FIxLAlfHSfqA1CS4Mdnh2UHYmC7VNg60IYsnhA6C485GA%3D%3D&ec=3lx4d',
                headers={
                    'Host': 'r.tvkanba.com',
                    # 'User-Agent': 'curl/7.79.1',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',

                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57'
                }
            )

            if response.status_code == 200:
                break

            # 再尝试一次
            try_max -= 1
            time.sleep(5)

        # print("视频播放地址: {}".format(response.url))
        # print(response.text)
        result = re.search(r'https://.*\.m3u8', response.text)
        if result:
            play_url = result.group()
            # print('{} 的下载地址: {}'.format(index_name, play_url))
            absolute_urls.append((index_name, play_url))
        else:
            print('没有找到下载地址:{}'.format(response.url))
            absolute_urls.append(None)

    # 缓存到文件中
    with open(play_list_filename, 'w', encoding='utf-8') as play_list_fd:
        for index_name, play_url in absolute_urls:
            play_list_fd.write(index_name + ',' + play_url + '\n')

    return absolute_urls


# 1. 抓取每一集的连接全部的
def download_m3u8(save_filename, cache_dir, name, index_name, url, start_index=0):
    """
    下载每个m3u8文件对应的视频文件。

    :param save_filename:
    :param cache_dir:
    :param name:
    :param index_name:
    :param url:
    :param start_index:
    :return:
    """

    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'
    }

    # 获取m3u8的内容，解析视频的地址, 解决多层嵌套的m3u8格式的文件。
    real_url = url
    while True:
        playlist = m3u8.load(real_url, headers=headers)
        if playlist.segments:
            break
        else:
            if playlist.playlists:
                real_url = playlist.playlists[0].absolute_uri

    print('{}{}共有{}个片段, 开始下载:'.format(name, index_name, len(playlist.segments)))
    download_segments(playlist, save_filename, start_index=start_index)


def segment_download_done(future):
    print()




def download_segment(cache_dir, segment):
    # 检查ts缓存文件是否存在
    cache_file = os.path.join(cache_dir, *segment.absolute_uri.split('/')[3:])
    cache_dir = os.path.dirname(cache_file)
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir, exist_ok=True)
    if os.path.exists(cache_file):
        return cache_file

    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'
    }
    try_max = 5
    result = None
    while try_max > 0:
        response = requests.get(segment.absolute_uri, stream=True, verify=False, timeout=30, headers=headers)
        if response.status_code == 200:
            # 缓存下载的ts文件
            with open(cache_file, 'wb') as fd:
                fd.write(response.content)
            # print('保存片段: '.format(segment.absolute_uri))
            result = cache_file
            break

        # 开始尝试下载
        print('{} {}'.format(response.status_code, response.reason))
        try_max -= 1
        # TODO 这里的睡眠会导致线程池中没有可以使用的线程，后面改进
        time.sleep(3)
    return result

# url = 'https://www.xbsee.cc/play/565099/66-1.html'


def download_segments(playlist, save_filename, start_index=0, max_workers=32):
    executor = thread.ThreadPoolExecutor(max_workers=max_workers)
    cache_dir = os.path.join('caches', os.path.dirname(save_filename))

    total = len(playlist.segments)
    all_futures = []
    for index, segment in enumerate(playlist.segments[start_index:]):
        future = executor.submit(download_segment, cache_dir, segment)
        # future.add_done_callback(segment_download_done)
        all_futures.append(future)

    if not all(all_futures):
        print('有片段没有下载')
        return

    with open(save_filename, 'wb+') as merge_file:
        for index, future in enumerate(all_futures):
            if future.done():
                cache_file = future.result()
                if cache_file:
                    print("开始写入片段:{}/{}".format(index+1, total))
                    with open(cache_file, 'rb') as fd:
                        content = fd.read()
                        merge_file.write(content)
            else:
                print("还没有下载完成")


def main(url):
    name, all_url = view_list(url)

    # 创建缓存目录
    cache_dir = os.path.join('caches', name)
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir, exist_ok=True)

    # 获取整部视频的列表
    play_urls = get_a3u8(cache_dir, *all_url)
    print('{} 共有 {} 集'.format(name, len(play_urls)))

    # 下载系列的全部视频文件
    for index_name, url in play_urls:
        save_filename = os.path.join(name, str(index_name) + '.mp4')
        if os.path.exists(save_filename):
            print('{} 文件已经存在，如果需要重新下载，请删除已经存在的文件。'.format(save_filename))
            continue
        download_m3u8(save_filename, cache_dir, name, index_name, url)
    # download_m3u8('因为太怕痛就全点防御力了', '第1集', 'https://ukzyvod3.ukubf5.com/20220409/JGRDhy9h/index.m3u8')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python {} <url>'.format(sys.argv[0]))
        exit(1)

    url = sys.argv[1]
    main(url)
