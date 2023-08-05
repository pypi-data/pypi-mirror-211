from my_provider.hooks.dlc_hook import DLCHook

def get_provider_info():
    return {
        "package-name": "my-provider",
        "name": "my provider",
        "description": "my provider",
        "hook-class-names": [
            "my_provider.hooks.dlc_hook.DLCHook",
        ],
    }
