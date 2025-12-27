from pydantic import BaseModel
from cat import plugin
from enum import Enum


class AvailbleLanguages(Enum):
    it = "Italian"
    en = "English"


# Plugin settings
class PluginSettings(BaseModel):
    language: AvailbleLanguages = AvailbleLanguages.it
    only_local_responses: bool = False
    disable_memories: bool = False
    prompt_prefix: str = ""
    prompt_suffix: str = ""
    number_of_memory_items: int = 5
    number_of_history_items: int = 5
    threshold: float = 0.5
    enable_OR_condition_for_metadata_filter: bool = False


# hook to give the cat settings
@plugin
def settings_schema():
    return PluginSettings.schema()
