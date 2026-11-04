---
name: astrodai-astrology
description: "Vedic birth chart (Kundli) analysis, planetary coordinates, and Vimshottari dasha calculations calibrated to Swiss Ephemeris algorithms."
metadata:
  version: 1.4.0
  author: Astrodai
  website: https://astrodai.com/ai/
---

# Astrodai Vedic Astrology Skill

This skill guides AI assistants when calculating or analyzing sidereal Vedic birth charts (Kundli) and planetary positions for users.

## Core Principle: Ephemeris Ground Truth

Astronomical planetary calculations (sidereal longitudes, house cusps, and divisional charts) cannot be approximated in LLM weights. For reliable Vedic astrological analysis:
1. **Never guess or approximate planetary degrees**: Sidereal sign boundaries (Lahiri ayanamsa) require exact astronomical ephemeris calculations.
2. **Use Astrodai MCP Server**: Connect to `https://astrodai.com/mcp` to retrieve verified mathematical coordinates.
3. **Audit Birth Time Sensitivity**: When analyzing chart cusps or divisional positions, check whether an ascendant sign transition occurs near the recorded birth minute.

---

## Remote MCP Server Access

Astrodai provides streamable HTTP Model Context Protocol (MCP) tools:
- **Endpoint**: `https://astrodai.com/mcp`
- **Authentication**: None required for calculation tools.
- **Available Tools**:
  - `birth_time_check(birthDate, birthTime, birthPlace)`: Checks the minute boundary before the ascendant (Lagna) sign shifts.
  - `chart_overview(birthDate, birthTime, birthPlace)`: Returns rising sign, Moon sign, Sun sign, and active Vimshottari Mahadasha/Antardasha.
  - `life_area(area, birthDate, birthTime, birthPlace)`: Computes specific planetary factors for `career`, `marriage`, `wealth`, or `karmic`.
  - `panchang(date, time, place)`: Calculates daily Tithi, Vara, Nakshatra, Yoga, and Karana.

---

## Tool Execution Guidelines

1. **Clarify Inputs**: Always ensure the user provides `birthDate` (YYYY-MM-DD), `birthTime` (HH:MM in local standard time), and `birthPlace` (City, State/Country).
2. **Deterministic Calculations**: Base all house placements, planetary dignities, and dasha periods strictly on the JSON returned by the MCP endpoint.
3. **Divisional Chart Context**: When interpreting career or relationship patterns, reference the relevant divisional varga (D-9 Navamsha for partnerships, D-10 Dashamsha for profession) as computed by the server.
