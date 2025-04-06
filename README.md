# Python库管理器

![GitHub](https://img.shields.io/github/license/ikdxhz/Python-package-manager)
![Python Version](https://img.shields.io/badge/python-3.6.1%2B-blue)
![Platform](https://img.shields.io/badge/platform-Windows%2010%2B-blue)

## 下载
[下载链接](https://wwaw.lanzoub.com/icHkn2std76b) | 提取码: **e6ny**

## 简介

Python库管理器是一个专为Windows 10及以上系统设计的Python包管理工具，旨在简化Python包的安装、更新、卸载和管理过程。它特别针对国内网络环境进行了优化，支持多种国内镜像源，以解决国内用户在使用PyPI官方源时可能遇到的网络问题。

## 功能特点

### 镜像源切换

支持以下国内镜像源，加速包安装和更新：
- 阿里云
- 清华大学
- 豆瓣
- 中国科学技术大学
- 华为云
- 腾讯云
- 网易
- 百度

### 包管理功能

- **安装包**：支持安装指定版本或最新版本的包。
- **更新单个包**：更新已安装的包到最新版本。
- **更新所有包**：批量更新所有可更新的包。
- **卸载包**：支持单个包或多个包的卸载。
- **卸载所有非官方包**：一键卸载所有非Python标准库的第三方包。

### 信息查询与显示

- **列出所有包**：显示已安装的所有包及其版本信息。
- **显示包详情**：查看包的详细信息，包括版本、依赖项、安装路径等。
- **实时进度显示**：安装和更新过程中实时显示进度条。
- **错误处理**：智能分析和处理安装、更新过程中的错误。

### 环境检查

- 检测Python版本、操作系统版本、网络连接状态等环境信息。
- 自动检查工具是否有更新版本。

### 用户体验

- **随机一言**：每次启动时显示一条随机名言，增添趣味性。
- **操作日志**：记录操作过程中的关键信息，便于问题排查。

## 系统要求

- **操作系统**：Windows 10 及以上版本
- **Python版本**：3.6.1 或更高版本
- **依赖项**：requests库（用于网络请求）

## 安装方法

### 方法一：直接运行脚本

1. 下载最新版本的脚本：
   ```bash
   wget https://github.com/ikdxhz/Python-package-manager/raw/main/python库管理器-1.87.2.2.py
   ```

2. 运行脚本：
   ```bash
   python python库管理器-1.87.2.2.py
   ```

### 方法二：克隆GitHub仓库

1. 克隆仓库：
   ```bash
   git clone https://github.com/ikdxhz/Python-package-manager.git
   cd Python-package-manager
   ```

2. 运行脚本：
   ```bash
   python python库管理器-1.87.2.2.py
   ```

## 使用方法

### 启动工具

运行脚本后，工具会自动检测环境并显示主菜单：

```
作者: ikdxhz
程序版本: 1.87.2.2
当获取公告不可用时，请访问Github存储库：https://github.com/ikdxhz/Python-package-manager/

请选择操作:
1. 切换pip源
2. 安装包
3. 更新单个包
4. 更新所有包
5. 卸载包
6. 列出所有包
7. 显示包详情
8. 获取公告
9. 卸载所有非官方包
10. 退出
```

### 切换pip源

选择菜单中的 **1. 切换pip源**，然后选择一个镜像源：

```
请选择pip源:
1. 阿里云
2. 清华大学
3. 豆瓣
4. 中国科学技术大学
5. 华为云
6. 腾讯云
7. 网易
8. 百度
9. 默认源
```

### 安装包

选择 **2. 安装包**，输入包名和版本号（可选）：

```
请输入包名: requests
请输入版本号（留空以安装最新版本）: 2.26.0
```

### 更新单个包

选择 **3. 更新单个包**，输入包名：

```
请输入包名: requests
```

### 更新所有包

选择 **4. 更新所有包**，工具会列出所有可更新的包并提示确认：

```
以下包可更新:
包名                当前版本        最新版本
--------------------------------------------------
requests            2.25.1         2.26.0
numpy               1.19.5         1.20.0

确定要更新以上所有包吗？(y/n): y
```

### 卸载包

选择 **5. 卸载包**，输入包名：

```
请输入包名: requests
```

### 列出所有包

选择 **6. 列出所有包**，查看已安装的包列表：

```
已安装的包:
Package           Version
---------------------------
requests          2.26.0
numpy             1.20.0
```

### 显示包详情

选择 **7. 显示包详情**，输入包名查看详细信息：

```
包详细信息:
包名称          : requests
版本            : 2.26.0
简介            : HTTP for Humans.
主页            : https://requests.readthedocs.io
作者            : Kenneth Reitz
作者邮箱        : me@kennethreitz.org
许可证          : Apache 2.0
安装路径        : C:\Users\YourUser\AppData\Local\Programs\Python\Python39\site-packages\requests
依赖项          : urllib3, certifi, charset-normalizer
被以下包依赖     : None
```

### 获取公告

选择 **8. 获取公告**，查看最新公告内容。

### 卸载所有非官方包

选择 **9. 卸载所有非官方包**，工具会列出所有非官方包并提示确认：

```
以下非官方包将被卸载:
- requests
- numpy

确定要卸载以上所有非官方包吗？(yes/no): yes
```

## 常见问题

### Q: 为什么需要切换国内镜像源？

A: 国内用户访问PyPI官方源可能较慢或不稳定，切换到国内镜像源可以显著提高安装速度。

### Q: 如何检查工具是否有更新？

A: 工具启动时会自动检查是否有新版本，如果有更新会显示提示信息。

### Q: 如何处理安装失败？

A: 工具会自动分析错误原因并提供解决方案。如果问题无法解决，请访问GitHub仓库提交Issue。

### Q: 工具支持哪些操作系统？

A: 本工具专为Windows 10及以上系统设计，不支持Windows 7、8等旧版本操作系统。

## 贡献指南

欢迎贡献代码或提出改进建议！请遵循以下步骤：

1. Fork本仓库。
2. 创建一个新分支：`git checkout -b feature/your-feature`
3. 提交您的更改：`git commit -m 'Add some feature'`
4. 推送到分支：`git push origin feature/your-feature`
5. 提交Pull Request。

## License

本项目采用 [MIT License](LICENSE) 许可证。您可以自由使用、修改和分发本项目，但需要保留版权声明。

## 历史版本下载
1.87.2.2：https://wwaw.lanzoub.com/iiHlL2ssi5he 密码:7wj0

---

**ikdxhz出品，必属精品**
