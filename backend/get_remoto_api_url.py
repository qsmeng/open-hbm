import requests
from lxml import html
from dotenv import load_dotenv, set_key
import os

# 定义URL和请求头
url = "https://dashboard.cpolar.com/login"
status_url = "https://dashboard.cpolar.com/status"

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Cache-Control": "no-cache",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": url,
    "Referer": "https://dashboard.cpolar.com/get-started",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
}

types = ["dify", "cpolar", "ComfyUI", "open_web_ui","ollama"]# mysql 单独处理

def check_type(type:str):
    """检查传入的类型是否在允许的枚举值中"""
    if type not in types:
        raise ValueError(f"无效的类型参数: {type}. 允许的值是: {types}")

    
# def get_csrf_token(session): 
#     """获取CSRF Token"""
#     response = session.get(url, headers=headers)
#     response.raise_for_status()
#     tree = html.fromstring(response.content)
#     csrf_token = tree.xpath('//input[@name="csrf_token"]/@value')
#     if csrf_token:
#         return csrf_token[0]
#     else:
#         raise ValueError("未找到CSRF Token")


def update_remoto_api_url(type:str):
    """更新保存的url"""
    try:
        session = requests.Session()
        # csrf_token = get_csrf_token(session)
        
        data = {
            "login": os.getenv('cpolar_login'),
            "password": os.getenv('cpolar_password'),
            # "csrf_token": csrf_token,
            "csrf_token": "1538662349.68##b5aa35f374452a6198004dab20d88b13583c7c2c",
        }
        
        # 发送POST请求,获取cookies
        response = session.post(url, headers=headers, data=data)
        response.raise_for_status()

        # 发送GET请求,获取API URL
        status_response = session.get(status_url, headers=headers)
        status_response.raise_for_status()

        # 解析 HTML
        tree = html.fromstring(status_response.content)
        tbody = tree.xpath("/html/body/div[5]/div/div[2]/div[2]/table/tbody")[0]  # 获取tbody元素
        
        # XPath 查询,获取tbody中首列为特定值的 tr
        rows = tbody.xpath(f"tr[td[1][text()='{type}']]")
        # print(rows[0].text_content())  # 打印tbody中符合条件的行内容
        # print(rows[0].xpath("th/a/@href")[0])  # 打印tbody中符合条件的行内容

        if not rows:
            print("未找到符合条件的行。")
            return "未找到符合条件的API"  # 提前返回,避免继续处理
        
        # 获取符合条件的第一行的链接
        type_url = rows[0].xpath("th/a/@href")[0]
        print(type_url)
        os.environ[f'cpolar_{type}_url']= type_url  # 保存API URL到环境变量
        set_key('.env', f'cpolar_{type}_url', type_url)  # 写入 .env 文件

    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
    except IndexError:
        print("未找到tbody元素,HTML结构可能已改变。")
    except Exception as e:
        print(f"发生错误: {e}")
def get_url_from_env_file(type: str):
    """从.env文件中获取对应type的URL"""
    check_type(type)
    key = f'cpolar_{type}_url'
    with open('.env', 'r', encoding='utf-8') as file:
        for line in file:
            if line.startswith(key):
                url=line.strip().split('=', 1)[1].replace('"', '').replace("'", '')
                # print(url)
                return url  # 分割并返回URL部分
    return None  # 未找到或发生错误时返回None
def check_url(type: str):
    """检查当前保存的url可用性"""  
    check_type(type)
    url = get_url_from_env_file(type)  # 从文件读取API URL
    response = None
    print(f"检查 {type} API URL: {url}")
    response = requests.get(url)
    status_code = response.status_code
    print(f"{type} API URL: 状态码: {status_code}")
    if status_code not in [200, 502, 403]: # 成功 未启动 拒绝
        print(f"{status_code} 不可用,尝试更新...{type} API URL: {url}")
        update_remoto_api_url(type) # 更新API URL

def get_remoto_api_url(type: str = None):
    """获取远程API的URL或更新所有类型的URL""" 
    if type is not None:
        check_type(type)
        try:
            url =  get_url_from_env_file(type) 
            if not url:
                print(f"未找到类型为 {type} 的API URL,尝试更新...")
                update_remoto_api_url(type)
                url =  get_url_from_env_file(type) 
            return url
        except Exception as e:
            print(f"发生错误: {e}")
    else:
        # 如果type为None,则更新所有API URL        
        urls = []  # 初始化为列表以收集所有URL
        for t in types:
            try:
                check_url(t)
                url =  get_url_from_env_file(t)   # 直接使用当前类型的URL
                if url:  # 确保URL不为空
                    urls.append(url)  # 追加到列表中
            except Exception as e:
                print(f"更新类型 {t} 的API URL时发生错误: {e}")
        return '已更新全部api_url: ' + ', '.join(urls)