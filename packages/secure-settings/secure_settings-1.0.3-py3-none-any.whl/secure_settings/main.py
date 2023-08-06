import os
import sqlite3
import sys
import base64


class DictOnes(dict):
    def __init__(self, keys=None, *values):
        if keys is None:
            return
        index = 0
        for key in [i.strip() for i in keys.split(',')]:
            if len(values) and len(values) >= index + 1:
                value = values[index]
            else:
                value = None
            self[key] = value
            index += 1

    def __getattr__(self, attrname):
        if attrname not in self:
            raise KeyError(attrname)
        return self[attrname]

    def __setattr__(self, attrname, value):
        self[attrname] = value

    def __delattr__(self, attrname):
        del self[attrname]

    def copy(self):
        return DictOnes(super(DictOnes, self).copy())


class Settings(object):
    def __init__(self, name_db=None, delete_after_filling=True, close_after_get=True):
        if name_db is None:
            name_db = os.getcwd() + os.sep + 'dataset'

        self.path = name_db
        self.close_after_get = close_after_get
        self.delete_after_filling = delete_after_filling

        if len(sys.argv) < 2:
            raise AttributeError('Missing key parameter. Read help.\nPress ENTER to exit.')

        self.salt = sys.argv[1]

        self.conn = sqlite3.connect(self.path)
        self.cur = self.conn.cursor()
        sql = '''CREATE TABLE IF NOT EXISTS settings(
              name TEXT,
              value TEXT)
            '''
        self.cur.execute(sql)
        self.conn.commit()

        if sys.argv[1] == 'help':
            text = '''
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
            '''
            print(text)
            sys.exit()

        if len(sys.argv) == 2:
            return

        if sys.argv[2] == 'set_settings':
            if len(sys.argv) < 4:
                input('For set setting you need use 5 arguments.\nPress ENTER to exit.')
                sys.exit()
            command = sys.argv[3]
            all_data = [i.strip() for i in command.split(',')]
            result = DictOnes()
            for data in all_data:
                keyvalue = [i.strip() for i in data.split('=')]
                result[keyvalue[0]] = keyvalue[1]

            if len(result):
                for key, value in result.items():
                    self.set(key, value)

            print('Success.')
            sys.exit()

        elif sys.argv[2] == 'get_settings':
            if len(sys.argv) < 3:
                input('For get setting you need use 4 arguments.\nPress ENTER to exit.')
                sys.exit()
            self.get_all(True)
            sys.exit()

        elif sys.argv[2] == 'clear_settings':
            self.clear_all()
            print('All settings deleted.')
            sys.exit()

        elif sys.argv[2] == 'from_file':
            if len(sys.argv) < 4:
                print('You may use 4 arguments for this command')
                sys.exit()
            path_to_file = sys.argv[3]
            with open(path_to_file, 'r', encoding='utf8') as file:
                all_text = file.read()

            if len(all_text) == 0:
                print('File is empty.')
                sys.exit()

            to_set = DictOnes()
            for line in all_text.split('\n'):
                if line:
                    keyvalue = line.split(';')
                    to_set[keyvalue[0]] = keyvalue[1]

            for key, value in to_set.items():
                self.set(key, value)
                print(f'setting [{key}] readed and recorded.')
            if self.delete_after_filling:
                os.remove(path_to_file)
            sys.exit()

        elif sys.argv[2] == 'to_file':
            if len(sys.argv) < 4:
                print('You may use 4 arguments for this command')
                sys.exit()
            path_to_file = sys.argv[3]
            data = self.get_all()
            with open(path_to_file, 'w', encoding='utf8') as file:
                for key, value in data.items():
                    file.write(f'{key};{value}\n')
            print('Success.')
            sys.exit()


    def clear_all(self):
        sql = '''DELETE FROM settings'''
        self.cur.execute(sql)
        self.conn.commit()

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

    def set(self, name, value):
        sql = 'select value from settings where name=:name'
        self.cur.execute(sql, {'name': name})
        result = self.cur.fetchall()
        if len(result):
            self.cur.execute('delete from settings where name=:name', {'name': name})
        self.cur.execute('insert into settings(name,value) values(?,?)', (name, self.encode(value)))
        self.conn.commit()

    def get(self, name):
        sql = 'select value from settings where name=:name'
        self.cur.execute(sql, {'name': name})
        result = self.cur.fetchall()
        if len(result):
            return self.decode(result[0][0])
        else:
            raise KeyError(f'settings with name [{name}] was not found. Please set it.')

    def get_all(self, only_print=False):
        self.cur.execute('select * from settings')
        data = self.cur.fetchall()
        if not only_print:
            result = DictOnes()
        if len(data):
            for row in data:
                value = self.decode(row[1])
                if only_print:
                    print(f'name: {row[0]}. value: "{value}"')
                else:
                    result[row[0]] = value
            if not only_print:
                if self.close_after_get:
                    self.conn.close()
                return result
        else:
            if only_print:
                input('Empty. Press ENTER to exit.')
            else:
                return None
