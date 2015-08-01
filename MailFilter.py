#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib
import time
import datetime

"""Email filter converter.
Given an .dat or .xml E-mail filter rule file, and convert it to the other type, making thunderbird filters compatible with Gmail!
"""

class FilterRule:
	"""All the data needed for one E-mail filter rule"""
	def __init__(self, name, enabled, types, action, actionValue, condition, time_id, date, time):
		self.name = name
		self.enabled = enabled
		self.types = types
		self.action = action
		self.actionValue = actionValue
		self.condition = condition
		self.time_id = time_id
		self.date = date
		self.time = time
		
class FilterList:
	"""List with all the rules in it"""
	def __init__(self, address, rule_list):
		self.address = address
		self.rule_list = rule_list



def read_filters(filename):
  """Reads the filtername, let the file be read to be used later. Then writes the appropriate converted file."""
  if re.search(r'[.]\w+', filename):
  	  extension = re.search(r'[.]\w+', filename).group()
  else:
  	  print "The given file has no extension. Closing now."
  	  return None
  namefile = filename[:-1*len(extension)]
  
  if extension == '.xml':
  	  ext = 0
  	  filters = xml_read(filename)
  	  dat_write(filename, filters)
  elif extension == '.dat':
  	  ext = 1
  	  filters = dat_read(filename)
  	  print filters.address
  	  print namefile
  	  xml_write(namefile, filters)
  	  print "Your .xml filter has been written."
  else:
  	  print 'This converter only handles .dat or .xml Mail filters, your extension was' + extension + '. Please find the correct file.'
  	  return None
  	  
def xml_read(filename):
	"""Reads the XML file and get the rules out of it to write into a .dat file."""
	filter_list = []
	
	
  	f = open(filename, 'r')
  	for line in f:
  	  print line
	  	  
	  
  	f.close()
	
	print "XML"
	
	return filters
	
def dat_read(filename):
	"""Reads the DAT file and get the rules out of it to write into a .xml file."""
	filter_list = []
	
	filter_dict = {}
		
	i = 0
	j = 0
  	f = open(filename, 'r')
  	
  	for line in f:
  	  	  
	  if i < 2:
	  	  i += 1
	  else:
	  	  ident = re.search(r'\w+=', line).group()[:-1]
	  	  value = line[len(ident)+2:-2]
	  	  #print ident + ":    " + value
		  if ident == "name" and i > 2 and filter_dict['enabled'] == 'yes': 		  
	  	  	  time_id = str(int(round(time.time()*1000)))
	  	  	  date = str(datetime.date.today())
	  	  	  times = str(datetime.datetime.now().time())[:-7]
	  	  	  filter_list.append(FilterRule(filter_dict['name'], filter_dict['enabled'], filter_dict['type'], filter_dict['action'], filter_dict['actionValue'], filter_dict['condition'], time_id, date, times))
	  	  	  #print filter_list[len(filter_list)-1].time_id
		  filter_dict[ident] = value
	  	  i += 1
  	f.close()
  	
  	print "DAT" + str(datetime.date.today()) + " " + str(datetime.datetime.now().time())[:-7] 
  	mail = raw_input("Please enter your complete e-mail address: ")
	filters = FilterList(mail, filter_list)
	print filters.address
	return filters
	
def xml_write(namefile, filters):
	"""Writes the XML filter file to be used in GMail."""
	xml_string = """<?xml version='1.0' encoding='UTF-8'?><feed 
		xmlns='http://www.w3.org/2005/Atom' 
		xmlns:apps='http://schemas.google.com/apps/2006'>"""
	xml_string += "\n	<title>Mail Filters</title> \n	<id>tag:mail.google.com,2008:filters:"
	
	date = str(datetime.date.today())
	times = str(datetime.datetime.now().time())[:-7]
	
	filter_list = filters.rule_list
	for i in range(0, len(filter_list)):
		xml_string += filter_list[i].time_id
		xml_string += ","
	xml_string += "</id>"
	xml_string += "\n	<updated>" + date + "T" + times + "Z</updated>"
	name = raw_input("Please enter your full name: ")
	xml_string += "\n	<author>\n		<name>" + name + "</name>\n		<email>" + filters.address + "</email>\n	</author>"
	for i in range(0, len(filter_list)):
		xml_string += xml_write_rule(filter_list[i], date, times)
	
	xml_string += "\n</feed>"
	f = open(namefile + '.xml', 'w')
	f.write(xml_string)
	f.close()
	
	print len(filter_list)
	
