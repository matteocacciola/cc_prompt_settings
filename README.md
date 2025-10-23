<h1 align="center" id="title">Cheshire Cat Prompt Settings</h1>

<p id="description">This is a plugin for the <a href="https://github.com/cheshire-cat-ai/core">Cheshire Cat </a>Project which allows you to change the default prompt settings, also dynamically on websocket messages</p>
  
<h2>🧐 Plugins Settings</h2>

Here're the settings you can change with this plugin:

- Language: set the language of the prompt sent to LLM (Italian or English)
- Only local response: force cheshire cat to respond only with data previusly sent into the rabbit hole
- Prompt prefix: custom prompt prefix
- Prompt suffix: custom prompt suffix
- Disable declarative memory: not use declarative memory to generate the LLM response
- Disable tools: disable usage of tools
- Number of declarative items: number of declarative items to insert in the prompt and set to LLM
- Declarative threshold: minimum score of declarative items to get retrieved from vector database
- Enable OR Condition for Metadata Filter: enable to change from MUST (=AND) to SHOULD (=OR) the metadata filter on Qrdant queries

<h2>🛠️ Installation:</h2>

<p>1. Clone this repo and copy it on cat plugins folder</p>
<p>2. Install from admin panel on the [Cheshire Cat Web Admin](https://github.com/matteocacciola/cheshirecat-admin)</p>

<h2>😾 Dynamic settings change</h2>
You can change dynamically the settings of plugin adding a prompt_settings json on the websocket message. You can also send a tags to filter the query on QDRANT database, here an example:

```json
{
     "text": user_message,
     "prompt_settings": {
        "language": "Italian",
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
