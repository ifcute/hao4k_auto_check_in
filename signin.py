# coding=utf-8
import requests
import os
import re
import time
from datetime import datetime
import pytz
import sys
from lxml import etree

# hao4k 账户信息
username = os.environ["HAO4K_USERNAME"]
password = os.environ["HAO4K_PASSWORD"]

# Bark 通知
bark_key = os.environ["SECRET_BARK_KEY"]
bark_url = "https://api.day.app/%s/" % (bark_key)

# hao4k 签到 url
user_url = "https://www.hao4k.cn/member.php?mod=logging&action=login"
base_url = "https://www.hao4k.cn/"
signin_url = "https://www.hao4k.cn/plugin.php?id=k_misign:sign&operation=qiandao&formhash={formhash}&format=empty"
form_data = {
    'formhash': "",
    'referer': "https://www.hao4k.cn/",
    'username': username,
    'password': password,
    'questionid': "0",
    'answer': ""
}
inajax = '&inajax=1'

signin_ranking = ''       # 签到排名
consecutive_days = ''     # 连续天数
signin_level = ''         # 签到等级
points_reward = ''        # 积分奖励
total_days = ''           # 总天数
today_signin = ''         # 今日签到数


def run(form_data):
  # 通过Session类新建一个会话（会话保持）
  s = requests.Session()
  s.headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36'})
  headers = {"Content-Type": "text/html", 'Connection': 'close'}
  # 发送网络请求
  user_resp = s.get(user_url, headers=headers)
  #print("############ [%d] %s" % (sys._getframe().f_lineno, user_resp.text))
  # 返回 user_resp.text 中所有与 action="(.*?)" 相匹配的全部字串，返回形式为数组
  login_text = re.findall('action="(.*?)"', user_resp.text)
  print("############ [%d] %s" % (sys._getframe().f_lineno, login_text))
  for loginhash in login_text:
    if 'loginhash' in loginhash:
      login_url = base_url + loginhash + inajax
      login_url = login_url.replace("amp;", "")     # 将"amp;"替换为""，及删除amp;
      print("############ [%d] %s" % (sys._getframe().f_lineno, login_url))
  # 返回 user_resp.text 中与 formhash=(.*?)\' 相匹配的第一个字串
  form_text = re.search('formhash=(.*?)\'', user_resp.text)
  print("############ [%d] %s" % (sys._getframe().f_lineno, form_text.group(1)))
  form_data['formhash'] = form_text.group(1)        # 记录验证数据
  print("############ [%d] %s" % (sys._getframe().f_lineno, form_data))

  login_resp = s.post(login_url, data=form_data)
  test_resp = s.get('https://www.hao4k.cn/k_misign-sign.html', headers=headers)
  if username in test_resp.text:
    print('登陆成功')
  else:
    return '登录失败'
  # 返回 test_resp.text 中与 formhash=(.*?)" 相匹配的第一个字串
  signin_text = re.search('formhash=(.*?)"', test_resp.text)
  signin_resp = s.get(signin_url.format(formhash=signin_text.group(1)))
  test_resp = s.get('https://www.hao4k.cn/k_misign-sign.html', headers=headers)
  #print("############ [%d] %s" % (sys._getframe().f_lineno, test_resp.text))
  if '您的签到排名' in test_resp.text:
    print('signin!')
  else:
    print(test_resp.text)
    return '签到失败或者已经签到，请登录 hao4k 查看签到状态'

  global signin_ranking       # 签到排名
  global consecutive_days     # 连续天数
  global signin_level         # 签到等级
  global points_reward        # 积分奖励
  global total_days           # 总天数
  global today_signin         # 今日签到数
  form_text1 = re.search(r'您的签到排名：\d+', test_resp.text)
  signin_ranking = form_text1.group()
  form_text1 = re.search(r'\d+<span>人</span>', test_resp.text)
  today_signin = form_text1.group()
  print("############ [%d] %s" % (sys._getframe().f_lineno, today_signin))
  today_signin = "今日签到人数：" + today_signin.replace("\\<(.*?)\\>", "")     # 将"<.*?>"替换为""，及删除"<.*?>";
  html = etree.HTML(test_resp.text)
  value = html.xpath('//input[@id="lxdays"]/@value')[0]
  consecutive_days = "连续天数：%s天" %(value)
  value = html.xpath('//input[@id="lxlevel"]/@value')[0]
  signin_level = "签到等级：%s" %(value)
  value = html.xpath('//input[@id="lxreward"]/@value')[0]
  points_reward = "积分奖励：%s" %(value)
  value = html.xpath('//input[@id="lxtdays"]/@value')[0]
  total_days = "总天数：%s天" %(value)
  print("############ [%d] %s" % (sys._getframe().f_lineno, signin_ranking))
  print("############ [%d] %s" % (sys._getframe().f_lineno, consecutive_days))
  print("############ [%d] %s" % (sys._getframe().f_lineno, signin_level))
  print("############ [%d] %s" % (sys._getframe().f_lineno, points_reward))
  print("############ [%d] %s" % (sys._getframe().f_lineno, total_days))
  print("############ [%d] %s" % (sys._getframe().f_lineno, today_signin))



# 可以理解为程序的入口
if __name__ == "__main__":
  # 判断参数信息是否存在
  if not username or not password or not bark_key:
    print('未找到登录信息，请参考 readme 中指导，前往仓库 setting/secrets，添加对应 key')
    # 执行异常处理命令
    raise Exception('Could not find any keys')
    # 异常处理执行后，不在执行后续语句

  # 执行登录流程，若登录成功返回信息为空，若登录失败将失败信息放到signin_log
  signin_log = run(form_data)

  # 判断signin_log是否为空，为空表示登录成功
  if signin_log is None:
    send_content = "hao4k 每日签到成功！"
    print('Sign in automatically!')
  # 不为空，登录失败，打印失败信息
  else:
    send_content = signin_log
    print(signin_log)

  # BARK 消息推送
  #tim = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
  tz = pytz.timezone('Asia/Shanghai') #东八区
  tim = datetime.fromtimestamp(int(time.time()),
    pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S %Z%z')
  message = "Hao4K签到结果通知/%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s" %(username, tim, send_content, signin_ranking, consecutive_days, signin_level, points_reward, total_days, today_signin)
  url = "%s%s" %(bark_url, message)
  params = {'group': 'Hao4k 每日签到结果通知'}
  r = requests.post(url, params=params)
  if r.status_code == 200:
    print('已通知 BARK')
  else:
    print('通知 BARK 推送失败，详情：\n请求状态码：{}\n{}'.format(r.status_code, r.text))

