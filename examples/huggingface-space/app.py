import json
import urllib.request
import urllib.error
import gradio as gr

ASTRODAI_MCP_URL = "https://astrodai.com/mcp"

def call_mcp(method: str, params: dict) -> dict:
    """Helper to query Astrodai's Streamable HTTP MCP Server."""
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
            "User-Agent": "Astrodai-HuggingFace-Space/1.0",
        },
        data=json.dumps(payload).encode("utf-8"),
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}: {e.reason}"}
    except Exception as e:
        return {"error": str(e)}

def resolve_place_token(city_name: str):
    """Lookup place token from Astrodai atlas."""
    if not city_name or not city_name.strip():
        return None, "Please provide a valid birth town (e.g. 'New Delhi, India' or 'San Francisco, USA')."
    
    res = call_mcp("tools/call", {
        "name": "find_birthplace",
        "arguments": {"place": city_name.strip()}
    })
    
    if "error" in res:
        return None, f"Connection error: {res['error']}"
    
    result = res.get("result", {})
    if result.get("isError"):
        msg = result.get("content", [{}])[0].get("text", "Error finding place.")
        return None, msg

    structured = result.get("structuredContent", {})
    candidates = structured.get("candidates", [])
    if not candidates:
        return None, f"No matching towns found for '{city_name}'. Try nearest major city."
    
    # Return first candidate token and label
    return candidates[0]["place_token"], candidates[0]["label"]

# ---------------------------------------------------------------------------
# Handlers for Gradio Tabs
# ---------------------------------------------------------------------------
def compute_chart_overview(birth_date: str, birth_time: str, birth_city: str):
    token, place_label_or_err = resolve_place_token(birth_city)
    if not token:
        return f"⚠️ **Error:** {place_label_or_err}", ""

    res = call_mcp("tools/call", {
        "name": "chart_overview",
        "arguments": {
            "birth_date": birth_date.strip(),
            "birth_time": birth_time.strip(),
            "place_token": token
        }
    })

    if "error" in res:
        return f"⚠️ **Server Error:** {res['error']}", ""

    result = res.get("result", {})
    content_text = ""
    if "content" in result and result["content"]:
        content_text = result["content"][0].get("text", "")

    structured = result.get("structuredContent", {})
    
    # Render rich markdown card
    md_output = f"""
### 🪐 Sidereal Kundli & Dasha Overview
* **Resolved Location:** {place_label_or_err}
* **Date & Time:** {birth_date} at {birth_time}

---
{content_text}
"""
    return md_output, json.dumps(structured, indent=2)

def compute_birth_sensitivity(birth_date: str, birth_time: str, birth_city: str):
    token, place_label_or_err = resolve_place_token(birth_city)
    if not token:
        return f"⚠️ **Error:** {place_label_or_err}", ""

    res = call_mcp("tools/call", {
        "name": "birth_time_check",
        "arguments": {
            "birth_date": birth_date.strip(),
            "birth_time": birth_time.strip(),
            "place_token": token
        }
    })

    if "error" in res:
        return f"⚠️ **Server Error:** {res['error']}", ""

    result = res.get("result", {})
    content_text = result.get("content", [{}])[0].get("text", "")
    structured = result.get("structuredContent", {})

    md_output = f"""
### ⏱️ Birth-Time Sensitivity Audit
* **Location:** {place_label_or_err}
* **Calculated against Swiss Ephemeris true horizon:**

---
{content_text}
"""
    return md_output, json.dumps(structured, indent=2)

def compute_life_area(birth_date: str, birth_time: str, birth_city: str, area: str):
    token, place_label_or_err = resolve_place_token(birth_city)
    if not token:
        return f"⚠️ **Error:** {place_label_or_err}", ""

    res = call_mcp("tools/call", {
        "name": "life_area",
        "arguments": {
            "birth_date": birth_date.strip(),
            "birth_time": birth_time.strip(),
            "place_token": token,
            "area": area.lower()
        }
    })

    if "error" in res:
        return f"⚠️ **Server Error:** {res['error']}", ""

    result = res.get("result", {})
    content_text = result.get("content", [{}])[0].get("text", "")
    structured = result.get("structuredContent", {})

    md_output = f"""
### 🏛️ Life Area Analysis: {area.title()}
* **Location:** {place_label_or_err}

---
{content_text}
"""
    return md_output, json.dumps(structured, indent=2)

