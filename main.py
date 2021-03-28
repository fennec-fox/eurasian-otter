# -*- coding: utf-8 -*-
# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import yaml
import os
import logging.config
import shutil
from tag_detector import SimpleTagDetector
from tag_detector import SeriesTagDetector

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

    logging.info("- processing simple tags")
    simpleTagDetector = SimpleTagDetector(app_config)

    tags = simpleTagDetector.find_tags()
    for tag in tags:
        path_of_target_folder = create_or_nothing_folder(tag)
        logging.debug("-- target: %s ----", tag)
        files = simpleTagDetector.find_files(tag)
        for target_file in files:
            copy_or_move_file(target_file, path_of_target_folder)

    logging.info("- processing series tags")
    if bool(app_config['tags']['series']['auto-detect']):
        seriesTagDetector = SeriesTagDetector(app_config)

        tags = seriesTagDetector.find_tags()
        for tag in tags:
            path_of_target_folder = create_or_nothing_folder(tag)
            logging.debug("-- target: %s ----", tag)
            files = seriesTagDetector.find_files(tag)
            for target_file in files:
                copy_or_move_file(target_file, path_of_target_folder)
