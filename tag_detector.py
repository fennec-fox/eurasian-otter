import os
import logging
import re


class TagDetector:
    def __init__(self, app_config):
        self.app_config = app_config
        self.path_of_source = app_config['config']['paths']['source']
        self.media_types = app_config['config']['media-types']['video']

    def find_simple_tags(self):
        return self.app_config["tags"]["simple"].split(',')

    def find_series_tags(self):
        _pattern = r'(.*)((E\d{1,2})|(S\d{1,2}))'
        _found_tags = []

        for dir_name, dir_names, file_names in os.walk(self.path_of_source):
            for filename in file_names:
                matcher = re.match(_pattern, filename)
                if bool(matcher) and bool(matcher.groups()[0]):
                    tag = re.sub("\\.$", '', matcher.groups()[0])
                    _found_tags.append(tag)
                    logging.debug('matched_tag=%s, file_name=%s', tag, filename)
        return _found_tags

    def find_files(self, word):
        _pattern = (".*%s*.*(%s)$" % (word, self.media_types)).encode("utf-8")
        _found_files = []

        for dir_name, dir_names, file_names in os.walk(self.path_of_source):
            # print path to all filenames.
            for filename in file_names:
                file_full_path = os.path.join(dir_name, filename)
                matched = bool(re.match(_pattern, file_full_path.encode("utf-8")))
                if matched:
                    logging.debug('matched_path=%s', file_full_path)
                    _found_files.append(file_full_path)

        _found_files = list(set(_found_files))

        return sorted(_found_files, key=len)
