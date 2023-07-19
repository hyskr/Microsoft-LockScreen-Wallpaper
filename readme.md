# Microsoft-LockScreen-Wallpaper

本项目是一个 Python 脚本，用于从 Windows 系统的 Spotlight 功能中复制并整理图片。脚本将图片分为横版和竖版两类，并将它们分别存储到两个不同的文件夹中。

## 安装

你需要在你的系统上安装 Python 3，并且安装以下的依赖库：

```bash
pip install Pillow
```

## 使用
首先，你需要修改脚本中的源文件夹和目标文件夹的路径，以符合你的系统设置。然后，你可以直接运行这个脚本：
```bash
python wallpaper_getter.py
```
脚本将会复制所有新的图片到指定的文件夹，并且在日志文件中记录已经复制过的文件。

## 依赖
本项目依赖于以下的 Python 库：
- os
- re
- shutil
- hashlib
- logging
- datetime
- PIL (Pillow)
- ctype
