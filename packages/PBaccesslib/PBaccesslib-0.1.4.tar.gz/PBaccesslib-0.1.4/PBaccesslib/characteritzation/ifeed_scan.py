from PBaccesslib.characteritzation.logic.test_logic import Scan
from Bconvertacceslib.use_linda_data_manager import use_chip_reg_to_pack_data, use_pixel_reg_to_pack_data
from PBaccesslib.characteritzation.logic.use_matrix_operations import pr_feed_true_all, pr_feed_false_all,\
    pr_set_ifeed, pr_tpena_on
from PBaccesslib import BITMAP
from PBaccesslib.characteritzation import logger


class IfeedScan(Scan):
    def __init__(self, dac_pos_arr: list, data_ref: int, data_low: int, data_max: int, data_incr: int, bridge):
        super(IfeedScan, self).__init__(dac_pos_arr, data_ref, data_low, data_max, data_incr)
        self.bridge = bridge

    def _init_registers(self, pixel_reg, chip_reg, ifeed_range, ifeed_value):
        """ Initial values to set on chip register"""
        md_cr, _ = self.replace_data_in_matrix(chip_reg, self.data_ref, (0, self.DAC_REF_POS))
        for dac_pos in self.dac_pos_arr:
            md_cr, _ = self.replace_data_in_matrix(md_cr, self.data_low, (0, dac_pos))

        """ Initial values to set on pixel register"""
        md_pr = pixel_reg
        if ifeed_range:
            md_pr = pr_feed_true_all(md_pr)
        else:
            md_pr = pr_feed_false_all(md_pr)

        md_pr = pr_set_ifeed(md_pr, ifeed_value)
        md_pr = pr_tpena_on(md_pr)

        """Activate TDAC"""
        self.bridge.use_set_tdac(0.4)

        """ Programing chip register """
        pack_data = use_chip_reg_to_pack_data(md_cr)
        self.bridge.use_chip_register_write(pack_data, BITMAP)

        """ Programing pixel register """
        pack_data = use_pixel_reg_to_pack_data(md_pr)
        self.bridge.use_pixel_register_write(pack_data, BITMAP)

        return md_cr

    def test(self, pixel_reg, chip_reg, ifeed_range, ifeed_value, pulses_width, pulses, timer_reg, belt_dir,
             test_pulses, frames, folder_path, folder_name):
        pixel_reg = pixel_reg.copy()
        chip_reg = chip_reg.copy()

        md_pr = self.mask_unmask_disc(pixel_reg)
        md_cr = self._init_registers(md_pr, chip_reg, ifeed_range, ifeed_value)
        error, all_counters_data = self.loop_scan(md_cr, pulses_width, pulses, timer_reg, belt_dir, test_pulses, frames,
                                                  self.bridge)
        if error:
            return True
        if all_counters_data is None:
            logger.error("All the counters in data are None")
            return True
        error = self.save_data(all_counters_data, folder_path, folder_name)
        return error