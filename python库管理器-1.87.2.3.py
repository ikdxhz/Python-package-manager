import subprocess#导入subprocess模块
import sys#导入sys模块
import re#导入re模块
import json#导入json模块
import requests#导入requests模块
from socket import gethostbyname, gaierror#导入socket模块
import threading#导入threading模块
import os#导入os模块

# 定义当前版本号
CURRENT_VERSION = "1.87.2.3"#定义CURRENT_VERSION变量

print("作者: ikdxhz")#打印作者
print(f"程序版本: {CURRENT_VERSION}")#打印程序版本
print("当获取公告不可用时，请访问Github存储库：https://github.com/ikdxhz/Python-package-manager/")#打印Github存储库
print("当获取公告不可用时，请访问Github存储库：https://github.com/ikdxhz/Python-package-manager/")#打印Github存储库
print("当获取公告不可用时，请访问Github存储库：https://github.com/ikdxhz/Python-package-manager/")#打印Github存储库

pip_source = []#定义pip_source变量

PIP_SOURCES = {#定义PIP_SOURCES变量
    "aliyun": "https://mirrors.aliyun.com/pypi/simple/",#定义aliyun变量
    "tsinghua": "https://pypi.tuna.tsinghua.edu.cn/simple/",#定义tsinghua变量
    "douban": "https://pypi.douban.com/simple/",#定义douban变量
    "ustc": "https://pypi.mirrors.ustc.edu.cn/simple/",#定义ustc变量
    "huawei": "https://mirrors.huaweicloud.com/repository/pypi/simple/",#定义huawei变量
    "tencent": "https://mirrors.cloud.tencent.com/pypi/simple/",#定义tencent变量
    "netease": "https://mirrors.163.com/pypi/simple/",#定义netease变量
    "baidu": "https://mirror.baidu.com/pypi/simple/",#定义baidu变量
    "default": "https://pypi.org/simple/"#定义default变量
}

lock = threading.Lock()#定义lock变量

def check_python_version():#定义check_python_version函数
    major, minor, micro, releaselevel, serial = sys.version_info#获取Python版本信息
    if major < 3 or (major == 3 and minor < 6) or (major == 3 and minor == 6 and micro < 1):#判断Python版本是否符合要求
        print(f"当前Python版本为 {sys.version}, 脚本需要Python 3.6.1或更高版本.")
        sys.exit(1)#退出程序
    else:#如果Python版本符合要求
        print(f"当前Python版本为 {sys.version}, 符合要求.")#打印Python版本

def check_pip_installed():#定义check_pip_installed函数
    try:#尝试执行以下代码
        subprocess.check_call([sys.executable, '-m', 'pip', '--version'])#执行pip命令
        return True#返回True
    except subprocess.CalledProcessError:#如果执行失败
        print("未找到pip，请确保pip已安装并添加到PATH中.")#打印未找到pip
        return False#返回False

def set_pip_source(source):#定义set_pip_source函数
    global pip_source#定义pip_source变量
    if source in PIP_SOURCES:#判断source是否在PIP_SOURCES中
        pip_source = ["-i", PIP_SOURCES[source]]#将pip_source设置为PIP_SOURCES[source]
        print(f"已切换到 {source} 源: {PIP_SOURCES[source]}")#打印已切换到source源
    else:#如果source不在PIP_SOURCES中
        print("无效的源选择，可用源包括:")#打印无效的源选择
        for name in PIP_SOURCES:#遍历PIP_SOURCES中的所有源
            if name != "default":#如果name不是default
                print(f"- {name}")#打印name
        pip_source = []#将pip_source设置为空列表

def get_current_source():#定义get_current_source函数
    for key, value in PIP_SOURCES.items():#遍历PIP_SOURCES中的所有源
        if pip_source == ["-i", value]:#如果pip_source等于["-i", value]
            return key#返回key
    return "default"#返回default

