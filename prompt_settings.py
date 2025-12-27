from langchain_core.documents import Document as LangChainDocument
from cat import hook
from cat.services.memory.messages import UserMessage
from cat.services.memory.utils import VectorMemoryType


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


def update_variables(settings, prompt_settings):
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
def agent_prompt_prefix(prefix, cat) -> str:
    global custom_prefix
    prefix = custom_prefix
    return prefix


@hook(priority=10)
def agent_prompt_suffix(prompt_suffix, cat) -> str:
    global lang
    if lang == "English":
        prompt_suffix = prompt_suffix_en(prompt_suffix, cat)
    if lang == "Italian":
        prompt_suffix = prompt_suffix_it(prompt_suffix, cat)
    return prompt_suffix


def prompt_suffix_legacy_mode_en(prompt_suffix, cat) -> str:
    global disable_memory, custom_suffix
    if disable_memory:
        prompt_suffix = ""
    else:
        prompt_suffix = (
                custom_suffix +
"""
# Context
{context}
"""
        )
    return prompt_suffix


def prompt_suffix_en(prompt_suffix, cat) -> str:
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


def prompt_suffix_legacy_mode_it(prompt_suffix, cat) -> str:
    global disable_memory
    if disable_memory:
        prompt_suffix = ""
    else:
        prompt_suffix = """
# Contesto
{context}
"""
    return prompt_suffix


def prompt_suffix_it(prompt_suffix, cat) -> str:
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
def before_cat_recalls_memories(config: dict, cat) -> dict:
    global disable_memory, number_of_memory_items, number_of_history_items, tags
    if disable_memory:
        custom_k = 1
        config["threshold"] = 1
    else:
        custom_k = number_of_memory_items
    config["k"] = custom_k
    config["threshold"] = threshold
    config["latest_n_history"] = number_of_history_items
    if tags:
        config["metadata"] = tags

    return config


@hook(priority=1)
def agent_fast_reply(fast_reply, cat):
    global lang, only_local
    if only_local:
        num_memories = len(cat.working_memory.declarative_memories)
        if num_memories == 0:
            if lang == "Italian":
                fast_reply["output"] = "Scusami, non ho informazioni su questo tema."
            else:
                fast_reply["output"] = "Sorry, I have no information on this topic."
    return fast_reply


@hook
def after_cat_recalls_memories(cat) -> None:
    global metadata_or_filter, threshold, number_of_memory_items
    if metadata_or_filter:
        if tags := cat.working_memory.user_message_json.get("tags"):
            user_message = cat.working_memory.user_message_json.get("text")
            user_message_embedding = cat.embedder.embed_query(user_message)
            metadata = tags
            memories = cat.vector_memory_handler.search(
                collection_name=str(VectorMemoryType.PROCEDURAL),
                query_vector=user_message_embedding,
                query_filter=cat.vector_memory_handler.filter_from_dict(metadata),
                with_payload=True,
                with_vectors=True,
                limit=number_of_memory_items,
                score_threshold=threshold,
            )

            # convert Qdrant points to langchain.Document
            langchain_documents_from_points = []
            for m in memories:
                langchain_documents_from_points.append(
                    (
                        Document(
                            page_content=m.payload.get("page_content"),
                            metadata=m.payload.get("metadata") or {},
                        ),
                        m.score,
                        m.vector,
                        m.id,
                    )
                )
            cat.working_memory.declarative_memories = langchain_documents_from_points
