# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['secure_settings']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'secure-settings',
    'version': '1.0.3',
    'description': 'Secure storage of settings for your python programs. Use strong salt',
    'long_description': '\n## API Reference\n\n#### import\n\n```python\n  from secure_settings import Settings\n```\n\nThe settings are stored in sqlite in encrypted form\n\n#### CLI\n\n    You need to use salt to access correct data.\n    main.py <salt> <command> <argv_command>\n    \n    Commands:\n    1. set_settings:\n            argv:\n                "name_settings=value_settings,name_settings2=value_settings2"\n            description:\n                Set settings into base\n            example:\n                main.py salt set_settings "name_settings=value_settings,name_settings2=value_settings2"\n    2. get_settings\n            description:\n                Get all settings from base\n    3. clear_settings\n            description:\n                Delete all settings on base\n    4. from_file\n            argv:\n                path_to_settings\n            description:\n                Filling in settings from a file\n            example:\n                main.py salt from_file file_settings                             \n            example file:\n                path_to_work;C:\\\\\\\\Program Files(x86)\\\\projects\\\\tralala.prj\n                git_repo;E:\\\\\\\\tralala\\\\git\n    5. to_file\n            argv:\n                path_to_settings_to_upload\n            description:\n                Upload settings into file\n            example:\n                main.py salt to_file file_settings\n\t\t\t\t\n#### Library\nThe program must be run with at least one parameter indicating the encryption key.\n```\n\tmain.py this_is_salt\n```\n\nRunning without salt will result in a program error:\n```\nMissing key parameter. Read help.\\nPress ENTER to exit.\n```\n\nDefault values when initializing the class\n```\nSettings(delete_after_filling=True, close_after_get=True)\n```\n\nsettings = Settings()\nreaded_settings = settings.get_all()\nprint(readed_settings.path_to_lib)\n\n```\nvar/lib/\n```\n\n#### Using in you programms\n\nrun with argument string\n\n```\nfrom from secure_settings import Settings\n\nsettings = Settings()\ndict_settings = settings.get_all()\n\n```\n\nThats all, simple as one, two, three\nYou may read settings:\n```\ndict_settings[\'path_to_repo\']\n```\nor \n```\ndict_settings.path_to_repo\n```\n\n#### Security\nThere are two methods of encryption and decryption for the settings class:\n```python\n    def encode(self, clear):\n        enc = []\n        for i in range(len(clear)):\n            key_c = self.salt[i % len(self.salt)]\n            enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)\n            enc.append(enc_c)\n        return base64.urlsafe_b64encode("".join(enc).encode()).decode()\n\n    def decode(self, enc):\n        dec = []\n        enc = base64.urlsafe_b64decode(enc).decode()\n        for i in range(len(enc)):\n            key_c = self.salt[i % len(self.salt)]\n            dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)\n            dec.append(dec_c)\n        return "".join(dec)\n```\n\nAfter viewing the settings file without decryption, we will see something like the following:\n```\n#=path_to_libwqLDl8ONw6bCosONw5XDlsKi\n```',
    'author': 'to101',
    'author_email': 'to101kv@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.1,<4.0',
}


setup(**setup_kwargs)
