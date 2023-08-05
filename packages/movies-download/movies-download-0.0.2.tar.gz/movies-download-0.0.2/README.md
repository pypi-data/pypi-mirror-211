# 自由行
一个下载电影的助手。
方便下载m3u8格式的视频文件。

# 使用方法
请自行研究。

# 打包程序

## 安装打包工具
```shell
python -m pip install --upgrade build
```
## 创建配置文件后, 开始打包，执行下面的命令
```shell
python -m build
```

## 安装上传工具并上传到PyPI，执行下面的命令
```shell
python -m pip install --upgrade twine
python -m twine upload dist/*
```
