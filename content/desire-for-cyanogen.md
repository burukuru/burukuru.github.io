Title: Desire for Cyanogen
Date: 2012-03-22 10:44
Author: Thanh
Category: misc
Tags: android
Slug: desire-for-cyanogen
Status: published

It's been over a year and a half since I set up this site/blog so I
thought it was about time to write something. For the past week and a
half I've been on night shift at work which has a habit of over running
and eating a lot of my spare time. This made me choose a couple of
things I wanted to get working in the little time I had left during the
day so without further ado, I'll jump into what I've been getting up to
in the past couple of days.

I've owned the HTC Desire (GSM) for about a year and a half. It was one
of the better phones at the time but there's a couple of things that are
quite annoying about it; most notably the very limited internal storage.
After Google+ and Swype there is very little room for much else. I
decided to get Cyanogen hoping it was clear some of the HTC bloatware,
give me some extra space and give a breath of fresh air to the phone.
Also, it would be nice to move up from Froyo to Gingerbread

#### Getting S-OFF, root and CWM

[Revolutionary](http://revolutionary.io/) will set the secureflag to off
on the phone. Just download and run as root. I'm on Linux so ran into
some issues when installing ClockworkMod:

     Do you want to download (Internet connection required) and flash ClockworkMod Recovery? [Y/n]
     Downloading recovery for your phone (bravo)...revolutionary: ../sysdeps/unix/sysv/linux/getpagesize.c:32: __getpagesize: Assertion `_rtld_global_ro._dl_pagesize != 0' failed.

After some digging it was just easier to download CWM Recovery and
install it manually. I followed the instructions posted by attn1 from
the [xda-developers
forum](http://forum.xda-developers.com/showthread.php?p=14693680):

1.  Download the adb tool and appropriate CWM img file
2.  Extract and put them all in the same directory
3.  Put the phone into fastboot USB mode
4.  Run

<!-- -->

    sudo ./fastboot flash recovery recovery_name.img

CWM is now installed! Now follow the instructions on the forum to obtain
root!

If you'd like to read some more about CWM, here's [a nice
write-up](http://www.addictivetips.com/mobile/what-is-clockworkmod-recovery-and-how-to-use-it-on-android-complete-guide/).

#### Radio and Cyanogen

To get this rolling, we need the [latest radio
flashed](http://wiki.cyanogenmod.com/wiki/HTC_Desire_%28GSM%29:_FAQ#Fastboot_process)
using the fastboot process.

Then all that remains is [flashing Cyanogen and Google
Apps](http://wiki.cyanogenmod.com/wiki/HTC_Desire_%28GSM%29:_Full_Update_Guide#ClockworkMod_Recovery_process)!
