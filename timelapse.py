#!/usr/bin/python

from datetime import datetime
from datetime import timedelta
import subprocess
import time
import sys
import os

from wrappers import RaspiStill
from wrappers import Identify

logfile = os.path.dirname(os.path.realpath(__file__)) + "/timelapse.log"
sys.stdout = open(logfile, 'w')

MIN_INTER_SHOT_DELAY_SECONDS = timedelta(seconds=30)
MIN_BRIGHTNESS = 22500
MAX_BRIGHTNESS = 27500

CONFIGS = [
	("1/8000", 100),
	("1/6400", 100),
	("1/5000", 100),
	("1/4000", 100),
	("1/3200", 100),
	("1/2500", 100),
	("1/2000", 100),
	("1/1600", 100),
	("1/1250", 100),
	("1/1000", 100),
	("1/800", 100),
	("1/640", 100),
	("1/500", 100),
	("1/400", 100),
	("1/320", 100),
	("1/250", 100),
	("1/200", 100),
	("1/160", 100),
	("1/125", 100),
	("1/100", 100),
	("1/80", 100),
	("1/60", 100),
	("1/50", 100),
	("1/40", 100),
	("1/30", 100),
	("1/25", 100),
	("1/20", 100),
	("1/15", 100),
	("1/13", 100),
	("1/10", 100),
	("1/8", 100),
	("1/6", 100),
	("1/5", 100),
	("1/4", 100),
	("1/3", 100),
	("1/2.5", 100),
	("1/2", 100),
	("1/1.6", 100),
	("1/1.3", 100),
	("1", 100),
	("1.3", 100),
	("1.6", 100),
	("2", 100),
	("2.5", 100),
	("3", 100),
	("4", 100),
	("5", 100),
	("6", 100),
	("6", 125),
	("6", 160),
	("6", 200),
	("6", 250),
	("6", 320),
	("6", 400),
	("6", 500),
	("6", 640),
	("6", 800)
]

def main():
    print "Timelapse starting at %s" % (time.asctime())
    camera = RaspiStill(subprocess)
    idy = Identify(subprocess)

    current_config = 20
    shot = 0
    prev_acquired = None
    last_acquired = None
    last_started = None

    try:
        while True:
            last_started = datetime.now()
            config = CONFIGS[current_config]
            print "Shot: %d Shutter: %s ISO: %d" % (shot, config[0], config[1])
            sys.stdout.flush()

            camera.set_shutter_speed(secs=config[0])
            camera.set_iso(iso=str(config[1]))
            try:
              filename = camera.capture_image_and_download()
            except Exception, e:
              print "Error on capture: " + str(e)
              print "Retrying..."
              sys.stdout.flush()
              # Occasionally, capture can fail but retries will be successful.
              continue
            print "Shot: %d Filename: %s" % (shot, filename)
            sys.stdout.flush()

            prev_acquired = last_acquired
            brightness = float(idy.mean_brightness(filename))
            last_acquired = datetime.now()

            print "Shot: %d Brightness: %s" % (shot, brightness)
            sys.stdout.flush()

            if brightness < MIN_BRIGHTNESS and current_config < len(CONFIGS) - 1:
                current_config = current_config + 1
            elif brightness > MAX_BRIGHTNESS and current_config > 0:
                current_config = current_config - 1
            else:
                if last_started and last_acquired and last_acquired - last_started < MIN_INTER_SHOT_DELAY_SECONDS:
                    sleep_for = max((MIN_INTER_SHOT_DELAY_SECONDS - (last_acquired - last_started)).seconds, 0);
                    print "Sleeping for %s" % str(sleep_for)
                    sys.stdout.flush()
                    time.sleep(sleep_for)
            shot = shot + 1
    except Exception,e:
        print str(e)


if __name__ == "__main__":
    main()
