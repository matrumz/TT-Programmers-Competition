#!/usr/bin/python3

import requests

def githubImport(user, repo, branch, module):
	data = {}
	url = url = 'https://raw.githubusercontent.com/{}/{}/{}/{}.py'.format(user, repo, branch, module)
	request = requests.get(url).text
	exec(request, data)
	return data

user = 'matrumz'
repo = 'PythonModules'
branch = 'master'
module = 'Logger/logger'

logger = githubImport(user, repo, branch, module)
print(logger)
