Title: Microphone feedback loop with PulseAudio
Date: 2015-10-06 14:33
Author: Thanh
Category: Linux
Tags: alsa, arch, archlinux, pulseaudio
Slug: microphone-feedback-loop-with-pulseaudio
Status: published

Moving to PulseAudio is pretty painless. Just need to install the
package and edit /etc/pulse/client.conf to have:

    autospawn = yes

One issue I did have was I kept hearing my microphone input in my
headphones using a USB headset.  
Fixing this was quite simple - in alsamixer, use F6 to select the
'sound card' and select your headset.  
Mute the 'Playback' for the microphone while leaving the capture
options on.