def xml_write_rule(filter_rule, date, times):
	string = ""
	string += "\n	<entry>\n		<category term='filter'></category>\n		<title>Mail Filter</title>"
	string += "\n		<id>tag:mail.google.com,2008:filter:" + filter_rule.time_id + "</id>"
	string += "\n		<updated>" + date + "T" + times + "Z</updated>"
	string += "\n		<content></content>"
	
	"""condition_from = re.search(r'\(\w+,', filter_rule.condition).group()[1:-1]
	condition_value = (re.search(r"\).+,", filter_rule.condition[::-1]).group()[1:-1])[::-1]
	condition_value = re.search(r",.+", condition_value).group()[1:]
	
	if "AND" in filter_rule.condition and "OR" in filter_rule.condition:
		print "WOahHH!"
	if filter_rule.condition.count("AND") > 1:
		print "MORE THAN ONE AND!!"
		print filter_rule.condition
		
	string += "\n		<apps:property name='" + condition_from + "' value='" + condition_value + "'/>"
	"""
	string += xml_write_condition(filter_rule.condition)
	string += xml_write_action(filter_rule.actionValue)	
	
	string += "\n		<apps:property name='sizeOperator' value='s_sl'/>"
	string += "\n		<apps:property name='sizeUnit' value='s_smb'/>"
	string += "\n	</entry>"
	return string
	
	
def xml_write_condition(string):
	'Writes the lines needed for setting the correct condition.'
	or_match = [match.start() for match in re.finditer(re.escape("OR"), string)]
	and_match = [match.start() for match in re.finditer(re.escape("AND"), string)]
	string2 = []
	if len(or_match)>0:
		string2 = string.split("OR")
	elif len(and_match)>0:
		string2 = string.split("AND")
	else:
		string2.append(string)
	
	string4 = []
	string5 = []
	for string3 in string2:
		if "(" in string3 and "," in string3:
			commas = [match.start() for match in re.finditer(re.escape(","), string3)]
			open_bracket = re.search(re.escape("("), string3).start()
			close_bracket = re.search(re.escape(")"), string3).start()
			string4.append(string3[max(commas)+1:close_bracket])
			string5.append(string3[open_bracket+1:min(commas)])			
	condition_cat = {}
	for i in range(0,len(string5)):
		if string5[i] in condition_cat:
			condition_cat[string5[i]].append(i)
		else:
			condition_cat[string5[i]] = [i]

	return_string = ''
	for key in condition_cat:
		return_string += "\n		<apps:property name='" + key + "' value='"
		j = 0
		for k in condition_cat[key]:
			if j >= 1:
				return_string += " OR "
			return_string +=  string4[k]
			j +=1
		return_string += "'/>"
	return return_string
	
def xml_write_action(actionValue):
	string = '' 
	if '/Trash' in actionValue:
		string += "\n		<apps:property name='shouldTrash' value='true'/>"
	elif re.search(r'googlemail.com/.+', actionValue):
		label = re.search(r'googlemail.com/.+', actionValue).group()[15:]
		string += "\n		<apps:property name='label' value='" + label + "'/>"
	else:
		print "This is an exception on the rule!"
		print actionValue
	return string
	
def dat_write(filename, filters):
    """Writes the DAT filter file to be used in Thunderbird."""  
    return "Yay!"


def main():
  args = sys.argv[1:]

  if not args:
    print 'usage: [--tofile file] inputfile '
    sys.exit(1)

  tofile = ''
  if args[0] == '--tofile':
    todir = args[1]
    del args[0:2]

  Filter_logs = read_filters(args[0])

  #if tofile:
  #  download_images(img_urls, todir)
  #else:
  # print '\n'.join(img_urls)

if __name__ == '__main__':
  main()
