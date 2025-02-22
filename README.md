# Markdown Viewer

A modern, cross-platform Markdown viewer built with GTK and WebKit, featuring themes, zooming, and printing capabilities. View your Markdown files with a clean, user-friendly interface that enhances readability and productivity.

## Features

### Core Features
- **Dual Themes**: Switch between light and dark modes
- **Zoom Controls**: Easily adjust content size with keyboard shortcuts
- **Print Support**: Print documents directly from the viewer
- **Fullscreen Mode**: Distraction-free reading experience

### User Interface
- **Modern GTK Interface**: Clean, native look and feel
- **Responsive Design**: Adapts to different window sizes
- **Status Bar**: Shows current file and application status
- **Intuitive Controls**: Easy-to-use toolbar with tooltips

### Document Handling
- **File Filtering**: Quick access to Markdown files
- **Code Highlighting**: Proper rendering of code blocks
- **Table Support**: Clean rendering of markdown tables
- **File Associations**: Opens .md files directly from file manager

### Keyboard Shortcuts
- Open File: `Ctrl+O`
- Refresh: `Ctrl+R`
- Print: `Ctrl+P`
- Zoom In: `Ctrl++`
- Zoom Out: `Ctrl+-`
- Reset Zoom: `Ctrl+0`
- Toggle Fullscreen: `F11`

## Requirements

### Common Requirements
- Python 3.6+
- markdown2 Python package

### Linux Requirements
- GTK 3.0
- WebKit2GTK
- Python GObject bindings

### macOS Requirements
- Homebrew
- GTK+3
- WebKit2GTK3

## Installation

### Linux Installation

1. Install system dependencies:

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

3. Run the installation script:
```bash
chmod +x upgrade-install.sh
sudo ./upgrade-install.sh
```

### macOS Installation

1. Install Homebrew (if not already installed):
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. Clone the repository:
```bash
git clone https://github.com/yourusername/markdown-viewer.git
cd markdown-viewer
```

3. Run the macOS installation script:
```bash
chmod +x macos-install.sh
./macos-install.sh
```

## Usage

### Starting the Application

#### Linux
1. From file manager:
   - Double click any .md file
   - Select "Markdown Viewer" from Open With menu

2. From command line:
```bash
python3 /opt/markdown-viewer/markdown_viewer.py [optional_markdown_file]
```

#### macOS
1. From Finder:
   - Double click any .md file
   - Select "Markdown Viewer" from Open With menu

2. From command line:
```bash
~/Applications/MarkdownViewer/markdown_viewer.py [optional_markdown_file]
```

### File Structure

#### Linux
```
/opt/markdown-viewer/
├── markdown_viewer.py   # Main application file
├── templates.py         # HTML templates
├── styles.css          # CSS styles
├── version.txt         # Version information
└── uninstall.sh        # Uninstallation script
```

#### macOS
```
~/Applications/
├── Markdown Viewer.app/    # macOS application bundle
└── MarkdownViewer/
    ├── markdown_viewer.py  # Main application file
    ├── templates.py        # HTML templates
    ├── styles.css         # CSS styles
    ├── version.txt        # Version information
    └── uninstall.sh       # Uninstallation script
```

## Customization

### Styling

#### Linux
Edit the CSS file at:
```bash
/opt/markdown-viewer/styles.css
```

#### macOS
Edit the CSS file at:
```bash
~/Applications/MarkdownViewer/styles.css
```

### Themes
The application supports both light and dark themes through CSS variables. You can customize colors, fonts, and other visual elements by modifying the CSS file.

## Upgrading

### Linux
```bash
sudo ./upgrade-install.sh
```

### macOS
```bash
./macos-install.sh
```

Both scripts will:
- Backup existing installation
- Preserve user customizations
- Update application files
- Restore user settings

## Uninstalling

### Linux
```bash
sudo /opt/markdown-viewer/uninstall.sh
```

### macOS
```bash
~/Applications/MarkdownViewer/uninstall.sh
```

## Development

### Project Structure
```
markdown-viewer/
├── markdown_viewer.py   # Main application source
├── templates.py         # HTML templates
├── styles.css          # CSS styles
├── upgrade-install.sh  # Linux installation script
├── macos-install.sh   # macOS installation script
└── README.md          # This file
```

### Contributing

1. Fork the repository
2. Create your feature branch:
```bash
git checkout -b feature/amazing-feature
```
3. Commit your changes:
```bash
git commit -m 'Add some amazing feature'
```
4. Push to the branch:
```bash
git push origin feature/amazing-feature
```
5. Open a Pull Request

## Future Improvements

- [ ] Recent files menu
- [ ] Table of contents sidebar
- [ ] Find in page functionality (Ctrl+F)
- [ ] Export to PDF option
- [ ] Line numbers for code blocks
- [ ] Configurable font size and family
- [ ] Auto-reload on file changes
- [ ] Outline view for document headers

## Troubleshooting

### Common Issues

1. File picker showing twice:
   - This has been fixed in the latest version
   - Upgrade your installation to resolve

2. Missing dependencies:
   - Run the appropriate installation commands for your OS
   - Check system requirements section

3. Permission issues:
   - Ensure proper file permissions
   - Run installation scripts with appropriate privileges

## Support

- GitHub Issues: Report bugs and request features
- Wiki: Additional documentation and guides
- Discussions: Community support and discussion

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- GTK team for the excellent toolkit
- WebKit for the rendering engine
- markdown2 package for Markdown parsing
- All contributors who have helped improve this project