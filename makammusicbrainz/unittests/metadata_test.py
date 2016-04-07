from makammusicbrainz.AudioMetadata import AudioMetadata
from makammusicbrainz.WorkMetadata import WorkMetadata
import json
import os

_curr_folder = os.path.dirname(os.path.abspath(__file__))


def test_audio_metadata():
    # get the recording metadata
    audioMetadata = AudioMetadata(print_warnings=True)
    mp3file = os.path.join(_curr_folder, '..', '..', 'sampledata',
                           'huzzam_fasil.mp3')
    audio_meta = audioMetadata.from_musicbrainz(
        mp3file, get_work_attributes=True)

    # load the metadata computed earlier
    saved_meta = _get_saved_meta('audio')

    # remove paths since they are both relative to something else
    audio_meta.pop("path", None)
    saved_meta.pop("path", None)

    assert audio_meta == saved_meta


def test_work_metadata():
    # load the audio metadata for the work mbids
    audio_meta = _get_saved_meta('audio')

    # get the work metadata
    workMetadata = WorkMetadata(print_warnings=True)
    work_meta = []
    for w in audio_meta['works']:
        work_meta.append(workMetadata.from_musicbrainz(w['mbid']))

    # load the metadata computed earlier
    saved_meta = _get_saved_meta('work')

    assert work_meta == saved_meta


def _get_saved_meta(meta_type):
    saved_meta_file = os.path.join(_curr_folder, meta_type + '_meta.json')
    saved_meta = json.load(open(saved_meta_file, 'r'))
    return saved_meta

