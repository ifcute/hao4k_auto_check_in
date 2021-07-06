# coding=utf-8
import requests
import os
import re

# hao4k 账户信息
username = os.environ["HAO4K_USERNAME"]
password = os.environ["HAO4K_PASSWORD"]

# 添加 server 酱通知
sckey = os.environ["SERVERCHAN_SCKEY"]
send_url = "https://sctapi.ftqq.com/%s.send" % (sckey)
send_content = 'Server ERROR'

# Bark 通知
bark_key = os.environ["SECRET_BARK_KEY"]
bark_url = "https://api.day.app/%s/Hao4K签到/%s" % (bark_key, username)

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

def run(form_data):
    s = requests.Session()
    s.headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36'})
    headers = {"Content-Type": "text/html", 'Connection': 'close'}
    user_resp = s.get(user_url, headers=headers)
    login_text = re.findall('action="(.*?)"', user_resp.text)
    for loginhash in login_text:
        if 'loginhash' in loginhash:
            login_url = base_url + loginhash + inajax
            login_url = login_url.replace("amp;", "")
            print(login_url)
    form_text = re.search('formhash=(.*?)\'', user_resp.text)
    print(form_text.group(1))
    form_data['formhash'] = form_text.group(1)
    print(form_data)

    login_resp = s.post(login_url, data=form_data)
    test_resp = s.get('https://www.hao4k.cn/k_misign-sign.html', headers=headers)
    if username in test_resp.text:
      print('登陆成功')
    else:
      return '登录失败'
    signin_text = re.search('formhash=(.*?)"', test_resp.text)
    signin_resp = s.get(signin_url.format(formhash=signin_text.group(1)))
    test_resp = s.get('https://www.hao4k.cn/k_misign-sign.html', headers=headers)
    if '您的签到排名' in test_resp.text:
      print('signin!')
    else:
      print(test_resp.text)
      return '签到失败或者已经签到，请登录 hao4k 查看签到状态'

# 可以理解为程序的入口
if __name__ == "__main__":
  # 判断参数信息是否存在
  if not username or not password or not sckey:
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

  params = {'title': 'Hao4k 每日签到结果通知：', 'desp': send_content}
  r = requests.post(send_url, params=params)
  if r.status_code == 200:
    print('已通知 server 酱')
  else:
    print('通知 Server 酱推送失败，详情：\n请求状态码：{}\n{}'.format(r.status_code, r.text))

  r = requests.post(bark_url)
  if r.status_code == 200:
    print('已通知 BEAK')
  else:
    print('通知 BEAK 推送失败，详情：\n请求状态码：{}\n{}'.format(r.status_code, r.text))