def get_pip_command():#定义get_pip_command函数
    commands_to_try = ['pip', 'pip3']#定义commands_to_try变量
    for cmd in commands_to_try:#遍历commands_to_try中的所有命令
        try:#尝试执行以下代码
            subprocess.check_call([cmd, '--version'])#执行cmd命令
            return [cmd]#返回cmd
        except FileNotFoundError:#如果执行失败
            continue#继续执行
    #不想写注释了
    retries = 3#定义retries变量
    while retries > 0:#当retries大于0时
        manual_input = input("未找到pip或pip3，请手动输入pip命令 (例如 'pip' 或 'pip3')，或输入 'exit' 退出: ").strip()#手动输入pip命令
        if manual_input.lower() == 'exit':#如果manual_input等于exit
            print("退出程序.")#退出程序
            sys.exit(1)#退出程序
        try:#尝试执行以下代码
            subprocess.check_call([manual_input, '--version'])#执行manual_input命令
            return [manual_input]#返回manual_input
        except FileNotFoundError:#如果执行失败
            retries -= 1
            print(f"手动输入的pip命令无效，请重新输入 ({retries} 次尝试剩余).")#打印手动输入的pip命令无效
    
    print("多次尝试无效，请确保pip已安装并添加到PATH中。你可以通过以下命令安装pip:")#打印多次尝试无效
    print("curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python get-pip.py")#打印安装pip命令
    sys.exit(1)#退出程序

def run_pip_command(pip_command, command, args=[], include_source=True, current_package=None):
    full_command = pip_command + command + args#定义full_command变量
    if include_source:#如果include_source为True
        full_command += pip_source#将full_command设置为pip_source
    
    # 新增实时输出处理
    try:#尝试执行以下代码
        process = subprocess.Popen(#执行full_command命令
            full_command,#full_command命令
            stdout=subprocess.PIPE,#标准输出
            stderr=subprocess.STDOUT,#标准错误
            text=True,#文本模式
            bufsize=1,#缓冲区大小
            universal_newlines=True#通用新行
        )#执行full_command命令

        # 实时输出缓冲区
        output_buffer = []#定义output_buffer变量
        progress_bar_active = False#定义progress_bar_active变量

        while True:#当True时
            line = process.stdout.readline()#读取process.stdout.readline()
            if not line:#如果line为False
                break#退出循环
                
            # 保留原始输出用于错误处理
            output_buffer.append(line)#将line添加到output_buffer中
            
            # 处理进度条显示
            if "━━━━" in line:
                # 进度条行处理
                sys.stdout.write('\r' + line.strip())
                sys.stdout.flush()
                progress_bar_active = True
                continue
            elif progress_bar_active:#如果progress_bar_active为True
                # 进度条结束换行    
                print()#打印
                progress_bar_active = False#将progress_bar_active设置为False

            # 原有中文处理逻辑保持不变
            processed_line = process_pip_output(line.strip())
            if processed_line:
                print(processed_line)

        process.wait()
        
        # 错误处理部分使用缓冲的完整输出
        output = ''.join(output_buffer)
        if process.returncode != 0:
            handle_pip_errors(full_command, output, current_package)
            return False
        return True

    except Exception as e:
        print(f"\n错误: 执行过程中发生未知错误: {e}")
        return False

# 新增辅助函数
def process_pip_output(line):
    # 保持原有的中文处理逻辑
    if "Looking in indexes:" in line:
        return f"当前使用的索引源: {line.split(': ')[1]}"
    elif "Requirement already satisfied:" in line:
        return process_requirement_line(line)
    # 新增安装过程汉化
    elif "Installing collected packages:" in line:
        packages = line.split(":")[1].strip()
        return f"▰ 正在安装软件包: {packages}"
    elif "Successfully installed" in line:
        packages_info = line.replace("Successfully installed", "").strip()
        # 格式化版本信息
        formatted = []
        for pkg in packages_info.split():
            if '-' in pkg:
                name, version = pkg.rsplit('-', 1)
                formatted.append(f"{name} 版本: {version}")
            else:
                formatted.append(pkg)
        return f"✓ 成功安装: {', '.join(formatted)}"
    # 其他处理逻辑...
    return line

