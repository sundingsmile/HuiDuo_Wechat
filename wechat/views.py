from django.shortcuts import render
from django.http import HttpResponse
from hashlib import sha1
import requests
import wechatpy
# Create your views here.

'''全局变量'''
wx_id = 'wxdba6bfce4509444b'  # 微信账号
wx_pw = 'f2137f686be39b0baff10410b44f14c7'  # 微信密码
token = 'huiduowulian'  # 微信公众号平台设置的token

# 微信公众号服务程序
def wx(request):

    '''和微信服务器进行连接'''
    if request.method == 'GET':
        print('配置服务器')
        wx_gw_cs = request.GET  # 微信服务器在GET中携带的参数

        '''分别取出其中重要参数'''
        wx_gw_signature = wx_gw_cs['signature']
        wx_gw_echostr = wx_gw_cs['echostr']
        wx_gw_timestamp = wx_gw_cs['timestamp']
        wx_gw_nonce = wx_gw_cs['nonce']

        hash_list = [token,wx_gw_timestamp,wx_gw_nonce]  #新建一个临时文件list

        '''服务器对接步骤：
        1、token,wx_gw_timestamp,wx_gw_nonce这几个参数进行排序；
        2、按照排好的顺序拼接成一个字符串然后进行sha1加密；
        3、跟微信服务器发送过来的wx_gx_signature参数进行对比，如果相同并且原样返回wx_gx_echostr字符串表示对接成功；
        '''
        if all(hash_list):
            hash_list.sort()  # 对三个参数进行排序
            temp_str = ''.join(hash_list)  # 将排序好的字符串连接起来
            local_signature = sha1(temp_str.encode('utf-8')).hexdigest()  # 对排序好的字符串进行sha1加密并且以16进制方式显示
            if local_signature == wx_gw_signature:  # 如果签名相同原样返回wx_gw_echostr，表示服务器链接成功
                return HttpResponse(wx_gw_echostr)
            else:
                return HttpResponse('Signature is wrong!')

    elif request.method == 'POST':  # 对接收到的信息进行处理
        msg = wechatpy.parse_message(request.body)  # 解析用户发送过来的信息
        if msg.type == 'text':
            reply = wechatpy.replies.TextReply(content = msg.content,message=msg)
        elif msg.type == 'image':
            reply = wechatpy.replies.TextReply(content='图片消息', message=msg)
        elif msg.type == 'voice':
            reply = wechatpy.replies.TextReply(content='语音消息', message=msg)
        elif msg.type == 'video':
            reply = wechatpy.replies.TextReply(content='视频消息', message=msg)
        elif msg.type == 'shortvideo':
            reply = wechatpy.replies.TextReply(content='短视频消息', message=msg)
        elif msg.type == 'location':
            reply = wechatpy.replies.TextReply(content='位置消息', message=msg)
        elif msg.type == 'link':
            reply = wechatpy.replies.TextReply(content='链接消息', message=msg)
        elif msg.type == 'event':
            if msg.event == 'subscribe':
                reply = wechatpy.replies.TextReply(content='欢迎订阅，祝您一路顺风！', message=msg)
            else:
                reply = wechatpy.replies.TextReply(content='欢迎订阅，祝您一路顺风！', message=msg)
        else:
            reply = wechatpy.replies.TextReply(content='其他类型', message=msg)
        print(msg.type)
        return HttpResponse(reply.render())
    else:
        print(wechatpy.parse_message(request.body))
        print('===========================')
        return HttpResponse('Thanks')