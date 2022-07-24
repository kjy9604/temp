import subprocess
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

Driver = None # 공용 웹드라이버

class DriverUtil:

	# 공용 웹드라이버 리턴
	@staticmethod
	def getDriver():
		global Driver
		return Driver

	# selenium과 tor 연결
	@staticmethod
	def connection(): 

		global Driver

		DriverUtil.changeIp()
		if (Driver is None):

			temp = True
			num = 0 # 커넥션 시도 회수
			while temp and num < 90:
				try:
					num += 1
					print(num)
					# selenium option
					PROXY="localhost:9050"
					opts = Options()
					user_agent = 'Mozilla/5.0 CK={} (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'

					webdriver.DesiredCapabilities.CHROME['proxy'] = {
						"httpProxy": PROXY,
						"ftpProxy": PROXY,
						"sslProxy": PROXY,
						"proxyType": "MANUAL"
					}

					# soup option
					# proxies = {
					#     'http': 'socks5://127.0.0.1:9050',
					#     'https': 'socks5://127.0.0.1:9050'
					# }
					webdriver.DesiredCapabilities.CHROME['acceptSslCerts']=True

					opts.add_argument("user-agent="+user_agent)
					opts.add_argument('--headless')
					opts.add_argument('--no-sandbox')
					opts.add_argument('--proxy-server='"socks5://"+PROXY)
					opts.binary_location = '/usr/bin/google-chrome'

					url = "http://wtfismyip.com/text"
					Driver =webdriver.Chrome(executable_path="/usr/local/bin/chromedriver",options=opts)
					Driver.create_options()
					Driver.execute_script("window.open('');")
					Driver.switch_to.window(Driver.window_handles[-1])
					Driver.get(url)
					time.sleep(5)
					ip = Driver.find_element_by_tag_name('pre').text

					print(f'현재 IP  ::::  {ip}')
					temp = False
				except Exception as e:
					print(e)
					Driver.quit()
			return Driver
		else:
			url = "http://wtfismyip.com/text"
			Driver.get(url)
			time.sleep(5)
			ip = Driver.find_element_by_tag_name('pre').text

			print(f'현재 IP  ::::  {ip}')
			return Driver

	@staticmethod
	def changeIp():
		global Driver
		if (Driver is None):
			return
		else :
			# IP Change
			subprocess.Popen(['systemctl', 'reload']+['tor']).wait()
			print('tor reload')
			time.sleep(2)
			Driver.execute_script("window.open('');")
			Driver.switch_to.window(Driver.window_handles[-1])
			return Driver

	# selenium 탭 종료 후 2분 슬립
	@staticmethod
	def closeSelenium():
		global Driver
		if (Driver is None) :
			return None
		else :
			Driver.delete_all_cookies()
			# Driver.close()
			time.sleep(120)
			return None

	# selenium 종료 후 2분 슬립
	@staticmethod
	def quitSelenium():
		global Driver
		if (Driver is None) :
			return None
		else :
			Driver.delete_all_cookies()
			Driver.close()
			Driver.quit()
			print(Driver.session_id)
			time.sleep(120)
			return None