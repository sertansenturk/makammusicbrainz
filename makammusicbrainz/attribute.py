import json, os

def getAttributeDict(attrstr):
    attrfile = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), 'makam_data', attrstr + '.json')
    return json.load(open(attrfile, 'r'))

def getAttributeKeyFromMbAttr(attr_str, attr_type):
    attr_dict = getAttributeDict(attr_type)
    for attr_key, attr_val in attr_dict.iteritems():
        if attr_val['dunya_name'] == attr_str:
            return attr_key

def getAttributeKeyFromMBTag(attr_str, attr_type):
    attr_dict = getAttributeDict(attr_type)
    for attr_key, attr_val in attr_dict.iteritems():
        if attr_str in attr_val['mb_tag']:
            return attr_key

def getAttributeTags(meta):
    theory_attribute_keys = ['makam', 'form', 'usul']
    attributes = dict()
    if 'tag-list' in meta.keys():
        for k in theory_attribute_keys:
            attr_dict = getAttributeDict(k)
            for t in meta['tag-list']:  # no work get attrs from the tags
                try:
                    key, val = t['name'].split(': ')
                    if k in key:
                        if not k in attributes.keys():
                            attributes[k] = []
                        attributes[k].append({'mb_tag':val,
                            'attribute_key':getAttributeKeyFromMBTag(val, k)})
                except ValueError:
                    pass  # skip
    return attributes

