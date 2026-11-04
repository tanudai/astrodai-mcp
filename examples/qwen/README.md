# Qwen 2.5 + Astrodai Vedic Astrology & MCP Integration

Connect Alibaba's **Qwen 2.5** (including Qwen 2.5-Coder and Qwen 2.5-72B) directly to the **Astrodai Model Context Protocol (MCP)** server.

Standard LLMs cannot calculate spherical astronomy or planetary coordinates in their weights. By binding Qwen 2.5 to Astrodai's streamable HTTP endpoint (`https://astrodai.com/mcp`), Qwen delegates all planetary longitudes, house cusps, and Vimshottari dasha calculations directly to the Swiss Ephemeris engine calibrated to Jagannatha Hora (JHora).

---

## Architecture Overview

```
                      ┌─────────────────────────────────────────┐
                      │    User Query (Natural Language)        │
                      └────────────────────┬────────────────────┘
                                           │
                                           ▼
                      ┌─────────────────────────────────────────┐
                      │    Qwen 2.5 / Qwen-Agent (LLM)          │
                      │  (Ollama / DashScope / vLLM / HF)       │
                      └────────────────────┬────────────────────┘
                                           │ Tool Calling
                        JSON-RPC 2.0 (HTTP)│ (place_token, birth details)
                                           ▼
                      ┌─────────────────────────────────────────┐
                      │    Astrodai Remote MCP Server           │
                      │    https://astrodai.com/mcp             │
                      │  (Swiss Ephemeris + JHora Desktop Sync) │
                      └────────────────────┬────────────────────┘
                                           │ Verified Sidereal Math
                                           ▼
                      ┌─────────────────────────────────────────┐
                      │    Zero-Hallucination Consultation      │
                      │  (Lagna, Nakshatra, Dasha Dates, Vargas)│
                      └─────────────────────────────────────────┘
```

---

## 🚀 Quickstart: Run with Local Ollama

Run Qwen 2.5 100% locally on your computer with Ollama:

### Step 1: Install Ollama & Pull Qwen 2.5
```bash
# Pull any Qwen model (7B, 14B, or 32B recommended)
ollama pull qwen2.5:7b
```

### Step 2: Install Python dependencies
```bash
pip install openai requests
```

### Step 3: Run the Astrodai Agent
```bash
python examples/qwen/qwen_agent_astrodai.py --provider ollama --model qwen2.5:7b
```

Sample query:
> *"I was born on 15 October 1995 at 14:30 in New Delhi, India. What is my rising sign, Moon nakshatra, and what life chapter (dasha) am I currently running?"*

---

## ☁️ Run with Alibaba Cloud DashScope API

If you use Alibaba Cloud DashScope:

```bash
export DASHSCOPE_API_KEY="your-dashscope-api-key"

python examples/qwen/qwen_agent_astrodai.py \
  --provider dashscope \
  --model qwen-plus
```

---

## 💻 3-Line Python Integration

If you already have a Python script or agent framework, connect to Astrodai MCP directly:

```python
import urllib.request, json

def query_astrodai(method: str, params: dict):
    req = urllib.request.Request(
        "https://astrodai.com/mcp",
        headers={"Content-Type": "application/json", "Accept": "application/json, text/event-stream"},
        data=json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

# 1. Resolve town token
town = query_astrodai("tools/call", {"name": "find_birthplace", "arguments": {"place": "New Delhi, India"}})
token = town["result"]["structuredContent"]["candidates"][0]["place_token"]

# 2. Get verified chart & dasha overview
chart = query_astrodai("tools/call", {
    "name": "chart_overview",
    "arguments": {"birth_date": "1995-10-15", "birth_time": "14:30", "place_token": token}
})

print(chart["result"]["content"][0]["text"])
```

---

## 🏛️ Upgrading to the Full Master Dossier

While this open MCP server provides quick snapshots, enterprise founders, venture investors, and high-conviction decision-makers unlock the complete multi-decade predictive architecture by ordering their authoritative **Astrodai Life Dossier File** at **[astrodai.com/ai](https://astrodai.com/ai/)**.

Uploading this comprehensive mathematical dossier (`astrodai-file.md`) into your private AI agent gives Qwen all 23 divisional vargas, 16 Shadbala factors, and dated 120-year Vimshottari timelines offline with zero external server dependencies.