def compute_panchang(date: str, time: str, city: str):
    token, place_label_or_err = resolve_place_token(city)
    if not token:
        return f"⚠️ **Error:** {place_label_or_err}", ""

    res = call_mcp("tools/call", {
        "name": "panchang",
        "arguments": {
            "date": date.strip(),
            "time": time.strip() if time else "12:00",
            "place_token": token
        }
    })

    if "error" in res:
        return f"⚠️ **Server Error:** {res['error']}", ""

    result = res.get("result", {})
    content_text = result.get("content", [{}])[0].get("text", "")
    structured = result.get("structuredContent", {})

    md_output = f"""
### 📅 Vedic Panchang
* **Location:** {place_label_or_err}
* **Date & Time:** {date} at {time or '12:00'}

---
{content_text}
"""
    return md_output, json.dumps(structured, indent=2)

# ---------------------------------------------------------------------------
# Custom CSS for Luxury Emerald & Gold Styling
# ---------------------------------------------------------------------------
custom_css = """
body, .gradio-container {
    background-color: #081714 !important;
    color: #e5e7eb !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
}
.header-box {
    text-align: center;
    padding: 24px 16px;
    background: linear-gradient(180deg, rgba(14,38,33,0.9) 0%, rgba(8,23,20,0.95) 100%);
    border: 1px solid rgba(212,175,55,0.25);
    border-radius: 16px;
    margin-bottom: 24px;
}
.header-title {
    color: #d4af37;
    font-size: 28px;
    font-weight: 700;
    margin-bottom: 8px;
}
.header-subtitle {
    color: #9ca3af;
    font-size: 15px;
    max-width: 720px;
    margin: 0 auto 14px auto;
}
.cta-banner {
    background: linear-gradient(135deg, rgba(212,175,55,0.15) 0%, rgba(14,38,33,0.6) 100%);
    border: 1px solid #d4af37;
    border-radius: 12px;
    padding: 16px 20px;
    margin-top: 24px;
    text-align: center;
}
.cta-button {
    display: inline-block;
    background: #d4af37 !important;
    color: #081714 !important;
    font-weight: 700 !important;
    padding: 10px 24px !important;
    border-radius: 8px !important;
    text-decoration: none !important;
    margin-top: 10px;
}
"""

