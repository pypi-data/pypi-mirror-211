import json
from openplugin.interfaces.plugin_selector import Message, Plugin, Config, ToolSelectorConfig, LLM


def run_plugin_selector(inp_json, binding_name):
    if type(inp_json) == str:
        inp_json = json.loads(inp_json)
    messages = [Message(**m) for m in inp_json["messages"]]
    plugins = [Plugin(**p) for p in inp_json["plugins"]]
    config = Config(**inp_json["config"])
    tool_selector_config = ToolSelectorConfig(**inp_json["tool_selector_config"])
    llm = LLM(**inp_json["llm"])
    if binding_name == "imprompt":
        from openplugin.api.imprompt import run_plugin
        response = run_plugin(messages, tool_selector_config, plugins, config, llm)
        return response.json()
    elif binding_name == "langchain":
        from openplugin.api.langchain import run_plugin
        response = run_plugin(messages, tool_selector_config, plugins, config, llm)
        return response.json()
    raise Exception("Unknown binding name: " + binding_name)
