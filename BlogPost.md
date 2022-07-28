# How to install 'perf' on the HiFive Unmatched

## Updating Ubuntu

```Source : https://ubuntu.com/tutorials/how-to-install-ubuntu-on-risc-v-hifive-boards```

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
    Note: _mmcblk0_ is the part to the SD card when it is directly connected to the system that you have downloaded the image on. If you are using a USB adapter, the path to _of_ could change to something along the lines of _/dev/sdb_.

3. Connect to the board via serial connection after inserting the microSD back into it. <br>

    Assuming you are on Linux, <br>

    ``` 
    ls /dev/serial/by-path 
    ```

    This should give you a couple ports that the serial connection can be accessed from. Pick one, and run:

    ``` 
    sudo screen -L /dev/serial/by-path/<YOUR PORT> 115200 
    ``` 

4. Boot up the image on the board. Once you are in the kernel, you need to redownload the image using the same commands as in step 1.
    ```
    wget https://cdimage.ubuntu.com/releases/22.04/release/ubuntu-22.04-preinstalled-server-riscv64+unleashed.img.xz
    
    unxz ubuntu-22.04-preinstalled-server-riscv64+unleashed.img.xz
    ```

5. Check if the NVMe drive exists.
    ```
    ls -l /dev/nvme*
    ```
    Choose the partition of the NVMe that appears. It could be _/dev/nvme0n1_ or even _/dev/nvme0n1p1_. <br>
    Flash the image onto your partition.
    ```
    sudo dd if=/ubuntu-22.04-preinstalled-server-riscv64+unmatched.img of=/dev/<YOUR PARTITION> bs=1M status=progress
    ```

6. There is a race condition that could result in the board booting off the microSD card instead of the NVMe drive. To prevent it, mount the NVMe drive and chroot it.
    ```
    sudo mount /dev/<YOUR PARTITION> /mnt
    sudo chroot /mnt
    ```

7. Edit ```/etc/default/u-boot``` and uncomment the line ```U_BOOT_ROOT="root=/dev/<YOUR PARTITION>"``` <br>
    Apply your changes.
    ```
    u-boot-update
    ```

8. Reboot your system.

NOTE: if you already have a previous version of Ubuntu installed on the board, you should delete it to free up the NVMe drive for the new version. One way of doing that is deleting the _.config_ file in _extlinux_.

## Updating the Kernel

## Updating perf