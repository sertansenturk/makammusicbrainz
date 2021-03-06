[![Build Status](https://travis-ci.org/sertansenturk/makammusicbrainz.svg?branch=master)](https://travis-ci.org/sertansenturk/makammusicbrainz) [![codecov.io](https://codecov.io/github/sertansenturk/makammusicbrainz/coverage.svg?branch=master)](https://codecov.io/github/sertansenturk/makammusicbrainz?branch=master) [![Code Climate](https://codeclimate.com/github/sertansenturk/makammusicbrainz/badges/gpa.svg)](https://codeclimate.com/github/sertansenturk/makammusicbrainz) [![GitHub version](https://badge.fury.io/gh/sertansenturk%2Fmakammusicbrainz.svg)](https://badge.fury.io/gh/sertansenturk%2Fmakammusicbrainz) [![DOI](https://zenodo.org/badge/21104/sertansenturk/makammusicbrainz.svg)](https://zenodo.org/badge/latestdoi/21104/sertansenturk/makammusicbrainz)

# makammusicbrainz
Packages to fetch metadata related to the makam music recordings and works from MusicBrainz

If you are using **makammusicbrainz** in your work, please cite the PhD dissertation:

> Şentürk, S. (2016). [Computational Analysis of Audio Recordings and Music Scores for the Description and Discovery of Ottoman-Turkish Makam Music](http://sertansenturk.com/research/works/phd-thesis/). PhD thesis, Universitat Pompeu Fabra, Barcelona, Spain.

Usage
-----
```python
# audio metadata
from makammusicbrainz.audiometadata import AudioMetadata
audioMetadata = AudioMetadata(get_work_attributes=True, print_warnings=True)

audio_meta = audioMetadata.from_musicbrainz(rec_input)
```
You can either supply recording MBID or recording filepath as the `rec_input`

```python
# work metadata 
from makammusicbrainz.workmetadata import WorkMetadata
workMetadata = WorkMetadata(print_warnings=True)

work_meta = workMetadata.from_musicbrainz(mbid)
```

Please refer to [demo.ipynb](https://github.com/sertansenturk/makammusicbrainz/blob/master/demo.ipynb) for an interactive demo.

Installation
------------

If you want to install makammusicbrainz, it is recommended to install the package and its dependencies into a virtualenv. In the terminal, do the following:

    virtualenv env
    source env/bin/activate
    python setup.py install

If you want to be able to edit files and have the changes be reflected, then
install compmusic like this instead

    pip install -e .

Now you can install the rest of the dependencies:

    pip install -r requirements

Authors
-------
Sertan Senturk
contact@sertansenturk.com

Acknowledgements
------
We would like to thank Dr. Robert Grafias for allowing us to use [his makam music collection](https://eee.uci.edu/programs/rgarfias/films.html) in our research (in this repository the recording with MBID: [635530df-8e13-4587-a94d-32f3c1643ca6](http://musicbrainz.org/recording/635530df-8e13-4587-a94d-32f3c1643ca6)).
