
# -*- coding: utf-8 -*-
import os
import re
import urllib.parse

regex = {
    "Linker": r'(?:"|\')((?!text\/javascript)((?:[a-zA-Z]{1,10}://|//)[^"\'/]{1,}\.[a-zA-Z]{2,}[^"\']{0,})|((?:/|\.\./|\./)[^"\'><,;|*()(%%$^/\\\[\]][^"\'><,;|()]{1,})|([a-zA-Z0-9_\-/]{1,}/[a-zA-Z0-9_\-/]{1,}\.(?:[a-zA-Z]{1,4}|action)(?:[\?|#][^"|\']{0,}|))|([a-zA-Z0-9_\-/]{1,}/[a-zA-Z0-9_\-/]{3,}(?:[\?|#][^"|\']{0,}|))|([a-zA-Z0-9_\-]{1,}\.(?:php|asp|aspx|jsp|json|action|html|js|txt|xml)(?:[\?|#][^"|\']{0,}|)))(?:"|\')',
}

def extract_routes_from_file(filepath):
    """
    从指定文件中提取所有路由
    Args:
        filepath: 文件路径
    Returns:
        routes: 列表，存储提取到的路由
    """
    with open(filepath, 'r', errors='ignore') as file:
        # 读取文件内容
        content = file.read()
        if not content:
            return []
        routes = []
        for name, pattern in regex.items():
            # 使用正则表达式匹配路由
            matches = re.findall(pattern, content)
            for match in matches:
                route = match[0].encode('ascii', 'ignore').decode()
                # 解码路由
                route = urllib.parse.unquote(route)
                # 排除以下后缀的路由
                if not route.endswith('.css') and not route.endswith('.png') and not route.endswith('.jpge'):
                        # 只提取第一个位置是/的路由
                        routes.append(route)

        return routes

def find_routes(root_dir):
    """
    从根目录下查找所有路由
    :param root_dir: 根目录路径
    :return: 所有路由列表
    """
    routes = set()  # 存储所有路由
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)  # 拼接文件路径
            routes_in_file = extract_routes_from_file(filepath)
            routes.update(routes_in_file)
    return routes


def main():
    # 获取当前工作目录
    root_dir = os.getcwd()
    # 查找路由
    routes = find_routes(root_dir)
    routes = list(set(routes))

    # 询问用户是否只提取第一个位置是/的路由
    filter_choice = input("深情哥问你：是否只提取第一个位置是/的路由？回答我！！！(y/n): ").strip().lower()
    if filter_choice == 'y':
        # 只保留第一个位置是/的路由
        routes = [route for route in routes if route.startswith('/')]

    # 询问用户是否确保每个路由都以/开头
    ensure_slash = input("深情哥问你：是否确保每个路由都以/开头？回答我！！！(y/n): ").strip().lower()
    if ensure_slash == 'y':
        # 确保每个路由都以/开头
        routes = [route if route.startswith('/') else '/' + route for route in routes]

    # 将结果写入文件
    with open('routes.txt', 'w') as f:
        for path in routes:
            f.write(path + '\n')

    # 打印结果
    print(routes)


if __name__ == "__main__":
    main()

