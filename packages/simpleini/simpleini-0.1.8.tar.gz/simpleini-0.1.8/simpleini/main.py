import configparser
import os
import sys
from datetime import datetime


def logging(text):
    with open(f'{os.getcwd() + os.sep}log.txt', 'a', encoding='utf8') as log_file:
        for log_text in text.split('\n'):
            text_to_write = f'{datetime.now()} :   {log_text}'
            log_file.write(text_to_write + '\n')
            print(text_to_write)


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


class SETTINGS(object):

    def __init__(self, keys_for_read=None, required_fields=None, file_name=None):
        if file_name is None:
            file_name = f'{os.getcwd() + os.sep}settings.ini'
        self.__config_file = configparser.ConfigParser()
        self._path_to_settings = file_name
        self._required_fields = required_fields

        if not os.path.exists(self._path_to_settings):

            if not keys_for_read is None:
                for name_setting in [i.strip() for i in keys_for_read.split(',')]:
                    self.__config_file['DEFAULT'][name_setting] = ''

            with open(self._path_to_settings, 'w', encoding='utf8') as configfile:
                self.__config_file.write(configfile)

            logging('Settings.ini created. Please fill it and restart program.')
            sys.exit()

        else:
            result = dict()
            self.__config_file.read(self._path_to_settings, encoding='utf8')

            if keys_for_read is None:
                for section, values in self.__config_file.items():
                    self.__dict__[section] = DictOnes()
                    for key in values.keys():
                        self.__dict__[section][key] = self.__config_file[section][key]
                if not required_fields is None:
                    self.inspect_required(self.__dict__, False)
                return

            all_keys = list(self.config_file['DEFAULT'].keys())
            for setting in keys_for_read.split(','):
                name_setting = setting.strip()
                if not name_setting in all_keys:
                    logging(f'Key [{name_setting}] not find on settings.ini')
                    sys.exit()
                result[name_setting] = self.__config_file['DEFAULT'][name_setting]

            self.inspect_required(result, True)

            for key, value in result.items():
                self.__dict__[key] = value

    def inspect_required(self, result, default_section):
        if self._required_fields == 'all':
            fields_to_check = result.keys()
        else:
            fields_to_check = [i.strip() for i in self._required_fields.split(',')]

        for field_check in fields_to_check:
            if default_section:
                if field_check in result and result[field_check] == '':
                    raise ValueError(
                        f'Field [{field_check}] on settings.ini must be filled in. Please fill it and restart '
                        f'program.')
            else:
                sectionkey = [i.strip() for i in field_check.split('.')]
                if sectionkey[0] in result and sectionkey[1] in result[sectionkey[0]]:
                    continue
                else:
                    raise ValueError(f'Field [{field_check}] on settings.ini must be filled in. Please fill it and restart '
                            f'program.')


    def __getattr__(self, name):
        return self.__dict__[name]

    def set(self, destination, value):
        section_key = [i.strip() for i in destination.split('.')]
        if len(section_key) != 2:
            raise KeyError('For set you need to use format [ set("<section_name>.<parameter_name>", <value> ]')
        if not section_key[0] in self.__dict__:
            self.__config_file.add_section(section_key[0])
        self.__config_file[section_key[0]][section_key[1]] = str(value)
        with open(self._path_to_settings, 'w', encoding='utf8') as configfile:
            self.__config_file.write(configfile)

    def remove(self, destination):
        sectionkey = [i.strip() for i in destination.split('.')]
        if len(sectionkey) == 1:
            # deleting section
            if not sectionkey[0] in self.__dict__:
                raise KeyError(f'Remove error. Section [{sectionkey[0]}] does not exists.')
            self.__config_file.remove_section(sectionkey[0])
        elif len(sectionkey) == 2:
            self.__config_file.remove_option(sectionkey[0], sectionkey[1])
        else:
            raise KeyError('Remove error. You need to use following argument "<name_section>.<name_option>"')

        with open(self._path_to_settings, 'w', encoding='utf8') as configfile:
            self.__config_file.write(configfile)


settings = SETTINGS(required_fields='NEW_DEFAULT.path_default')
settings.set('test.one', 123)

settings.remove('test')
