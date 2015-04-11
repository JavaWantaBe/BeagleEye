__author__ = 'richard'

import logging
from os import path, makedirs
from xml.etree import ElementTree as Et


# Setup logger for module logging system.  Usages are settinglog.info( "This is info" )
settinglog = logging.getLogger('settings')

# Populate the element structure from xml file
xml_file = path.join('settings', 'settings.xml')

"""
if not path.exists('settings'):
    try:
        makedirs('settings')
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

if not path.exists(xml_file):
    tmp = open(xml_file, 'w')
    tmp.close()
"""

try:
    tree = Et.parse(xml_file)
except Et.ParseError:
    settinglog.error("Failed to open settings file")

root = tree.getroot()


##
# Reads network settings from settings file
#
# @return dictionary of settings
def get_network_settings():
    network = {}

    for child in root.iter('setting'):
        if child.attrib['name'] == 'network':
            for temp in child.iter():
                if temp.tag == 'setting':
                    continue
                network[temp.tag] = temp.text
            break
    return network


def set_network_settings(**kwargs):
    # TODO Impliment setting network settings
    _write_settings()


def get_camera_settings():
    camera = {}

    for child in root.iter('setting'):
        if child.attrib['name'] == 'camera':
            for temp in child.iter():
                if temp.tag == 'setting':
                    continue
                camera[temp.tag] = temp.text
            break
    return camera


def set_camera_settings(**kwargs):
    # TODO Impliment setting camera settings
    _write_settings()


def get_ocr_settings():
    ocr = {}

    for child in root.iter('setting'):
        if child.attrib['name'] == 'ocr':
            for temp in child.iter():
                if temp.tag == 'setting':
                    continue
                ocr[temp.tag] = temp.text
            break
    return ocr


def set_ocr_settings(**kwargs):
    # TODO Impliment setting ocr settings
    _write_settings()


def get_server_settings():
    server = {}

    for child in root.iter('setting'):
        if child.attrib['name'] == 'camera':
            for temp in child.iter():
                if temp.tag == 'setting':
                    continue
                server[temp.tag] = temp.text
            break
    return server


def set_server_settings(**kwargs):
    # TODO Impliment setting server settings
    _write_settings()


def _write_settings():
    # TODO: Write settings
    tree.write(xml_file)
    settinglog.debug("Wrote new settings")
    print "Write settings here"


