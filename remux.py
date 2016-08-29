#!/usr/bin/env python

import sys, os, re
import subprocess

def extract_subs(src_file, srt_file):
        popen = subprocess.Popen('mkvmerge -i "%s"' % (src_file), shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        output = popen.stdout.read()

	if (output):
		regexp = re.search('Track ID (\d+): subtitles.*?SRT\\)', output)

		if regexp and regexp.group(1).isdigit():
			os.system('mkvextract tracks "%s" %s:"%s"' % (src_file, regexp.group(1), srt_file))
			return True
		else:
			return False
	else:
		return False

def processing(src_file, dst_file):

	srt_file = os.path.splitext(dst_file)[0] + '.srt'

	if not os.path.isfile(srt_file):
		try:
			print 'Extracting built-in subs if exists: '
			if extract_subs(src_file, srt_file):
				print 'Done.'
			else:
				print 'None'
		except OSError:
			print 'Error: Problem with extracting subs.'

	try:
		print 'Extacting audio: ' 
		os.system('avconv -y -i "%s" -acodec libmp3lame -vn -ab 320k -ac 2 -af "volume=2" "%s"' % (src_file, os.path.dirname(dst_file) + '/.audio.mp3'))
#		os.system('avconv -y -i "%s" -acodec libfdk_aac -vn -b:a 384k -ac 2 -af "volume=2" "%s"' % (src_file, os.path.dirname(dst_file) + '/.audio.aac'))
		print 'Done.'
	except OSError:
		print 'Error: Problem with extracting audio track.'
		
	try:
		print 'Merging streams: '
		# mkvmerge -o out [global options] [options1] <file1> [@optionsfile ...]
		os.system('mkvmerge -o "%s" --no-subtitles "%s" --track-name 0:"English MP3 Stereo" "%s"' % (os.path.dirname(dst_file) + '/.' + os.path.basename(dst_file) + '.tmp', src_file, os.path.dirname(dst_file) + '/.audio.mp3'))
		print 'Done.'
	except OSError:
		print 'Error: Problem with merging tracks.'
		
	# moving/deleting files
	try:
		os.remove(os.path.dirname(dst_file) + '/.audio.mp3')
		os.rename(os.path.dirname(dst_file) + '/.' + os.path.basename(dst_file) + '.tmp', dst_file)
	except OSError:
		print 'Error: Problem renaming files.'

	# making cover
	try:
		print 'Making cover: '
		os.system('avconv -ss 00:10:00 -y -i "%s" -an -vframes 1 "%s"' % (src_file, os.path.dirname(dst_file) + '/Cover.jpg'))
		print 'Done.'
	except OSError:
		print 'Error: Problem making cover.'

	print '\n--------------------------------\n'
	
	return 1

def main():
	# checking if avconv exists
	popen = subprocess.Popen('avconv', shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
	if (not popen.stdout.read()):
		print 'You must install avconv to use this program.'
		return 0

	# checking if mkvtoolnix exists
	popen = subprocess.Popen('mkvmerge', shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
	if (not popen.stdout.read()):
        	print 'You must install mkvtoolnix to use this program.'
	        return 0

	if len(sys.argv) == 3:
		src_file = sys.argv[1]
		dst_file = sys.argv[2]
	else:
        	print 'usage: %s source destination' % os.path.basename(sys.argv[0])
	        return 0

	# checking if file
	if not os.path.isfile(src_file):
		print 'Source file doesn\'t exist'
		return 0
		
	# checking destination dir
	if not os.path.isdir(os.path.dirname(dst_file)):
		print 'Destination directory doesn\'t exist'
	        return 0

	# check if this is .mkv file
	if not os.path.splitext(src_file)[1] == '.mkv':
		print 'Script supports only matroska files'
        	return 0

	processing(src_file, dst_file)
	return 1

# START:
if __name__ == '__main__':
	sys.exit(main())
