import os
import json

import musicbrainzngs as mb
mb.set_useragent("Makam corpus metadata", "0.1", "compmusic.upf.edu")

def getWorkMetadata(mbid):
    work = mb.get_work_by_id(mbid, includes=['artist-rels', 
        'recording-rels'])['work']

    data = ({'makam':dict(),'form':dict(),'usul':dict(),
        'mbid':mbid,'title':work['title'],'composer':dict(),
        'lyricist':dict()})

    # makam, form, usul attributes
    if 'attribute-list' in work.keys():
        w_attrb = work['attribute-list']

        makam = [a['attribute'] for a in w_attrb if 'Makam' in a['type']]
        data['makam'] = {'mb_attribute': makam[0] if len(makam) == 1 else makam}

        form = [a['attribute'] for a in w_attrb if 'Form' in a['type']]
        data['form'] = {'mb_attribute': form[0] if len(form) == 1 else form}

        usul = [a['attribute'] for a in w_attrb if 'Usul' in a['type']]
        data['usul'] = {'mb_attribute': usul[0] if len(usul) == 1 else usul}

    # language
    if 'language' in work.keys():
        data['language'] = work['language']

    # composer and lyricist
    if 'artist-relation-list' in work.keys():
        for a in work['artist-relation-list']:
            if a['type'] == 'composer':
                data['composer'] = {'name':a['artist']['name'],'mbid':a['artist']['id']}
            elif a['type'] == 'lyricist':
                data['lyricist'] = {'name':a['artist']['name'],'mbid':a['artist']['id']}

    # add recordings
    data['recordings'] = []
    if 'recording-relation-list' in work.keys():
        for r in work['recording-relation-list']:
            rr = r['recording']
            data['recordings'].append({'mbid':rr['id'], 'title':rr['title']})

    # add scores
    score_work_file = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), 'makam_data', 'symbTr_mbid.json')
    score_work = json.load(open(score_work_file, 'r'))
    data['scores'] = [] 
    for sw in score_work:
        if sw['uuid']['mbid'] == mbid:
            data['scores'].append(sw['name'])

    return data