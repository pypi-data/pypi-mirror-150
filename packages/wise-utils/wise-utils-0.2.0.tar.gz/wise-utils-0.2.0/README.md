# 小工具
- common
  - exceptions: 异常处理
  - ftp: FTP上传下载
  - logger: 日志打印
  - mail: 邮件发送
  - mysql: mysql增删改查
  - retry_decorator: 重试装饰器
  - setqueue: 去重队列，有序去重队列
- configuration_center 配置中心
  - apollo 阿波罗
- spider 爬虫基类
  - basespider 


```shell
# 安装
pip install -i https://pypi.org/simple/ wise-utils

# 打包
python3 -m build

python3 -m twine upload --repository testpypi dist/*

python3 -m twine upload --repository pypi dist/*
```
