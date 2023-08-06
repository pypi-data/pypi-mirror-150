import os
import os.path
import sys
import json

if sys.platform == "win32":
	confroot = os.environ["APPDATA"] + "\\binwb-cli"

elif sys.platform == "darwin":
	confroot = os.path.expanduser("~/Library/Preferences/binwb-cli")

else:
	confroot = os.path.expanduser("~/.config")
	if not os.path.exists(confroot): os.mkdir(confroot)
	confroot += "/binwb-cli"

if not os.path.exists(confroot):
	os.mkdir(confroot)

conffile = confroot + "/config.json"
if not os.path.exists(conffile):
	with open(conffile, "wb") as file: file.write(b"{}")

class Configuration():
	def __init__(self):
		with open(conffile, "rb") as file:
			self._obj = json.loads(file.read())

	def __setattr__(self, key, value):
		if key == "_obj":
			self.__dict__[key] = value
			return

		self._obj[key] = value
		with open(conffile, "w", encoding = "utf-8") as file:
			file.write(json.dumps(self._obj))

	def __getattr__(self, key):
		return self._obj.get(key, None)

config = Configuration()
