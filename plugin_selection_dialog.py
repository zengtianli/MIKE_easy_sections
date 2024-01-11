# plugin_selection_dialog.py
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QListWidget, QDialogButtonBox
import os
class PluginSelectionDialog(QDialog):
    def __init__(self, plugin_source, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select a Plugin")
        self.layout = QVBoxLayout(self)
        self.listWidget = QListWidget()
        if isinstance(plugin_source, str):
            self.populate_plugin_list_from_directory(plugin_source)
        elif isinstance(plugin_source, list):
            self.populate_plugin_list_from_names(plugin_source)
        self.layout.addWidget(self.listWidget)
        self.buttonBox = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonBox)
    def populate_plugin_list_from_directory(self, plugin_directory):
        for filename in os.listdir(plugin_directory):
            if filename.endswith('.py') and not filename.startswith('__'):
                self.listWidget.addItem(filename)
    def populate_plugin_list_from_names(self, plugin_names):
        for name in plugin_names:
            self.listWidget.addItem(name)
    def selected_plugin(self):
        return self.listWidget.currentItem().text() if self.listWidget.currentItem() else None
