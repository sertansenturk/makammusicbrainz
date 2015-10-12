import musicbrainzngs as mb
import eyed3

def getAudioMetadata(audioIn):
    try:  # mp3 input
    	audiofile = eyed3.load(audio_files[i])
        mbid = audiofile.tag.unique_file_ids.get(
            'http://musicbrainz.org').data[-36:]
    except IOError:
        mbid = audioIn

    meta = mb.get_recording_by_id(mbid, includes=['artist-rels',
        'tags','releases','work-rels'])['recording']

    # releases
    releases = getReleases(meta)

    # performers
    artists = getArtistRelations(meta)

    audioMetadata = {'title':meta['title'],'path':audio_files[i],
                     'mbid':mbid,'duration':audiofile.info.time_secs,
                     'releases':releases,'artists':artists}
    
    # works 
    if 'work-relation-list' in meta.keys():  # has work
        audioMetadata['works'] = getWorks(meta)
    else:   # no works, most likely improvisation get makam/form/usul attributes
        attributes = getAttributes(meta)
        for key, vals in attributes.iteritems():
            audioMetadata[key] = vals

    return audioMetadata

def getReleases(meta):
    return [{'title':rel['title'], 'mbid':rel['id']} for rel in meta['release-list']]

def getArtistRelations(meta):
    artists = []
    if 'artist-relation-list' in meta.keys():
        for artist in meta['artist-relation-list']:
            artists.append({'name':artist['artist']['name'], 
                          'mbid':artist['artist']['id'],
                          'type':artist['type']})
            if (artist['type'] in ['vocal', 'instrument'] and 
               'attribute-list' in artist.keys()):
                artists[-1]['attribute-list'] = artist['attribute-list']
    return artists

def getWorks(meta):
    return ([{'title':work['work']['title'], 'mbid':work['work']['id']} 
        for work in meta['work-relation-list']])

def getAttributes(meta):
    attributes = dict()
    if 'tag-list' in meta.keys():
        for t in meta['tag-list']:  # no work get attrs from the tags
            try:
                key, val = t['name'].split(': ')
                if any(k in key for k in ['makam', 'form', 'usul']):
                    if not key in attributes .keys():
                        attributes [key] = []
                    attributes[key].append({'name':val})
            except ValueError:
                pass
    return attributes