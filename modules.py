from script_executor import (
    R_xlsx2csv, R_rename_csv, R_mks2chain, R_split_chg,
    R_insert_chg, R_clean_csv, R_mkcc, R_get_virt_end,
    R_virt_start, R_virt_end, R_upd_virt_end, R_combine_txt
)


def convert_module(window, output_area):
    R_xlsx2csv(window, output_area)
    R_rename_csv(window, output_area)


def process_module(window, output_area):
    R_mks2chain(window, output_area)
    R_split_chg(window, output_area)
    R_insert_chg(window, output_area)
    R_clean_csv(window, output_area)
    R_mkcc(window, output_area)


def virt_section_module(window, output_area):
    R_get_virt_end(window, output_area)
    R_virt_start(window, output_area)
    R_virt_end(window, output_area)
    R_upd_virt_end(window, output_area)
    R_combine_txt(window, output_area)
