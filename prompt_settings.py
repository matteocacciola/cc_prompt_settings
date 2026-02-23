from typing import Dict

from cat import hook, AgenticWorkflowOutput, UserMessage, RecallSettings


# Default prompt settings
lang = "Italian"
only_local = False
disable_memory = False
custom_prefix = ""
number_of_memory_items = 5
number_of_history_items = 5
threshold = 0.5
tags = {}
custom_suffix = ""
metadata_or_filter = False


def update_variables(settings: Dict, prompt_settings: Dict | None):
    global lang, only_local, disable_memory, custom_prefix, number_of_memory_items, number_of_history_items, threshold, tags, custom_suffix, metadata_or_filter
    lang = settings["language"]
    only_local = settings["only_local_responses"]
    disable_memory = settings["disable_memories"]
    custom_prefix = settings["prompt_prefix"]
    number_of_memory_items = settings["number_of_memory_items"]
    number_of_history_items = settings["number_of_history_items"]
    threshold = settings["threshold"]
    metadata_or_filter = settings["enable_OR_condition_for_metadata_filter"]

    if prompt_settings is not None:
        if "language" in prompt_settings:
            lang = prompt_settings["language"]
        if "only_local_responses" in prompt_settings:
            only_local = prompt_settings["only_local_responses"]
        if "disable_memories" in prompt_settings:
            disable_memory = prompt_settings["disable_memories"]
        if "prompt_prefix" in prompt_settings:
            custom_prefix = prompt_settings["prompt_prefix"]
        if "prompt_suffix" in prompt_settings:
            custom_suffix = prompt_settings["prompt_suffix"]
        if "number_of_memory_items" in prompt_settings:
            number_of_memory_items = prompt_settings["number_of_memory_items"]
        if "number_of_history_items" in prompt_settings:
            number_of_history_items = prompt_settings["number_of_history_items"]
        if "threshold" in prompt_settings:
            threshold = prompt_settings["threshold"]


@hook(priority=10)
def before_cat_reads_message(user_message: UserMessage, cat):
    global tags
    settings = cat.mad_hatter.get_plugin().load_settings()
    prompt_settings = None
    tags = {}
    if "prompt_settings" in user_message:
        prompt_settings = user_message.prompt_settings
    if "tags" in user_message:
        tags = user_message.tags
    update_variables(settings, prompt_settings)
    return user_message


@hook(priority=10)
def agent_prompt_prefix(prefix: str, cat) -> str:
    global custom_prefix
    prefix = custom_prefix
    return prefix


@hook(priority=10)
def agent_prompt_suffix(prompt_suffix: str, cat) -> str:
    global lang
    if lang == "English":
        prompt_suffix = prompt_suffix_en()
    if lang == "Italian":
        prompt_suffix = prompt_suffix_it()
    return prompt_suffix


def prompt_suffix_en() -> str:
    global disable_memory
    if disable_memory:
        prompt_suffix = ""

    else:
        prompt_suffix = (custom_suffix +
 """
 # Context
 {context}
 """
        )
    return prompt_suffix


def prompt_suffix_it() -> str:
    global disable_memory
    if disable_memory:
        prompt_suffix = ""
    else:
        prompt_suffix = """
# Contesto
{context}
"""
    return prompt_suffix


@hook(priority=1)
def before_cat_recalls_memories(config: RecallSettings, cat) -> RecallSettings:
    global disable_memory, number_of_memory_items, number_of_history_items, tags
    if disable_memory:
        custom_k = 1
        config.threshold = 1
    else:
        custom_k = number_of_memory_items
    config.k = custom_k
    config.threshold = threshold
    config.latest_n_history = number_of_history_items
    if tags:
        config.metadata |= tags

    return config


@hook(priority=1)
def agent_fast_reply(cat) -> AgenticWorkflowOutput | None:
    global lang, only_local
    if not only_local:
        return None

    num_memories = len(cat.working_memory.context_memories)
    if num_memories > 0:
        return None

    if lang == "Italian":
        return AgenticWorkflowOutput(output="Scusami, non ho informazioni su questo tema.")

    return AgenticWorkflowOutput(output="Sorry, I have no information on this topic.")


@hook
def after_cat_recalls_memories(config: RecallSettings, cat) -> None:
    global metadata_or_filter, threshold, number_of_memory_items

    if not metadata_or_filter or not (tags_ := getattr(cat.working_memory.user_message, "tags")):
        return

    config.metadata |= tags_
    cat.recall_context_to_working_memory(config)
