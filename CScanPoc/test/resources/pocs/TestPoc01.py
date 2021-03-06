# coding: utf-8

import json
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType


class Vuln(ABVuln):
    vuln_id = '00000000-0000-0000-VULN-000000000000'
    name = 'Test Vuln'
    level = VulnLevel.HIGH
    type = VulnType.OTHER
    disclosure_date = '2049-04-02'
    desc = '''Test Vuln 01 '''
    ref = 'http://lotuc.org'
    cnvd_id = 'cnvd-no-such-thing'  # cnvd漏洞编号
    cve_id = 'cve-no-such-thing'  # cve编号
    product = 'LotucTestProduct'  # 漏洞应用名称
    product_version = 'all'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '00000000-0000-0000-0POC-000000000000'
    author = 'lotuc'
    create_date = '2049-04-02'

    def __init__(self):
        super(Poc, self).__init__(Vuln())
        self.option_schema = {
            'properties': {
                'base_path': {
                    'type': 'string',
                    'description': '部署路径',
                    '$default_ref': {
                        'property': 'deploy_path'
                    }
                },
                'component': {
                    'type': 'string',
                    'default': 'Unkown'
                }
            }
        }

    def verify(self):
        self.output.info('扫描 %s' % self.target)
        self.output.info('传入的组件属性：')
        for line in json.dumps(
                self.components_properties, indent=2).split('\n'):
            self.output.info(line)
        self.output.info('传入的执行参数：')
        for line in json.dumps(
                self.exec_option, indent=2).split('\n'):
            self.output.info(line)
        try:
            self.output.info('部署路径：%s' % self.get_option('base_path'))
        except:
            pass
        try:
            self.output.info('传入组件：%s' % self.get_option('component'))
        except:
            pass
        self.output.warning('警告信息 001')
        self.output.warning(self.vuln, '漏洞警告信息 001')
        self.output.warning('警告信息 002')
        self.output.report(self.vuln, '报告漏洞信息')

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
