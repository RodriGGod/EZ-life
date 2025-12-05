"""
EZLife Tool - Browser Proxy Entry Point
Opens URLs in the currently selected browser.
"""
import sys
from modules.browser.proxy import open_url


def main():
    """Open URL in current browser."""
    # Get URL from command line arguments
    url = sys.argv[1] if len(sys.argv) > 1 else "https://www.google.com"
    
    # Open in current browser
    open_url(url)


if __name__ == '__main__':
    main()
