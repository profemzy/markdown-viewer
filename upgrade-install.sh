#!/bin/bash

# Version of this installation
VERSION="1.0.0"
INSTALL_DIR="/opt/markdown-viewer"
BACKUP_DIR="/opt/markdown-viewer.backup"
CONFIG_DIR="/etc/markdown-viewer"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print status messages
print_status() {
    echo -e "${GREEN}[*]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[x]${NC} $1"
}

# Check if script is run with sudo
if [ "$EUID" -ne 0 ]; then 
    print_error "Please run as root or with sudo"
    exit 1
fi

print_status "Starting Markdown Viewer installation/upgrade process..."

# Check if this is an upgrade
if [ -d "$INSTALL_DIR" ]; then
    if [ -f "$INSTALL_DIR/version.txt" ]; then
        CURRENT_VERSION=$(cat "$INSTALL_DIR/version.txt")
        print_status "Current installation detected (version $CURRENT_VERSION)"
        
        # Create backup of existing installation
        print_status "Creating backup of current installation..."
        if [ -d "$BACKUP_DIR" ]; then
            rm -rf "$BACKUP_DIR"
        fi
        cp -r "$INSTALL_DIR" "$BACKUP_DIR"
        
        # Save user configuration if it exists
        if [ -f "$INSTALL_DIR/styles.css" ]; then
            print_status "Preserving user styles..."
            cp "$INSTALL_DIR/styles.css" "$BACKUP_DIR/styles.css.user"
        fi
    else
        print_warning "Existing installation found but no version information available"
    fi
fi

# Create desktop entry content
print_status "Creating desktop entry..."
cat > markdown-viewer.desktop << EOL
[Desktop Entry]
Version=$VERSION
Name=Markdown Viewer
GenericName=Markdown Document Viewer
Comment=View Markdown files with syntax highlighting and themes
Exec=python3 $INSTALL_DIR/markdown_viewer.py %f
TryExec=python3
Icon=text-editor
Terminal=false
Type=Application
Categories=GTK;Utility;TextEditor;
Keywords=markdown;md;viewer;editor;
MimeType=text/markdown;text/x-markdown;
StartupNotify=true
Actions=new-window;

[Desktop Action new-window]
Name=New Window
Exec=python3 $INSTALL_DIR/markdown_viewer.py %f
EOL

# Create necessary directories
print_status "Creating installation directories..."
mkdir -p "$INSTALL_DIR"
mkdir -p "$CONFIG_DIR"
mkdir -p /usr/share/applications

# Copy application files
print_status "Installing application files..."
cp markdown_viewer.py "$INSTALL_DIR/"
cp templates.py "$INSTALL_DIR/"
cp styles.css "$INSTALL_DIR/"

# Create version file
echo "$VERSION" > "$INSTALL_DIR/version.txt"

# Make the main script executable
chmod +x "$INSTALL_DIR/markdown_viewer.py"

# Restore user configuration if it exists
if [ -f "$BACKUP_DIR/styles.css.user" ]; then
    print_status "Restoring user styles..."
    cp "$BACKUP_DIR/styles.css.user" "$INSTALL_DIR/styles.css"
fi

print_status "Installing desktop entry..."
cp markdown-viewer.desktop /usr/share/applications/

print_status "Updating MIME database..."
update-desktop-database

print_status "Setting permissions..."
chown -R root:root "$INSTALL_DIR"
chmod -R 755 "$INSTALL_DIR"

print_status "Cleaning up..."
rm markdown-viewer.desktop

# Remove backup if installation successful
if [ -d "$BACKUP_DIR" ]; then
    print_status "Installation successful, removing backup..."
    rm -rf "$BACKUP_DIR"
fi

print_status "Installation/upgrade completed successfully!"
echo -e "${GREEN}Current version: $VERSION${NC}"
echo "You can now open Markdown files with Markdown Viewer from your file manager."

# Create uninstall script
cat > "$INSTALL_DIR/uninstall.sh" << 'EOF'
#!/bin/bash
echo "Uninstalling Markdown Viewer..."
sudo rm -rf /opt/markdown-viewer
sudo rm -rf /etc/markdown-viewer
sudo rm /usr/share/applications/markdown-viewer.desktop
sudo update-desktop-database
echo "Uninstallation complete!"
EOF

chmod +x "$INSTALL_DIR/uninstall.sh"