import requests
import subprocess
import time
url = 'https://ifconfig.me'

proxies = {
        'http':'socks5:192.168.203.128:9050',
        'https':'socks5:192.168.203.128:9050'
        }

res = requests.get(url, proxies=proxies)
print(res.text)

subprocess.Popen(['systemctl', 'reload']+['tor']).wait()
print('tor reload')
time.sleep(2)
res = requests.get(url, proxies=proxies)
print(res.text)