# ⚡ EZLife Tool

#### by RodriGGod

![Version](https://img.shields.io/badge/version-1.0.0-green) ![Platform](https://img.shields.io/badge/platform-Windows-blue) ![License](https://img.shields.io/badge/license-MIT-white)

**EZLife Tool** is a high-performance productivity utility designed to automate context switching in Windows. It features a modern, frameless, semi-transparent "hacker/terminal" UI and allows you to toggle your default web browser instantly using global keyboard shortcuts.

![Screenshot](https://via.placeholder.com/800x450.png?text=EZLife+Tool+Interface+Preview)
*(Replace this link with a real screenshot of your app once uploaded)*

---

## 🚀 Features

* **Global Hotkeys:** Switch contexts instantly from anywhere in Windows.
* **Smart Detection:** Automatically finds installed browsers (Opera GX, Brave, Chrome, etc.).
* **Manual Linking:** Add any portable or custom `.exe` as a target.
* **Visual & Audio Feedback:** On-screen tooltips and sound cues when switching.
* **Minimalist UI:** Frameless, transparent window that blends into your desktop.
* **Drag & Drop:** Move the window from the top invisible bar.

---

## 📥 Installation

We have simplified the process with an automatic installer.

1.  Go to the **[Releases](../../releases)** section of this repository.
2.  Download the latest file named **`EZLifeInstaller.exe`**.
3.  Run the installer.
    * *Note: Since this tool interacts with system hotkeys, Windows SmartScreen might show a warning. Click "More Info" -> "Run Anyway".*
4.  Follow the installation wizard steps.
5.  Launch **EZLife Tool** from your desktop or start menu.

---

## ⚙️ How to Use

### 1. Initial Configuration
1.  Open **EZLife Tool**.
2.  **Set Trigger:** Click the **REC** button and press your desired key combination (e.g., `AltGr` + `B`).
3.  **Select Targets:** Check the browsers you want to cycle through.
    * *Missing one?* Click **+ LINK MANUAL .EXE** to browse for it.
4.  Click **INITIALIZE CONFIG**.

### 2. IMPORTANT: Windows Setup
For the tool to intercept links, you must set the internal proxy as your default browser:

1.  Open Windows **Settings** -> **Apps** -> **Default Apps**.
2.  Search for **Web Browser**.
3.  Click on your current browser and select **EZLife Browser Proxy** (or the name of the installed helper executable).
4.  **Done!** Now, every time you click a link in Discord, Slack, or any app, it will open in your *currently selected* active target.

### 3. Usage
* Press your hotkey (e.g., `AltGr` + `B`) to toggle between your selected browsers.
* A tooltip will appear next to your mouse indicating the active browser (e.g., "🦁 Brave Active").

---

## 🔮 Roadmap & Future Updates

We are constantly expanding the capabilities of EZLife Tool. Here is what is coming next:

- [ ] **Code Editor Switcher:**
    - Add a new hotkey to toggle your default IDE (VS Code, JetBrains, Sublime, etc.).
    - **Context Menu Integration:** Right-click a file -> "Open with EZLife" -> Opens in the currently selected editor.
- [ ] **Profile Management:** Create different presets for "Work", "Gaming", and "Coding".
- [ ] **Cloud Sync:** Save your configuration across different machines.
- [ ] **Theme Selector:** Customize the accent colors (currently locked to Lime Green).

---

## 🛠️ Built With

* **Python** (Core Logic)
* **PyWebview** (Frameless Engine)
* **HTML5/CSS3** (Interface)
* **Keyboard** (Global Hooks)

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

#### Crafted with 💻 by **RodriGGod**