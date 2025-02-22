#!/bin/bash

# Version of this installation
VERSION="1.0.0"
INSTALL_DIR="$HOME/Applications/MarkdownViewer"
BACKUP_DIR="$HOME/Applications/MarkdownViewer.backup"
APP_NAME="Markdown Viewer.app"
APP_DIR="$HOME/Applications/$APP_NAME"

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

print_status "Starting Markdown Viewer installation/upgrade process for macOS..."

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    print_error "Homebrew is not installed. Please install it first:"
    echo '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
    exit 1
fi

# Install dependencies
print_status "Installing/Updating dependencies..."
brew install python3 gtk+3 webkit2gtk3 || {
    print_error "Failed to install dependencies"
    exit 1
}

# Install Python dependencies
print_status "Installing Python dependencies..."
pip3 install markdown2 || {
    print_error "Failed to install Python dependencies"
    exit 1
}

# Check if this is an upgrade
if [ -d "$INSTALL_DIR" ]; then
    if [ -f "$INSTALL_DIR/version.txt" ]; then
        CURRENT_VERSION=$(cat "$INSTALL_DIR/version.txt")
        print_status "Current installation detected (version $CURRENT_VERSION)"
        
        # Create backup
        print_status "Creating backup..."
        if [ -d "$BACKUP_DIR" ]; then
            rm -rf "$BACKUP_DIR"
        fi
        cp -r "$INSTALL_DIR" "$BACKUP_DIR"
    fi
fi

# Create installation directory
print_status "Creating installation directories..."
mkdir -p "$INSTALL_DIR"

# Copy application files
print_status "Installing application files..."
cp markdown_viewer.py "$INSTALL_DIR/"
cp templates.py "$INSTALL_DIR/"
cp styles.css "$INSTALL_DIR/"

# Create version file
echo "$VERSION" > "$INSTALL_DIR/version.txt"

# Create macOS app bundle
print_status "Creating macOS app bundle..."
mkdir -p "$APP_DIR/Contents/MacOS"
mkdir -p "$APP_DIR/Contents/Resources"

# Create Info.plist
cat > "$APP_DIR/Contents/Info.plist" << EOL
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>markdown-viewer</string>
    <key>CFBundleIdentifier</key>
    <string>com.example.markdown-viewer</string>
    <key>CFBundleName</key>
    <string>Markdown Viewer</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>$VERSION</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.10</string>
    <key>CFBundleDocumentTypes</key>
    <array>
        <dict>
            <key>CFBundleTypeExtensions</key>
            <array>
                <string>md</string>
                <string>markdown</string>
            </array>
            <key>CFBundleTypeName</key>
            <string>Markdown Document</string>
            <key>CFBundleTypeRole</key>
            <string>Viewer</string>
        </dict>
    </array>
</dict>
</plist>
EOL

# Create launcher script
cat > "$APP_DIR/Contents/MacOS/markdown-viewer" << EOL
#!/bin/bash
export PATH="/usr/local/bin:\$PATH"
python3 "$INSTALL_DIR/markdown_viewer.py" "\$@"
EOL

chmod +x "$APP_DIR/Contents/MacOS/markdown-viewer"

# Create uninstall script
cat > "$INSTALL_DIR/uninstall.sh" << EOL
#!/bin/bash
rm -rf "$INSTALL_DIR"
rm -rf "$APP_DIR"
echo "Markdown Viewer has been uninstalled"
EOL

chmod +x "$INSTALL_DIR/uninstall.sh"

print_status "Installation completed successfully!"
echo -e "${GREEN}Current version: $VERSION${NC}"
echo "The application has been installed to your Applications folder"
echo "You can now open Markdown files with Markdown Viewer from Finder"

# Ask user if they want to configure file associations
read -p "Would you like to set Markdown Viewer as the default application for .md files? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    duti -s com.example.markdown-viewer .md all
    duti -s com.example.markdown-viewer .markdown all
    print_status "File associations have been set"
fi