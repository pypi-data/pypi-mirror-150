
## API Reference

#### import

```python
  from secure_settings import Settings
```

The settings are stored in sqlite in encrypted form

#### CLI

    You need to use salt to access correct data.
    main.py <salt> <command> <argv_command>
    
    Commands:
    1. set_settings:
            argv:
                "name_settings=value_settings,name_settings2=value_settings2"
            description:
                Set settings into base
            example:
                main.py salt set_settings "name_settings=value_settings,name_settings2=value_settings2"
    2. get_settings
            description:
                Get all settings from base
    3. clear_settings
            description:
                Delete all settings on base
    4. from_file
            argv:
                path_to_settings
            description:
                Filling in settings from a file
            example:
                main.py salt from_file file_settings                             
            example file:
                path_to_work;C:\\\\Program Files(x86)\\projects\\tralala.prj
                git_repo;E:\\\\tralala\\git
    5. to_file
            argv:
                path_to_settings_to_upload
            description:
                Upload settings into file
            example:
                main.py salt to_file file_settings
				
#### Library
The program must be run with at least one parameter indicating the encryption key.
```
	main.py this_is_salt
```

Running without salt will result in a program error:
```
Missing key parameter. Read help.\nPress ENTER to exit.
```

Default values when initializing the class
```
Settings(delete_after_filling=True, close_after_get=True)
```

settings = Settings()
readed_settings = settings.get_all()
print(readed_settings.path_to_lib)

```
var/lib/
```

#### Using in you programms

run with argument string

```
from from secure_settings import Settings

settings = Settings()
dict_settings = settings.get_all()

```

Thats all, simple as one, two, three
You may read settings:
```
dict_settings['path_to_repo']
```
or 
```
dict_settings.path_to_repo
```

#### Security
There are two methods of encryption and decryption for the settings class:
```python
    def encode(self, clear):
        enc = []
        for i in range(len(clear)):
            key_c = self.salt[i % len(self.salt)]
            enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
            enc.append(enc_c)
        return base64.urlsafe_b64encode("".join(enc).encode()).decode()

    def decode(self, enc):
        dec = []
        enc = base64.urlsafe_b64decode(enc).decode()
        for i in range(len(enc)):
            key_c = self.salt[i % len(self.salt)]
            dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
            dec.append(dec_c)
        return "".join(dec)
```

After viewing the settings file without decryption, we will see something like the following:
```
#=path_to_libwqLDl8ONw6bCosONw5XDlsKi
```