from datetime import datetime
import time
import os
import __future__

class Wrapper(object):

    def __init__(self, subprocess):
        self._subprocess = subprocess

    def call(self, cmd):
        p = self._subprocess.Popen(cmd, shell=True, stdout=self._subprocess.PIPE,
            stderr=self._subprocess.PIPE)
        out, err = p.communicate()
        return p.returncode, out.rstrip(), err.rstrip()

class Identify(Wrapper):
    """ A class which wraps calls to the external identify process. """

    def __init__(self, subprocess):
        Wrapper.__init__(self, subprocess)
        self._CMD = 'convert'

    def mean_brightness(self, filepath):
	# Use the thumbnail for the mean brightness check, because it's faster than using the full image
        code, out, err = self.call(self._CMD + ' ' + filepath + ' thumbnail:- | identify -format "%[mean]" -')
        if code != 0:
            raise Exception(err)
        return out

class RaspiStill(Wrapper):
    """ A class which wraps calls to the external raspistill process. """

    def __init__(self, subprocess):
        Wrapper.__init__(self, subprocess)
	# Create a thumbnail with a useful size for mean brightness checks
        self._CMD = 'raspistill --nopreview --encoding jpg --width 1920 --height 1080 --quality 96 --thumb 512:288:80 --timeout 2000'

    def capture_image_and_download(self):
	time = datetime.now()
	filepath = os.path.dirname(os.path.realpath(__file__)) + "/photos"
	filenamePrefix = "img"
	shutter = str(eval(compile(self._shutter_choice, '<string>', 'eval', __future__.division.compiler_flag))*1000000)
	filename = filepath + "/" + filenamePrefix + "-%04d%02d%02d-%02d%02d%02d.jpg" % (time.year, time.month, time.day, time.hour, time.minute, time.second)
        code, out, err = self.call(self._CMD + ' --shutter ' + shutter + ' --ISO ' + self._iso_choice + ' --output ' + filename)
        if code != 0:
            raise Exception(err)
        return filename

    def set_shutter_speed(self, secs=None):
        code, out, err = None, None, None
        if secs:
		self._shutter_choice = secs

    def set_iso(self, iso=None):
        code, out, err = None, None, None
        if iso:
		self._iso_choice = iso
