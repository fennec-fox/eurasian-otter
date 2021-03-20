# -*- coding: utf-8 -*-
# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import yaml
import os
import re
import logging.config
import shutil
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

loggingConfigPath = 'logging.yaml'
if os.path.exists(loggingConfigPath):
    with open(loggingConfigPath, 'rt') as f:
        loggingConfig = yaml.load(f.read(), Loader=yaml.FullLoader)
        logging.config.dictConfig(loggingConfig)
else:
    logging.basicConfig(
        filename='move.log',
        level=logging.DEBUG,
        format='%(asctime)s:%(levelname)s:%(funcName)s:%(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def get_tags_by_simple():
    return app_config["tags"]["simple"].split(',')


def search_files(word):
    _path_of_source = app_config['config']['paths']['source']
    _media_types = app_config['config']['media-types']['video']
    _pattern = (".*%s*.*(%s)$" % (word, _media_types)).encode("utf-8")
    _found_files = []

    for dir_name, dir_names, file_names in os.walk(_path_of_source):
        # print path to all filenames.
        for filename in file_names:
            file_full_path = os.path.join(dir_name, filename)
            matched = bool(re.match(_pattern, file_full_path))
            if matched:
                logging.debug('matched_path=%s', file_full_path)
                _found_files.append(file_full_path)
    return _found_files


def create_or_nothing_folder(word):
    _path_of_target = app_config['config']['paths']['target']
    try:
        path_of_word = os.path.join(_path_of_target, word)
        if not os.path.isdir(path_of_word):
            os.mkdir(path_of_word)
            logging.debug("folder created. %s", path_of_word)

        return path_of_word
    except OSError:
        return _path_of_target


def copy_or_move_file(source_file, target_folder):
    _action = app_config['config']['operations']['file']['action']
    _is_over_write = app_config['config']['operations']['file']['overwrite']
    _file_name = os.path.basename(source_file)
    _path_of_target_file = os.path.join(target_folder, _file_name)
    _has_target_file = os.path.exists(_path_of_target_file)

    logging.info("target file=%s", _file_name)

    if _has_target_file and not _is_over_write:
        logging.info("exist file. %s", _path_of_target_file)
        return False

    if _action == 'copy':
        shutil.copyfile(source_file, _path_of_target_file)
    if _action == 'move':
        shutil.move(source_file, _path_of_target_file)

    logging.debug("action=%s, source=%s, target=%s", _action, source_file, _path_of_target_file)

    return True


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    global app_config

    logging.info("- start --------------------")
    with open('configuration.yaml') as f:
        app_config = yaml.load(f, Loader=yaml.FullLoader)

    tags = get_tags_by_simple()
    for tag in tags:
        path_of_target_folder = create_or_nothing_folder(tag)
        logging.debug("-- target: %s ----", tag)
        files = search_files(tag)
        for target_file in files:
            copy_or_move_file(target_file, path_of_target_folder)
