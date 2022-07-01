import requests
from bs4 import BeautifulSoup
import re
import execjs
import urllib3
from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings(InsecureRequestWarning)


class CUMT:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36 Edg/103.0.1264.37',
            'Referer': 'http://authserver.cumt.edu.cn/authserver/login'
        }

    # 获取登录需要的表单数据
    def get_login_data(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36 Edg/103.0.1264.37'
        }
        url = 'https://authserver-cumt-edu-cn.webvpn.cumt.edu.cn:8118/authserver/login?service=https://webvpn.cumt.edu.cn/auth/cas_validate?entry_id=1'
        username = self.username
        password = self.password
        # 解析网页源代码
        html = s.get(url, headers=headers, verify=False)
        # 利用JS脚本加密密码
        with open('EncryPSW.js', encoding='utf-8') as f:
            jscode = f.read()
        ctx = execjs.compile(jscode)
        execution = re.findall(r'name="execution" value="(.*?)"', html.text)[0]
        pwdEncryptSalt = re.findall(r'id="pwdEncryptSalt" value="(.*?)"', html.text)[0]
        encrypted_password = ctx.call('encryptPassword', password, pwdEncryptSalt)
        data = {
            'username': username,
            'password': encrypted_password,
            'captcha': '',
            '_eventId': 'submit',
            'cllt': 'userNameLogin',
            'dllt': 'generalLogin',
            'lt:': '',
            'execution': execution
        }
        return data

    def login(self):
        url = 'https://authserver-cumt-edu-cn.webvpn.cumt.edu.cn:8118/authserver/login?service=https://webvpn.cumt.edu.cn/auth/cas_validate?entry_id=1'
        data = self.get_login_data()
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36 Edg/103.0.1264.37'
        }
        s.post(url, data=data, headers=headers, verify=False)
        return

    def isLogin(self):
        url = "https://webvpn.cumt.edu.cn/por/perinfo.csp?apiversion=1"
        result = s.get(url, verify=False).content
        soup = BeautifulSoup(result, 'xml')
        res = soup.find_all('ErrorCode')
        if res[0].string == '20026':
            print("\033[31m登录失败！\033[0m")
            return False
        else:
            print('\033[32m登录成功！\033[0m')
            return True


username = input('请输入学号')
password = input('请输入密码')
s = requests.Session()
cumt = CUMT(username, password)
cumt.login()