# How to install 'perf' on the HiFive Unmatched

## Updating Ubuntu

```
Sources : 
[1] https://ubuntu.com/tutorials/how-to-install-ubuntu-on-risc-v-hifive-boards
```

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

## Updating the Kernel

``` 
Sources: 
[1]: https://www.kernel.org 
[2]: https://www.linux.com/topic/desktop/how-compile-linux-kernel-0/
[3]: https://github.com/carlosedp/riscv-bringup/tree/master/unmatched/patches
```


### Steps
1. Download the image of the latest stable Linux kernel and extract it.

    ``` 
    wget https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.18.14.tar.xz
    unxz linux-5.18.14.tar.xz
    ```

2. Verify the signature of the tar file.

    ```
    wget https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.18.14.tar.sign
    gpg2 --locate-keys torvalds@kernel.org gregkh@kernel.org
    gpg2 --verify linux-5.18.14.tar.sign
    ```

3. Once verified, extract the tar file.

    ```
    tar -xvf linux-5.18.14.tar 
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
    cd linux-5.18.14
    ```

7. Generate a config file for the newest kernel version from the old config.

    ```
    make oldconfig
    ```
    If prompted, it is okay to accept the defaults for all by hitting enter.

8. Make an Image file from the extracted folder.

    ``` 
    make Image -j4
    ```

    After the command finishes running, there should be an ```Image``` file in ```arch/riscv/boot```.

9. Link the files that were made to the system configurations.

    ```
    sudo make install
    sudo u-boot-update
    ```

10. Go into ```extlinux/extlinux.config``` and check the generated configurations. There should be 4, 2 for the old kernel and 2 for the new kernel.

    Every entry should have a label, and 5 lines inside a label beginning with menu, linux, initrd, fdtdir, and append.

    If the ```fdtdir``` line is missing in the new kernel, copy the line from the old kernel and paste it in the new kernel. The assumption here is that the memory maps will remain consistent across all kernels due to similar hardware configurations.

    In the end, the labels should look something like this:

    ```
    label l1
            menu label Ubuntu 22.04 LTS 5.18.14
            linux /boot/vmlinuz-5.18.14
            initrd /boot/initrd.img-5.18.14
            fdtdir /lib/firmware/5.15.0-1015-generic/device-tree
            append root=/dev/nvme0n1p1 ro earlycon

    label l1r
            menu label Ubuntu 22.04 LTS 5.18.14 (rescue target)
            linux /boot/vmlinuz-5.18.14
            initrd /boot/initrd.img-5.18.14
            fdtdir /lib/firmware/5.15.0-1015-generic/device-tree
            append root=/dev/nvme0n1p1 ro earlycon single
    ``` 
11. Reboot your system. On startup, choose the new kernel to boot into.

## Updating perf
Once you are booted into the latest kernel, you should have the necessary drivers
to track more hardware events in addition to cycles and instructions. Here we
will compile the perf from source for the kernel that was just installed. From
the linux source directory run.


    make tools/perf -j 4
    
It may take some time to compile. once it is compiled, the perf binary can be
found in ```<Kernel Source Directory>/tools/perf/```. To run,

    cd tools/perf/
    ./perf list

This should print the list of hardware events that can be tracked. The list
should now include more hardware events in addition to cycles and isntructions.