include("$(MPY_DIR)/extmod/uasyncio/manifest.py")
#freeze("$(MPY_DIR)/drivers/dht", "dht.py")
#freeze("$(MPY_DIR)/drivers/display", ("lcd160cr.py", "lcd160cr_test.py"))
#freeze("$(MPY_DIR)/drivers/onewire", "onewire.py")
freeze("$(MPY_DIR)/ports/stm32/modules", "dht.py")
freeze("$(MPY_DIR)/ports/stm32/modules", "font.py")
freeze("$(MPY_DIR)/ports/stm32/modules", "onewire.py")
freeze("$(MPY_DIR)/ports/stm32/modules", "ophyra_botones.py")
freeze("$(MPY_DIR)/ports/stm32/modules", "ophyra_eeprom.py")
freeze("$(MPY_DIR)/ports/stm32/modules", "ophyra_mpu60.py")
freeze("$(MPY_DIR)/ports/stm32/modules", "ophyra_tftdisp.py")
