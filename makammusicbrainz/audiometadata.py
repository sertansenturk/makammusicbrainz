import musicbrainzngs as mb
import eyed3
mb.set_useragent("Makam corpus metadata", "0.1", "compmusic.upf.edu")

def getAudioMetadata(audioIn):
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
    audioMetadata['artists_credits'] = getArtistCredits(meta)

    # performers
    audioMetadata['artists'] = getArtistRelations(meta)

    # works 
    if 'work-relation-list' in meta.keys():  # has work
        audioMetadata['works'] = getWorks(meta)
    else:   # no works, most likely improvisation get makam/form/usul attributes
        attributes = getAttributes(meta)
        for key, vals in attributes.iteritems():
            audioMetadata[key] = vals

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
        credits.append({'name':credit['artist']['name'],
            'mbid':credit['artist']['id']})

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

def getAttributes(meta):
    theory_attribute_keys = ['makam', 'form', 'usul']
    attributes = dict()
    if 'tag-list' in meta.keys():
        for t in meta['tag-list']:  # no work get attrs from the tags
            try:
                key, val = t['name'].split(': ')
                for k in theory_attribute_keys:
                    if k in key:
                        if not k in attributes.keys():
                            attributes[k] = []
                        attributes[k].append({'name':val})
            except ValueError:
                pass  # skip
    return attributes