from makammusicbrainz.audiometadata import AudioMetadata
from makammusicbrainz.workmetadata import WorkMetadata
import json
import os

_curr_folder = os.path.dirname(os.path.abspath(__file__))


def test_recording_mbid_metadata():
    # get the recording metadata
    audio_metadata = AudioMetadata(get_work_attributes=True,
                                   print_warnings=True)
    mbid = '5cbd1b2d-d1ef-4627-a4d4-135a95de2b69'

    mbid_meta = audio_metadata.from_musicbrainz(mbid)

    # load the metadata computed earlier
    saved_meta = _get_saved_meta(mbid + '.json')

    assert mbid_meta == saved_meta, 'test_recording_mbid_metadata failed'


def test_audio_metadata():
    # get the recording metadata
    audio_metadata = AudioMetadata(get_work_attributes=True,
                                   print_warnings=True)
    mp3file = os.path.join(_curr_folder, '..', '..', 'sampledata',
                           'huzzam_fasil.mp3')
    audio_meta = audio_metadata.from_musicbrainz(mp3file)

    # load the metadata computed earlier
    saved_meta = _get_saved_meta('audio_meta.json')

    # remove paths since they are both relative to something else
    audio_meta.pop("path", None)
    saved_meta.pop("path", None)

    assert audio_meta == saved_meta, 'test_audio_metadata failed'


def test_work_metadata():
    # load the audio metadata for the work mbids
    audio_meta = _get_saved_meta('audio_meta.json')

    # get the work metadata
    work_metadata = WorkMetadata(print_warnings=True)
    work_meta = []
    for w in audio_meta['works']:
        work_meta.append(work_metadata.from_musicbrainz(w['mbid']))

    # load the metadata computed earlier
    saved_meta = _get_saved_meta('work_meta.json')

    assert work_meta == saved_meta, 'test_work_metadata failed'


def _get_saved_meta(meta_type):
    saved_meta_file = os.path.join(_curr_folder, meta_type)
    saved_meta = json.load(open(saved_meta_file, 'r'))
    return saved_meta
