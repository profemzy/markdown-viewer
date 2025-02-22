"""
A GTK-based Markdown viewer with support for themes, zooming, and printing.

This module provides a graphical interface for viewing
Markdown files with various
features like dark/light themes, zoom controls, and print capabilities.
"""

import os
import sys
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')

from gi.repository import Gtk, WebKit2, Gdk, Gio  # noqa: E402

import markdown2  # noqa: E402

from templates import (MAIN_TEMPLATE,  # noqa: E402
                       EMPTY_PAGE_TEMPLATE, ERROR_TEMPLATE)


class MarkdownViewer(Gtk.ApplicationWindow):
    """Main window for the Markdown viewer application."""

    def __init__(self, *args, **kwargs):
        """Initialize the Markdown viewer window."""
        super().__init__(*args, **kwargs)
        self.current_file = None
        self.zoom_level = 1.0
        self.is_fullscreen = False
        self.dark_theme = False
        self.load_styles()
        self.setup_window()
        self.create_header_bar()
        self.create_main_content()
        self.setup_actions()

    def setup_window(self):
        """Configure the main window properties."""
        self.set_default_size(1000, 800)
        self.set_position(Gtk.WindowPosition.CENTER)

    def load_styles(self):
        """Load CSS styles from file or use default styles."""
        # Default minimal styles in case the file cannot be loaded
        self.styles = """
            body {
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                font-family: system-ui, -apple-system, sans-serif;
                line-height: 1.6;
            }
            .light-theme {
                color: #333;
                background-color: #fff;
            }
            .dark-theme {
                color: #e0e0e0;
                background-color: #1a1a1a;
            }
        """

        try:
            style_path = os.path.join(os.path.dirname(__file__), 'styles.css')
            with open(style_path, 'r', encoding='utf-8') as file:
                self.styles = file.read()
        except Exception as error:
            print(f"Error loading styles: {error}, using default styles")

    def create_header_bar(self):
        """Create and configure the header bar with controls."""
        header = Gtk.HeaderBar()
        header.set_show_close_button(True)
        header.props.title = "Markdown Viewer"

        # Create left side box for file operations
        left_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

        # Open button
        open_button = self.create_button(
            "document-open-symbolic",
            "Open File (Ctrl+O)",
            self.on_open_clicked
        )
        left_box.add(open_button)

        # Refresh button
        refresh_button = self.create_button(
            "view-refresh-symbolic",
            "Refresh (Ctrl+R)",
            self.on_refresh_clicked
        )
        left_box.add(refresh_button)

        left_box.add(Gtk.Separator(orientation=Gtk.Orientation.VERTICAL))

        # Print button
        print_button = self.create_button(
            "document-print-symbolic",
            "Print (Ctrl+P)",
            self.on_print_clicked
        )
        left_box.add(print_button)

        header.pack_start(left_box)

        # Create right side box for view controls
        right_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

        # Zoom controls
        zoom_out_button = self.create_button(
            "zoom-out-symbolic",
            "Zoom Out (Ctrl+-)",
            self.on_zoom_out_clicked
        )

        self.zoom_level_label = Gtk.Label(label="100%")
        self.zoom_level_label.set_width_chars(5)

        zoom_in_button = self.create_button(
            "zoom-in-symbolic",
            "Zoom In (Ctrl++)",
            self.on_zoom_in_clicked
        )

        zoom_reset_button = self.create_button(
            "zoom-original-symbolic",
            "Reset Zoom (Ctrl+0)",
            self.on_zoom_reset_clicked
        )

        right_box.add(zoom_out_button)
        right_box.add(self.zoom_level_label)
        right_box.add(zoom_in_button)
        right_box.add(zoom_reset_button)
        right_box.add(Gtk.Separator(orientation=Gtk.Orientation.VERTICAL))

        # Theme toggle
        theme_button = self.create_button(
            "weather-clear-night-symbolic",
            "Toggle Dark Mode",
            self.on_theme_toggle
        )
        right_box.add(theme_button)

        # Fullscreen toggle
        fullscreen_button = self.create_button(
            "view-fullscreen-symbolic",
            "Toggle Fullscreen (F11)",
            self.on_fullscreen_clicked
        )
        right_box.add(fullscreen_button)

        header.pack_end(right_box)
        self.set_titlebar(header)

    def create_button(self, icon_name, tooltip, callback):
        """Create a button with an icon and tooltip."""
        button = Gtk.Button()
        icon = Gio.ThemedIcon(name=icon_name)
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        button.add(image)
        button.set_tooltip_text(tooltip)
        button.connect("clicked", callback)
        return button

    def create_main_content(self):
        """Create the main content area with WebView and status bar."""
        self.webview = WebKit2.WebView()
        self.webview.set_background_color(Gdk.RGBA(1, 1, 1, 1))

        settings = self.webview.get_settings()
        settings.set_enable_developer_extras(True)

        scrolled = Gtk.ScrolledWindow()
        scrolled.add(self.webview)

        self.statusbar = Gtk.Statusbar()
        self.statusbar.push(0, "Ready")

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        vbox.pack_start(scrolled, True, True, 0)
        vbox.pack_start(self.statusbar, False, False, 0)

        self.add(vbox)
        self.show_empty_page()

    def setup_actions(self):
        """Set up keyboard shortcuts and accelerators."""
        accel = Gtk.AccelGroup()
        self.add_accel_group(accel)

        # Define shortcuts
        shortcuts = [
            ("<Control>O", self.on_open_clicked),
            ("<Control>R", self.on_refresh_clicked),
            ("<Control>P", self.on_print_clicked),
            ("<Control>plus", self.on_zoom_in_clicked),
            ("<Control>minus", self.on_zoom_out_clicked),
            ("<Control>0", self.on_zoom_reset_clicked),
            ("F11", self.on_fullscreen_clicked)
        ]

        # Add shortcuts
        for accelerator, callback in shortcuts:
            key, mod = Gtk.accelerator_parse(accelerator)
            accel.connect(
                key,
                mod,
                Gtk.AccelFlags.VISIBLE,
                lambda *x, cb=callback: cb(None)
            )

        self.connect("key-press-event", self.on_key_press)

    def show_empty_page(self):
        """Show the empty page template when no file is loaded."""
        html = EMPTY_PAGE_TEMPLATE.format(
            styles=self.styles,
            theme="dark" if self.dark_theme else "light"
        )
        self.webview.load_html(html, "file:///")

    def load_file(self, file_path):
        """Load and render a markdown file."""
        try:
            self.current_file = file_path
            with open(file_path, 'r', encoding='utf-8') as file:
                md_text = file.read()

            html = markdown2.markdown(
                md_text,
                extras=['fenced-code-blocks', 'tables', 'task_list']
            )

            full_html = MAIN_TEMPLATE.format(
                styles=self.styles,
                theme="dark" if self.dark_theme else "light",
                content=html
            )

            base_uri = f"file://{os.path.dirname(file_path)}/"
            self.webview.load_html(full_html, base_uri)
            self.statusbar.push(0, f"Loaded: {os.path.basename(file_path)}")

        except Exception as error:
            error_html = ERROR_TEMPLATE.format(
                styles=self.styles,
                theme="dark" if self.dark_theme else "light",
                error_message=str(error)
            )
            self.webview.load_html(error_html, "file:///")
            self.statusbar.push(0, "Error loading file")

    def on_open_clicked(self, button):
        """Handle the open file button click."""
        dialog = Gtk.FileChooserDialog(
            title="Select a Markdown file",
            parent=self,
            action=Gtk.FileChooserAction.OPEN
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN, Gtk.ResponseType.OK
        )

        filter_md = Gtk.FileFilter()
        filter_md.set_name("Markdown files")
        filter_md.add_pattern("*.md")
        filter_md.add_pattern("*.markdown")
        dialog.add_filter(filter_md)

        filter_all = Gtk.FileFilter()
        filter_all.set_name("All files")
        filter_all.add_pattern("*")
        dialog.add_filter(filter_all)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            file_path = dialog.get_filename()
            self.load_file(file_path)

        dialog.destroy()

    def on_refresh_clicked(self, button):
        """Handle the refresh button click."""
        if self.current_file:
            self.load_file(self.current_file)

    def on_print_clicked(self, button):
        """Handle the print button click."""
        if self.current_file:
            print_operation = WebKit2.PrintOperation.new(self.webview)
            print_operation.run_dialog(self)

    def on_theme_toggle(self, button):
        """Handle the theme toggle button click."""
        self.dark_theme = not self.dark_theme
        if self.dark_theme:
            self.webview.set_background_color(Gdk.RGBA(0.1, 0.1, 0.1, 1))
        else:
            self.webview.set_background_color(Gdk.RGBA(1, 1, 1, 1))

        if self.current_file:
            self.load_file(self.current_file)
        else:
            self.show_empty_page()

    def on_zoom_in_clicked(self, button):
        """Handle the zoom in button click."""
        self.zoom_level = min(self.zoom_level * 1.1, 5.0)  # Max 500% zoom
        self.update_zoom()

    def on_zoom_out_clicked(self, button):
        """Handle the zoom out button click."""
        self.zoom_level = max(self.zoom_level / 1.1, 0.2)  # Min 20% zoom
        self.update_zoom()

    def on_zoom_reset_clicked(self, button):
        """Handle the zoom reset button click."""
        self.zoom_level = 1.0
        self.update_zoom()

    def update_zoom(self):
        """Update the zoom level of the WebView."""
        self.webview.set_zoom_level(self.zoom_level)
        self.zoom_level_label.set_text(f"{int(self.zoom_level * 100)}%")

    def on_fullscreen_clicked(self, button):
        """Handle the fullscreen toggle button click."""
        if self.is_fullscreen:
            self.unfullscreen()
        else:
            self.fullscreen()
        self.is_fullscreen = not self.is_fullscreen

    def on_key_press(self, widget, event):
        """Handle key press events."""
        if event.state & Gdk.ModifierType.CONTROL_MASK:
            if event.keyval == Gdk.KEY_plus:
                self.on_zoom_in_clicked(None)
                return True
            elif event.keyval == Gdk.KEY_minus:
                self.on_zoom_out_clicked(None)
                return True
        return False


class MarkdownViewerApp(Gtk.Application):
    """Main application class for the Markdown viewer."""

    def __init__(self):
        """Initialize the application."""
        super().__init__(
            application_id="com.example.markdown-viewer",
            flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE
        )
        self.args = None

    def do_startup(self):
        """Handle application startup."""
        Gtk.Application.do_startup(self)

    def do_activate(self):
        """Handle application activation."""
        win = MarkdownViewer(application=self)
        win.show_all()

        # If there are command line arguments, try to open the first one
        if self.args and len(self.args) > 1:
            win.load_file(self.args[1])

    def do_command_line(self, command_line):
        """Handle command line arguments."""
        self.args = command_line.get_arguments()
        self.activate()
        return 0


def main():
    """Main entry point of the application."""
    app = MarkdownViewerApp()
    return app.run(sys.argv)


if __name__ == "__main__":
    sys.exit(main())
