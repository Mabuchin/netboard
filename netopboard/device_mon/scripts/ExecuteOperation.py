##!/usr/bin/env python
# -*- coding: utf-8 -*-

from Exscript.protocols import SSH2
from Exscript.Account import Account
from Exscript.PrivateKey import PrivateKey
from cmd_manipulation import IOSXRStringManipulation,JUNOSStringManipulation

class IOSXROperation:
	conn = SSH2()
	os_version = ''
	str_ope = IOSXRStringManipulation(os_version)

	def __init__(self,ip,user_id,password,version):
		self.conn.connect(ip)
		self.os_version = version
		account = Account(user_id, password)
		self.conn.login(account)
		self.conn.execute('terminal length 0')

	def exit_session(self):
		self.conn.send('exit\r')
		self.conn.close()

	def save_status(self,filename=None):
		pass

	def get_bgp_summary(self):
		try:
			self.conn.execute('show bgp summary')
			split_result = self.conn.response.splitlines()
			result = self.str_ope.bgp_summary_cleanup(split_result)
		except Exception as e:
			self.exit_session()
			raise e
		return result

	def any_cmd(self,command):
		try:
			self.conn.execute(command)
			result = self.conn.response
		except Exception as e:
			self.exit_session()
			raise e
		return result

	def ping_send(self,dist,count = 10,size = 1400):
		try:
			self.conn.execute('ping %s count %s size %s'%(dist,count,size))
			result = self.conn.response
			split_result = self.conn.response.splitlines()
			result = self.str_ope.ping_cleanup(split_result)
		except Exception as e:
			self.exit_session()
			raise e
		return result

	def get_processes_status(self):
		try:
			result={'processes' : {}}
			self.conn.execute('show process cpu')
			split_result = self.conn.response.splitlines()
			cpu_result = self.str_ope.cpu_process_cleanup(split_result)
			self.conn.execute('show memory sum bytes location 0/RSP0/CPU0')
			split_result = self.conn.response.splitlines()
			memory_result = self.str_ope.memory_used_cleanup(split_result)
			result['processes'].update({'cpu_used_percentage': cpu_result , 'memory_used_percentage' : memory_result})
		except Exception as e:
			self.exit_session()
			raise e
		return result

	def get_log(self,num):
		try:
			self.conn.execute('show logging | utility tail count %s'%num)
			split_result = self.conn.response.splitlines()
			result = self.str_ope.logcheck(split_result,num)
		except Exception as e:
			self.exit_session()
			raise e
		return result

	def get_session(self):
		try:
			return self.conn
		except Exception as e:
			self.exit_session()
			ErrorCatch().error_out(e)
			raise e

	def get_interface_status(self):
		try:
			self.conn.execute('show interfaces description')
			split_result = self.conn.response.splitlines()
			result = self.str_ope.interfaces_status_cleanup(split_result)
		except Exception as e:
			self.exit_session()
			raise
		return result


class JUNOSOperation:
	# session
	conn = SSH2()
	os_version = ''
	def __init__(self,ip,user_id,password,version):
		self.os_version = version
		self.conn.connect(ip,port='2222')
		account = Account(user_id,password)
		self.conn.login(account)
		self.conn.set_prompt(self.conn.get_prompt())
		self.conn.execute('set cli screen-length 0')

	def any_cmd(self,command):
		str_ope = JUNOSStringManipulation(self.os_version)
		try:
			self.conn.execute(command)
			result = self.conn.response
		except Exception as e:
			ErrorCatch().error_out()
			self.exit_session()
			raise e
		return result

	def get_processes_status(self):
		str_ope = JUNOSStringManipulation(self.os_version)
		try:
			self.conn.execute('show chassis routing-engine')
			split_result = self.conn.response.splitlines()
			result = str_ope.process_cleanup(split_result)
		except Exception as e:
			self.exit_session()
			raise e
		return result

	def exit_session(self):
		self.conn.send('exit\r')
		self.conn.close()

	def get_bgp_summary(self):
		str_ope = JUNOSStringManipulation(self.os_version)
		try:
			self.conn.execute('show bgp summary')
			split_result = self.conn.response.splitlines()
			result = str_ope.bgp_summary_cleanup(split_result)
		except Exception as e:
			self.exit_session()
			raise e
		return result

	def get_interface_status(self):
		str_ope = JUNOSStringManipulation(self.os_version)
		try:
			self.conn.execute('show interfaces terse')
			interface_terse = self.conn.response.splitlines()
			self.conn.execute('show interfaces description')
			description_terse = self.conn.response.splitlines()
			result = str_ope.interfaces_status_cleanup(interface_terse , description_terse)
		except Exception as e:
			self.exit_session()
			raise e
		return result

	def get_log(self,num):
		str_ope = JUNOSStringManipulation(self.os_version)
		try:
			self.conn.execute('show log messages | last %s'%num)
			split_result = self.conn.response.splitlines()
			result = str_ope.logcheck(split_result,num)
		except Exception as e:
			self.exit_session()
			raise e
		return result

	def ping_send(self,dist,count = 10,size = 1400):
		str_ope = JUNOSStringManipulation(self.os_version)
		try:
			self.conn.execute('ping %s count %s size %s rapid'%(dist,count,size))
			result = self.conn.response
			split_result = self.conn.response.splitlines()
			result = str_ope.ping_cleanup(split_result)
		except Exception as e:
			ErrorCatch().error_out()
			self.exit_session()
			raise e
		return result
