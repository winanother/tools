import re
import requests
import os
import sys
import argparse
import urllib3
urllib3.disable_warnings()

def fetch_javascript_chunks(url):
    try:
        # 发送 GET 请求获取 JavaScript 文件内容
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'cache-control': 'max-age=0',
            'connection': 'keep-alive',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0',
            'sec-ch-ua': '"Microsoft Edge";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1'
        }
        response = requests.get(url, verify=False, headers=headers)
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
    except requests.exceptions.RequestException as e:
        print(f"Error fetching JavaScript chunks from {url}: {e}")
    except Exception as e:
        print(f"Unexpected error in fetch_javascript_chunks: {e}")

def fetch_javascript_indexes(url):
    try:
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
    except requests.exceptions.RequestException as e:
        print(f"Error fetching JavaScript indexes from {url}: {e}")
    except Exception as e:
        print(f"Unexpected error in fetch_javascript_indexes: {e}")

# 新增函数：用于匹配静态资源路径格式的JavaScript文件
def fetch_static_chunks(url):
    try:
        # 发送 GET 请求获取JavaScript文件内容
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, verify=False, headers=headers)
        base_url = os.path.dirname(url)
        all_static = []
        
        # 检查请求是否成功
        if response.status_code == 200:
            # 提取JavaScript文件内容
            source_code = response.text
            seen_static_names = set()
            
            # 定义匹配静态资源路径的正则表达式
            # 匹配类似 static/chunks/pages/awards/campaigns/100kmoments/mobile-b1b6524cbaa114a2.js 的路径
            regex_pattern = r'(static/chunks/pages/[^"]+\.js)'
            
            # 使用正则表达式进行匹配
            matches = re.findall(regex_pattern, source_code)
            
            # 去重并构建完整URL
            for match in matches:
                # 检查是否已经处理过该路径
                if match in seen_static_names:
                    continue
                else:
                    seen_static_names.add(match)
                    # 构建完整的URL
                    file_name = base_url + '/' + match
                    print(file_name)
                    all_static.append(file_name)
            
            # 直接将结果写入文件，一行一个URL
            with open('result.txt', 'w') as f:
                for url in all_static:
                    f.write(url + '\n')
            print(f"Results saved to result.txt ({len(all_static)} URLs found)")
        else:
            print("Failed to request:", url)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching static chunks from {url}: {e}")
    except Exception as e:
        print(f"Unexpected error in fetch_static_chunks: {e}")