with gr.Blocks(title="Astrodai Vedic Ephemeris & MCP Engine", css=custom_css) as demo:
    gr.HTML("""
    <div class="header-box">
        <div class="header-title">🪐 Astrodai Vedic Astrology & Ephemeris Engine</div>
        <div class="header-subtitle">
            The #1 Institutional Vedic Astrology Engine for AI Assistants (Claude, Cursor, ChatGPT, Qwen).
            Calibrated directly to Swiss Ephemeris algorithms and Jagannatha Hora (JHora) desktop ground truth.
        </div>
        <div>
            <span style="display:inline-block; margin:0 6px; padding:4px 10px; background:rgba(212,175,55,0.15); border:1px solid #d4af37; border-radius:20px; font-size:12px; color:#d4af37;">True Chitra Paksha (Lahiri)</span>
            <span style="display:inline-block; margin:0 6px; padding:4px 10px; background:rgba(16,185,129,0.15); border:1px solid #10b981; border-radius:20px; font-size:12px; color:#10b981;">Remote Streamable HTTP MCP</span>
            <span style="display:inline-block; margin:0 6px; padding:4px 10px; background:rgba(59,130,246,0.15); border:1px solid #3b82f6; border-radius:20px; font-size:12px; color:#93c5fd;">Zero Hallucination</span>
        </div>
    </div>
    """)

    with gr.Tabs():
        # Tab 1: Chart Overview
        with gr.TabItem("🔮 Kundli & Dasha Overview"):
            with gr.Row():
                with gr.Column(scale=1):
                    in_date = gr.Textbox(label="Birth Date (YYYY-MM-DD)", value="1995-10-15")
                    in_time = gr.Textbox(label="Birth Time (24-hour HH:MM)", value="14:30")
                    in_city = gr.Textbox(label="Birth Town / City", value="New Delhi, India", info="Town and region/country")
                    btn_overview = gr.Button("Calculate Kundli Overview", variant="primary")
                with gr.Column(scale=2):
                    out_overview = gr.Markdown(label="Astrodai Calculation")
                    with gr.Accordion("Raw MCP Structured Output", open=False):
                        out_json = gr.Code(language="json")
            btn_overview.click(compute_chart_overview, inputs=[in_date, in_time, in_city], outputs=[out_overview, out_json])

        # Tab 2: Sensitivity Check
        with gr.TabItem("⏱️ Birth-Time Sensitivity"):
            with gr.Row():
                with gr.Column(scale=1):
                    sens_date = gr.Textbox(label="Birth Date (YYYY-MM-DD)", value="1995-10-15")
                    sens_time = gr.Textbox(label="Birth Time (24-hour HH:MM)", value="14:30")
                    sens_city = gr.Textbox(label="Birth Town / City", value="New Delhi, India")
                    btn_sens = gr.Button("Audit Time Sensitivity", variant="primary")
                with gr.Column(scale=2):
                    out_sens = gr.Markdown()
                    with gr.Accordion("Raw MCP Structured Output", open=False):
                        out_sens_json = gr.Code(language="json")
            btn_sens.click(compute_birth_sensitivity, inputs=[sens_date, sens_time, sens_city], outputs=[out_sens, out_sens_json])

        # Tab 3: Life Area Deep Dive
        with gr.TabItem("🏛️ Life Area Analysis"):
            with gr.Row():
                with gr.Column(scale=1):
                    la_date = gr.Textbox(label="Birth Date (YYYY-MM-DD)", value="1995-10-15")
                    la_time = gr.Textbox(label="Birth Time (24-hour HH:MM)", value="14:30")
                    la_city = gr.Textbox(label="Birth Town / City", value="New Delhi, India")
                    la_area = gr.Dropdown(
                        label="Life Area",
                        choices=["career", "relationships", "wealth", "foreign_settlement", "home_property", "children", "education", "spiritual_growth"],
                        value="career"
                    )
                    btn_area = gr.Button("Analyze Life Domain", variant="primary")
                with gr.Column(scale=2):
                    out_area = gr.Markdown()
                    with gr.Accordion("Raw MCP Structured Output", open=False):
                        out_area_json = gr.Code(language="json")
            btn_area.click(compute_life_area, inputs=[la_date, la_time, la_city, la_area], outputs=[out_area, out_area_json])

        # Tab 4: Panchang
        with gr.TabItem("📅 Vedic Panchang"):
            with gr.Row():
                with gr.Column(scale=1):
                    p_date = gr.Textbox(label="Date (YYYY-MM-DD)", value="2026-11-04")
                    p_time = gr.Textbox(label="Local Time (HH:MM)", value="12:00")
                    p_city = gr.Textbox(label="Place / City", value="New Delhi, India")
                    btn_panchang = gr.Button("Calculate Panchang", variant="primary")
                with gr.Column(scale=2):
                    out_panchang = gr.Markdown()
                    with gr.Accordion("Raw MCP Structured Output", open=False):
                        out_panchang_json = gr.Code(language="json")
            btn_panchang.click(compute_panchang, inputs=[p_date, p_time, p_city], outputs=[out_panchang, out_panchang_json])

        # Tab 5: Connect AI Assistants (MCP)
        with gr.TabItem("🤖 Connect AI Assistants (MCP)"):
            gr.Markdown("""
### Connect Any AI Assistant to Astrodai MCP

You can connect **Claude**, **Cursor**, **ChatGPT**, or **Qwen** directly to Astrodai's remote streamable HTTP server:

#### 1. Claude Code CLI (1-Line Quickstart)
```bash
claude mcp add --transport http astrodai https://astrodai.com/mcp
```

#### 2. Cursor IDE (.cursor/mcp.json)
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

#### 3. Hugging Face smolagents (Python)
```python
from smolagents import ToolCallingAgent, HfApiModel
from mcp import ClientSession

# Connect to https://astrodai.com/mcp via HTTP transport
```

#### 4. Qwen 2.5 (Local or DashScope API)
See our complete [Qwen-Agent Python Integration](https://github.com/tanudai/astrodai-mcp/tree/main/examples/qwen) for 3-line plug-and-play code.
            """)

    gr.HTML("""
    <div class="cta-banner">
        <h3 style="color:#d4af37; margin:0 0 6px 0; font-size:20px;">Unlock Your Authoritative Astrodai Life Dossier File</h3>
        <p style="color:#cbd5e1; margin:0 0 10px 0; font-size:14px;">
            While this free MCP server provides snapshot answers, founders and high-conviction decision-makers unlock the complete multi-decade predictive architecture — all 23 divisional vargas (D-1 to D-60), 16 Shadbala strength matrices, and 120-year Vimshottari dasha dates in permanent AI-native Markdown.
        </p>
        <a href="https://astrodai.com/ai/?ref=hf-space" target="_blank" class="cta-button">Order Astrodai Master Dossier &rarr;</a>
    </div>
    """)

if __name__ == "__main__":
    demo.launch()
