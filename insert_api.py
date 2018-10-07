import sublime, sublime_plugin, os, re, threading

mutex = threading.Lock()
apis  = []
snips = []
debug = 0

def plugin_loaded():
	print("InsertApi loading...")
	apis.clear()
	snips.clear()
	t = threading.Thread(target = WorkThread)
	t.start()

def WorkThread():
	print("WorkThread")
	insert_api_settings = sublime.load_settings("InsertApi.sublime-settings")
	dir_list = insert_api_settings.get("c_h_file_dirs")
	for i in dir_list:
		print("[%s]:%s" % (i[0], i[1]))
		ListAndParseHeaderFiles(i[1], "[%s] " % i[0])
	return

def ListAndParseHeaderFiles(rootdir, location):
	print("ListAndParseHeaderFiles")
	files = ListHeaderFiles(rootdir, location)
	for file in files:
		# print("ParseFile: %s" % file[0])
		ParseFile(file[0], file[1])
	print("parse done - [%s]" % rootdir)

def ListHeaderFiles(rootdir, location):
	files = []
	list = os.listdir(rootdir) 
	for i in range(0, len(list)):
		path = os.path.join(rootdir, list[i])
		if os.path.isdir(path):
			files.extend(ListHeaderFiles(path, location + list[i] + "/"))
		if os.path.isfile(path) and re.search(r'\.[h|H]$', path):
			files.append([path, location + list[i]])
		# else:
		# 	log("not .h file")

	return files

def ParseFile(file, location):
	try:
		f = open(file, 'r')
		content = f.read()
		if not content:
			return
	except Exeption as e:
		print("Cannot Parse file %s" % file)
		return
	finally:
		f.close()
	try:
		# remove all /* */ comments first
		content = re.sub(r'/\*([^\*]|(\*)*[^\*/])*(\*)*\*/', '', content, 0, re.M|re.S)
		# remove all // comments
		content = re.sub(r'//[^\n]*', '', content, 0, re.M|re.S)
		# turn macro from multiple lines into a single line
		content = re.sub(r'\s*\\\s*\n\s*', ' ', content, 0, re.M|re.S)
		# remove all {} content
		content = RemoveBraces(content)

		# match function
		p1 = re.compile(r'(^[\w+\s*]*\s+[\*&]*)\s*(\w+)\s*(\([^;]*\))(\s*;)', re.M|re.S)
		# match macro
		p2 = re.compile(r'(^\s*#\s*define\s+)(\w+)\s*(\([^\(\)]*\))', re.M|re.S)

		for m in re.finditer(p1, content):
			AppendItems(m, location)

		for m in re.finditer(p2, content):
			AppendItems(m, location)
	except UnicodeDecodeError as e:
		print("Cannot Parse file %s" % file)
		return

def RemoveBraces(content):
	newcontent = ""
	brace = 0
	start = 0
	for i in range(0, len(content)):
		if content[i] == '{':
			if brace == 0:
				if i > 0:
					end = i-1
				else:
					end = 0
				newcontent += content[start:end] + ';'
			brace += 1
		elif content[i] == '}':
			brace -= 1
			start = i+1
		else:
			continue

	return newcontent

def AppendItems(m, location):
	g1 = m.group(1).strip()
	g2 = m.group(2).strip()
	g3 = m.group(3).strip()
	items = GetParamItems(g3)
	api  = g1 + " " + g2 + "(" 
	snip = g2 + "(" 
	for i in range(0, len(items)):
		snip += "${%d:%s}" % (i+1, items[i])
		api  += items[i]
		if i+1 < len(items):
			snip += ", "
			api  += ", "

	snip += ")"
	api  += ")"
	mutex.acquire()
	apis.append([api, location])
	snips.append(snip)
	mutex.release()
	log(api)
	log(snip)

def GetParamItems(params):
	parenthesis = 0 
	start = -1
	items = []

	for i in range(1, len(params)):
		if start < 0:
			if not params[i].isalpha() and params[i] != '.':					
				continue
			else:
				start = i

		if parenthesis == 0 and (params[i] == ',' or params[i] == ')'):
			items.append(params[start:i])
			start = -1;
		elif params[i] == '(':
			parenthesis += 1
		elif params[i] == ')':
			parenthesis -= 1
		else:
			continue
	return items;

def log(message):
	if debug:
		print(message)


class InsertApiCommand(sublime_plugin.TextCommand):

	def __init__(self, view):
		sublime_plugin.TextCommand.__init__(self, view)
	
	def run(self, edit):
		self.view.window().show_quick_panel(apis, self.selected)

	def selected(self, index):
		if index >= 0 :
			self.view.run_command("insert_api_snippet", {"snip": snips[index]})

class InsertApiSnippetCommand(sublime_plugin.TextCommand):
	def run(self, edit, snip):
		sels = self.view.sel()
		for sel in sels:
			self.view.run_command("insert_snippet", {'contents':snip})

class InsertApiReloadCommand(sublime_plugin.WindowCommand):
	def run(self):
		plugin_loaded()

from .Test.test import *