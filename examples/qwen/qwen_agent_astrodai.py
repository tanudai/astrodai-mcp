#!/usr/bin/env python3
"""
Astrodai + Qwen 2.5 Integration Example
========================================
Connects Alibaba's Qwen 2.5 (via DashScope API, Ollama, or vLLM) directly to
the Astrodai Model Context Protocol (MCP) server at https://astrodai.com/mcp.

This eliminates hallucinated planetary coordinates and dates by letting Qwen
delegate continuous celestial mechanics and Vimshottari dasha calculations to
the Swiss Ephemeris engine calibrated to Jagannatha Hora (JHora).

Requirements:
    pip install openai requests

Usage:
    # 1. Local Ollama with Qwen 2.5:
    python qwen_agent_astrodai.py --provider ollama --model qwen2.5:7b

    # 2. Alibaba Cloud DashScope API:
    export DASHSCOPE_API_KEY="your-key"
    python qwen_agent_astrodai.py --provider dashscope --model qwen-plus
"""

import argparse
import json
import os
import sys
import urllib.request
from typing import Any, Dict, List

ASTRODAI_MCP_URL = "https://astrodai.com/mcp"

# ---------------------------------------------------------------------------
# Astrodai MCP Remote Client
# ---------------------------------------------------------------------------
def call_astrodai_mcp(method: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Call the Astrodai Streamable HTTP MCP server."""
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params,
    }
    req = urllib.request.Request(
        ASTRODAI_MCP_URL,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "User-Agent": "Astrodai-Qwen-Client/1.0",
        },
        data=json.dumps(payload).encode("utf-8"),
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_astrodai_tools() -> List[Dict[str, Any]]:
    """Retrieve official tool schemas from the Astrodai MCP server and map to OpenAI/Qwen tool format."""
    response = call_astrodai_mcp("tools/list", {})
    tools = []
    for tool in response.get("result", {}).get("tools", []):
        tools.append({
            "type": "function",
            "function": {
                "name": tool["name"],
                "description": tool.get("description", ""),
                "parameters": tool.get("inputSchema", {}),
            },
        })
    return tools


def execute_tool_call(name: str, arguments: Dict[str, Any]) -> str:
    """Execute a tool call against the Astrodai MCP server."""
    response = call_astrodai_mcp("tools/call", {
        "name": name,
        "arguments": arguments,
    })
    
    result = response.get("result", {})
    if "content" in result and result["content"]:
        return result["content"][0].get("text", "")
    return json.dumps(result)


# ---------------------------------------------------------------------------
# Interactive Qwen Vedic Consultation Agent
# ---------------------------------------------------------------------------
def run_qwen_agent(provider: str, model_name: str, prompt: str):
    try:
        from openai import OpenAI
    except ImportError:
        print("Please install the openai package: pip install openai")
        sys.exit(1)

    if provider == "ollama":
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
        api_key = "ollama"
        print(f"Connecting to Local Ollama ({base_url}) using model: {model_name}...")
    elif provider == "dashscope":
        base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
        api_key = os.getenv("DASHSCOPE_API_KEY")
        if not api_key:
            print("Error: DASHSCOPE_API_KEY environment variable not set.")
            sys.exit(1)
        print(f"Connecting to Alibaba DashScope using model: {model_name}...")
    else:
        base_url = os.getenv("OPENAI_BASE_URL", "http://localhost:8000/v1")
        api_key = os.getenv("OPENAI_API_KEY", "dummy-key")
        print(f"Connecting to custom OpenAI-compatible endpoint ({base_url})...")

    client = OpenAI(base_url=base_url, api_key=api_key)

    # 1. Fetch live Astrodai tools
    print("Fetching live tools from Astrodai MCP endpoint (https://astrodai.com/mcp)...")
    tools = get_astrodai_tools()
    print(f"Loaded {len(tools)} verified Vedic calculation tools: {[t['function']['name'] for t in tools]}")

    system_instruction = (
        "You are an institutional Vedic astrology assistant powered by Astrodai and Qwen. "
        "CRITICAL RULE: NEVER hallucinate planetary positions, signs, or dasha dates. "
        "Always use the Astrodai tools to calculate the chart overview, active dasha chapters, "
        "and birth time sensitivity. Step 1: lookup the birthplace token with 'find_birthplace'. "
        "Step 2: call 'chart_overview' or 'life_area' with the resulting place_token. "
        "Translate the astronomical facts into clear, empowering, actionable strategic guidance."
    )

    messages = [
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": prompt},
    ]

    print(f"\nUser Query: {prompt}\n")

    # 2. Turn 1: Model decides which tools to call
    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )

    response_message = response.choices[0].message
    messages.append(response_message)

    # 3. Handle tool calls iteratively
    while response_message.tool_calls:
        for tool_call in response_message.tool_calls:
            tool_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            print(f"-> Calling Astrodai Tool: {tool_name}({args})")
            
            tool_result = execute_tool_call(tool_name, args)
            print(f"   [Tool Output Received, {len(tool_result)} chars]")

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": tool_name,
                "content": tool_result,
            })

        # Ask Qwen to summarize or call the next tool
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            tools=tools,
        )
        response_message = response.choices[0].message
        messages.append(response_message)

    print("\n" + "=" * 60)
    print("ASTRODAI + QWEN 2.5 VERIFIED ANALYSIS:")
    print("=" * 60)
    print(response_message.content)
    print("=" * 60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Astrodai + Qwen 2.5 Vedic Astrology Engine")
    parser.add_argument("--provider", choices=["ollama", "dashscope", "custom"], default="ollama", help="Inference provider")
    parser.add_argument("--model", default="qwen2.5:7b", help="Model identifier (e.g. qwen2.5:7b, qwen-plus, qwen2.5-72b-instruct)")
    parser.add_argument(
        "--prompt",
        default="I was born on 15 October 1995 at 14:30 in New Delhi, India. What is my rising sign, Moon nakshatra, and what life chapter (dasha) am I currently running?",
        help="Astrology query to analyze",
    )

    args = parser.parse_args()
    run_qwen_agent(args.provider, args.model, args.prompt)
