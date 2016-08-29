# DTS-Remuxer

## What is it
It's simple python script to add new audio stereo track to .mkv files.
It's being useful to allow play video on platforms which don't support DTS do to licenses.

### Main features
* Creates new audio stereo track basing on exist DTS track
* Removes built-in subtitle track
* Crates thumbnail of video

## Dependenties
You need to have installed mkvtoolnix and libav-tools

If you are Debian's user just do `apt-get install mkvtoolnix libav-tools`

## Usage
`remux.py /path/to/source/file.mkv /path/to/destination/directory/file.mkv`