def process_requirement_line(line):
    parts = line.split("Requirement already satisfied:")
    package_info = parts[1].strip()
    if "from requests" in package_info or "from" in package_info and "(" in package_info:
        pkg_parts = package_info.split("(from")
        pkg_name = pkg_parts[0].strip()
        dependency = pkg_parts[1].strip().rstrip(")")
        return f"需求已满足: {pkg_name} [作为 {dependency} 的依赖项已安装]"
    return f"需求已满足: {package_info} [已安装]"

def handle_pip_errors(full_command, output, current_package):
    print(f"\n命令 {' '.join(full_command)} 失败:")
    # 使用完整输出进行错误分析
    if "No matching distribution found" in output:
        print("错误: 未找到匹配的分发版本")
    elif "Installing collected packages:" in output:
        print("安装过程被中断")
    # 其他错误处理逻辑保持不变...

def install(pip_command, package, version=None):
    if not validate_package_name(package):
        print(f"\n包名 '{package}' 在PyPI上不存在.")
        return
    
    if version:
        package_with_version = f"{package}=={version}"
    else:
        package_with_version = package
    
    print(f"\n正在准备安装 {package_with_version}...")
    print("正在下载包信息...")
    
    if run_pip_command(pip_command, ['install'], [package_with_version]):
        print(f"\n{package_with_version} 安装成功.")
    else:
        print(f"\n{package_with_version} 安装失败.")
        suggest_similar_packages(package)

