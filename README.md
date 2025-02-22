# Markdown Viewer

A GTK-based Markdown viewer application with support for themes, zooming, and printing capabilities. This application provides a clean and modern interface for viewing Markdown files with various features to enhance readability and user experience.

## Features

- **Dark/Light Theme**: Toggle between dark and light modes for comfortable reading
- **Zoom Controls**: Adjust text size with zoom in/out and reset options
- **Print Support**: Print your markdown documents directly from the viewer
- **Fullscreen Mode**: Distraction-free reading experience
- **Keyboard Shortcuts**: Quick access to all major functions
- **File Filtering**: Easy selection of Markdown files
- **Status Bar**: Shows current file and application status
- **Responsive Design**: Adapts to different window sizes
- **Code Highlighting**: Proper rendering of code blocks
- **Table Support**: Clean rendering of markdown tables

## Requirements

- Python 3.6+
- GTK 3.0
- WebKit2
- markdown2

## Installation

1. First, ensure you have the required system libraries:

```bash
# Ubuntu/Debian
sudo apt-get install python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-webkit2-4.0

# Fedora
sudo dnf install python3-gobject gtk3 webkit2gtk3

# Arch Linux
sudo pacman -S python-gobject gtk3 webkit2gtk
```

2. Install Python dependencies:

```bash
pip install markdown2
```

3. Clone the repository and run the installation script:

```bash
git clone https://github.com/profemzy/markdown-viewer.git
cd markdown-viewer
chmod +x upgrade-install.sh
sudo ./upgrade-install.sh
```

## Installation Details

The installation script (`upgrade-install.sh`) handles both fresh installations and upgrades:

- Installs the application to `/opt/markdown-viewer/`
- Creates desktop entry in `/usr/share/applications/`
- Preserves user customizations during upgrades
- Creates automatic backup before upgrades
- Provides uninstall capability

### Upgrading

To upgrade an existing installation:

```bash
sudo ./upgrade-install.sh
```

The script will:
- Backup existing installation
- Preserve user customizations
- Update application files
- Restore user settings

### Uninstalling

To uninstall the application:

```bash
sudo /opt/markdown-viewer/uninstall.sh
```

## Usage

### Starting the Application

1. From file manager:
   - Double click any .md file
   - Select "Markdown Viewer" from Open With menu

2. From command line:
```bash
python3 /opt/markdown-viewer/markdown_viewer.py [optional_markdown_file]
```

### Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Open File | Ctrl+O |
| Refresh | Ctrl+R |
| Print | Ctrl+P |
| Zoom In | Ctrl++ |
| Zoom Out | Ctrl+- |
| Reset Zoom | Ctrl+0 |
| Toggle Fullscreen | F11 |

## Customization

### Styling

You can customize the appearance by modifying:
```bash
/opt/markdown-viewer/styles.css
```

The application supports both light and dark themes through CSS variables.

## File Structure

```
/opt/markdown-viewer/
├── markdown_viewer.py   # Main application file
├── templates.py         # HTML templates
├── styles.css          # CSS styles
├── version.txt         # Version information
└── uninstall.sh        # Uninstallation script
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Future Improvements

- [ ] Recent files menu
- [ ] Table of contents sidebar
- [ ] Find in page functionality
- [ ] Export to PDF option
- [ ] Line numbers for code blocks
- [ ] Configurable font size and family
- [ ] Auto-reload on file changes
- [ ] Outline view for document headers

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.