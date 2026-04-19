# WeatherAid Agent

WeatherAid is a local MCP-based weather assistant project that connects an LLM agent to custom MCP tools.

The project currently includes:
- A weather MCP server that fetches live weather data from Open-Meteo
- A write MCP server for file write and append actions
- A command-line chat client that uses LangGraph ReAct agent flow

## Repository Structure

- [Agent/WeatherAid/client.py](Agent/WeatherAid/client.py): CLI chat entrypoint
- [Agent/WeatherAid/weather_server.py](Agent/WeatherAid/weather_server.py): weather MCP tools
- [Agent/WeatherAid/write_server.py](Agent/WeatherAid/write_server.py): write MCP tools
- [Agent/WeatherAid/servers_config.json](Agent/WeatherAid/servers_config.json): MCP server config for the client
- [Agent/WeatherAid/api_server.py](Agent/WeatherAid/api_server.py): FastAPI integration draft
- [Agent/WeatherAid/requirements.txt](Agent/WeatherAid/requirements.txt): Python dependencies
- [Agent/WeatherAid/.gitignore](Agent/WeatherAid/.gitignore): ignore rules for envs, secrets, and local artifacts

## Features

- Query weather by city via MCP tool
- Return weather condition and temperature in Celsius
- Add seasonal weather tips to weather responses
- Write or append content to local files through MCP tools
- Switch LLM providers by changing one model string in [Agent/WeatherAid/client.py](Agent/WeatherAid/client.py)

## Prerequisites

- Python 3.11+
- pip
- macOS or Linux shell
- API key for selected provider:
- Anthropic for Claude models
- Google AI for Gemini models

## Setup

1. Go to project folder

    cd /Users/xxx/WeatherAid

2. Create virtual environment

    python3.11 -m venv venv

3. Activate environment

    source venv/bin/activate

4. Install dependencies

    pip install -r requirements.txt

## Environment Variables

Do not store real keys in source files.

Set API keys in your shell profile, for example in ~/.zshrc:

    export ANTHROPIC_API_KEY="your_key_here"
    export GOOGLE_API_KEY="your_key_here"

Reload shell config:

    source ~/.zshrc

Verify variable exists without printing full key:

    if [ -n "$ANTHROPIC_API_KEY" ]; then echo "ANTHROPIC_API_KEY set"; else echo "ANTHROPIC_API_KEY missing"; fi
    if [ -n "$GOOGLE_API_KEY" ]; then echo "GOOGLE_API_KEY set"; else echo "GOOGLE_API_KEY missing"; fi

## Run WeatherAid CLI

Start the client:

    python3 client.py

Usage:
- Type a prompt such as:
- weather in Tokyo
- give me weather in Seattle
- Type exit or quit to stop

## Model Configuration

Model is selected in [/WeatherAid/client.py](/WeatherAid/client.py).

Example Anthropic model format:
- anthropic:model_id

Example Google model format:
- google_genai:model_id

If model errors occur:
- not_found_error: model id is not available for your account
- authentication errors: missing or wrong API key
- quota errors: provider usage limits exceeded

## MCP Server Configuration

[WeatherAid/servers_config.json](WeatherAid/servers_config.json) defines MCP servers used by the client:
- weather server runs [WeatherAid/weather_server.py](WeatherAid/weather_server.py)
- write server runs [WeatherAid/write_server.py](WeatherAid/write_server.py)

Current transport mode:
- stdio

## FastAPI Status

[WeatherAid/api_server.py](WeatherAid/api_server.py) is currently a draft and needs cleanup before production use. The CLI flow via [Agent/WeatherAid/client.py](Agent/WeatherAid/client.py) is the main tested path.

## Security Notes

- Never hardcode API keys in Python or JSON files
- Keep keys in shell environment variables or ignored env files
- Rotate keys if they were ever pasted in chat, logs, screenshots, or terminal output
- Check ignored patterns in [WeatherAid/.gitignore](WeatherAid/.gitignore) before pushing to GitHub

## GitHub Push Checklist

1. Confirm repository has no secrets

    git grep -nE "AIza|sk-ant-|ANTHROPIC_API_KEY|GOOGLE_API_KEY|Authorization: Bearer|x-api-key"

2. Confirm ignored files

    git status --ignored

3. Push

    git push -u origin main

## Troubleshooting

- Module not found:
- Re-activate venv and reinstall requirements

- MCP connection closed:
- Ensure [WeatherAid/weather_server.py](WeatherAid/weather_server.py) and [WeatherAid/write_server.py](WeatherAid/write_server.py) run with mcp.run in main block

- JSON decode error:
- Validate [WeatherAid/servers_config.json](WeatherAid/servers_config.json) contains valid JSON with no comments

- Anthropic auth error:
- Ensure ANTHROPIC_API_KEY is present in current shell session

- Gemini quota error:
- Check provider quota and billing status
