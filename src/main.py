"""
EZLife Tool - Configuration GUI Entry Point
Launches the PyWebview configuration interface.
"""
import webview
import os
from core.paths import get_web_dir
from ui.api import ConfigAPI


def main():
    """Launch the configuration GUI."""
    api = ConfigAPI()
    
    # Get path to HTML file
    html_file = os.path.join(get_web_dir(), 'index.html')
    
    if not os.path.exists(html_file):
        print(f"ERROR: Cannot find {html_file}")
        print("Make sure the web directory is properly bundled.")
        return
    
    # Create and start window
    window = webview.create_window(
        'EZLife Tool',
        url=html_file,
        js_api=api,
        width=800,
        height=600,
        min_size=(600, 400),
        frameless=True,
        transparent=True,
        easy_drag=True,
        resizable=True
    )
    
    webview.start(debug=False)


if __name__ == '__main__':
    main()
