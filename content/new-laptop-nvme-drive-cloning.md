pre-req: external hard drive with bigger capacity than nvme drive, connectable via USB.

On old laptop:
dd if=/dev/nvme0n1 of=/mnt/thinkpad.img conv=sync bs=32M status=progress

On new laptop:
dd if=/mnt/thinkpad.img of=/dev/nvme0n1

```
cryptsetup open /dev/nvme0n1p2 cryptlvm
mount /dev/MyVolGroup/root /mnt
mount /dev/MyVolGroup/home /mnt/home
swapon /dev/MyVolGroup/swap
mount /dev/nvme0n1p1 /mnt/boot
```

Install EFI:

```
arch-root /mnt
ls -l /dev/disk/by-uuid > /uuid.txt
vim efi.sh uuid.txt
## efibootmgr --disk /dev/nvme0n1 --part 1 --create --label "Arch Linux" --loader /vmlinuz-linux --unicode 'root=/dev/MyVolGroup/root rw initrd=\initramfs-linux.img rd.luks.name={nvme0n1p2 UUID}=cryptlvm' --verbose
sh efi.sh
efibootmgr -v -u
logout
reboot
```

Make sure the `root=` argument matches the correct partition inside the PV, not the physical drive partition.