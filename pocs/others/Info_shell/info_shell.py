# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType


class Vuln(ABVuln):
    vuln_id = 'Info_shell'  # 平台漏洞编号，留空
    name = '疑似webshell木马后门文件'  # 漏洞名称
    level = VulnLevel.MED  # 漏洞危害级别
    type = VulnType.INFO_LEAK  # 漏洞类型
    disclosure_date = 'Unknown'  # 漏洞公布时间
    desc = '''
    webshell就是以asp、php、jsp或者cgi等网页文件形式存在的一种命令执行环境，也可以将其称做为一种网页后门。黑客在入侵了一个网站后，通常会将asp或php后门文件与网站服务器WEB目录下正常的网页文件混在一起，然后就可以使用浏览器来访问asp或者php后门，得到一个命令执行环境，以达到控制网站服务器的目的。
    '''  # 漏洞描述
    ref = 'Unknown'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'Info_shell'  # 漏洞应用名称
    product_version = 'Unknown'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '49e2e37c-3bab-4217-8fcc-43511ee07849'
    author = 'cscan'  # POC编写者
    create_date = '2018-04-26'  # POC创建时间

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
            filename_list = ['shell', 'webshell', 'ma',
                             'caidao', 'yi', 'a', 'muma', 'dama', 'xiaoma']
            filetypt_list = ['.asp', '.php', '.aspx', '.asa', '.jsp']

            for filename in filename_list:
                for filetype in filetypt_list:
                    webshell = filename+filetype
                    request = requests.get(
                        '{target}/{payload}'.format(target=self.target, payload=webshell))
                    if request.status_code == 200 and "404" not in request.text and "不存在" in request.text and "未找到" in request.text:
                        self.output.report(self.vuln, '发现{target}存在{name}漏洞;文件地址为{url}'.format(
                            target=self.target, name=self.vuln.name, url=request.url))
        except Exception as e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.target = self.target.rstrip(
            '/') + '/' + (self.get_option('base_path').lstrip('/'))
        try:
            self.output.info('开始对 {target} 进行 {vuln} 漏洞利用'.format(
                target=self.target, vuln=self.vuln))
            filename_list = ['shell', 'webshell', 'ma',
                             'caidao', 'yi', 'a', 'muma', 'dama', 'xiaoma']
            filetypt_list = ['.asp', '.php', '.aspx', '.asa', '.jsp']
            for filename in filename_list:
                for filetype in filetypt_list:
                    webshell = filename+filetype
                    request = requests.get(
                        '{target}/{payload}'.format(target=self.target, payload=webshell))
                    if request.status_code == 200 and "404" not in request.text and "不存在" in request.text and "未找到" in request.text:
                        url = request.url
                        self.output.report(self.vuln, '发现{target}存在{name}漏洞,文件地址为{url}'.format(
                            target=self.target, name=self.vuln.name, url=url))

        except Exception as e:
            self.output.info('执行异常{}'.format(e))


if __name__ == '__main__':
    Poc().run()
