from Attribute import Attribute
import os
import json

import musicbrainzngs as mb
mb.set_useragent("Makam corpus metadata", "1.1", "compmusic.upf.edu")


class WorkMetadata(object):
    def __init__(self, get_recording_rels=True, print_warnings=None):
        self.get_recording_rels = get_recording_rels
        self.print_warnings = print_warnings

    def from_musicbrainz(self, mbid):
        included_rels = (['artist-rels', 'recording-rels']
                         if self.get_recording_rels else ['artist-rels'])
        work = mb.get_work_by_id(mbid, includes=included_rels)['work']

        data = ({'makam': [], 'form': [], 'usul': [], 'title': work['title'],
                 'mbid': mbid, 'composer': dict(), 'lyricist': dict()})

        # assign makam, form, usul attributes to data
        self._assign_makam_form_usul(data, mbid, work)

        # language
        self._assign_language(data, work)

        # composer and lyricist
        self._assign_composer_lyricist(data, work)

        # add recordings
        self._assign_recordings(data, work)

        # add scores
        self._add_scores(data, mbid)

        # warnings
        self._chk_warnings(data)

        return data

    @staticmethod
    def _add_scores(data, mbid):
        score_work_file = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'makam_data', 'symbTr_mbid.json')
        score_work = json.load(open(score_work_file, 'r'))
        data['scores'] = []
        for sw in score_work:
            if mbid in sw['uuid']:
                data['scores'].append(sw['name'])

    def _chk_warnings(self, data):
        if self.print_warnings:
            if not data['makam']:
                print('http://musicbrainz.org/work/' + data['mbid'] +
                      ' Makam is not entered!')
            if not data['form']:
                print('http://musicbrainz.org/work/' + data['mbid'] +
                      ' Form is not entered!')
            if not data['usul']:
                print('http://musicbrainz.org/work/' + data['mbid'] +
                      ' Usul is not entered!')
            if not data['composer']:
                print('http://musicbrainz.org/work/' + data['mbid'] +
                      ' Composer is not entered!')
            if 'language' not in data.keys():
                if not data['lyricist']:
                    print('http://musicbrainz.org/work/' + data['mbid'] +
                          'Language is not entered!')
                else:
                    print('http://musicbrainz.org/work/' + data['mbid'] +
                          'Language of the vocal work is not entered!')
            else:
                if data['language'] == "zxx":  # no lyics
                    if data['lyricist']:
                        print('http://musicbrainz.org/work/' + data['mbid'] +
                              'Lyricist is entered to the instrumental work!')
                else:
                    if not data['lyricist']:
                        print('http://musicbrainz.org/work/' + data['mbid'] +
                              'Lyricist is not entered!')

    @staticmethod
    def _assign_recordings(data, work):
        data['recordings'] = []
        if 'recording-relation-list' in work.keys():
            for r in work['recording-relation-list']:
                data['recordings'].append({'mbid': r['recording']['id'],
                                           'title': r['recording']['title']})

    @staticmethod
    def _assign_composer_lyricist(data, work):
        if 'artist-relation-list' in work.keys():
            for a in work['artist-relation-list']:
                if a['type'] in ['composer', 'lyricist']:
                    data[a['type']] = {'name': a['artist']['name'],
                                       'mbid': a['artist']['id']}

    @staticmethod
    def _assign_language(data, work):
        if 'language' in work.keys():
            data['language'] = work['language']

    @classmethod
    def _assign_makam_form_usul(cls, data, mbid, work):
        if 'attribute-list' in work.keys():
            w_attrb = work['attribute-list']
            for attr_name in ['makam', 'form', 'usul']:
                cls._assign_attr(data, mbid, w_attrb, attr_name)

    @staticmethod
    def _assign_attr(data, mbid, w_attrb, attrname):
        attr = [a['attribute'] for a in w_attrb
                if attrname.title() in a['type']]
        data[attrname] = [
            {'mb_attribute': m,
             'attribute_key': Attribute.get_attr_key_from_mb_attr(m, attrname),
             'source': 'http://musicbrainz.org/work/' + mbid}
            for m in attr]
