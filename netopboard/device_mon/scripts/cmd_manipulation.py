##!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

class IOSXRStringManipulation():

	os_version = ''
	def __init__(self,version):
		pass

	def include_keyword_lines(self,split_result,search_word):
		separate_summary = []
		pattern = search_word
		prog = re.compile(pattern)
		for line in split_result:
			test = prog.match(line)
			if test == None:
				pass
			else:
				separate = line.split()
				separate_summary.append(separate)
		return separate_summary

	def bgp_summary_cleanup(self,split_result):
		bgp_status={'bgp': []}
		execute_result = self.include_keyword_lines(split_result,r'^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+')
		for state in execute_result:
			neighbor_status = re.compile(r'^[0-9]+').match(state[9])
			routenum = 0
			state[9]=state[9].strip('!')
			if neighbor_status == None:
				status_str = state[9]
			else :
				status_str = 'Establ'
				routenum = int(state[9])

			bgp_status['bgp'].append({'neighbor' : state[0] , 'status' : status_str ,'route' : routenum , 'as' : state[2]})
		return bgp_status

	def ping_cleanup(self,split_result):
		execute_result = self.include_keyword_lines(split_result,r'^Success*')
		print 'Ping result : %s'%(execute_result)
		return execute_result


	def cpu_process_cleanup(self,split_result):
		execute_result = self.include_keyword_lines(split_result,r'^CPU*')
		for state in execute_result:
				cpu_usage_percentage = int(state[5].strip('%;'))
		return cpu_usage_percentage


	def memory_used_cleanup(self,split_result):
		execute_result = self.include_keyword_lines(split_result,r'.*Application')
		empty_mem = execute_result[0][4].strip('(')
		used_mem = execute_result[0][3]

		mem_percentage = (float(empty_mem) / float(used_mem))*100
		return mem_percentage

	def logcheck(self,split_result,num):
		result = {'logs' : []}
		#line = line.strip('RP/0/RSP0/CPU0:')
		#line = line.strip('LC/0/1/CPU0:')
		pattern = r'.*(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec).*'
		prog = re.compile(pattern)
		for line in split_result:
			test = prog.match(line)
			if test == None:
				pass
			else:
				result['logs'].append({'message' : line})
		return result

	def interfaces_status_cleanup(self,split_result):
		result = {'interface' : []}
		execute_result = self.include_keyword_lines(split_result,r'^(Lo.*)|(Nu.*)|(Mg.*)|(Te.*)|(Bu.*)')
		for state in execute_result:
			descri_len=len(state)
			descript = ''
			if descri_len >= 4:
				for i in range(3,descri_len):
					state[i] = state[i] + ' '
					descript = descript + state[i]
			result['interface'].append({'interface_name':state[0] , 'admin' : state[1] , 'physical' : state[2] ,'description' : descript})
		return result


class JUNOSStringManipulation():

	os_version = ''
	def __init__(self,version):
		self.os_version = version

	def include_keyword_lines(self,split_result,search_word):
		separate_summary = []
		for line in split_result:
			if line != '':
				pattern = search_word
				prog = re.compile(pattern)
				test = prog.match(line)
				if test == None:
					pass
				else:
					separate = line.split()
					separate_summary.append(separate)

		return separate_summary

	def include_keyword_string(self,split_result,search_word):
		separate_summary = []
		for line in split_result:
			if line != '':
				pattern = search_word
				prog = re.compile(pattern)
				test = prog.match(line)
				if test == None:
					pass
				else:
					separate_summary.append(line.split())
		return separate_summary


	def include_keyword_configure(self,split_result,search_word):
		separate_summary = []
		for line in split_result:
			if line != '':
				pattern = search_word
				prog = re.compile(pattern)
				test = prog.match(line)
				if test == None:
					pass
				else:
					separate_summary.append(line.strip('biglobe@MX960#'))
		return separate_summary

	def configure_cleanup(self,split_result):
		execute_result = self.include_keyword_configure(split_result,r'^biglobe.*\#.*(edit.*)|(set.*)|(delete.*)|(top.*)|(up.*)')
		return execute_result

	def bgp_summary_cleanup(self,split_result):
		bgp_status={'bgp': []}
		execute_result = self.include_keyword_lines(split_result,r'^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+')
		if len(execute_result) == 0:
			bgp_status['bgp'].append({'neighbor' : 'Can not find this Version %s'%self.os_version , 'status' : 'None' ,'route' : 'None' , 'as' : 'None'})
			return bgp_status

		for state in execute_result:

			neighbor_status = re.compile(r'^([0-9]+)/([0-9]+)/([0-9]+)/([0-9]+)').match(state[7])
			route_state = state[7]
			if neighbor_status == None:
					routenum = 0
					status_str = route_state
			else :
				status_str = 'Establ'
				routenum = int(neighbor_status.group(1))

			bgp_status['bgp'].append({'neighbor' : state[0] , 'status' : status_str ,'route' : routenum , 'as' : state[1]})
		return bgp_status

	def ping_cleanup(self,split_result):
		execute_result = self.include_keyword_lines(split_result,r'^round-trip*')
		print 'Ping result : %s'%(execute_result)
		return execute_result


	def process_cleanup(self,split_result):
		result={'processes' : {}}
		cpu_result = self.include_keyword_lines(split_result,r'.*Idle*')
		memory_result = self.include_keyword_lines(split_result,r'.*Memory*')
		cpu_usage_percentage = 100 - int(cpu_result[0][1])
		memory_usage_percentage = int(memory_result[0][2])
		result['processes'].update({'cpu_used_percentage': cpu_usage_percentage , 'memory_used_percentage' : memory_usage_percentage})
		return result


	def cpu_process_cleanup(self,split_result):
		execute_result = self.include_keyword_lines(split_result,r'^Idle*')
		for state in execute_result:
				cpu_usage_percentage = 100 - int(state[1])
		return cpu_usage_percentage

	def memory_process_cleanup(self,split_result):
		execute_result = self.include_keyword_lines(split_result,r'^Memory*')
		for state in execute_result:
				memory_usage_percentage = int(state[2])
		return int(memory_usage_percentage)

	def interfaces_status_cleanup(self, interface_terse , description_terse):
		result = {'interface' : []}
		execute_result = self.include_keyword_lines(interface_terse,r'^(lo.*)|(ae.*)|(xe.*)')
		description_terses = self.include_keyword_lines(description_terse,r'^(lo.*)|(ae.*)|(xe.*)')
		for state in execute_result:
			descript = ''
			for description in description_terses:

				if description[0] == state[0]:
					description_len = len(description)
					for i in range(3,description_len):
						description[i] = description[i] + ' '
						descript = descript + description[i]
			result['interface'].append({'interface_name':state[0] , 'admin' : state[1] , 'physical' : state[2] ,'description' : descript})
		return result

	def logcheck(self,split_result,num):
		result = {'logs' : []}
		pattern = r'.*(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec).*'
		prog = re.compile(pattern)
		for line in split_result:
			log_line = prog.match(line)
			if log_line == None:
				pass
			else:
				result['logs'].append({'message' : line})
		return result