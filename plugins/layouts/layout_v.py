# layout_v.py
from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QTextEdit

def create_conversion_layout(xlsx_to_csv_func, csv_rename_func, conversion_module_func, mks2chainage_func):
    conversion_layout = QVBoxLayout()
    conversion_module_button = QPushButton('Conversion Module')
    con_xlsx_to_csv_button = QPushButton('xlsxToCsv')
    con_csv_rename_button = QPushButton('renameCsv')
    con_xlsx_to_csv_button.clicked.connect(xlsx_to_csv_func)
    con_csv_rename_button.clicked.connect(csv_rename_func)
    conversion_module_button.clicked.connect(conversion_module_func)
    pro_mks2chainage_button = QPushButton('mkChainCsv')
    pro_mks2chainage_button.setObjectName("specialButton")
    pro_mks2chainage_button.clicked.connect(mks2chainage_func)
    conversion_layout.addWidget(con_xlsx_to_csv_button)
    conversion_layout.addWidget(con_csv_rename_button)
    conversion_layout.addWidget(pro_mks2chainage_button)
    conversion_layout.addStretch()
    conversion_layout.addWidget(conversion_module_button)
    return conversion_layout

def create_processing_layout(chg_split_func, chg_insert_func, clean_csv_func, mkcc_func, processing_module_func):
    processing_layout = QVBoxLayout()
    processing_module_button = QPushButton('Processing Module')
    pro_chg_split_button = QPushButton('splitChg')
    pro_chg_insert_button = QPushButton('insertChg')
    pro_clean_csv_button = QPushButton('cleanCsv')
    pro_mkcc_button = QPushButton('mkMikeTxt')
    pro_chg_split_button.clicked.connect(chg_split_func)
    pro_chg_insert_button.clicked.connect(chg_insert_func)
    pro_clean_csv_button.clicked.connect(clean_csv_func)
    pro_mkcc_button.clicked.connect(mkcc_func)
    processing_module_button.clicked.connect(processing_module_func)
    processing_layout.addWidget(pro_chg_split_button)
    processing_layout.addWidget(pro_chg_insert_button)
    processing_layout.addWidget(pro_clean_csv_button)
    processing_layout.addWidget(pro_mkcc_button)
    processing_layout.addStretch()
    processing_layout.addWidget(processing_module_button)
    return processing_layout

def create_virtual_section_layout(get_virtual_end_func, virtual_start_func, virtual_end_func, virtual_end_update_func, combine_files_func, virtual_section_module_func):
    virtual_section_layout = QVBoxLayout()
    virtual_section_module_button = QPushButton('Virtual Section Module')
    virtual_get_end_button = QPushButton('getVirtEnd')
    virtual_start_button = QPushButton('virtStart')
    virtual_end_button = QPushButton('virtEnd')
    virtual_end_update_button = QPushButton('virtEndUpdate')
    vir_combine_files_button = QPushButton('combineTxt')
    virtual_get_end_button.clicked.connect(get_virtual_end_func)
    virtual_start_button.clicked.connect(virtual_start_func)
    virtual_end_button.clicked.connect(virtual_end_func)
    virtual_end_update_button.clicked.connect(virtual_end_update_func)
    vir_combine_files_button.clicked.connect(combine_files_func)
    virtual_section_module_button.clicked.connect(virtual_section_module_func)
    virtual_section_layout.addWidget(virtual_get_end_button)
    virtual_section_layout.addWidget(virtual_start_button)
    virtual_section_layout.addWidget(virtual_end_button)
    virtual_section_layout.addWidget(virtual_end_update_button)
    virtual_section_layout.addWidget(vir_combine_files_button)
    virtual_section_layout.addStretch()
    virtual_section_layout.addWidget(virtual_section_module_button)
    return virtual_section_layout


