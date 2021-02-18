MCU_SERIES = f4
CMSIS_MCU = STM32F407xx
AF_FILE = boards/stm32f407_af.csv
LD_FILES = boards/stm32f407.ld boards/common_ifs.ld
TEXT0_ADDR = 0x08000000
TEXT1_ADDR = 0x08020000
# MicroPython settings
#MICROPY_VFS_LFS2 = 1
