import requests
import binwb_cli

ENDPOINT = "https://bw.hexalinq.com/api"

class RPCError(Exception): pass

class Client():
	def __init__(self):
		if type(binwb_cli.config.apikey) != str or len(binwb_cli.config.apikey) < 8 or len(binwb_cli.config.apikey) > 255:
			print("Invalid API key")
			print("Type `binwb config apikey <API_KEY>` to set your API key.")
			raise SystemExit(1)

		self._token = binwb_cli.config.apikey
		self._session = requests.Session()
		self._session.headers["User-Agent"] = f'binwb-cli/{binwb_cli.__version__}'
		self._session.headers["X-Version"] = "1"
		self._session.headers["X-Token"] = self._token

	def _rpc_call(self, fn, args):
		resp = self._session.post(ENDPOINT, headers = { "X-Endpoint": fn }, json = args)
		if resp.status_code != 200: raise RPCError(resp.status_code, resp.content)
		return resp.json()

	def __getattr__(self, attr):
		if attr in ["ListProjects"]: return lambda **args: self._rpc_call(attr, args)
		raise AttributeError(attr)
