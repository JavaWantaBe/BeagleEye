__author__ = 'richard'

import logging
from os import path, makedirs
from xml.etree import ElementTree as Et


setting_log = logging.getLogger('settings')
xml_file = path.join('settings', 'settings.xml')

##
#   Beautifies xml output for strings or file writing
#
#   @param elem - Element tree structure
#   @param level - starting level of tree
#
def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

##
#   Builds a new XML settings document is one does not exist with
#   with default settings for the unit
#
def _build_default_tree():

    beagle = Et.Element('beagleeye')

    # Network Settings - Holds local unit netowork settings
    net_setting = Et.SubElement(beagle, 'setting')
    net_setting.set("name", "network")

    ip = Et.SubElement(net_setting, 'ip')
    ip.text = '192.168.1.10'

    sub = Et.SubElement(net_setting, 'sub')
    sub.text = '255.255.255.0'

    gw = Et.SubElement(net_setting, 'gw')
    gw.text = '192.168.1.0'

    dhcp = Et.SubElement(net_setting, 'dhcp')
    dhcp.text = 'manual'

    # Camera settings
    cam_setting = Et.SubElement(beagle, 'setting')
    cam_setting.set('name', 'camera')

    res = Et.SubElement(cam_setting, 'resolution')
    res.text = '1280x720'

    device = Et.SubElement(cam_setting, 'device')
    device.text = '0'

    fps = Et.SubElement(cam_setting, 'fps')
    fps.text = '10'

    # Server settings
    serv_settings = Et.SubElement(beagle, 'setting')
    serv_settings.set('name', 'server')

    sip = Et.SubElement(serv_settings, 'ip')
    sip.text = '192.168.1.5'

    user = Et.SubElement(serv_settings, 'user')
    user.text = 'beagleeye'

    password = Et.SubElement(serv_settings, 'password')
    password.text = 'foo'

    # OCR Settings
    ocr_setting = Et.SubElement(beagle, 'setting')
    ocr_setting.set('name', 'ocr')

    pos = Et.SubElement(ocr_setting, 'positives')
    pos.text = '3'

    indent(beagle)

    new_tree = Et.ElementTree(beagle)
    new_tree.write(xml_file, xml_declaration=True, encoding='utf-8', method="xml")

##
#   @brief Manages all settings for the system
#
#   All settings are maintained in a xml file that is created if not found.
#
class SettingManager(object):

    def __init__(self):

        if not path.exists('settings'):
            try:
                makedirs('settings')
            except OSError as exception:
                if exception.errno != exception.errno.EEXIST:
                    setting_log.error("Unable to create director")
                    raise

        if not path.exists(xml_file):
            _build_default_tree()

        try:
            self.tree = Et.parse(xml_file)
        except Et.ParseError:
            setting_log.error("Failed to open settings file")

        self.root = self.tree.getroot()

    ##
    #   @brief Reads settings from settings file
    #
    #   Searches tree of elements populated from a search of tags with setting
    #   then iterates those tags for one with a name of the passed setting_name.
    #   Once found it populates the dictionary with all the attributes found in
    #   network.
    #
    #   @param setting_name - name of setting
    #
    # @return dictionary of settings
    def get_settings(self, setting_name):
        setting = {}

        for child in self.root.iterfind('setting'):
            if child.attrib['name'] == setting_name:
                for temp in child.iter():
                    if temp.tag == 'setting':
                        continue
                    setting[temp.tag] = temp.text
                break
        return setting

    ##
    #   @brief Sets settings into settings file
    #
    #   @param setting_name - name of setting
    #   @param **kwargs - dictionary of settings
    #
    def set_settings(self, setting_name, **kwargs):

        for child in self.root.iter('setting'):
            if child.attrib['name'] == setting_name:
                # Have the correct child
                for temp in child.iter():
                    # For each child in network, iterate through and compare tags
                    for args in kwargs.keys():
                        if args == temp.tag:
                            temp.text = kwargs[args]

        self._write_settings()

    ##
    #   @brief Writes any changes back to settings file
    #
    def _write_settings(self):
        self.tree.write(xml_file, xml_declaration=True, encoding='utf-8', method="xml")
        setting_log.debug("Wrote new settings")
