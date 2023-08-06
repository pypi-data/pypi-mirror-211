# -*- coding:utf-8 -*-
import json
import pika


class sendnews(object):
    def __init__(self, queueName, priority, environment = 'dev', is_parse = True):
        self.queueName = queueName
        self.priority = priority
        if environment == 'dev':
            username = 'admin'
            password = 'finchina'
            hosts = ['10.17.207.61', '10.17.207.78', '10.17.207.94']
            port = 5672
        elif environment == 'product':
            username = 'finchina'
            password = 'finchina'
            hosts = ['10.17.206.140', '10.17.205.97', '10.17.205.94']
            port = 5672
        else:
            return

        userinfo = pika.PlainCredentials(username, password)
        parameters = (
            pika.ConnectionParameters(host=hosts[0], port=port, connection_attempts=5, retry_delay=1,
                                      credentials=userinfo),
            pika.ConnectionParameters(host=hosts[1], port=port, connection_attempts=5, retry_delay=1,
                                      credentials=userinfo),
            pika.ConnectionParameters(host=hosts[2], port=port, connection_attempts=5, retry_delay=1,
                                      credentials=userinfo)
        )
        self.__connection = pika.BlockingConnection(parameters)
        self.__channel = self.__connection.channel()  # 生成管道，在管道里跑不同的队列
        if is_parse:
            print(self.queueName)
            self.__channel.queue_declare(queue=self.queueName, durable=True)
        else:
            self.__channel.queue_declare(queue=self.queueName, durable=True, arguments={'x-max-priority': 32})

    def send_object(self, object, ensure_ascii=False):
        try:
            content = json.dumps(object, ensure_ascii=ensure_ascii)
            self.__channel.basic_publish(exchange='', routing_key=self.queueName, body=str(content),
                                  properties=pika.BasicProperties(delivery_mode=2, priority=self.priority))  # 历史数据消息等级2 ，日常消息等级15
        except Exception as e:
            print(f"消息发送出错 {e}")
            return False
        else:
            return True

    def send_json(self, jsonStr):
        try:
            self.__channel.basic_publish(exchange='', routing_key=self.queueName, body=str(jsonStr),
                                  properties=pika.BasicProperties(delivery_mode=2, priority=self.priority))  # 历史数据消息等级2 ，日常消息等级15
        except Exception as e:
            return False
        else:
            return True

    def distory(self):
        self.__connection.close()
