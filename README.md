# LearnRabbitMQ
学习rabbitmq  
rabbitmq安装再wsl上，编程语言使用python

# 0.安装RabbitMQ

## 在unbuntu或者Diebian安装Rabbitmq及Erlang
仅操作ubuntu安装Rabbitmq及Erlang，其他方式请参见<a href="https://www.rabbitmq.com/docs/download">官方安装文档</a>

### (1)升级wsl-ubuntu至22.04版本
***注：ubuntu版本在22.04版本的直接跳过此步骤***  
1.修改升级文件  
```sh
sudo vim /etc/update-manager/release-upgrades
```
确保最下边一行`Prompt=lts`  
2.执行命令升级
```sh
# 升级系统组件并检查软件更新
sudo apt update

# 更新软件
sudo apt upgrade -y

# 更新发行版
sudo do-release-upgrade
```
点击y下载新包，再点击y删除旧包  
3.检验是否升级完成
```sh
neofetch
```
版本显示未22.04  

### (2)安装rabbitmq
<a href="https://www.rabbitmq.com/docs/install-debian#apt-quick-start-cloudsmith">Cloudsmith Quick Start Script</a>  
1.安装基本依赖项
```sh
sudo apt-get update -y

sudo apt-get install curl gnupg -y
```
2.启用 apt HTTPS传输  
为了使 apt 能够从 Cloudsmith.io 镜像或 Launchpad 下载 RabbitMQ 和 Erlang 软件包
```sh
sudo apt-get install apt-transport-https
```
3.添加存储库签名密钥  
Cloudsmith 使用自己的 GPG 密钥（每个存储库一个）对分布式包进行签名。
为了使用存储库，必须将其签名密钥添加到系统中。这将使 apt 能够信任由该密钥签名的包。
```sh
sudo apt-get install curl gnupg apt-transport-https -y

## Team RabbitMQ's main signing key
curl -1sLf "https://keys.openpgp.org/vks/v1/by-fingerprint/0A9AF2115F4687BD29803A206B73A36E6026DFCA" | sudo gpg --dearmor | sudo tee /usr/share/keyrings/com.rabbitmq.team.gpg > /dev/null
## Community mirror of Cloudsmith: modern Erlang repository
curl -1sLf https://github.com/rabbitmq/signing-keys/releases/download/3.0/cloudsmith.rabbitmq-erlang.E495BB49CC4BBE5B.key | sudo gpg --dearmor | sudo tee /usr/share/keyrings/rabbitmq.E495BB49CC4BBE5B.gpg > /dev/null
## Community mirror of Cloudsmith: RabbitMQ repository
curl -1sLf https://github.com/rabbitmq/signing-keys/releases/download/3.0/cloudsmith.rabbitmq-server.9F4587F226208342.key | sudo gpg --dearmor | sudo tee /usr/share/keyrings/rabbitmq.9F4587F226208342.gpg > /dev/null
```
4.添加源列表文件  
与所有第 3 方 apt 存储库一样，描述 RabbitMQ 和 Erlang 包存储库的文件必须放置在该/etc/apt/sources.list.d/目录下。 /etc/apt/sources.list.d/rabbitmq.list是推荐的位置
```sh
## Provides modern Erlang/OTP releases from a Cloudsmith mirror
##
deb [signed-by=/usr/share/keyrings/rabbitmq.E495BB49CC4BBE5B.gpg] https://ppa1.novemberain.com/rabbitmq/rabbitmq-erlang/deb/ubuntu $distribution main
deb-src [signed-by=/usr/share/keyrings/rabbitmq.E495BB49CC4BBE5B.gpg] https://ppa1.novemberain.com/rabbitmq/rabbitmq-erlang/deb/ubuntu $distribution main

# another mirror for redundancy
deb [signed-by=/usr/share/keyrings/rabbitmq.E495BB49CC4BBE5B.gpg] https://ppa2.novemberain.com/rabbitmq/rabbitmq-erlang/deb/ubuntu $distribution main
deb-src [signed-by=/usr/share/keyrings/rabbitmq.E495BB49CC4BBE5B.gpg] https://ppa2.novemberain.com/rabbitmq/rabbitmq-erlang/deb/ubuntu $distribution main

## Provides RabbitMQ from a Cloudsmith mirror
##
deb [signed-by=/usr/share/keyrings/rabbitmq.9F4587F226208342.gpg] https://ppa1.novemberain.com/rabbitmq/rabbitmq-server/deb/ubuntu $distribution main
deb-src [signed-by=/usr/share/keyrings/rabbitmq.9F4587F226208342.gpg] https://ppa1.novemberain.com/rabbitmq/rabbitmq-server/deb/ubuntu $distribution main

# another mirror for redundancy
deb [signed-by=/usr/share/keyrings/rabbitmq.9F4587F226208342.gpg] https://ppa2.novemberain.com/rabbitmq/rabbitmq-server/deb/ubuntu $distribution main
deb-src [signed-by=/usr/share/keyrings/rabbitmq.9F4587F226208342.gpg] https://ppa2.novemberain.com/rabbitmq/rabbitmq-server/deb/ubuntu $distribution main
```
5.安装包  
更新源列表后，apt需要运行apt-get update：
```sh
sudo apt-get update -y
```
然后安装该软件包
```sh
## Install Erlang packages
sudo apt-get install -y erlang-base \
                        erlang-asn1 erlang-crypto erlang-eldap erlang-ftp erlang-inets \
                        erlang-mnesia erlang-os-mon erlang-parsetools erlang-public-key \
                        erlang-runtime-tools erlang-snmp erlang-ssl \
                        erlang-syntax-tools erlang-tftp erlang-tools erlang-xmerl

## Install rabbitmq-server and its dependencies
sudo apt-get install rabbitmq-server -y --fix-missing
```
6.启用rabbitmq  
```sh
## 检验状态
sudo /etc/init.d/rabbitmq-server status
## 启动服务
sudo /etc/init.d/rabbitmq-server start
## 关闭服务
sudo /etc/init.d/rabbitmq-server stop
## 启用前台管理面板
rabbitmq-plugins enable rabbitmq_management
```
后端端口5672  
前台访问`localhost:15672`  
账号、密码为guest


# 1.Hello World!
rabbitmq是一个消息代理，作为一个**消息中间件**，作用是**转发消息**

**生产者**就是发送消息  
**队列**就是存储消息  
**消费者**就是接受消息  

## 1.1 Hello World!(使用pika客户端)

安装pika客户端
```sh
python -m pip install pika --upgrade
```

1.连接rabbitmq  
```python
#!/usr/bin/env python

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel
```

2.声明队列
