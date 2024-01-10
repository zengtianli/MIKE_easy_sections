# plugin_loader.py
import os
import importlib.util


def load_plugins(plugin_directory):
    plugins = []
    for filename in os.listdir(plugin_directory):
        if filename.endswith('.py') and not filename.startswith('__'):
            module_name = filename[:-3]
            module_path = os.path.join(plugin_directory, filename)
            spec = importlib.util.spec_from_file_location(
                module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, 'Plugin'):
                plugins.append(module.Plugin())
    return plugins
