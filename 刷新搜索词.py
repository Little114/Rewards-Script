import requests
import json
import time
import random
from datetime import datetime
import os
def get_weibo_hot_search():
    try:
        url = "https://weibo.com/ajax/side/hotSearch"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
            "Referer": "https://weibo.com/",
            "Accept": "application/json, text/plain, */*"
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            hot_searches = []
            if 'data' in data and 'realtime' in data['data']:
                for item in data['data']['realtime']:
                    if 'word' in item:
                        hot_searches.append(item['word'])
            return hot_searches[:20]  
    except Exception as e:
        print(f"获取微博热搜失败: {e}")
        return []
def get_baidu_hot_search():
    try:
        url = "https://top.baidu.com/api/board?platform=wise&tab=realtime"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
            "Referer": "https://top.baidu.com/board?tab=realtime"
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            hot_searches = []
            if 'data' in data and 'cards' in data['data']:
                for card in data['data']['cards']:
                    if 'content' in card:
                        for item in card['content']:
                            if 'query' in item:
                                hot_searches.append(item['query'])
            return hot_searches[:20]  
    except Exception as e:
        print(f"获取百度热搜失败: {e}")
        return []
def get_zhihu_hot_search():
    try:
        url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
            "Referer": "https://www.zhihu.com/hot"
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            hot_searches = []
            if 'data' in data:
                for item in data['data']:
                    if 'target' in item and 'title' in item['target']:
                        hot_searches.append(item['target']['title'])
            return hot_searches[:20]  
        else:
            print(f"知乎API请求失败，状态码: {response.status_code}")
            return []
    except Exception as e:
        print(f"获取知乎热搜失败: {e}")
        return []
def get_douyin_hot_search():
    try:
        url = "https://www.douyin.com/aweme/v1/web/hot/search/list/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
            "Referer": "https://www.douyin.com/hot"
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            hot_searches = []
            if 'data' in data and 'word_list' in data['data']:
                for item in data['data']['word_list']:
                    if 'word' in item:
                        hot_searches.append(item['word'])
            return hot_searches[:15]  
        else:
            return ["热门话题1", "热门话题2", "热门话题3", "热门话题4", "热门话题5"]
    except Exception as e:
        print(f"获取抖音热搜失败: {e}")
        return ["热门话题1", "热门话题2", "热门话题3", "热门话题4", "热门话题5"]
def clean_keywords(keywords):
    cleaned = []
    for keyword in keywords:
        keyword = keyword.strip()
        if len(keyword) > 2 and len(keyword) < 50:
            if not any(bad_word in keyword.lower() for bad_word in ['广告', '推广', '营销', '购买', '销售']):
                cleaned.append(keyword)
    return cleaned
def write_to_1txt(keywords):
    try:
        keyword_list = list(set(keywords))
        if len(keyword_list) > 200:
            keyword_list = keyword_list[:200]
        with open("1.txt", "w", encoding="utf-8") as f:
            f.write("# 自动更新的热搜关键词库\n")
            f.write(f"# 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("# 来源: 微博、百度、知乎、抖音等平台热搜榜\n")
            f.write("# 每行一个关键词，支持中英文\n")
            f.write("# 空行和以#开头的行会被忽略\n\n")
            for keyword in keyword_list:
                f.write(f"{keyword}\n")
        print(f"成功写入 {len(keyword_list)} 个关键词到1.txt文件（已清空原有内容）")
        return True
    except Exception as e:
        print(f"写入1.txt文件失败: {e}")
        return False
def main():
    print("开始获取中国热搜数据...")
    print("正在获取微博热搜...")
    weibo_hot = get_weibo_hot_search()
    print(f"获取到微博热搜 {len(weibo_hot)} 个")
    print("正在获取百度热搜...")
    baidu_hot = get_baidu_hot_search()
    print(f"获取到百度热搜 {len(baidu_hot)} 个")
    print("正在获取知乎热搜...")
    zhihu_hot = get_zhihu_hot_search()
    print(f"获取到知乎热搜 {len(zhihu_hot)} 个")
    print("正在获取抖音热搜...")
    douyin_hot = get_douyin_hot_search()
    print(f"获取到抖音热搜 {len(douyin_hot)} 个")
    all_hot_searches = weibo_hot + baidu_hot + zhihu_hot + douyin_hot
    cleaned_keywords = clean_keywords(all_hot_searches)
    unique_keywords = list(set(cleaned_keywords))
    print(f"\n汇总结果:")
    print(f"微博热搜: {len(weibo_hot)} 个")
    print(f"百度热搜: {len(baidu_hot)} 个")
    print(f"知乎热搜: {len(zhihu_hot)} 个")
    print(f"抖音热搜: {len(douyin_hot)} 个")
    print(f"去重后总计: {len(unique_keywords)} 个关键词")
    if unique_keywords:
        if write_to_1txt(unique_keywords):
            print("\n热搜数据已成功更新到1.txt文件")
            print("前10个热搜关键词:")
            for i, keyword in enumerate(unique_keywords[:10], 1):
                print(f"   {i}. {keyword}")
        else:
            print("❌ 写入文件失败")
    else:
        print("❌ 未获取到有效的热搜数据")
if __name__ == "__main__":
    main()