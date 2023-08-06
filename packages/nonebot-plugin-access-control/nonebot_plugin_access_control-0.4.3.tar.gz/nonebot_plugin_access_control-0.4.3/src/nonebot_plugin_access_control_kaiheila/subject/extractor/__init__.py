from nonebot.adapters.kaiheila import Bot, Event
from nonebot.adapters.kaiheila.event import ChannelMessageEvent, PrivateMessageEvent

from nonebot_plugin_access_control.subject import SubjectExtractor
from nonebot_plugin_access_control.utils.superuser import is_superuser


class KaiheilaSubjectExtractor(SubjectExtractor[Bot, Event]):
    def get_adapter_shortname(self) -> str:
        return 'kaiheila'

    def get_adapter_fullname(self) -> str:
        return 'Kaiheila'

    def is_platform_supported(self, platform: str) -> bool:
        return platform == 'kaiheila'

    def extract(self, bot: Bot, event: Event):
        li = []

        user_id = getattr(event, "user_id", None)
        if user_id is not None:
            li.append(f"kaiheila:{user_id}")
            if is_superuser(bot, event):
                li.append("superuser")

        channel_id = getattr(event, "group_id", None)
        if channel_id is not None:
            li.append(f"kaiheila:c{channel_id}")

        if event.extra.guild_id is not None:
            li.append(f"kaiheila:g{event.extra.guild_id}")

        if isinstance(event, ChannelMessageEvent):
            li.append("kaiheila:channel")
        elif isinstance(event, PrivateMessageEvent):
            li.append("kaiheila:private")

        li.append("kaiheila")
        li.append("all")

        return li
