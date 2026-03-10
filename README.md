<h1 align="center" id="title">Grinning Cat Prompt Settings</h1>

<p id="description">This is a plugin for the <a href="https://github.com/matteocacciola/grinning-cat-core">Grinning Cat </a>Project which allows you to change the default prompt settings, also dynamically on websocket messages</p>
  
<h2>🧐 Plugins Settings</h2>

Here are the settings you can change with this plugin:

- Only local response: force cheshire cat to respond only with data previusly sent into the rabbit hole
- Disable memory: do not use context memory to generate the LLM response
- Prompt prefix: custom prompt prefix
- Prompt suffix: custom prompt suffix
- Reply message with no memory: if the LLM response is empty, use this message as reply
- Number of memory items: number of context items to insert in the prompt and set to LLM
- Number of history items: number of past messages to use as additional context for the LLM
- Context threshold: minimum score of context items to get retrieved from the vector database
- Enable OR Condition for Metadata Filter: enable to change from MUST (=AND) to SHOULD (=OR) the metadata filter on Vector Memory queries

<h2>🛠️ Installation:</h2>

<p>1. Clone this repo and copy it on cat plugins folder</p>
<p>2. Install from admin panel on the [Grinning Cat Web Admin](https://github.com/matteocacciola/grinning-cat-admin)</p>

<h2>😾 Dynamic settings change</h2>
You can change dynamically the settings of plugin adding a prompt_settings json on the websocket message. You can also send a tags to filter the query on QDRANT database, here an example:

```json
{
     "text": user_message,
     "prompt_settings": {
        "disable_memories": "True",
        "prompt_prefix": "You are an expert Python Developer",
     },
     "tags"{
         "category": "report"
     }
}
```

<h2>🛡️ License:</h2>
This project is licensed under the GNU GENERAL PUBLIC LICENSE
