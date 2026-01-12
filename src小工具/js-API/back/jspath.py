import re
import requests
import os
import sys
import argparse
import urllib3
urllib3.disable_warnings()

def fetch_javascript_chunks(url):
    # 发送 GET 请求获取 JavaScript 文件内容
    response = requests.get(url, verify=False)
    final_url = os.path.dirname(url)
    all_chunk = []
    # 检查请求是否成功
    if response.status_code == 200:
        # 提取 JavaScript 文件内容
        javascript_code = response.text

        # 定义正则表达式
        regex_pattern = r'"(chunk-\w+)":"(\w+)"'

        # 使用正则表达式进行匹配
        matches = re.findall(regex_pattern, javascript_code)

        # 创建一个集合用于存储已经出现过的 chunk_name
        seen_chunk_names = set()

            # 写入匹配结果，同时进行去重操作
        for match in matches:
            chunk_name, data = match
            # 检查当前 chunk_name 是否已经出现过，如果是则跳过
            if chunk_name in seen_chunk_names:
                continue
            else:
                seen_chunk_names.add(chunk_name)
                # 拼接 URL 和 chunk 名称，再传入内容匹配中
                file_name = final_url + '/' + chunk_name + '.' + data + '.js'
                print(file_name)
                all_chunk.append(file_name)
        reg_context(all_chunk)
    else:
        print("Failed to request:", url)

def fetch_javascript_indexes(url):
    # 发送 GET 请求获取网页源代码
    response = requests.get(url, verify=False)
    final_url = os.path.dirname(url)
    all_index = []
    # 检查请求是否成功
    if response.status_code == 200:
        # 提取网页源代码
        source_code = response.text
        seen_index_names = set()
        # 定义正则表达式
        regex_pattern = r'(\d+):"(\w+)"'

        # 使用正则表达式进行匹配
        matches = re.findall(regex_pattern, source_code)

        # 写入匹配结果，同时进行去重操作
        for match in matches:
            index, data = match
            # 检查当前 index 是否已经出现过，如果是则跳过
            if index in seen_index_names:
                continue
            else:
                seen_index_names.add(index)
                # 拼接 URL 和 chunk 名称，再传入内容匹配中
                file_name = final_url + '/' + index + '.' + data + '.js'
                print(file_name)
                all_index.append(file_name)
        reg_context(all_index)
    else:
        print("Failed to request:", url)

def reg_context(urls):
    #匹配包含相对路径和绝对路径的文本内容
    regex_path = r'''(?:"|')(((?:[a-zA-Z]{1,10}://|//)[^"'/]{1,}\.[a-zA-Z]{2,}[^"']{0,})|((?:/|\.\./|\./)[^"'><,;|*()(%%$^/\\\[\]][^"'><,;|()]{1,})|([a-zA-Z0-9_\-/]{1,}/[a-zA-Z0-9_\-/]{1,}\.(?:[a-zA-Z]{1,4}|action)(?:[\?|#][^"|']{0,}|))|([a-zA-Z0-9_\-/]{1,}/[a-zA-Z0-9_\-/]{3,}(?:[\?|#][^"|']{0,}|))|([a-zA-Z0-9_\-]{1,}\.(?:php|asp|aspx|jsp|json|action|html|js|txt|xml)(?:[\?|#][^"|']{0,}|)))(?:"|')'''
    all_path = []
    # all_urls = []
    for url in urls:
        # 发送 GET 请求获取网页源代码
        response = requests.get(url, verify=False)
        if response.status_code == 200:
        # 提取 JavaScript 文件内容
            javascript_code = response.text
            match_path = re.findall(regex_path,javascript_code)
            # 匹配结果,放进各自的列表
            for path in match_path:
                all_path.append(path[0])

        else:
            print("Failed to fetch JavaScript file:", url)
    #将结果写入文件中    
    with open('result.txt', 'wb') as file:
        for path in all_path:
            file.write((str(path)+'\n').encode('utf-8'))




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch JavaScript from a URL.')
    parser.add_argument('-uc', '--chunk', help='URL of the JavaScript file')
    parser.add_argument('-um', '--manifest', help='URL of the JavaScript file')    
    args = parser.parse_args()

    if args.manifest:
        fetch_javascript_indexes(args.manifest)
    if args.chunk:
        fetch_javascript_chunks(args.chunk)


