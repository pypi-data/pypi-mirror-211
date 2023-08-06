from nonebot import require

require("nonebot_plugin_datastore")
require("nonebot_plugin_apscheduler")

from .config import conf
from .service import get_nonebot_service

from importlib import import_module
from nonebot import logger, get_driver, get_loaded_plugins

supported_modules = {
    "OneBot V11": "nonebot_plugin_access_control_onebot",
    "OneBot V12": "nonebot_plugin_access_control_onebot",
    "Kaiheila": "nonebot_plugin_access_control_kaiheila",
}

loaded_modules = []

driver = get_driver()
for adapter in driver._adapters:
    if adapter in supported_modules:
        import_module(supported_modules[adapter])
        loaded_modules.append(adapter)
        logger.debug(f"Succeed to loaded plugin for {adapter}")

if len(loaded_modules):
    logger.success(f"Loaded plugin for: {', '.join(loaded_modules)}")

if conf.access_control_auto_patch_enabled:
    @get_driver().on_startup
    def _():
        nonebot_service = get_nonebot_service()

        patched_plugins = []

        for plugin in get_loaded_plugins():
            if plugin.name == 'nonebot_plugin_access_control' or plugin.name in conf.access_control_auto_patch_ignore:
                continue

            service = nonebot_service.get_or_create_plugin_service(plugin.name)
            if service.auto_created:
                for matcher in plugin.matcher:
                    service.patch_matcher(matcher)
                patched_plugins.append(plugin)

        logger.opt(colors=True).success(
            "auto patched plugin(s): " + ', '.join([f'<y>{p.name}</y>' for p in patched_plugins]))
