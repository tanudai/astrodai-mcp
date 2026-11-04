# Hugging Face + Astrodai Vedic Ephemeris & MCP Integration

Deploy and run institutional Vedic astrology tools within the Hugging Face open-source ecosystem.

---

## 1. Hugging Face Spaces (Live Gradio Demo)

We provide a complete, interactive Gradio 5 application ready to deploy to Hugging Face Spaces in `examples/huggingface-space/`:

* **Live Features:**
  - 🔮 **Instant Kundli & Dasha Overview:** Sidereal Lagna, Moon sign & Nakshatra, Sun sign, and active Vimshottari Mahadasha/Antardasha.
  - ⏱️ **Birth-Time Sensitivity Audit:** Minute threshold before ascendant or subtle divisionals (D9/D10) shift.
  - 🏛️ **Domain Analysis:** Career, Wealth, Relationships, Foreign Settlement.
  - 📅 **Vedic Panchang:** Tithi, Vara, Nakshatra, Yoga, Karana.
* **Colors & Aesthetic:** Styled in deep emerald `#0e2621` with gold `#d4af37` accents matching Astrodai's brand.

### How to Deploy Your Own Space on Hugging Face (2 minutes)
1. Go to [huggingface.co/new-space](https://huggingface.co/new-space).
2. Name your Space (e.g. `astrodai-vedic-engine`), choose **Gradio**, and set Visibility to **Public**.
3. Clone your new space repo and copy files:
   ```bash
   git clone https://huggingface.co/spaces/<your-username>/astrodai-vedic-engine
   cp -r examples/huggingface-space/* astrodai-vedic-engine/
   cd astrodai-vedic-engine
   git add .
   git commit -m "Deploy Astrodai Vedic Engine Gradio Space"
   git push
   ```
4. Hugging Face will automatically build and launch the space in ~60 seconds!

---

## 2. Hugging Face `smolagents` Integration

Hugging Face's official agent framework `smolagents` allows autonomous code agents to call Astrodai MCP tools directly.

### Installation
```bash
pip install smolagents requests
```

### Running the Example
```bash
export HF_TOKEN="your-huggingface-token"
python examples/huggingface/smolagents_astrodai.py
```

This pairs Hugging Face's `Qwen/Qwen2.5-72B-Instruct` model with Astrodai's verified Swiss Ephemeris tools, ensuring the agent executes zero-hallucination astrological reasoning.

---

## 🏛️ Astrodai Master Dossier File

For complete 23-varga divisional charts, 16 Shadbala strength matrices, and 120-year Vimshottari dasha dates in permanent AI-native Markdown, visit **[astrodai.com/ai](https://astrodai.com/ai/?ref=hf-agents)**.
