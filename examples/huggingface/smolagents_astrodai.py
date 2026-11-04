#!/usr/bin/env python3
"""
Astrodai + Hugging Face smolagents Integration
==============================================
Connects Hugging Face's official `smolagents` framework to the Astrodai
Model Context Protocol (MCP) server at https://astrodai.com/mcp.

Requirements:
    pip install smolagents requests

Usage:
    export HF_TOKEN="your-huggingface-token"
    python smolagents_astrodai.py
"""

import json
import urllib.request
from typing import Optional
from smolagents import CodeAgent, HfApiModel, tool

ASTRODAI_MCP_URL = "https://astrodai.com/mcp"

def _call_astrodai_mcp(tool_name: str, arguments: dict) -> str:
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments
        }
    }
    req = urllib.request.Request(
        ASTRODAI_MCP_URL,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "User-Agent": "Astrodai-smolagents-Client/1.0"
        },
        data=json.dumps(payload).encode("utf-8")
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        result = data.get("result", {})
        if "content" in result and result["content"]:
            return result["content"][0].get("text", "")
        return json.dumps(result)


@tool
def find_birthplace(place: str) -> str:
    """Look up a town in the Astrodai atlas.
    
    Args:
        place: Town name, optionally followed by country/region (e.g. 'New Delhi, India').
    """
    return _call_astrodai_mcp("find_birthplace", {"place": place})


@tool
def chart_overview(birth_date: str, birth_time: str, place_token: str) -> str:
    """Calculates true sidereal rising sign, Moon sign, nakshatra, Sun sign, and active Vimshottari Mahadasha.
    
    Args:
        birth_date: Birth date formatted as YYYY-MM-DD.
        birth_time: Local birth time as recorded (24-hour HH:MM).
        place_token: The place_token string returned from find_birthplace.
    """
    return _call_astrodai_mcp("chart_overview", {
        "birth_date": birth_date,
        "birth_time": birth_time,
        "place_token": place_token
    })


@tool
def birth_time_check(birth_date: str, birth_time: str, place_token: str) -> str:
    """Audits birth-time sensitivity, checking how many minutes before rising sign (Lagna) or D9/D10 divisional signs shift.
    
    Args:
        birth_date: Birth date formatted as YYYY-MM-DD.
        birth_time: Local birth time as recorded (24-hour HH:MM).
        place_token: The place_token string returned from find_birthplace.
    """
    return _call_astrodai_mcp("birth_time_check", {
        "birth_date": birth_date,
        "birth_time": birth_time,
        "place_token": place_token
    })


@tool
def life_area_analysis(area: str, birth_date: str, birth_time: str, place_token: str) -> str:
    """Extracts verified astrological house strength and planetary guidance for a specific life area.
    
    Args:
        area: One of: 'career', 'relationships', 'wealth', 'foreign_settlement', 'home_property', 'children', 'education', 'spiritual_growth'.
        birth_date: Birth date formatted as YYYY-MM-DD.
        birth_time: Local birth time (HH:MM).
        place_token: The place_token string returned from find_birthplace.
    """
    return _call_astrodai_mcp("life_area", {
        "area": area,
        "birth_date": birth_date,
        "birth_time": birth_time,
        "place_token": place_token
    })


def main():
    print("Initializing Hugging Face smolagent with Astrodai Vedic Tools...")
    
    # Initialize model (Qwen 2.5 72B Instruct on Hugging Face Hub)
    model = HfApiModel(model_id="Qwen/Qwen2.5-72B-Instruct")
    
    agent = CodeAgent(
        tools=[find_birthplace, chart_overview, birth_time_check, life_area_analysis],
        model=model,
        additional_authorized_imports=["json"]
    )
    
    query = (
        "Analyze the Vedic birth chart for a person born on 15 October 1995 at 14:30 in New Delhi, India. "
        "Find their birthplace token, calculate their rising sign and current dasha, and check how sensitive "
        "their chart is to their recorded birth time."
    )
    
    print(f"\nRunning Query: {query}\n")
    result = agent.run(query)
    print("\nResult:\n", result)


if __name__ == "__main__":
    main()
