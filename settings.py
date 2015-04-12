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
    # @brief Reads network settings from settings file
    #
    # Searches tree of elements populated from a search of tags with setting
    # then iterates those tags for one with a name of network.  Once found it
    # populates the dictionary with all the attributes found in network.
    #
    # @return dictionary of network settings
    def get_network_settings(self):

        network = {}

        for child in self.root.iter('setting'):
            if child.attrib['name'] == 'network':
                for temp in child.iter():
                    if temp.tag == 'setting':
                        continue
                    network[temp.tag] = temp.text
                break
        return network

    ##
    #   @brief Sets network settings
    #
    #   @param **kwargs - dictionary of settings
    #
    def set_network_settings(self, **kwargs):
        # TODO Impliment setting network settings

        for child in self.root.iter('setting'):
            if child.attrib['name'] == 'network':
                # Have the correct child
                for temp in child.iter():
                    # For each child in network, iterate through and compare tags
                    for args in kwargs.keys():
                        if args == temp.tag:
                            temp.txt = kwargs[args]

        self._write_settings()

    def get_camera_settings(self):
        camera = {}

        for child in self.root.iter('setting'):
            if child.attrib['name'] == 'camera':
                for temp in child.iter():
                    if temp.tag == 'setting':
                        continue
                    camera[temp.tag] = temp.text
                break
        return camera

    def set_camera_settings(self, **kwargs):
        # TODO Impliment setting camera settings
        self._write_settings()

    def get_ocr_settings(self):
        ocr = {}

        for child in self.root.iter('setting'):
            if child.attrib['name'] == 'ocr':
                for temp in child.iter():
                    if temp.tag == 'setting':
                        continue
                    ocr[temp.tag] = temp.text
                break
        return ocr

    def set_ocr_settings(self, **kwargs):
        # TODO Impliment setting ocr settings
        self._write_settings()

    def get_server_settings(self):
        server = {}

        for child in self.root.iter('setting'):
            if child.attrib['name'] == 'camera':
                for temp in child.iter():
                    if temp.tag == 'setting':
                        continue
                    server[temp.tag] = temp.text
                break
        return server

    def set_server_settings(self, **kwargs):
        # TODO Impliment setting server settings
        self._write_settings()

    def _write_settings(self):
        # TODO: Write settings

        self.tree.write(self.xml_file, xml_declaration=True, encoding='utf-8', method="xml")
        setting_log.debug("Wrote new settings")






tempsettings = {'ip': '192.168.1.11', 'sub': '255.255.255.0', 'gw': '192.168.1.1', 'dhcp': 'auto'}
#set_network_settings(**tempsettings)
test_ojbect = SettingManager()

print test_ojbect.get_network_settings()