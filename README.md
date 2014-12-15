Timelapse photography with a Raspberry Pi
=========================================

This set of files allows a Raspberry Pi to take timelapse photos, starting the
timelapse sequence as part of the boot process if no network devices are
present. It's set up this way because, generally, I run this from a Model A or
A+ for the battery life and if there's a Wifi dongle plugged in then I want to
control the Pi, if there isn't it's because it's on a hillside somewhere so I
want it to start taking photos as soon as it powers on.

In some respects this is a cut-down version of the DSLR-controlling timelapse
by David Singleton <https://github.com/dps/rpi-timelapse>.

It includes an autocorrection feature for under/over exposure, to handle
sunrise/sunset or other changes in light levels, within the limits of the
values in the array `CONFIGS` in `timelapse.py`.


Setup
-----

Clone this repo into the home directory of the `pi` user and merge the example
`rc.local` file with your system's `/etc/rc.local` (assuming you're using
Raspbian) to have it run on startup if there's no `wlan0` interface.

To run it manually, start it with

```Shell
/home/pi/rpi-timelapse/timelapse.py &
```

and stop it with

```Shell
ps aux|grep 'python.*/timelapse.py$'|awk 'NR==1 {print $2}'|xargs kill -9
```

Dependencies
------------

Requires `imagemagick` to perform autocorrection of exposure settings based on
the mean brightness of the last photo. Created and tested on Raspbian, may not
play nicely with others.
