import json
import os


class Attribute(object):
    @staticmethod
    def _get_attrib_dict(attrstr):
        attrfile = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'makam_data', attrstr + '.json')
        return json.load(open(attrfile, 'r'))

    @staticmethod
    def get_attr_key_from_mb_attr(attr_str, attr_type):
        attr_dict = Attribute._get_attrib_dict(attr_type)
        for attr_key, attr_val in attr_dict.iteritems():
            if attr_val['dunya_name'] == attr_str:
                return attr_key

    @staticmethod
    def _get_attr_key_from_mb_tag(attr_str, attr_type):
        attr_dict = Attribute._get_attrib_dict(attr_type)
        for attr_key, attr_val in attr_dict.iteritems():
            if attr_str in attr_val['mb_tag']:
                return attr_key

    @staticmethod
    def get_attrib_tags(meta):
        theory_attribute_keys = ['makam', 'form', 'usul']
        attributes = dict()
        if 'tag-list' in meta.keys():
            for k in theory_attribute_keys:  # for makam/form/usul keys
                for t in meta['tag-list']:  # for each tag
                    try:  # attempt to assign the tag to the attribute key
                        Attribute._assign_attrib(attributes, k, t)
                    except ValueError:
                        pass  # not a makam/form/usul tag; skip
        return attributes

    @staticmethod
    def _assign_attrib(attributes, k, t):
        key, val = t['name'].split(': ')
        if k in key:
            if k not in attributes.keys():  # create the key
                attributes[k] = []

            attributes[k].append({'mb_tag': val, 'attribute_key':
                Attribute._get_attr_key_from_mb_tag(val, k)})