def update_single(pip_command, package):
    if not validate_package_name(package):
        print(f"\n包名 '{package}' 在PyPI上不存在.")
        return
    
    try:
        result = subprocess.run(pip_command + ['show', package], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        details = result.stdout.splitlines()
        current_version = None
        for detail in details:
            if detail.startswith('Version:'):
                current_version = detail.split(': ')[1].strip()
        
        if current_version is None:
            print(f"\n无法获取 {package} 的当前版本.")
            return
        
        print(f"\n正在更新 {package}...")
        print(f"当前版本: {current_version}")
        print(f"正在下载 {package} 的最新版本信息...")
        
        if run_pip_command(pip_command, ['install', '--upgrade'], [package]):
            new_result = subprocess.run(pip_command + ['show', package], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            new_details = new_result.stdout.splitlines()
            updated_version = None
            for new_detail in new_details:
                if new_detail.startswith('Version:'):
                    updated_version = new_detail.split(': ')[1].strip()
            
            if updated_version is None:
                print(f"无法获取 {package} 的更新后版本.")
            else:
                print(f"更新成功. 新版本: {updated_version}.")
        else:
            print(f"{package} 更新失败.")
            suggest_similar_packages(package)
    except subprocess.CalledProcessError as e:
        print(f"\n获取 {package} 详细信息失败: {e.stderr.strip()}")
    except Exception as e:
        print(f"发生未知错误: {e}")

def update_all(pip_command):
    try:
        result = subprocess.run(pip_command + ['list', '--outdated'] + pip_source, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        lines = result.stdout.splitlines()[2:]  # Skip header lines
        outdated_packages = []
        for line in lines:
            parts = line.split()
            if len(parts) >= 3:
                package_name = parts[0]
                current_version = parts[1]
                latest_version = parts[2]
                outdated_packages.append((package_name, current_version, latest_version))
        
        if not outdated_packages:
            print("\n没有可更新的包.")
            list_all_packages(pip_command)
            return
        
        # 显示可更新列表
        print("\n以下包可更新:")
        print("{:<20} {:<15} {:<15}".format("包名", "当前版本", "最新版本"))
        print("-" * 50)
        for pkg, curr, latest in outdated_packages:
            print("{:<20} {:<15} → {:<15}".format(pkg, curr, latest))
        
        # 添加确认步骤
        confirm = input("\n确定要更新以上所有包吗？(y/n): ").strip().lower()
        if confirm != 'y':
            print("已取消批量更新.")
            return
        
        # 修改为单线程顺序更新
        failed_updates = []
        total = len(outdated_packages)
        for idx, (package_name, current_version, latest_version) in enumerate(outdated_packages, 1):
            print(f"\n▰ 正在处理更新 ({idx}/{total}): {package_name}")
            print(f"  当前版本: {current_version} → 最新版本: {latest_version}")
            print(f"正在下载 {package_name} 的更新...")
            if not run_pip_command(pip_command, ['install', '--upgrade'], [package_name]):
                print(f"{package_name} 更新失败.")
                failed_updates.append(package_name)
        
        if failed_updates:
            print("\n以下包更新失败:")
            for pkg in failed_updates:
                print(f"- {pkg}")
            confirm_retry = input("是否重试失败的更新? (y/n): ").strip().lower()
            if confirm_retry == 'y':
                for pkg in failed_updates:
                    update_single(pip_command, pkg)
    
    except subprocess.CalledProcessError as e:
        print(f"\n获取过时包列表失败: {e.stderr.strip()}")
    except Exception as e:
        print(f"发生未知错误: {e}")

def uninstall(pip_command, package):
    # 支持批量卸载多个包
    packages = package.split()
    success_list = []
    fail_list = []

    for pkg in packages:
        print(f"\n▰▰▰ 开始处理 {pkg} 卸载 ▰▰▰")
        
        # 检查包是否存在
        try:
            subprocess.run(pip_command + ['show', pkg], check=True)
        except subprocess.CalledProcessError:
            print(f"✗ 包 {pkg} 未安装或不存在")
            fail_list.append(pkg)
            continue

        # 新增依赖检查
        print(f"▰ 正在检查 {pkg} 的依赖关系...")
        try:
            dependents = subprocess.check_output(
                pip_command + ['pipdeptree', '-rp', pkg],
                stderr=subprocess.STDOUT
            ).decode()
            if dependents.strip():
                print(f"⚠️ 警告: 以下包依赖 {pkg}:")
                print(dependents)
                confirm = input("仍要强制卸载？(y/n): ").lower()
                if confirm != 'y':
                    print(f"已取消 {pkg} 卸载")
                    fail_list.append(pkg)
                    continue
        except subprocess.CalledProcessError:
            pass  # 没有依赖项

        # 执行卸载
        if run_pip_command(pip_command, ['uninstall', '-y'], [pkg], 
                          include_source=False, 
                          current_package=pkg):
            success_list.append(pkg)
            # 检查残留文件
            print(f"▰ 正在验证 {pkg} 卸载结果...")
            result = subprocess.run(pip_command + ['show', pkg], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if b"not found" in result.stderr:
                print(f"✓ {pkg} 已完全移除")
            else:
                print(f"⚠️ 警告: {pkg} 可能仍有残留文件，请手动检查安装目录")
        else:
            fail_list.append(pkg)

    # 显示汇总结果
    print("\n▰▰▰ 卸载结果汇总 ▰▰▰")
    if success_list:
        print(f"✓ 成功卸载: {', '.join(success_list)}")
    if fail_list:
        print(f"✗ 卸载失败: {', '.join(fail_list)}")

def list_all_packages(pip_command):
    try:
        result = subprocess.run(pip_command + ['list', '--format=columns'] + pip_source, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        print("\n已安装的包:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"\n列出已安装包失败: {e.stderr.strip()}")
    except Exception as e:
        print(f"发生未知错误: {e}")

def show_package_details(pip_command, package):
    try:
        result = subprocess.run(pip_command + ['show', package], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        print("\n包详细信息:")
        
        # 汉化字段映射
        field_translation = {
            'Name': '包名称',
            'Version': '版本',
            'Summary': '简介',
            'Home-page': '主页',
            'Author': '作者',
            'Author-email': '作者邮箱',
            'License': '许可证',
            'Location': '安装路径',
            'Requires': '依赖项',
            'Required-by': '被以下包依赖'
        }

        in_license = False
        license_lines = []
        
        for line in result.stdout.splitlines():
            # 处理许可证信息块
            if line.startswith('Copyright') or in_license:
                in_license = True
                license_lines.append(line)
                continue
                
            # 分割字段
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                
                # 翻译字段名称
                if key in field_translation:
                    print(f"{field_translation[key]:<12}: {value}")
                else:
                    print(f"{key:<12}: {value}")
            else:
                print(line)

        # 处理许可证信息
        if license_lines:
            print("\n▰ 许可证信息:")
            print("(以下为简化摘要，完整内容请查看包目录)")
            print("-" * 60)
            print("\n".join(license_lines[:6]))  # 显示前6行关键信息
            print("..."*10 + " [已截断完整许可证内容]")
            
    except subprocess.CalledProcessError as e:
        print(f"\n获取包详细信息失败: {e.stderr.strip()}")
    except Exception as e:
        print(f"发生未知错误: {e}")

def suggest_similar_packages(package_name):
    try:
        print(f"\n正在搜索与 '{package_name}' 相似的包...")
        response = requests.get(f"https://pypi.org/search/?q={package_name}", timeout=5)
        response.raise_for_status()
        
        # 使用正则表达式解析搜索结果
        pattern = re.compile(r'<a class="package-snippet" href="[^"]+">\s*<h3 class="package-snippet__title">\s*<span class="package-snippet__name">([^<]+)</span>\s*<span class="package-snippet__version">([^<]+)</span>')
        matches = pattern.findall(response.text)
        
        if matches:
            print(f"\n找到 {len(matches)} 个可能相关的包:")
            for i, (name, version) in enumerate(matches[:5], 1):  # 显示前5个结果
                print(f"{i}. {name} ({version})")
        else:
            print("未找到相似的包")
            
    except requests.RequestException as e:
        print(f"搜索失败: {e}")
    except Exception as e:
        print(f"发生未知错误: {e}")

def get_random_hitokoto():
    url = "https://api.52vmy.cn/api/wl/yan/yiyan"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, dict) and data.get("code") == 200 and "data" in data and "hitokoto" in data["data"]:
            hitokoto = data["data"]["hitokoto"]
            print(hitokoto)
        else:
            print("\n获取随机一言失败，数据结构不正确.")
    except requests.HTTPError as http_err:
        print(f"\nHTTP 错误: {http_err}")
    except requests.ConnectionError as conn_err:
        print(f"\n连接错误: {conn_err}")
    except requests.Timeout as timeout_err:
        print(f"\n请求超时: {timeout_err}")
    except requests.RequestException as req_err:
        print(f"\n请求失败: {req_err}")
    except json.JSONDecodeError as json_err:
        print(f"\nJSON解码错误: {json_err}")
    except Exception as e:
        print(f"发生未知错误: {e}")

def fetch_announcement():
    url = "https://wz.ikdxhz.top/gg"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        announcement = response.text.strip()
        if announcement:
            print("\n公告内容:")
            print(announcement)
        else:
            print("\n获取公告内容失败，数据为空.")
    except requests.HTTPError as http_err:
        print(f"\nHTTP 错误: {http_err}")
    except requests.ConnectionError as conn_err:
        print(f"\n连接错误: {conn_err}")
    except requests.Timeout as timeout_err:
        print(f"\n请求超时: {timeout_err}")
    except requests.RequestException as req_err:
        print(f"\n请求失败: {req_err}")
    except json.JSONDecodeError as json_err:
        print(f"\nJSON解码错误: {json_err}")
    except Exception as e:
        print(f"发生未知错误: {e}")

def check_version_update():
    """检查程序是否有更新版本"""
    print("正在检查程序更新...")
    url = "https://wz.ikdxhz.top/gg/bb.html"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        update_info = response.text.strip().split('\n')
        
        # 解析服务器返回的信息
        latest_version = update_info[0].strip()
        update_type = update_info[1].strip()
        download_info = update_info[2].strip()
        
        is_important_update = "重要更新" in update_type
        
        if latest_version and latest_version != CURRENT_VERSION:
            print("\n")
            print(" ╔═══════════════════════════════════════════════════════════════╗")#打印标题
            print(" ║                                                               ║")#打印标题
            if is_important_update:
                print(" ║                  ⚠️⚠️ 重要版本更新提醒 ⚠️⚠️                  ║")#打印标题
            else:
                print(" ║                    ⚠️ 版本更新提醒 ⚠️                      ║")#打印标题
            print(" ║                                                               ║")#打印标题
            print(" ╠═══════════════════════════════════════════════════════════════╣")#打印标题
            print(f" ║  当前版本: {CURRENT_VERSION}                                   ║")#打印当前版本
            print(f" ║  最新版本: {latest_version}                                    ║")#打印最新版本
            print(f" ║  更新类型: {update_type}                                     ║")#打印更新类型
            print(" ║                                                               ║")#打印标题
            print(" ║  " + download_info.ljust(65) + "║")#打印下载信息
            print(" ║                                                               ║")#打印标题
            
            if is_important_update:
                print(" ║  ※※※ 重要更新，程序需要更新后才能继续使用 ※※※            ║")#打印强制更新提示
            else:
                print(" ║  建议更新到最新版本以获取新功能和修复                       ║")#打印建议更新提示
            
            print(" ║                                                               ║")#打印标题
            print(" ╚═══════════════════════════════════════════════════════════════╝")#打印标题
            print("\n")#打印标题
            
            # 如果是重要更新，程序将退出
            if is_important_update:
                input("\n按回车键退出程序...")#等待用户按回车键
                sys.exit(0)#退出程序
                
            return False
        else:
            print("检查完成，当前已是最新版本。")#打印检查完成
            return True
    except requests.HTTPError as http_err:
        print(f"\n检查更新失败: HTTP 错误 {http_err}")#打印HTTP错误
    except requests.ConnectionError:
        print("\n检查更新失败: 无法连接到服务器")#打印连接错误
    except requests.Timeout:
        print("\n检查更新失败: 连接超时")#打印超时错误
    except IndexError:
        print("\n检查更新失败: 服务器返回格式不正确")#打印格式错误
    except Exception as e:
        print(f"\n检查更新失败: 未知错误 {e}")#打印未知错误
    return True

def check_network_connection():
    try:
        host = "360.com"
        gethostbyname(host)
        return True
    except gaierror:
        print("无法连接到互联网，请检查您的网络连接.")
        return False

def get_valid_package_name(prompt):
    while True:
        package_name = input(prompt).strip()
        if package_name:
            return package_name
        else:
            print("请输入有效的包名.")

def validate_package_name(package_name):
    try:
        response = requests.get(f"https://pypi.org/pypi/{package_name}/json", timeout=5)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.RequestException as e:
        print(f"验证包名时发生错误: {e}")
        return False

def uninstall_all_non_standard(pip_command):
    def is_standard_package(pkg_name):
        # 更准确的判断方式
        try:
            __import__(pkg_name)
            return True
        except ImportError:
            return False
        except Exception:
            return False

    try:
        # 获取所有用户安装的包
        result = subprocess.run(
            pip_command + ['list', '--format=freeze'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        
        # 解析包列表并过滤
        all_packages = [line.split('==')[0] for line in result.stdout.splitlines()]
        to_uninstall = [
            pkg for pkg in all_packages 
            if not is_standard_package(pkg) 
            and not pkg.lower().startswith('pip')
            and not pkg.lower().startswith('setuptools')
            and not pkg.lower().startswith('wheel')
        ]

        if not to_uninstall:
            print("\n没有可卸载的非官方包")
            return

        print("\n以下非官方包将被卸载:")
        print("\n".join(f"- {pkg}" for pkg in to_uninstall))
        print(f"\n总计: {len(to_uninstall)} 个包")

        confirm = input("\n确定要卸载以上所有非官方包吗？(y/n): ").strip().lower()
        if confirm != 'y':
            print("取消操作")
            return

        # 分批卸载防止命令过长
        batch_size = 10
        total_batches = (len(to_uninstall) + batch_size - 1) // batch_size
        for batch_num, i in enumerate(range(0, len(to_uninstall), batch_size), 1):
            batch = to_uninstall[i:i+batch_size]
            print(f"\n▰▰▰ 正在处理第 {batch_num}/{total_batches} 批 ▰▰▰")
            print(f"本批包含 {len(batch)} 个包: {', '.join(batch)}")
            
            if run_pip_command(pip_command, ['uninstall', '-y'], batch, include_source=False):
                print(f"✓ 成功卸载本批 {len(batch)} 个包")
                print(f"进度: [{batch_num}/{total_batches}] {batch_num/total_batches:.0%}")
            else:
                print(f"✗ 本批 {len(batch)} 个包中有部分卸载失败")
            
            # 显示分隔线
            print("-" * 60)

        print("\n✅ 操作完成，建议重启Python环境使更改生效")

    except subprocess.CalledProcessError as e:
        print(f"获取包列表失败: {e.stderr.strip()}")
    except Exception as e:
        print(f"发生未知错误: {str(e)}")

def main(pip_command):
    # 在程序启动时检查版本更新
    check_version_update()
    
    current_source = get_current_source()
    print(f"\n当前使用的pip源: {current_source}\n")
    
    # 新增环境检查
    print("\n=== 环境检查 ===")
    print(f"Python版本: {sys.version.split()[0]}")
    print(f"操作系统: {sys.platform} ({'64位' if sys.maxsize > 2**32 else '32位'})")
    
    try:
        import platform
        print(f"系统版本: {platform.platform()}")
        print(f"处理器架构: {platform.machine()}")
    except ImportError:
        pass
    
    try:
        pip_version = subprocess.check_output(pip_command + ['--version']).decode().split()[1]
        print(f"Pip版本: {pip_version}")
    except Exception as e:
        print(f"获取pip版本失败: {str(e)}")
    
    print(f"当前工作目录: {os.getcwd()}")
    print(f"Python可执行路径: {sys.executable}")
    print("================\n")
    
    if check_network_connection():
        get_random_hitokoto()
    
    print("\nikdxhz出品，必属精品")
    
    while True:
        print("\n请选择操作:")
        print("1. 切换pip源")
        print("2. 安装包")
        print("3. 更新单个包")
        print("4. 更新所有包")
        print("5. 卸载包")
        print("6. 列出所有包")
        print("7. 显示包详情")
        print("8. 获取公告")
        print("9. 卸载所有非官方包")
        print("10. 退出")
        
        choice = input("请输入选项 (1-10): ").strip()
        
        if choice == "10":
            print("退出程序.")
            break
        
        if choice == "1":
            print("\n请选择pip源:")
            print("1. 阿里云")
            print("2. 清华大学")
            print("3. 豆瓣")
            print("4. 中国科学技术大学")
            print("5. 华为云")
            print("6. 腾讯云")
            print("7. 网易")
            print("8. 百度")
            print("9. 默认源")
            
            source_choice = input("请输入源编号 (1-9): ").strip()
            
            source_mapping = {
                "1": "aliyun",
                "2": "tsinghua",
                "3": "douban",
                "4": "ustc",
                "5": "huawei",
                "6": "tencent",
                "7": "netease",
                "8": "baidu",
                "9": "default"
            }
            
            selected_source = source_mapping.get(source_choice)
            if selected_source:
                set_pip_source(selected_source)
            else:
                print("无效的选择，请输入 1-9 之间的数字。")
        
        elif choice == "2":
            package_name = get_valid_package_name("请输入包名: ")
            version = input("请输入版本号（留空以安装最新版本）: ").strip()
            install(pip_command, package_name, version if version else None)
        
        elif choice == "3":
            package_name = get_valid_package_name("请输入包名: ")
            update_single(pip_command, package_name)
        
        elif choice == "4":
            update_all(pip_command)
        
        elif choice == "5":
            package_name = get_valid_package_name("请输入包名: ")
            uninstall(pip_command, package_name)
        
        elif choice == "6":
            list_all_packages(pip_command)
        
        elif choice == "7":
            package_name = get_valid_package_name("请输入包名: ")
            show_package_details(pip_command, package_name)
        
        elif choice == "8":
            fetch_announcement()
        
        elif choice == "9":
            print("\n警告: 此操作将卸载所有非Python标准包!")
            print("包括通过pip安装的所有第三方包")
            confirm = input("确定要继续吗？(yes/no): ").strip().lower()
            if confirm == 'yes':
                uninstall_all_non_standard(pip_command)
            else:
                print("取消操作")
        
        else:
            print("无效的选择，请输入 1, 2, 3, 4, 5, 6, 7, 8, 9, 10.")
        
        input("\n按回车键返回主菜单...")

if __name__ == "__main__":
    check_python_version()
    try:
        import requests
    except ImportError:
        print("缺少requests包，请先安装requests包: pip install requests")
        sys.exit(1)
    
    pip_command = get_pip_command()
    main(pip_command)