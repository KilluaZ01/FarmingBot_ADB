# 🌟 Mirren Star Legends Guest Account Farming Bot

A full automation system for rerolling guest accounts in *Mirren Star Legends* using LDPlayer 9, Proxifier, and Python. This bot clones emulator instances, automates game tutorial flow, assigns custom guest names, performs summons, takes screenshots, and supports proxy routing via Airproxy or localhost.

---

## 📦 Features

- ✅ GUI for configuring bot options
- 🌀 Batch-based instance cloning and control
- ⌨️ Macro triggering using `pyautogui`
- 🌐 Airproxy API integration (fallback to localhost if unavailable)
- 🧪 Screenshot capture after 10x summon
- 📁 Organized project structure

---

## 📁 Project Structure

| File / Folder         | Purpose                                           |
|----------------------|--------------------------------------------------|
| `gui_main.py`         | GUI entry point                                   |
| `parallel_runner.py`  | Bot logic orchestrator, runs batch cycles        |
| `clone_utils.py`      | Instance cloning and launching utilities          |
| `adb_utils.py`        | ADB commands: input guest name, screenshots, close instances |
| `trigger_macro.py`    | Macro hotkey triggering for emulator windows      |
| `proxy_utils.py`      | Proxy handling with Airproxy API + localhost fallback |
| `config.py`           | Configuration settings and constants               |
| `macros/`             | LDPlayer macro scripts used in automation          |
| `screenshots/`        | Folder for output screenshots                       |
| `ProxifierProfiles/`  | Proxifier `.ppx` config files (for proxy routing)  |
| `requirements.txt`    | Python dependencies for environment setup          |

---

## ⚙️ Requirements

- [Python 3.8+](https://www.python.org/)
- [LDPlayer 9](https://www.ldplayer.net/)
- [Proxifier](https://www.proxifier.com/)
- Optional: [Airproxy.io](https://airproxy.io/) API key

Install dependencies:

```bash
pip install -r requirements.txt
```
---

## ⚙️ How It Works

1. **GUI Input**  
   You specify:
   - Base LDPlayer instance name (pre-installed and asset-ready)
   - Airproxy API key (or leave empty for localhost fallback)
   - Total accounts to generate
   - Batch size (number of simultaneous LDPlayer instances)

2. **Batch Execution**
   - The script clones the base LDPlayer instance into batch instances (e.g., LDPlayer-1, LDPlayer-2, etc.)
   - It launches each with an optional proxy (via Proxifier profile)
   - If no valid API key is given, all instances default to localhost IP

3. **Macro Automation**
   - The bot runs pre-recorded macros using `pyautogui` and `pygetwindow`
   - Macros simulate in-game actions: skipping tutorial, summoning, etc.

4. **Guest Name Injection**
   - Each emulator inputs a unique guest name via ADB

5. **Screenshot Capture**
   - The result of each summon is captured using ADB screencap
   - Screenshots are saved to the `screenshots/` directory

6. **Cleanup**
   - Instances are automatically closed after processing

---

## 📸 Output

- **Summon screenshots**  
  All summon result images are saved as:
  screenshots/North123X001.png
  
---

> “It is not because things are difficult that we do not dare; it is because we do not dare that they are difficult.”  
> — *Seneca*
