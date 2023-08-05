from airflow.plugins_manager import AirflowPlugin
from my_provider.hooks.dlc_hook import DLCHook


class MyProviderPlugin(AirflowPlugin):
    name = "my_provider"
    hooks = [DLCHook]


def get_provider_info():
    return {
        "package-name": "my_provider",
        "name": "my provider",
        "description": "my provider",
        "hook-class-names": [
            "my_provider.hooks.dlc_hook.DLCHook",
        ],
    }
