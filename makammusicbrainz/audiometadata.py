import eyed3

from attribute import *
from workmetadata import getWorkMetadata

import musicbrainzngs as mb
mb.set_useragent("Makam corpus metadata", "0.1", "compmusic.upf.edu")

def getAudioMetadata(audioIn, getWorkAttributes = None):
    try:  # audio file input
        mbid, duration, sampling_frequency, bit_rate = getFileMetadata(audioIn)
        audioMetadata = {'mbid':mbid, 'path':audioIn, 'duration':duration, 
            'sampling_frequency':sampling_frequency, 'bit_rate':bit_rate}
    except IOError:
        audioMetadata = {'mbid':mbid}

    meta = mb.get_recording_by_id(audioMetadata['mbid'], 
        includes=['artists','artist-rels','tags','releases','work-rels']
        )['recording']
    audioMetadata['title'] = meta['title']

    # releases
    audioMetadata['releases'] = getReleases(meta)

    # artist credits
    audioMetadata['artist_credits'] = getArtistCredits(meta)

    # performers
    audioMetadata['artists'] = getArtistRelations(meta)
    
    # works
    if 'work-relation-list' in meta.keys():  # has work
        audioMetadata['works'] = getWorks(meta)

    # get makam/usul/for from work attributes
    if getWorkAttributes and 'works' in audioMetadata.keys():
        attribute_keys = ['makam', 'form', 'usul']
        for w in audioMetadata['works']:
            workMetadata = getWorkMetadata(w['mbid'])
            for ak in attribute_keys:
                if ak not in audioMetadata.keys():
                    audioMetadata[ak] = workMetadata[ak]
                else:
                    for wm in workMetadata[ak]:
                        audioMetadata[ak].append(wm)

    # get makam/usul/for tags
    attributetags = getAttributeTags(meta)
    for key, vals in attributetags.iteritems():
        for val in vals:  # add the source
            val['source'] = 'http://musicbrainz.org/recording/' + mbid

        if key not in audioMetadata.keys():
            audioMetadata[key] = vals
        else:
            for val in vals:
                audioMetadata[key].append(val)

    return audioMetadata

def getFileMetadata(file):
    audiofile = eyed3.load(file)
    mbid = audiofile.tag.unique_file_ids.get('http://musicbrainz.org').data[-36:]
    duration = audiofile.info.time_secs
    sampling_frequency = audiofile.info.sample_freq  
    bit_rate = audiofile.info.mp3_header.bit_rate

    return mbid, duration, sampling_frequency, bit_rate

def getReleases(meta):
    return [{'title':rel['title'], 'mbid':rel['id']} for rel in meta['release-list']]

def getArtistCredits(meta):
    credits = []
    for credit in meta['artist-credit']:
        try:
            credits.append({'name':credit['artist']['name'],
                'mbid':credit['artist']['id']})
        except TypeError:
            pass  # skip join phrase

    return credits

def getArtistRelations(meta):
    artists = []
    if 'artist-relation-list' in meta.keys():
        for artist in meta['artist-relation-list']:
            artists.append({'name':artist['artist']['name'], 
                'mbid':artist['artist']['id'],'type':artist['type']})
            if (artist['type'] in ['vocal', 'instrument'] and 
               'attribute-list' in artist.keys()):
                artists[-1]['attribute-list'] = artist['attribute-list']
    return artists

def getWorks(meta):
    return ([{'title':work['work']['title'], 'mbid':work['work']['id']} 
        for work in meta['work-relation-list']])
