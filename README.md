# EZLife Tool

EZLife Tool is a context switching utility designed to make managing multiple browser instances and workflows easier. It allows you to define custom keyboard shortcuts to cycle through different browsers or browser profiles, helping you separate your work, personal life, and other contexts efficiently.

## Features

- **Context Switching**: Quickly toggle between different browsers (e.g., Brave, Opera GX, Chrome) with a global hotkey.
- **Custom Shortcuts**: Define your preferred key combination (default: `Alt Gr + B`) to switch contexts.
- **Tray Application**: Runs silently in the system tray (`controlador.exe`).
- **Configuration GUI**: Easy-to-use interface (`EZLife_Config.exe`) to manage your browser paths and settings.
- **Auto-Start**: Option to launch automatically with Windows.
- **Low Resource Usage**: Minimized footprint when running in the background.

## Installation

### For Users

1.  Download the latest installer (`EZLifeInstaller.exe`) from the [Releases](https://github.com/RodriGGod/EZ-life/releases) page.
2.  Run the installer and follow the on-screen instructions.
3.  Once installed, the EZLife Controller will start automatically. You can access the settings by opening "EZLife Tool".

### For Developers

If you want to contribute to the project or build it from source:

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/RodriGGod/EZ-life.git
    cd EZ-life
    ```

2.  **Create a virtual environment** (recommended):
    ```bash
    python -m venv .venv
    # On Windows:
    .\.venv\Scripts\activate
    # On macOS/Linux:
    source .venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up configuration**:
    Duplicate the example configuration file to create your local config.
    ```bash
    cp config_example.json config.json
    ```
    Open `config.json` and update the paths to point to the browsers executable on your machine.

## Usage

### Running from Source

You can run the components individually:

- **Controller** (Background Listener):
    ```bash
    python src/controlador.py
    ```

- **Configuration UI**:
    ```bash
    python src/main.py
    ```

### Building the Executables

This project uses `PyInstaller` to build the executables and `Inno Setup` to create the installer.

1.  **Build Executables**:
    Run the following commands to build the `.exe` files in `src/dist`:
    ```bash
    cd src
    pyinstaller main.spec
    pyinstaller controller.spec
    pyinstaller proxy.spec
    ```

2.  **Build Installer**:
    You need [Inno Setup 6](https://jrsoftware.org/isdl.php) installed.
    Run the PowerShell build script:
    ```powershell
    .\build_installer.ps1
    ```

## Contributing

Contributions are welcome! If you'd like to help improve EZLife Tool, please follow these steps:

1.  **Fork the repository** on GitHub.
2.  Create a new branch for your feature or bug fix:
    ```bash
    git checkout -b feature/amazing-feature
    ```
3.  Make your changes and verify they work.
4.  **Update `.gitignore`**: Ensure no temporary or local configuration files are tracked. `config.json` is ignored by default.
5.  Commit your changes:
    ```bash
    git commit -m "Add some amazing feature"
    ```
6.  Push to your branch:
    ```bash
    git push origin feature/amazing-feature
    ```
7.  Open a **Pull Request** on the original repository.

## License

[MIT License](LICENSE)