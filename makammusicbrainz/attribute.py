import json
import os


class Attribute(object):
    pass


def get_attrib_dict(attrstr):
    attrfile = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), 'makam_data', attrstr + '.json')
    return json.load(open(attrfile, 'r'))


def get_attrib_key_from_mb_attrib(attr_str, attr_type):
    attr_dict = get_attrib_dict(attr_type)
    for attr_key, attr_val in attr_dict.iteritems():
        if attr_val['dunya_name'] == attr_str:
            return attr_key


def get_attrib_key_from_mb_tag(attr_str, attr_type):
    attr_dict = get_attrib_dict(attr_type)
    for attr_key, attr_val in attr_dict.iteritems():
        if attr_str in attr_val['mb_tag']:
            return attr_key


def get_attrib_tags(meta):
    theory_attribute_keys = ['makam', 'form', 'usul']
    attributes = dict()
    if 'tag-list' in meta.keys():
        for k in theory_attribute_keys:
            for t in meta['tag-list']:  # no work get attrs from the tags
                try:
                    key, val = t['name'].split(': ')
                    if k in key:
                        if k not in attributes.keys():
                            attributes[k] = []
                        attributes[k].append(
                            {'mb_tag': val, 'attribute_key':
                                get_attrib_key_from_mb_tag(val, k)})
                except ValueError:
                    pass  # skip
    return attributes
