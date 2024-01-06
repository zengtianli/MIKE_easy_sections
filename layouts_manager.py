# layouts_manager.py
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget
from PyQt6.QtGui import QKeySequence, QAction
from PyQt6 import sip
import layout_h
import layout_v

# def clear_layout(layout, output_area):
#     if layout is not None:
#         while layout.count() > 0:
#             item = layout.takeAt(0)
#             widget = item.widget()
#             if widget is not None:
#                 if widget != output_area:  # Make sure not to delete output_area
#                     widget.deleteLater()
#                 else:
#                     widget.setParent(None)  # Reparent output_area to keep it alive
#             elif item.layout() is not None:
#                 clear_layout(item.layout(), output_area)
#         sip.delete(layout,output_area)

def clear_layout(layout):
    global output_area  # If output_area is global, declare it as such
    if layout is not None:
        while layout.count() > 0:
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                if widget != output_area:  # Make sure not to delete output_area
                    widget.deleteLater()
                else:
                    widget.setParent(None)  # Reparent output_area to keep it alive
            elif item.layout() is not None:
                clear_layout(item.layout())
            else:
                sip.delete(item)
def setup_layout(window, layout_type, output_area, function_map):
    central_widget = window.centralWidget()
    clear_layout(central_widget.layout() )
    # clear_layout(central_widget.layout(), output_area)
    
    main_layout = QVBoxLayout() if layout_type == 'horizontal' else QHBoxLayout()
    layout_module = layout_h if layout_type == 'horizontal' else layout_v
    
    conversion_layout = layout_module.create_conversion_layout(*function_map['conversion'])
    processing_layout = layout_module.create_processing_layout(*function_map['processing'])
    virtual_section_layout = layout_module.create_virtual_section_layout(*function_map['virtual_section'])
    
    for layout in [conversion_layout, processing_layout, virtual_section_layout]:
        main_layout.addLayout(layout)
    
    main_layout.addWidget(output_area)
    central_widget.setLayout(main_layout)

def add_layout_switch_actions(window, output_area, function_map):
    layout_menu = window.menuBar().addMenu('Layout')
    
    horizontal_layout_action = QAction('Horizontal Layout', window)
    horizontal_layout_action.setShortcut(QKeySequence('Ctrl+Alt+C'))
    horizontal_layout_action.triggered.connect(lambda: setup_layout(window, 'horizontal', output_area, function_map))
    
    vertical_layout_action = QAction('Vertical Layout', window)
    vertical_layout_action.setShortcut(QKeySequence('Ctrl+Alt+V'))
    vertical_layout_action.triggered.connect(lambda: setup_layout(window, 'vertical', output_area, function_map))
    
    layout_menu.addAction(horizontal_layout_action)
    layout_menu.addAction(vertical_layout_action)

