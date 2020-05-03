Title: Updating and resetting Raritan Dominion PX PDUs
Date: 2012-05-29 13:14
Author: Thanh
Category: SysAdmin
Tags: hardware
Slug: updating-and-resetting-raritan-dominion-px-pdus
Status: published

I just had the pleasure of resetting some PDUs to factory defaults
today. The models in question were Raritan Dominion PX20
(DPXR20A-16/32). After a mostly fruitless search for 'raritan px reset
to factory default' and 'raritan px restore to factory default', I have
managed to dig out a way to complete my task.

Nothing like homemade commando plugs with kettle leads, courtesy of my
colleague JT.

![Commando leads](https://thanhpham.cloud/upload/images/raritan/IMG_20120529_144041.jpg)

First I needed to upgrade the firmware to the latest version as the
command didn't seem to run on v1.3 for me. Grabbed my binaries from the
[Raritan
website](http://www.raritan.com/support/dominion-px/ "Raritan PX20 firmware").
I had to flash v1.5.2 before 1.5.5, YMMV. You can upgrade firmware using
the web interface:

-   Hook up to the console of the PDU with a DB9 to USB converter (top)
    and a special Raritan DB9 to Ethernet console cable (bottom), like
    this:
-		![Console cables](https://thanhpham.cloud/upload/images/raritan/IMG_20120528_152609.jpg "Console cables")
-   One of these, a Cisco compatible cable, won't work:
-		![Wrong console cables](https://thanhpham.cloud/upload/images/raritan/IMG_20120529_144401.jpg "Wrong console cables")
-   As I use Arch Linux I just ran the following as root:

<!-- -->

    screen /dev/ttyUSB0

-   Set the IP configuration to dhcp: 'config' at the prompt and then
    'dhcp'

<!-- -->

    [Old IP address] command: config
    IP autoconfiguration (none/dhcp/bootp) [none]: dhcp

Press [Enter] a few times until the old IP address becomes the new one,
you might have to unplug the network cable and plug it back in. Proceed
with the firmware upgrade in the web browser!

Once the upgrade is completed, go into 'clp' mode in the console and
type:

    clp:/-> set /system1 FactoryDefaults=true

Sorted! Now your PDU is ready to go on eBay :)

For more detailed information, check out the [Raritan Dominion PX Online
Help
site](http://www.raritan.com/help/px/v1.5.5/en/#3394 "Raritan Dominion PX Online Help").
