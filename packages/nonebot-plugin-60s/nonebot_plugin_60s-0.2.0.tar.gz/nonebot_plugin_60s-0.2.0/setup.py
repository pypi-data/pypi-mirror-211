# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_60s']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.0,<0.24.0',
 'nonebot-adapter-onebot>=2.0.0b1,<3.0.0',
 'nonebot-plugin-apscheduler>=0.2.0,<0.3.0',
 'nonebot2>=2.0.0b2,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-60s',
    'version': '0.2.0',
    'description': '每天60秒读懂世界',
    'long_description': '<div align="center">\n  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>\n  <br>\n  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>\n</div>\n\n<div align="center">\n\n# nonebot-plugin-60s\n\n_✨ 每天60秒读懂世界 ✨_\n\n<a href="./LICENSE">\n    <img src="https://img.shields.io/github/license/A-kirami/nonebot-plugin-moyu.svg" alt="license">\n</a>\n<a href="https://pypi.python.org/pypi/nonebot-plugin-60s">\n    <img src="https://img.shields.io/pypi/v/nonebot-plugin-60s.svg" alt="pypi">\n</a>\n<img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">\n\n</div>\n\n## 📖 介绍\n\n<details>\n  <summary>效果图</summary>\n\n![example](https://raw.githubusercontent.com/techotaku39/nonebot-plugin-60s/master/readme/example.jpg)\n\n</details>\n\n## 💿 安装\n\n<details>\n<summary>使用 nb-cli 安装</summary>\n在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装\n\n    nb plugin install nonebot-plugin-60s\n\n</details>\n\n<details>\n<summary>使用包管理器安装</summary>\n在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令\n\n<details>\n<summary>pip</summary>\n\n    pip install nonebot-plugin-60s\n</details>\n<details>\n<summary>pdm</summary>\n\n    pdm add nonebot-plugin-60s\n</details>\n<details>\n<summary>poetry</summary>\n\n    poetry add nonebot-plugin-60s\n</details>\n<details>\n<summary>conda</summary>\n\n    conda install nonebot-plugin-60s\n</details>\n\n打开 nonebot2 项目的 `bot.py` 文件, 在其中写入\n\n    nonebot.load_plugin(\'nonebot_plugin_60s\')\n\n</details>\n\n## 配置说明(可选)\n有时候api会失效，就改了下\n微信公众号地址：https://mp.weixin.qq.com/\n抓取的是公众号的内容，我也就找了一个直接分享图片的公众号：每日60s简报（dailybriefing60s），也是很稳定的每天都会在8点前就会推送当天简报\n\n先登陆你的公众号，因为我们要获取一些你的cookie以及token\n登陆后F12查看请求\n![](./images/123.png)\n红圆框是可以找到的地方（大概），红方框就是cookie以及token(cookies:后面的才是，你也可以右键复制值，token=后面的才是)(这也不懂就使用默认吧)\n| 配置项 | 说明 |\n|:-----:|:----:|\n| calendar_cookie: str = "" | 填写微信公众号的cookie |\n| calendar_token: str = "" | 填写微信公众号的token |\n\n## 🎉 使用\n### 指令表\n| 指令  | 说明 |\n|:-----:|:----:|\n| 60s/读懂世界 | 查看今天的60s日历 |\n| 60s/读懂世界+设置 | 以连续对话的形式设置60s日历的推送时间 |\n| 60s/读懂世界+设置 小时:分钟 | 设置60s日历的推送时间 |\n| 60s/读懂世界+状态 | 查看本群的60s日历状态 |\n| 60s/读懂世界+禁用 | 禁用本群的60s日历推送 |\n\n## 💡 鸣谢\n\n### [A-kirami摸鱼日历](https://github.com/A-kirami/nonebot-plugin-moyu)：本项目就是用大佬的项目改了几行代码，连说明文档也是（）',
    'author': 'Ananovo',
    'author_email': 'techotaku39@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
