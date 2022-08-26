# How to setup 'perf' on the HiFive Unmatched for Additional Events

## Installing Ubuntu

```
Sources : 
[1] https://ubuntu.com/tutorials/how-to-install-ubuntu-on-risc-v-hifive-boards
```
If you already have Ubuntu 22.04 installed on the HiFive Unmatched, you may skip
to [updating OpenSBI](#updating-opensbi-with-u-boot)
.
### Steps
1. Download the image for the _HiFive Unmatched_ </br>
    ```
    wget https://cdimage.ubuntu.com/releases/22.04/release/ubuntu-22.04-preinstalled-server-riscv64+unleashed.img.xz
    
    unxz ubuntu-22.04-preinstalled-server-riscv64+unleashed.img.xz
    ```

2. Flash the image onto the microSD card using the command line
    ```
    dd if=</path/to/image.img> of=/dev/mmcblk0 bs=1M status=progress
    ```
    Note: _mmcblk0_ is the name of the SD card when it is directly connected to the system that you have downloaded the image on. If you are using a USB adapter, the path to _of_ could change to something along the lines of _/dev/sdb_.

3. Connect to the board via serial connection after inserting the microSD back into it. <br>

    Assuming you are on Linux, <br>

    ``` 
    ls /dev/serial/by-path 
    ```

    This should give you a couple ports that the serial connection can be accessed from. Pick one, and run:

    ``` 
    sudo screen -L /dev/serial/by-path/<YOUR PORT> 115200 
    ``` 

4. Boot up the board. If you already have a previous version of Ubuntu installed on the board, the bootloader will boot the old version instead of the image on the SD card. You should delete the ```extlinux.conf``` bootloader file on the NVMe to force the stage 1 bootloader to boot the Ubuntu image on the SD card instead of the NVMe. Then reboot.
    ```
    sudo rm /boot/extlinux/extlinux.conf
    ```
5. Once you are in booted into the Ubuntu image on the SD card, you need to redownload the image using the same commands as in step 1.
    ```
    wget https://cdimage.ubuntu.com/releases/22.04/release/ubuntu-22.04-preinstalled-server-riscv64+unleashed.img.xz
    
    unxz ubuntu-22.04-preinstalled-server-riscv64+unleashed.img.xz
    ```

5. Check if the NVMe drive exists.
    ```
    ls -l /dev/nvme*
    ```
    Choose the name of the NVMe that appears. It may be something like _/dev/nvme0n1_. <br>
    
    Flash the image onto your partition.
    ```
    sudo dd if=/ubuntu-22.04-preinstalled-server-riscv64+unmatched.img of=/dev/<YOUR NVMe device name> bs=1M status=progress
    ```

6. There is a race condition that could result in the board booting off the microSD card instead of the NVMe drive. To prevent it, mount the NVMe drive and chroot it.
    ```
    sudo mount /dev/<YOUR NVMe NAME>p1 /mnt
    sudo chroot /mnt
    ```

7. Edit ```/etc/default/u-boot``` and uncomment the line ```U_BOOT_ROOT="root=/dev/<YOUR NVMe>p1"``` <br>
    Apply your changes.
    ```
    u-boot-update
    ```
    Exit the chroot environment.
    ```
    exit
    ```

8. Reboot your system. It should now boot the new Ubuntu version from the NVMe!

## Updating OpenSBI with U-Boot
```
Sources:
[1]: https://u-boot.readthedocs.io/en/latest/board/sifive/unmatched.html
```


### Steps
1. Download and extract the source code for the latest release of OpenSBI.
Version 1.1 or later is reccommended. 

    ```sh
    wget https://github.com/riscv-software-src/opensbi/archive/refs/tags/v1.1.zip
    unzip v1.1.zip
    ```

2. Download the source code for U-Boot
    ```sh
    git clone https://source.denx.de/u-boot/u-boot.git
    ```

3. Compile OpenSBI and store the path to the firmware binary in a variable. U-Boot
will look for this path during the U-boot compilation.

    ```sh
    cd opensbi-1.1
    make PLATFORM=generic -j4
    export OPENSBI=<full_path_to_opensbi-1.1>/build/platform/generic/firmware/fw_dynamic.bin
    ```

4. Change into the U-Boot source directory and checkout the branch for the latest
release.

    ```sh
    cd <path-to_u_boot_source>
    git checkout v2022.07
    ```

5. Compile U-Boot with OpenSBI.

    ```sh
    make sifive_unmatched_defconfig
    make -j4
    ```

6. Format the SD card that will contain OpenSBI and U-Boot.

    ```sh
    sudo sgdisk -g --clear -a 1 \
    --new=1:34:2081         --change-name=1:spl --typecode=1:5B193300-FC78-40CD-8002-E86C45580B47 \
    --new=2:2082:10273      --change-name=2:uboot  --typecode=2:2E54B353-1271-4842-806F-E436D6AF6985 \
    --new=3:16384:282623    --change-name=3:boot --typecode=3:0x0700 \
    --new=4:286720:13918207 --change-name=4:root --typecode=4:0x8300 \
    /dev/mmcblk0

    sudo mkfs.vfat /dev/mmcblk0p3
    sudo mkfs.ext4 /dev/mmcblk0p4
    ```
    The official instructions from U-Boot say to copy a Linux Image and a
    device tree binary to partition 3 of the SD card. This is not required here
    because U-Boot will boot Ubuntu from the NVMe, not a Linux Image from the
    SD card.

7. Program the SD card with U-Boot.

    ```sh
    sudo dd if=spl/u-boot-spl.bin of=/dev/mmcblk0 seek=34
    sudo dd if=u-boot.itb of=/dev/mmcblk0 seek=2082
    ```
    OpenSBI and U-Boot are now installed. Reboot the HiFive Unmatched. It should
    boot into Ubuntu.
## Patching and Compiling the Kernel for perf

``` 
Sources: 
[1]: https://www.kernel.org 
[2]: https://www.linux.com/topic/desktop/how-compile-linux-kernel-0/
[3]: https://github.com/carlosedp/riscv-bringup/tree/master/unmatched/patches
[4]: https://patchwork.kernel.org/project/linux-riscv/patch/20220727043829.151794-1-apatel@ventanamicro.com/
[5]: https://patchwork.kernel.org/project/linux-riscv/cover/20220815132251.25702-1-nikita.shubin@maquefel.me/
```


### Steps
1. Download the image of the latest stable Linux kernel and extract it.

    ``` 
    wget https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.19.4.tar.xz
    unxz linux-5.19.4.tar.xz
    ```

2. Verify the signature of the tar file.

    ```
    wget https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.19.4.tar.sign
    gpg2 --locate-keys torvalds@kernel.org gregkh@kernel.org
    gpg2 --verify linux-5.19.4.tar.sign
    ```

3. Once verified, extract the tar file.

    ```
    tar -xvf linux-5.19.4.tar 
    ```

4. Download the kernel configuration file for the HiFive Unmatched board.

    ```
    wget https://raw.githubusercontent.com/carlosedp/riscv-bringup/master/unmatched/patches/linux-5.13-defconfig
    ```

5. Copy the config file to the kernel source directory as .config.

    ```
    cp linux-5.13-defconfig <PATH_TO_KERNEL_SOURCE>/.config
    ```

6. Move into the kernel directory

    ```
    cd linux-5.19.4
    ```

7. Download the .patch files for the two kernel patch series needed for perf.

    ```sh
    wget -O v2-RISC-V-Add-mvendorid-marchid-and-mimpid-to-proc-cpuinfo-output.patch https://patchwork.kernel.org/series/663315/mbox/
    wget -O RISC-V-Create-unique-identification-for-SoC-PMU.patch https://patchwork.kernel.org/series/667649/mbox/
    ```

8. Apply the patches to the kernel source,

    ```sh
    git apply v2-RISC-V-Add-mvendorid-marchid-and-mimpid-to-proc-cpuinfo-output.patch
    git apply RISC-V-Create-unique-identification-for-SoC-PMU.patch
    ```

9. Generate a config file for the newest kernel version from the old config.

    ```
    make oldconfig
    ```
    If prompted, it is okay to accept the defaults for all by hitting enter.

10. Make an Image file from the extracted folder.

    ``` 
    make Image -j4
    ```

    After the command finishes running, there should be an ```Image``` file in ```arch/riscv/boot```.

11. Link the files that were made to the system configurations.

    ```
    sudo make install
    sudo u-boot-update
    ```

12. The previous commands will not generate the device tree blob that the kernel
requires to properly boot. Generate the device tree blob for the kernel and copy
it to the expected location.

    ```sh
    make dtbs
    sudo mkdir -p /lib/firmware/5.19.4/device-tree/sifive
    sudo cp ./arch/riscv/boot/dts/sifive/hifive-unmatched-a00.dtb /lib/firmware/5.19.4/device-tree/sifive
    ```

13. Go into ```extlinux/extlinux.config``` and check the generated configurations. There should be 4, 2 for the old kernel and 2 for the new kernel.

    Every entry should have a label, and 5 lines inside a label beginning with menu, linux, initrd, fdtdir, and append.

    If the ```fdtdir``` line is missing in the new kernel, add it to match
    the following:

    ```
    label l0
        menu label Ubuntu 22.04.1 LTS 5.19.4
        linux /boot/vmlinuz-5.19.4
        initrd /boot/initrd.img-5.19.4
        fdtdir /lib/firmware/5.19.4/device-tree/
        append root=/dev/nvme0n1p1 ro earlycon

    label l0r
        menu label Ubuntu 22.04.1 LTS 5.19.4 (rescue target)
        linux /boot/vmlinuz-5.19.4
        initrd /boot/initrd.img-5.19.4
        fdtdir /lib/firmware/5.19.4/device-tree/
        append root=/dev/nvme0n1p1 ro earlycon single
    ``` 
14. Reboot your system. On startup, choose the new kernel to boot into.

## Updating perf
Once you are booted into the latest kernel, you should have the necessary drivers
to track more hardware events in addition to cycles and instructions. Here we
will compile the perf from source for the kernel that was just installed. From
the linux source directory run.

    ```sh
    make tools/perf -j4
    ```
    
It may take some time to compile. once it is compiled, the perf binary can be
found in ```<Kernel Source Directory>/tools/perf/```. To run,

    ```sh
    cd tools/perf/
    ./perf list
    ```

This should print the list of hardware events that can be tracked. The list
should now include more hardware events in addition to cycles and isntructions.
As an example, run the following:

    ```sh
    ./perf stat -e cycles,instructions,branches,branch-misses,L1-icache-misses dd if=/dev/zero of=/dev/null count=100000
    ```
It should print something like this:

    100000+0 records in
    100000+0 records out
    51200000 bytes (51 MB, 49 MiB) copied, 0.17495 s, 293 MB/s

    Performance counter stats for 'dd if=/dev/zero of=/dev/null count=100000':

         211980211      cycles                                                        (59.53%)
         179394027      instructions              #    0.85  insn per cycle           (79.75%)
          23418613      branches                                                      (79.74%)
           6250208      branch-misses             #   26.69% of all branches          (80.17%)
                 0      L1-icache-misses                                              (40.08%)

       0.179009332 seconds time elapsed

       0.055746000 seconds user
       0.123438000 seconds sys