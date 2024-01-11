import os
import importlib.util
import json
from constants import PLUGIN_CONFIG_FILE

class PluginManager:
    def __init__(self, window, menu_bar, plugins_folder):
        self.window = window
        self.menu_bar = menu_bar
        self.plugins_folder = plugins_folder
        self.loaded_plugins = {}
    def save_plugin_config():
        config = {}
        if os.path.exists(PLUGIN_CONFIG_FILE):
            with open(PLUGIN_CONFIG_FILE, 'r') as file:
                config = json.load(file)
        config['plugins'] = list(loaded_plugins.keys())
        with open(PLUGIN_CONFIG_FILE, 'w') as file:
            json.dump(config, file)
    def load_plugin_config():
        if os.path.exists(PLUGIN_CONFIG_FILE):
            with open(PLUGIN_CONFIG_FILE, 'r') as file:
                config = json.load(file)
                plugin_files = config.get('plugins', [])
                for plugin_file in plugin_files:
                    load_plugin(plugin_file)
                # After all plugins are loaded, call a method to load their settings
                for plugin_file in plugin_files:
                    plugin_name = os.path.splitext(plugin_file)[0]  # Remove .py extension
                    plugin_settings = config.get(plugin_name, {})
                    if plugin_file in loaded_plugins:
                        loaded_plugins[plugin_file].load_settings(plugin_settings)
    def load_plugin(plugin_file):
        global loaded_plugins
        plugin_path = os.path.join(plugins_folder, plugin_file)
        if os.path.isfile(plugin_path) and plugin_file.endswith('.py'):
            spec = importlib.util.spec_from_file_location("plugin_module", plugin_path)
            plugin_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(plugin_module)
            if hasattr(plugin_module, 'Plugin'):
                plugin = plugin_module.Plugin()
                plugin.initialize(window, menu_bar)
                loaded_plugins[plugin_file] = plugin
        save_plugin_config()
    def remove_plugin(plugin_file):
        global loaded_plugins
        if plugin_file in loaded_plugins:
            plugin = loaded_plugins[plugin_file]
            if hasattr(plugin, 'deinitialize'):
                plugin.deinitialize(window, menu_bar)
            del loaded_plugins[plugin_file]
        save_plugin_config()
    def open_plugin_selection():
        dialog = PluginSelectionDialog(plugins_folder, window)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected_plugin_file = dialog.selected_plugin()
            if selected_plugin_file:
                load_plugin(selected_plugin_file)
    def open_plugin_removal():
        dialog = PluginSelectionDialog(list(loaded_plugins.keys()), window)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected_plugin_file = dialog.selected_plugin()
            if selected_plugin_file:
                remove_plugin(selected_plugin_file)