# 修改函数：用于匹配课程相关的JavaScript模块名称
def fetch_course_chunks(url):
    try:
        # 发送 GET 请求获取网页源代码
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'cache-control': 'max-age=0',
            'connection': 'keep-alive',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0',
            'sec-ch-ua': '"Microsoft Edge";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1'
        }
        response = requests.get(url, verify=False, headers=headers, timeout=30)  # 添加超时设置
        base_url = os.path.dirname(url)
        all_course_chunks = []
        
        # 检查请求是否成功
        if response.status_code == 200:
            # 提取网页源代码
            source_code = response.text
            
            # 查找动态路径拼接模式，如 "course_pc_detail/js/" + ({...}[e] || e) + ".js"
            # 更新正则表达式以更好地匹配所需的结构 - 匹配完整的动态路径拼接
            # 匹配模式: return a.p + "path/" + ({...}[e] || e) + "." + {...}[e] + ".js"
            dynamic_path_pattern = r'return\s+[^\+]*\+\s*"([^"]+/)"\s*\+\s*\(\{([^}]+)\}\s*\[\w+\]\s*\|\|\s*\w+\)\s*\+\s*"[^"]*"\s*\+\s*\{([^}]+)\}\s*\[\w+\]\s*\+\s*"[^"]*\.js"'
            dynamic_matches = re.findall(dynamic_path_pattern, source_code, re.DOTALL)
            
            # 如果上面的模式没有匹配到，尝试匹配更通用的模式
            if not dynamic_matches:
                # 匹配形如: "static/js/" + ({...}[e] || e) + "." + {...}[e] + ".js" 的模式
                dynamic_path_pattern = r'"([^"]+/)"\s*\+\s*\(\{([^}]+)\}\s*\[\w+\]\s*\|\|\s*\w+\)\s*\+\s*"[^"]*"\s*\+\s*\{([^}]+)\}\s*\[\w+\]\s*\+\s*"[^"]*\.js"'
                dynamic_matches = re.findall(dynamic_path_pattern, source_code, re.DOTALL)
            
            seen_paths = set()
            
            for base_path, module_mappings, hash_mappings in dynamic_matches:
                # 解析模块映射和哈希映射
                # 匹配 "key": "value" 格式
                module_pattern = r'"([^"]+)"\s*:\s*"([^"]+)"'
                modules = re.findall(module_pattern, module_mappings)
                hashes = re.findall(module_pattern, hash_mappings)
                
                # 创建模块名到哈希值的映射
                hash_map = {module: hash_val for module, hash_val in hashes}
                
                # 对每个模块生成对应的JS文件路径
                for module_key, module_value in modules:
                    # 获取对应的哈希值，如果不存在则使用模块名作为哈希
                    hash_value = hash_map.get(module_key, module_key)
                    
                    # 生成文件名格式: module_name.hash_value.js
                    file_name = f"{module_value}.{hash_value}.js"
                    
                    full_path = base_path + file_name
                    
                    if full_path in seen_paths:
                        continue
                    else:
                        seen_paths.add(full_path)
                        file_url = base_url + '/' + full_path
                        print(file_url)
                        all_course_chunks.append(file_url)
            
            # 如果上面的模式没有匹配到，尝试更通用的匹配方式
            if not all_course_chunks:
                # 直接匹配对象格式: {"module_name": "hash_value"}
                object_pattern = r'\{\s*("([^"]+)"\s*:\s*"([^"]+)"\s*,?\s*)+\s*\}'
                object_matches = re.findall(object_pattern, source_code)
                
                for match in object_matches:
                    # 解析整个对象
                    full_object = match[0]
                    entries = re.findall(r'"([^"]+)"\s*:\s*"([^"]+)"', full_object)
                    
                    # 检查是否包含多个模块定义
                    if len(entries) > 1:
                        for module_name, hash_value in entries:
                            # 检查模块名是否包含路径分隔符，如果是则提取文件名部分
                            if '/' in module_name:
                                # 如果模块名包含路径，则使用最后部分作为文件名
                                clean_module_name = module_name.split('/')[-1]
                            else:
                                clean_module_name = module_name
                            
                            # 生成文件名格式: module_name.hash_value.js
                            file_name = f"{clean_module_name}.{hash_value}.js"
                            
                            # 尝试找到静态路径前缀
                            # 查找在对象之前的路径字符串
                            path_prefix_pattern = r'(["\'])([^"\']*/[^"\']*)(["\'])\s*\+\s*\{'
                            prefix_matches = re.findall(path_prefix_pattern, source_code[:source_code.find(match[0])])
                            
                            if prefix_matches:
                                # 使用最后一个匹配的路径前缀
                                path_prefix = prefix_matches[-1][1]
                                full_path = path_prefix + '/' + file_name
                            else:
                                # 如果没找到路径前缀，直接使用文件名
                                full_path = file_name
                            
                            if full_path in seen_paths:
                                continue
                            else:
                                seen_paths.add(full_path)
                                file_url = base_url + '/' + full_path
                                print(file_url)
                                all_course_chunks.append(file_url)
            
            # 如果还是没有匹配到，尝试更简单的模式，匹配 { "module": "hash" } 这样的结构
            if not all_course_chunks:
                # 匹配类似 {"pages-protocol-service": "162c5c50", "pages-qrOpenDoor-open": "940a46e6"} 的模式
                simple_pattern = r'\{\s*("[^"]+"\s*:\s*"[^"]+"\s*,?\s*)+\s*\}'
                simple_matches = re.findall(simple_pattern, source_code)
                
                for match in simple_matches:
                    entries = re.findall(r'"([^"]+)"\s*:\s*"([^"]+)"', match)
                    # 检查是否是模块名:哈希值的对应关系
                    for module_name, hash_value in entries:
                        # 检查模块名和哈希值是否不同，以区分模块名和哈希
                        if module_name != hash_value and len(hash_value) > 4:  # 确保hash值长度合理
                            # 生成文件名: module_name.hash.js
                            file_name = f"{module_name}.{hash_value}.js"
                            full_path = file_name  # 简单情况下直接使用文件名
                            
                            if full_path in seen_paths:
                                continue
                            else:
                                seen_paths.add(full_path)
                                file_url = base_url + '/' + full_path
                                print(file_url)
                                all_course_chunks.append(file_url)
            
            # 将结果写入文件，覆盖原有内容
            if all_course_chunks:
                with open('result.txt', 'w') as f:  # 使用覆盖模式
                    for url in all_course_chunks:
                        f.write(url + '\n')
                print(f"Course chunks saved to result.txt ({len(all_course_chunks)} URLs found)")
        else:
            print("Failed to request:", url)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching course chunks from {url}: {e}")
    except Exception as e:
        print(f"Unexpected error in fetch_course_chunks: {e}")

