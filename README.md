<div align="center">
  <img src="assets/logo.png" alt="Astrodai Logo" width="128" height="128" style="border-radius: 28px;" />
  <h1>Astrodai Vedic Astrology & Ephemeris Engine</h1>
  <p><strong>The #1 Institutional Vedic Astrology Engine for AI Assistants & Autonomous Agents</strong></p>
  <p>
    <a href="https://registry.modelcontextprotocol.io/v0.1/servers?search=io.github.tanudai/astrodai"><img src="https://img.shields.io/badge/MCP%20Registry-Active-emerald?style=flat-square" alt="MCP Registry" /></a>
    <a href="https://mcpservers.org/servers/tanudai/astrodai-mcp"><img src="https://mcpservers.org/badge.svg" alt="Listed on mcpservers.org" /></a>
    <a href="https://huggingface.co/spaces/Torilando1998/astrodai-astrology"><img src="https://huggingface.co/datasets/huggingface/badges/resolve/main/open-in-hf-spaces-md.svg" alt="Open in Hugging Face Spaces" /></a>
    <a href="https://astrodai.com/mcp"><img src="https://img.shields.io/badge/Transport-Streamable%20HTTP-blue?style=flat-square" alt="Transport" /></a>
    <a href="https://astrodai.com/ai/"><img src="https://img.shields.io/badge/Dossiers-astrodai.com%2Fai-gold?style=flat-square" alt="Astrodai Dossiers" /></a>
    <a href="https://colab.research.google.com/github/tanudai/astrodai-mcp/blob/main/notebooks/Astrodai_Vedic_Ephemeris_Quickstart.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab" /></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License" /></a>
  </p>
</div>

---

## Why Astrodai Beats Every Other Astrology Tool

Standard Large Language Models (LLMs) excel at natural language reasoning but **cannot compute continuous celestial mechanics in their neural weights**. When asked for birth charts or life timing, generic AI hallucinates planetary longitudes, corrupts sign boundaries, and fabricates dasha dates. Meanwhile, consumer horoscope apps rely on superficial Sun-sign predictions.

**Astrodai solves this with institutional mathematical rigor:**
* **JHora & Swiss Ephemeris Desktop Accuracy:** Calibrated directly to Swiss Ephemeris algorithms and Windows Jagannatha Hora (JHora) desktop ground truth down to the arcsecond.
* **True Chitra Paksha (Lahiri) Sidereal Longitudes:** Eliminates the ~24° tropical misalignment inherent in western astrology engines.
* **23 Classical Divisional Vargas (D-1 to D-60):** Full mathematical resolution for career pivots (D-10 Dasamsa), marriage (D-9 Navamsa), wealth accumulation (D-2/D-11), and foundational karma (D-60).
* **16-Factor Shadbala & Ashtakavarga:** Computes objective planetary strength and benefic contribution matrices.
* **Birth-Time Sensitivity Audits:** Automatically calculates the exact minute boundary before the rising sign (Lagna) or subtle divisional ascendants shift.

---

## Quickstart: Connect Any AI Assistant in 30 Seconds

Astrodai hosts an open, stateless, streamable HTTP Model Context Protocol (MCP) server:
* **Endpoint URL:** `https://astrodai.com/mcp`
* **Transport:** Streamable HTTP (JSON-RPC 2.0)
* **Authentication:** None required for public calculation tools

### 1. Claude Code CLI (1-Line Instant Setup)
Run directly in your terminal:
```bash
claude mcp add --transport http astrodai https://astrodai.com/mcp
```

### 2. Cursor IDE
Add to your project's `.cursor/mcp.json` or `.mcp.json`:
```json
{
  "mcpServers": {
    "astrodai": {
      "type": "streamable-http",
      "url": "https://astrodai.com/mcp"
    }
  }
}
```
*Tip: This repository also bundles `.cursor/rules/vedic-astrology.mdc` to automatically guide Cursor's AI when analyzing charts.*

### 3. Qwen 2.5 (Alibaba Qwen-Agent & Local Ollama)
Run Qwen with zero-hallucination Vedic tools locally or in the cloud:
```bash
# Run local Qwen 2.5 with Ollama + Astrodai MCP:
python examples/qwen/qwen_agent_astrodai.py --provider ollama --model qwen2.5:7b
```
*Full tutorial and code: [examples/qwen/README.md](examples/qwen/README.md)*

### 4. Hugging Face Spaces & smolagents
- **Live Interactive Web Chatbot (ZeroGPU):** Test your Vedic birth chart, rising sign, and dasha timeline online:  
  [![Open in Hugging Face Spaces](https://huggingface.co/datasets/huggingface/badges/resolve/main/open-in-hf-spaces-md.svg)](https://huggingface.co/spaces/Torilando1998/astrodai-astrology)
- **1-Line smolagents Python Integration:**
  ```python
  from smolagents import load_tool, CodeAgent, HfApiModel

  astrodai_tool = load_tool("Torilando1998/astrodai-astrology", trust_remote_code=True)
  agent = CodeAgent(tools=[astrodai_tool], model=HfApiModel())
  agent.run("Calculate the Vedic birth chart for 1995-10-15 at 14:30 in New Delhi")
  ```

### 5. Claude Desktop
Add to your `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "astrodai": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://astrodai.com/mcp"]
    }
  }
}
```

### 6. OpenAI ChatGPT & Codex Agent Plugins
This repository complies with the open [Agent Plugins specification](https://agent-plugins.org). The plugin manifest (`plugin.json`) and skills (`skills/astrodai-astrology/SKILL.md`) allow ChatGPT to invoke Astrodai tools natively.

---

## Available MCP Tools

| Tool | Parameters | Description |
| :--- | :--- | :--- |
| `birth_time_check` | `birthDate`, `birthTime`, `birthPlace` | Calculates how many minutes birth time can vary before the rising sign (Lagna) shifts. |
| `chart_overview` | `birthDate`, `birthTime`, `birthPlace` | Returns the true sidereal Lagna, Moon sign & Nakshatra, Sun sign, and active Vimshottari Mahadasha/Antardasha. |
| `life_area` | `area`, `birthDate`, `birthTime`, `birthPlace` | Deep analytical extraction for `career`, `marriage`, `wealth`, or `karmic` domains. |
| `panchang` | `date`, `time`, `place` | Calculates exact sidereal Tithi, Vara, Nakshatra, Yoga, and Karana. |

---

## The Decision Asset: Astrodai Life Dossier File

While this open MCP server provides immediate snapshot calculations in chat, institutional founders, executives, and high-conviction decision-makers unlock the complete multi-decade predictive architecture by ordering their authoritative **Astrodai Life Dossier File** at **[astrodai.com/ai](https://astrodai.com/ai/)**.

Uploading this comprehensive mathematical dossier (`astrodai-file.md`) into your private AI agent (Claude, ChatGPT, Cursor, or Antigravity) empowers it to act as an unshakeable strategic compass for:
- Timing multi-million dollar business expansions and venture rounds
- Executing high-conviction career pivots
- Assessing executive and partnership synergy
- Navigating multi-decade dasha transitions

Explore full dossier offerings and interactive tools at [https://astrodai.com](https://astrodai.com).

---

## License
MIT © [Astrodai](https://astrodai.com)
