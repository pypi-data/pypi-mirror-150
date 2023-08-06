"""
Binary Workbench command line client
Copyright (C) 2022 Hexalinq [info@hexalinq.com] [https://bw.hexalinq.com]

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License version 2 as
published by the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

import argparse
import sys
import terminaltables
import binwb_cli

try: import importlib.resources as importlib_resources
except: import importlib_resources

def print_license(args):
	with importlib_resources.open_text("binwb_cli", "LICENSE") as file: license = file.read()
	print("Binary Workbench command line client")
	print("Copyright (C) 2022 Hexalinq [info@hexalinq.com] [https://bw.hexalinq.com]")
	print()
	print(license)

CONFIG_KEYS = {
	"apikey": {
		"help": "The API key used to access Binary Workbench",
		"type": str,
	},
}

TYPE_TO_STR = {
	str: "String",
	bool: "Boolean",
	int: "Integer",
	float: "Float",
	list: "Array",
	dict: "Map",
}

def config_cb(args):
	def econfig():
		print(f"Invalid configuration key `{args[0]}`.")
		print("Type `binwb config` for the list of supported keys.")
		raise SystemExit(1)

	if len(args) == 1:
		if args[0] not in CONFIG_KEYS: econfig()
		print(getattr(binwb_cli.config, args[0]))

	elif len(args) == 2:
		if args[0] not in CONFIG_KEYS: econfig()
		setattr(binwb_cli.config, args[0], args[1])

	else:
		table = [("Key", "Value", "Type", "Description")]
		for key, desc in sorted(CONFIG_KEYS.items(), key = lambda x: x[0]):
			table.append((key, binwb_cli.config.apikey, TYPE_TO_STR[desc["type"]], desc["help"]))

		print(terminaltables.SingleTable(table).table)
		print()
		print("Usage:")
		print("\tbinwb config <key> [new_value]")
		print()
		raise SystemExit(1)

def list_projects(args):
	client = binwb_cli.api.Client()
	table = [("ID", "Name", "Format")]
	for project in client.ListProjects():
		table.append((project["id"], project["name"], project["format"]))

	print(terminaltables.SingleTable(table).table)

L1_COMMANDS = {
	"config": {
		"help": "View or change the local configuration",
		"callback": config_cb,
	},

	#"yara": {
	#	"help": "Interact with the YARA rule database",
	#},

	"project": {
		"help": "Project-related operations",
		"commands": {
			"list": {
				"help": "List projects",
				"callback": list_projects,
			},
		},
	},

	"license": {
		"help": "Print the full license text",
		"callback": print_license,
	},
}

def l1_usage(desc, path):
	width = len(max(desc, key = lambda x: len(x))) + 2

	print("binwb-cli, Copyright (C) 2022 Hexalinq.")
	print("Website: https://bw.hexalinq.com/")
	print("binwb-cli comes with ABSOLUTELY NO WARRANTY.")
	print("This is free software, and you are welcome to redistribute it")
	print("under certain conditions; type `binwb license' for details.")
	print()
	print("Usage:")
	print(f'\t{" ".join(path)} <command> [arguments]')
	print()
	print("Available commands:")
	for cmd in sorted(desc):
		help = desc[cmd]["help"]
		print("\t" + cmd.ljust(width) + help)

	print()
	#print("Type any command without arguments for more information about that command.")
	#print()

	if binwb_cli.config.apikey is None:
		print("<WARNING> The API key is not set. Run `binwb config apikey <API_KEY>` to set your API key.")

	raise SystemExit(1)

def dispatch_command(cmd, args, path):
	if "commands" not in cmd: cmd["callback"](args)
	elif not len(args): l1_usage(cmd["commands"], path)
	elif args[0] in cmd["commands"]: dispatch_command(cmd["commands"][args[0]], args[1:], [*path, args[0]])
	else:
		print(f"Invalid command `{args[0]}`.")
		print(f'Type `" ".join(path)` without arguments for the list of supported commands.')
		raise SystemExit(1)

def main():
	if len(sys.argv) < 2: l1_usage(L1_COMMANDS, ["binwb"])
	if sys.argv[1] not in L1_COMMANDS:
		print(f"Invalid command `{sys.argv[1]}`.")
		print("Type `binwb` without arguments for the list of supported commands.")
		raise SystemExit(1)

	dispatch_command(L1_COMMANDS[sys.argv[1]], sys.argv[2:], ["binwb"])