def reg_context(urls):
    try:
        #匹配包含相对路径和绝对路径的文本内容
        regex_path = r'''(?:"|')(((?:[a-zA-Z]{1,10}://|//)[^"'/]{1,}\.[a-zA-Z]{2,}[^"']{0,})|((?:/|\.\./|\./)[^"'><,;|*()(%%$^/\\\[\]][^"'><,;|()]{1,})|([a-zA-Z0-9_\-/]{1,}/[a-zA-Z0-9_\-/]{1,}\.(?:[a-zA-Z]{1,4}|action)(?:[\?|#][^"|']{0,}|))|([a-zA-Z0-9_\-/]{1,}/[a-zA-Z0-9_\-/]{3,}(?:[\?|#][^"|']{0,}|))|([a-zA-Z0-9_\-]{1,}\.(?:php|asp|aspx|jsp|json|action|html|js|txt|xml)(?:[\?|#][^"|']{0,}|)))(?:"|')'''
        all_path = []
        # all_urls = []
        for url in urls:
            try:
                # 发送 GET 请求获取网页源代码
                headers = {
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'accept-encoding': 'gzip, deflate, br, zstd',
                    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                    'cache-control': 'max-age=0',
                    'connection': 'keep-alive',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0',
                    'sec-ch-ua': '"Microsoft Edge";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'document',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-site': 'none',
                    'sec-fetch-user': '?1',
                    'upgrade-insecure-requests': '1'
                }
                response = requests.get(url, verify=False, headers=headers)
                if response.status_code == 200:
                # 提取 JavaScript 文件内容
                    javascript_code = response.text
                    match_path = re.findall(regex_path,javascript_code)
                    # 匹配结果,放进各自的列表
                    for path in match_path:
                        all_path.append(path[0])

                else:
                    print("Failed to fetch JavaScript file:", url)
            except requests.exceptions.RequestException as e:
                print(f"Error fetching JavaScript file {url}: {e}")
            except Exception as e:
                print(f"Unexpected error processing URL {url}: {e}")
                
        #将结果写入文件中    
        with open('result.txt', 'wb') as file:
            for path in all_path:
                file.write((str(path)+'\n').encode('utf-8'))
    except IOError as e:
        print(f"Error writing to file: {e}")
    except Exception as e:
        print(f"Unexpected error in reg_context: {e}")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch JavaScript from a URL.')
    parser.add_argument('-uc', '--chunk', help='URL of the JavaScript file')
    parser.add_argument('-um', '--manifest', help='URL of the JavaScript file')    
    # 添加新的命令行参数用于处理静态资源路径
    parser.add_argument('-us', '--static', help='URL to fetch static chunk paths')
    # 添加新的命令行参数用于处理课程相关模块
    parser.add_argument('-uco', '--course', help='URL to fetch course related chunk paths')
    args = parser.parse_args()

    try:
        if args.manifest:
            fetch_javascript_indexes(args.manifest)
        if args.chunk:
            fetch_javascript_chunks(args.chunk)
        # 处理新增的静态资源路径参数
        if args.static:
            fetch_static_chunks(args.static)
        # 处理新增的课程模块参数
        if args.course:
            fetch_course_chunks(args.course)
    except Exception as e:
        print(f"Error in main execution: {e}")