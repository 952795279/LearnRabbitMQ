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
后端端口: 5672  
前台访问: **localhost:15672**  
账号、密码均为: guest


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

### 发送消息
1.连接rabbitmq  
```python
#!/usr/bin/env python

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel
```

2.声明队列
```python
channel.queue_declare(queue="hello")
```

3.指定交换机和队列名称  
交换机`exchange`，空字符串指定**默认交换**  
队列名称`routing_key`，命名为hello  
消息主体message`body`，传入字符串Hello World!
```python
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")
```

4.关闭连接
```
connection.close()
```

### 接收消息
1.连接及声明队列  
同样连接一样
```python
#!/usr/bin/env python

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel

channel.queue_declare("hello")
```
命令行查看队列及消息情况
```sh
## linux
sudo rabbitmqctl list_queues
## windows
rabbitmqctl list_queues
```

2.订阅消息  
`callback`向队列订阅函数
```python
## 定义回调函数
def callback(ch, method, properties, body):
    print(f"[x] Received {body}")
## 关联队列
channel.basic_consume(
        queue="hello", auto_ack=True, on_message_callback=callback)
## 循环，等待数据，并运行回调
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
```

# 2.工作队列


## 2.1 工作队列（使用pika客户端）

**1、先决条件**  
rabbitmq已安装，且标准端口为5672

**2、教程重点**  
在之前教程，编写了发送和接收消息的程序，在本教程，将创建一个队列，用于多个工人分配任务  

工作队列，背后主要思想是避免立即执行资源密集型并必须等待其完成。相反，我们安排稍后完成的任务。我们将任务封装成消息并将其发送到队列中。在后台运行的工作进程将弹出任务并最终执行作业。当您运行许多工作人员时，任务将在他们之间共享。  

这个概念在 Web 应用程序中特别有用，因为在 Web 应用程序中不可能在较短的 HTTP 请求窗口内处理复杂的任务。

在本教程的前一部分中，我们发送了一条包含“Hello World!”的消息。现在我们将发送代表复杂任务的字符串。我们没有现实世界的任务，比如要调整图像大小或要渲染 pdf 文件，所以让我们通过使用该time.sleep()函数来假装我们很忙来假装它。我们将字符串中点数作为其复杂度；每个点将占一秒钟的“工作”。例如， 描述的一个假任务Hello... 将花费三秒钟。

我们将稍微修改前面示例中的send.py代码，以允许从命令行发送任意消息。该程序会将任务安排到我们的工作队列中，所以我们将其命名为 `new_task.py`

```python
import sys

message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=message)
print(f" [x] Sent {message}")
```  

我们旧的receive.py脚本还需要一些更改：它需要为消息正文中的每个点伪造一秒钟的工作。它将从队列中弹出消息并执行任务，所以我们称它为`worker.py`：
```python
import time

def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")
    time.sleep(body.count(b'.'))
    print(" [x] Done")
```

## 2.2 循环调度
使用任务队列的优点之一是能够轻松并行工作。如果我们正在积压工作，我们可以添加更多工人，这样就可以轻松扩展。  

首先，让我们尝试worker.py同时运行两个脚本。他们都会从队列中获取消息，但是具体如何获取呢？让我们来看看。  

您需要打开三个控制台。两个将运行worker.py 脚本。这些控制台将是我们的两个消费者 - C1 和 C2。  

```sh
# shell 1
python worker.py
# => [*] Waiting for messages. To exit press CTRL+C
```

```sh
# shell 2
python worker.py
# => [*] Waiting for messages. To exit press CTRL+C
```

在第三个任务中，我们将发布新任务。启动消费者后，您可以发布一些消息：  
```sh
# shell 3
python new_task.py First message.
python new_task.py Second message..
python new_task.py Third message...
python new_task.py Fourth message....
python new_task.py Fifth message.....
```  

让我们看看向我们的工人交付了什么：
```sh
# shell 1
python worker.py
# => [*] Waiting for messages. To exit press CTRL+C
# => [x] Received 'First message.'
# => [x] Received 'Third message...'
# => [x] Received 'Fifth message.....'
```

```sh
# shell 2
python worker.py
# => [*] Waiting for messages. To exit press CTRL+C
# => [x] Received 'Second message..'
# => [x] Received 'Fourth message....'
```
默认情况下，RabbitMQ 会将每条消息按顺序发送给下一个消费者。平均而言，每个消费者都会收到相同数量的消息。这种分发消息的方式称为循环法。与三名或更多工人一起尝试此操作。


## 2.3 消息确认  
执行一项任务可能需要几秒钟的时间，您可能想知道如果消费者启动一项长任务并在完成之前终止会发生什么。使用我们当前的代码，一旦 RabbitMQ 将消息传递给消费者，它会立即将其标记为删除。在这种情况下，如果终止一个工作线程，它刚刚处理的消息就会丢失。已发送给该特定工作人员但尚未处理的消息也会丢失。  

但我们不想失去任何任务。如果一名工人死亡，我们希望将任务交付给另一名工人。  

为了确保消息永远不会丢失，RabbitMQ 支持 消息确认。消费者发回确认（确认），告诉 RabbitMQ 已收到并处理特定消息，并且 RabbitMQ 可以自由删除它。  

如果消费者在没有发送 ack 的情况下死亡（其通道关闭、连接关闭或 TCP 连接丢失），RabbitMQ 将了解消息未完全处理并将重新排队。如果同时有其他消费者在线，那么它会快速将其重新传递给另一个消费者。这样你就可以确保不会丢失任何消息，即使工人偶尔会死亡。  

消费者交付确认时强制执行超时（默认为 30 分钟）。这有助于检测从不确认交付的有问题（卡住）的消费者。您可以按照传送确认超时中所述增加此超时 。  

默认情况下，手动消息确认处于打开状态。在前面的示例中，我们通过标志显式关闭它们auto_ack=True 。一旦我们完成了任务，就应该删除这个标志并向工作人员发送适当的确认。  

```python
def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")
    time.sleep(body.count(b'.') )
    print(" [x] Done")
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_consume(queue='hello', on_message_callback=callback)
```

使用此代码，您可以确保即使在处理消息时使用 CTRL+C 终止工作程序，也不会丢失任何内容。工作线程终止后不久，所有未确认的消息都会被重新传递。  

确认必须在接收交付的同一通道上发送。尝试使用不同的通道进行确认将导致通道级协议异常。请参阅有关确认的文档指南 以了解更多信息。  

**忘记确认**  
错过 basic_ack 是一个常见的错误。 这是一个很容易犯的错误，但后果却很严重。 当您的客户端退出时，消息将被重新传送（这可能看起来像随机重新传送），但 RabbitMQ 会占用越来越多的内存，因为它无法释放任何未确认的消息。  

为了调试这种错误，您可以使用rabbitmqctl 打印该messages_unacknowledged字段：
```sh
sudo rabbitmqctl list_queues name messages_ready messages_unacknowledged
```
windows上去掉sudo:
```sh
rabbitmqctl.bat list_queues name messages_ready messages_unacknowledged
```

## 2.4 消息持久性