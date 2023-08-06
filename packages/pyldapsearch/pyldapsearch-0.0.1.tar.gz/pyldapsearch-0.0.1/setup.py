# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyldapsearch']

package_data = \
{'': ['*']}

install_requires = \
['impacket>=0.9.24,<0.10.0',
 'ldap3>=2.9.1,<3.0.0',
 'pyasn1>=0.4.8,<0.5.0',
 'typer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['pyldapsearch = pyldapsearch.__main__:app']}

setup_kwargs = {
    'name': 'pyldapsearch',
    'version': '0.0.1',
    'description': 'Tool for issuing manual LDAP queries which offers bofhound compatible output',
    'long_description': '# pyldapsearch\n\nThis is designed to be a python "port" of the ldapsearch BOF by TrustedSec, which is a part of this [repo](https://github.com/trustedsec/CS-Situational-Awareness-BOF).\n\npyldapsearch allows you to execute LDAP queries from Linux in a fashion similar to that of the aforementioned BOF. Its output format closely mimics that of the BOF and all query output will automatically be logged to the user\'s home directory in `.pyldapsearch/logs`, which can ingested by [bofhound](https://github.com/fortalice/bofhound).\n\n## Why would I ever use this?\nGreat question. pyldapsearch was built for a scenario where the operator is utilizing Linux and is attempting to issue LDAP queries while flying under the radar (BloodHound will be too loud, expensive LDAP queries are alerted on, etc). When pyldapsearch is combined with bofhound, you can still obtain BloodHound compatible data that allows for AD visualization and identification of ACL-based attack paths, which are otherwise difficult to identify through manually querying LDAP.\n\nOutside of usage during detection-conscious and bofhound-related situations, pyldapsearch can be useful for issuing targeted, one-off LDAP queries during generic engagements.\n\n## Installation\nUse `pip3` or `pipx`\n```\npip3 install pyldapsearch\n```\n\n## Usage\n```\nUsage: pyldapsearch [OPTIONS] TARGET FILTER\n  \n  Tool for issuing manual LDAP queries which offers bofhound compatible output\n\nArguments:\n  TARGET  [[domain/]username[:password]  [required]\n  FILTER  LDAP filter string  [required]\n\nOptions:\n  -attributes TEXT       Comma separated list of attributes\n  -limit INTEGER         Limit the number of results to return  [default: 0]\n  -dc-ip TEXT            Domain controller IP or hostname to query\n  -base-dn TEXT          Search base distinguished name to use. Default is\n                         base domain level\n  -no-sd                 Do not add nTSecurityDescriptor as an attribute\n                         queried by default. Reduces console output\n                         significantly\n  -debug                 Turn DEBUG output ON\n  -hashes LMHASH:NTHASH  NTLM hashes, format is LMHASH:NTHASH\n  -no-pass               Don\'t ask for password (useful for -k)\n  -k                     Use Kerberos authentication. Grabs credentials from\n                         ccache file (KRB5CCNAME) based on target parameters.\n                         If valid credentials cannot be found, it will use the\n                         ones specified in the command line\n  -aesKey TEXT           AES key to use for Kerberos Authentication (128 or\n                         256 bits)\n  -ldaps                 Use LDAPS instead of LDAP\n  -silent                Do not print query results to console (results will\n                         still be logged)\n  --help                 Show this message and exit.\n```\n\n## Examples\nQuery all the data - if you intend to do this, just run BloodHound :)\n```\npyldapsearch ez.lab/administrator:pass \'(objectClass=*)\'\n```\n\nQuery only the name, memberOf and ObjectSID of the user matt\n```\npyldapsearch ez.lab/administrator:pass \'(sAMAccountName=matt)\' -attributes name,memberof,objectsid\n```\n\nQuery all attributes for all user objects, but only return 3 results\n```\npyldapsearch ez.lab/administrator:pass \'(objectClass=user)\' -limit 3\n```\n\nQuery all attributes of the user matt, specifying the IP of the DC to query\n```\npyldapsearch ez.lab/administrator:pass \'(&(objectClass=user)(name=matt))\' -dc-ip 10.4.2.20\n```\n\nQuery all objects, specifying the search base to use\n```\npyldapsearch ez.lab/administrator:pass \'(objectClass=*)\' -base-dn \'CN=Users,DC=EZ,DC=LAB\'\n```\n\nExecute a query without displaying query results to the console (results will still be logged)\n```\npyldapsearch ez.lab/administrator:pass \'(objectClass=*)\' -silent\n```\n\nPerform a query using an anonymous bind\n```\npyldapsearch \'ez.lab\'/\'\':\'\' \'(objectClass=*)\'\n```\n\n## Development\npyldapsearch uses Poetry to manage dependencies. Install from source and setup for development with:\n```shell\ngit clone https://github.com/fortalice/pyldapsearch\ncd pyldapsearch\npoetry install\npoetry run pyldapsearch\n```\n\n## References\n- ldapsearch ([CS-Situational-Awareness-BOF](https://github.com/trustedsec/cs-situational-awareness-bof))\n- [ldapconsole](https://github.com/p0dalirius/ldapconsole)',
    'author': 'Matt Creel',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fortalice/pyldapsearch',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
