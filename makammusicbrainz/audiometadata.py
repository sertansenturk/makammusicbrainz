import eyed3
from attribute import *
from workmetadata import WorkMetadata

import musicbrainzngs as mb
mb.set_useragent("Makam corpus metadata", "1.1", "compmusic.upf.edu")


def get_audio_metadata(audio_in, get_work_attributes=None,
                       print_warnings=None):
    try:  # audio file input
        mbid, duration, sampling_frequency, bit_rate = get_file_metadata(
            audio_in)
        audio_metadata = {'mbid': mbid, 'path': audio_in, 'duration': duration,
                          'sampling_frequency': sampling_frequency,
                          'bit_rate': bit_rate}
    except IOError:
        audio_metadata = {'mbid': audio_in}

    meta = mb.get_recording_by_id(
        audio_metadata['mbid'], includes=['artists', 'artist-rels', 'releases',
                                          'tags', 'work-rels'])['recording']
    audio_metadata['title'] = meta['title']

    # releases
    audio_metadata['releases'] = get_releases(meta)

    # artist credits
    audio_metadata['artist_credits'] = get_artist_credits(meta)

    # performers
    audio_metadata['artists'] = get_artist_relations(meta)

    # works
    if 'work-relation-list' in meta.keys():  # has work
        audio_metadata['works'] = get_works(meta)

    # get makam/usul/for from work attributes
    if get_work_attributes and 'works' in audio_metadata.keys():
        workMetadata = WorkMetadata(print_warnings=print_warnings)
        attribute_keys = ['makam', 'form', 'usul']
        for w in audio_metadata['works']:
            work_metadata = workMetadata.from_mbid(w['mbid'])
            for ak in attribute_keys:
                if ak not in audio_metadata.keys():
                    audio_metadata[ak] = work_metadata[ak]
                else:
                    for wm in work_metadata[ak]:
                        audio_metadata[ak].append(wm)

    # get makam/usul/for tags
    attributetags = get_attrib_tags(meta)
    for key, vals in attributetags.iteritems():
        for val in vals:  # add the source
            val['source'] = 'http://musicbrainz.org/recording/' + \
                            audio_metadata['mbid']

        if key not in audio_metadata.keys():
            audio_metadata[key] = vals
        else:
            for val in vals:
                audio_metadata[key].append(val)

    return audio_metadata


def get_file_metadata(filepath):
    audiofile = eyed3.load(filepath)
    mbid = audiofile.tag.unique_file_ids.get('http://musicbrainz.org').data[
           -36:]
    duration = audiofile.info.time_secs
    sampling_frequency = audiofile.info.sample_freq
    bit_rate = audiofile.info.mp3_header.bit_rate

    return mbid, duration, sampling_frequency, bit_rate


def get_releases(meta):
    return [{'title': rel['title'], 'mbid': rel['id']} for rel in
            meta['release-list']]


def get_artist_credits(meta):
    artist_credits = []
    for credit in meta['artist-credit']:
        try:
            artist_credits.append({'name': credit['artist']['name'],
                                   'mbid': credit['artist']['id']})
        except TypeError:
            pass  # skip join phrase

    return artist_credits


def get_artist_relations(meta):
    artists = []
    if 'artist-relation-list' in meta.keys():
        for artist in meta['artist-relation-list']:
            artists.append({'name': artist['artist']['name'],
                            'mbid': artist['artist']['id'],
                            'type': artist['type']})
            is_performer = artist['type'] in ['vocal', 'instrument']
            if is_performer and 'attribute-list' in artist.keys():
                artists[-1]['attribute-list'] = artist['attribute-list']
    return artists


def get_works(meta):
    return ([{'title': work['work']['title'], 'mbid': work['work']['id']}
             for work in meta['work-relation-list']])
