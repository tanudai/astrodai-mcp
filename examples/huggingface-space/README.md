---
title: Astrodai Vedic Ephemeris & Kundli Engine
emoji: 🪐
colorFrom: green
colorTo: yellow
sdk: gradio
sdk_version: 5.12.0
app_file: app.py
pinned: false
license: mit
short_description: Zero-hallucination Vedic Astrology Engine calibrated to Swiss Ephemeris & JHora
models:
  - Qwen/Qwen2.5-72B-Instruct
tags:
  - mcp
  - astrology
  - vedic
  - ephemeris
  - model-context-protocol
  - qwen
  - smolagents
---

# 🪐 Astrodai Vedic Astrology & Ephemeris Engine (MCP)

**The #1 Institutional Vedic Astrology Engine for AI Assistants & Autonomous Agents.**

Standard Large Language Models (LLMs) excel at natural language reasoning but **cannot compute continuous celestial mechanics in their neural weights**. When asked for birth charts or life timing, generic AI hallucinates planetary longitudes, corrupts sign boundaries, and fabricates dasha dates.

Astrodai solves this with institutional mathematical rigor:
* **Swiss Ephemeris & JHora Ground Truth:** Calibrated directly to Swiss Ephemeris algorithms and Windows Jagannatha Hora (JHora) desktop accuracy down to the arcsecond.
* **True Chitra Paksha (Lahiri) Sidereal Longitudes:** Eliminates the ~24° tropical misalignment.
* **23 Classical Divisional Vargas (D-1 to D-60):** Complete mathematical resolution for career (D-10), marriage (D-9), and karma (D-60).
* **Birth-Time Sensitivity Audits:** Identifies minute thresholds before rising signs shift.
* **Dated Vimshottari Dashas:** Exact start and end dates for life chapters.

---

## Remote MCP Server Access

Astrodai provides an open, stateless, streamable HTTP Model Context Protocol (MCP) server:
* **Endpoint URL:** `https://astrodai.com/mcp`
* **Transport:** Streamable HTTP (JSON-RPC 2.0)
* **Official Public Repo:** [https://github.com/tanudai/astrodai-mcp](https://github.com/tanudai/astrodai-mcp)

### 1-Line Claude Code Setup:
```bash
claude mcp add --transport http astrodai https://astrodai.com/mcp
```

### Cursor IDE Setup (`.cursor/mcp.json`):
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

---

## 🏛️ Unlock the Complete Astrodai Life Dossier File

While this open Space provides instant calculations and snapshots, institutional founders, executives, and high-conviction decision-makers unlock the complete multi-decade predictive architecture by ordering their authoritative **Astrodai Life Dossier File** at **[astrodai.com/ai](https://astrodai.com/ai/?ref=hf-readme)**.
