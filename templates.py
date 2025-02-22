MAIN_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>{styles}</style>
</head>
<body class="{theme}-theme">
    {content}
</body>
</html>
"""

EMPTY_PAGE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>{styles}</style>
</head>
<body class="{theme}-theme">
    <h1>Markdown Viewer</h1>
    <p>Open a markdown file to get started (Ctrl+O)</p>
    <div class="keyboard-shortcuts">
        <h2>Keyboard Shortcuts</h2>
        <table>
            <tr>
                <th>Action</th>
                <th>Shortcut</th>
            </tr>
            <tr>
                <td>Open File</td>
                <td>Ctrl+O</td>
            </tr>
            <tr>
                <td>Refresh</td>
                <td>Ctrl+R</td>
            </tr>
            <tr>
                <td>Print</td>
                <td>Ctrl+P</td>
            </tr>
            <tr>
                <td>Zoom In</td>
                <td>Ctrl++</td>
            </tr>
            <tr>
                <td>Zoom Out</td>
                <td>Ctrl+-</td>
            </tr>
            <tr>
                <td>Reset Zoom</td>
                <td>Ctrl+0</td>
            </tr>
            <tr>
                <td>Toggle Fullscreen</td>
                <td>F11</td>
            </tr>
        </table>
    </div>
</body>
</html>
"""

ERROR_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>{styles}</style>
</head>
<body class="{theme}-theme">
    <h1>Error</h1>
    <p>{error_message}</p>
    <p>Please check if the file exists and is readable.</p>
</body>
</html>
"""
