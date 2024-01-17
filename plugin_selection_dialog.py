# plugin_selection_dialog.py
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QListWidget, QDialogButtonBox
import os


class PluginSelectionDialog(QDialog):
    """
    A dialog window for selecting a plugin.

    Args:
        plugin_source (str or list): The source of the plugins. It can be either a directory path
            containing plugin files or a list of plugin names.
        parent (QWidget, optional): The parent widget of the dialog.

    Attributes:
        listWidget (QListWidget): The list widget displaying the available plugins.

    Methods:
        populate_plugin_list_from_directory(plugin_directory): Populates the plugin list from a directory.
        populate_plugin_list_from_names(plugin_names): Populates the plugin list from a list of names.
        selected_plugin(): Returns the currently selected plugin name.

    Signals:
        accepted(): This signal is emitted when the dialog is accepted.
        rejected(): This signal is emitted when the dialog is rejected.
    """
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
        """
        Populates the plugin list from a directory.

        Args:
            plugin_directory (str): The directory path containing plugin files.
        """
        for filename in os.listdir(plugin_directory):
            if filename.endswith('.py') and not filename.startswith('__'):
                self.listWidget.addItem(filename)

    def populate_plugin_list_from_names(self, plugin_names):
        """
        Populates the plugin list from a list of names.

        Args:
            plugin_names (list): The list of plugin names.
        """
        for name in plugin_names:
            self.listWidget.addItem(name)

    def selected_plugin(self):
        """
        Returns the currently selected plugin name.

        Returns:
            str or None: The name of the selected plugin, or None if no plugin is selected.
        """
        return self.listWidget.currentItem().text() if self.listWidget.currentItem() else None
