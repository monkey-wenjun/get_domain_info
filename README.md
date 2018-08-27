# get_domain_info 脚本



这个脚本主要是用来查询(单或多)域名解析和备案的。

>源码开源但是备案查询接口调用的是 NowAPI 的，需要把get_single_filing_info 方法中的 appkey 或 sign 替换成你自己的。。或者使用其他接口。

# 环境

- python 3


**第三方模块安装**

```python
pip3 install -r requirements.txt 
```



requirements.txt 内容如下:    

```
dnspython3
argparse
requests
tldextract
```



**查看帮助**

```python
 #./get_domain_info.py

            This is Get domain info Tools

usage: get_domain_info.py [-h] [-dl DOMAIN_LIST [DOMAIN_LIST ...]]
                          [-df DOMAIN_FILE]
                          [-rl RECORD_LIST [RECORD_LIST ...]]
                          [-rf RECORD_FILE] [-ip IP [IP ...]] [-a] [-u] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -dl DOMAIN_LIST [DOMAIN_LIST ...], --domain_list DOMAIN_LIST [DOMAIN_LIST ...]
                        Query single or multiple domain name filing
                        information.
  -df DOMAIN_FILE, --domain_file DOMAIN_FILE
                        Query multiple domain name filing information as
                        files.
  -rl RECORD_LIST [RECORD_LIST ...], --record_list RECORD_LIST [RECORD_LIST ...]
                        Query single or multiple domain name resolution.
  -rf RECORD_FILE, --record_file RECORD_FILE
                        Query multiple domain name resolutions as files.
  -ip IP [IP ...], --ip IP [IP ...]
                        Query IP attribution.
  -a, --auth            Show Auth Info.
  -u, --update          Update Tools.
  -v, --version         Show Version.
```



## 使用说明

不管是备案还是 DNS 查询，如果域名包含完整 URL 的，会自动过滤提取裸域后进行查询，例如查询备案：

```
 ./get_domain_info.py -dl https://awen.me/post/18464.html
awen.me   ALREADY_BEIAN
```



或是查询 DNS



```
./get_domain_info.py -rl https://awen.me/post/18464.html
Domain                        CNAME                         NS                            A
awen.me                                                     adrian.ns.cloudflare.com.     183.131.200.74,183.131.200.69,183.131.200.61,183.131.200.72,183.131.200.68
```



### 1.批量查询域名解析



1.**获取单个或多个 域名的解析**

``` py
 ./get_domain_info.py -rl 163yun.com www.163yun.com 
```



2. **从文件读取域名列表进行域名解析查询**

```
./get_domain_info.py -rf ~/Downloads/domain.txt
```



> 从文件读取域名查询的，结果中会进行去重，有重复 IP 的只提取一个



### 2.查询备案



1.**获取单个或多个域名备案**（多个域名用空格分隔）

```
./get_domain_info.py -dl baidu.com awen.me
```



2.**从文件读取域名列表进行备案查询**

```
./get_domain_info.py -df ~/Downloads/domain.txt
```

### 3.批量查询 IP 归属地
1.**批量查询单个或多个域名的归属地**
```python
./get_domain_info.py -ip www.baidu.com www.awen.me www.163.com 59.111.10.12
14.215.177.38 归属地是: 中国,广东,广州,,电信
183.131.24.37 归属地是: 中国,浙江,杭州,,电信
115.231.22.125 归属地是: 中国,浙江,湖州,,电信
59.111.10.12 归属地是: 中国,浙江,杭州,,电信/联通/移动
```
