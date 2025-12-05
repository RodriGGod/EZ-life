# ⚡ EZLife Tool

#### by RodriGGod

![Version](https://img.shields.io/badge/version-1.0.0-green) ![Platform](https://img.shields.io/badge/platform-Windows-blue) ![License](https://img.shields.io/badge/license-MIT-white) ![Python](https://img.shields.io/badge/python-3.8+-blue)

**EZLife Tool** is a high-performance productivity utility designed to automate context switching in Windows. It features a modern, frameless, semi-transparent "hacker/terminal" UI and allows you to toggle your default web browser instantly using global keyboard shortcuts.

![Screenshot](https://via.placeholder.com/800x450.png?text=EZLife+Tool+Interface+Preview)
*(Replace this link with a real screenshot of your app once uploaded)*

---

## 🚀 Features

* **Global Hotkeys:** Switch contexts instantly from anywhere in Windows using customizable keyboard shortcuts.
* **Smart Detection:** Automatically finds installed browsers (Opera GX, Brave, Chrome, Edge, Firefox, etc.) from Windows Registry.
* **Manual Linking:** Add any portable or custom `.exe` as a target browser.
* **Visual Feedback:** On-screen tooltips appear near your cursor showing the active browser.
* **Minimalist UI:** Frameless, 85% transparent window with a sleek black background and lime green accents.
* **Drag & Drop:** Move the window freely from the top invisible bar.
* **Persistent Configuration:** Settings stored in `%APPDATA%\EZLifeTool\config.json`.
* **Background Controller:** Lightweight process that listens for hotkeys without keeping the UI open.
* **Windows Autostart:** Optional feature to automatically launch the controller when Windows starts up.

---

## 📥 Installation

### Option A: Using the Installer (Recommended)

1.  Go to the **[Releases](../../releases)** section of this repository.
2.  Download the latest file named **`EZLifeInstaller.exe`**.
3.  Run the installer.
    * *Note: Since this tool interacts with system hotkeys, Windows SmartScreen might show a warning. Click "More Info" -> "Run Anyway".*
4.  Follow the installation wizard steps.
5.  Launch **EZLife Tool** from your desktop or start menu.

### Option B: Running from Source

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/RodriGGod/EZ-life.git
    cd EZ-life
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the configuration app:**
    ```bash
    python src/main.py
    ```

4.  **Run the background daemon:**
    ```bash
    python src/daemon.py
    ```

---

## ⚙️ How to Use

### 1. Initial Configuration
1.  Open **EZLife Tool** (run `app.py` or the installed executable).
2.  **Set Trigger:** Click the **REC** button and press your desired key combination (e.g., `AltGr` + `B`).
3.  **Select Targets:** The app will automatically detect installed browsers. Check the ones you want to cycle through.
    * *Missing one?* Click **+ LINK MANUAL .EXE** to browse for it.
4.  Click **INITIALIZE CONFIG** to save your settings.
5.  **(Optional)** Check **Run on Windows Startup** to automatically start the controller when your computer boots up.
    * This adds the controller to the Windows Registry startup entries.
    * You can disable it anytime by unchecking the box.

### 2. IMPORTANT: Windows Setup
For the tool to intercept links from external applications, you must set the EZLife Browser Proxy as your default browser:

1.  Open Windows **Settings** → **Apps** → **Default Apps**.
2.  Search for **Web Browser**.
3.  Click on your current browser and select **EZLife Browser Proxy** (or `browser.exe` from the installed location).
4.  **Done!** Now, every time you click a link in Discord, Slack, or any app, it will open in your *currently selected* active browser.

### 3. Usage
* Press your configured hotkey (e.g., `AltGr` + `B`) to toggle between your selected browsers.
* A tooltip will appear near your mouse cursor indicating the active browser (e.g., "🌍 Cambiado a: Brave Browser").
* The controller runs in the background and doesn't require the UI to be open.

---

## 🏗️ Architecture

EZLife Tool consists of three main components:

### 1. **Configuration App** (`app.py`)
- **Purpose:** Graphical interface for setting up hotkeys and selecting browsers.
- **Technology:** PyWebview with HTML/CSS/JavaScript frontend.
- **Features:**
  - Auto-detects browsers from Windows Registry.
  - Records custom keyboard shortcuts.
  - Manages configuration stored in `%APPDATA%\EZLifeTool\config.json`.
  - Restarts the background controller when settings change.
  - Manages Windows startup registry entries for autostart functionality.

### 2. **Background Controller** (`controlador.py`)
- **Purpose:** Lightweight process that listens for the configured hotkey.
- **Technology:** Python with `keyboard` library for global hotkey detection.
- **Features:**
  - Runs silently in the background.
  - Cycles through selected browsers when hotkey is pressed.
  - Shows visual tooltip feedback.
  - Persists the current browser index to the config file.

### 3. **Browser Proxy** (`browser.py`)
- **Purpose:** Acts as the default browser handler to intercept URLs.
- **Technology:** Python script compiled to `.exe`.
- **Features:**
  - Reads the current active browser from config.
  - Opens URLs in the selected browser.
  - Fallback to Chrome if no configuration exists.

---

## 📂 Project Structure

```
EZ-life/
├── src/
│   ├── main.py                    # Configuration GUI entry point
│   ├── daemon.py                  # Background hotkey daemon
│   ├── proxy.py                   # Browser proxy handler
│   │
│   ├── core/                      # Core shared functionality
│   │   ├── config.py              # Configuration management
│   │   ├── paths.py               # Path resolution
│   │   └── registry.py            # Windows Registry operations
│   │
│   ├── modules/                   # Feature modules (pluggable)
│   │   ├── base_module.py         # Base class for modules
│   │   ├── browser/               # Browser switching module
│   │   │   ├── detector.py        # Browser detection
│   │   │   ├── switcher.py        # Switching logic
│   │   │   └── proxy.py           # URL handler
│   │   └── editor/                # Code editor module (future)
│   │       ├── detector.py        # Editor detection
│   │       └── switcher.py        # Switching logic
│   │
│   ├── ui/                        # User interface
│   │   ├── api.py                 # PyWebview API bridge
│   │   └── web/                   # HTML/CSS/JS
│   │       ├── index.html
│   │       └── style.css
│   │
│   ├── utils/                     # Utilities
│   │   ├── process.py             # Process management
│   │   └── tooltip.py             # Visual feedback
│   │
│   ├── main.spec                  # PyInstaller spec for GUI
│   ├── daemon.spec                # PyInstaller spec for daemon
│   └── proxy.spec                 # PyInstaller spec for proxy
│
├── requirements.txt               # Python dependencies
├── config.json                    # Default configuration template
├── README.md                      # User documentation
└── DEVELOPER.md                   # Developer documentation
```

---

## 🔧 Building from Source

To compile the application into standalone executables:

1.  **Install PyInstaller:**
    ```bash
    pip install pyinstaller
    ```

2.  **Build all components:**
    ```bash
    cd src
    pyinstaller main.spec
    pyinstaller daemon.spec
    pyinstaller proxy.spec
    ```

3.  **Executables will be in:**
    - `src/dist/EZLife_Config.exe` - Configuration GUI
    - `src/dist/daemon.exe` - Background daemon
    - `src/dist/proxy.exe` - Browser proxy

For detailed developer documentation, see [DEVELOPER.md](DEVELOPER.md).

---

## 🔮 Roadmap & Future Updates

We are constantly expanding the capabilities of EZLife Tool. Here's what's coming next:

- [ ] **Code Editor Switcher:**
    - Add a new hotkey to toggle your default IDE (VS Code, JetBrains, Sublime, etc.).
    - **Context Menu Integration:** Right-click a file → "Open with EZLife" → Opens in the currently selected editor.
- [ ] **Profile Management:** Create different presets for "Work", "Gaming", and "Coding".
- [ ] **Cloud Sync:** Save your configuration across different machines.
- [ ] **Theme Selector:** Customize the accent colors (currently locked to Lime Green).
- [ ] **Multi-Platform Support:** Extend to Linux and macOS.
- [ ] **Tray Icon:** Add system tray integration for quick access.

---

## 🛠️ Built With

* **[Python 3.8+](https://www.python.org/)** - Core logic and automation
* **[PyWebview](https://pywebview.flowrl.com/)** - Frameless window engine
* **[Keyboard](https://github.com/boppreh/keyboard)** - Global hotkey detection
* **[Psutil](https://github.com/giampaolo/psutil)** - Process management
* **[PyInstaller](https://www.pyinstaller.org/)** - Executable compilation
* **HTML5/CSS3/JavaScript** - User interface

---

## 🐛 Troubleshooting

### The hotkey doesn't work
- Make sure the controller (`controlador.exe`) is running in the background.
- Check that your hotkey doesn't conflict with other applications.
- Run the controller as Administrator if needed.

### Browser doesn't switch
- Verify that the browser paths in `%APPDATA%\EZLifeTool\config.json` are correct.
- Re-run the configuration app to refresh browser detection.

### Links don't open in the selected browser
- Ensure you've set **EZLife Browser Proxy** as your default browser in Windows Settings.
- Check that `browser.exe` is in the correct location.

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

#### Crafted with 💻 by **RodriGGod**

*If you find this tool useful, consider giving it a ⭐ on GitHub!*