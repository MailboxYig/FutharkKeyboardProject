import json
import keyboard
import sys
import os

def get_resource_path(relative_path):
    # This checks if the application is running as a script or as a bundled executable
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# 1. Load the mapping from the JSON file
with open(get_resource_path('map.json'), 'r', encoding='utf-8') as f:
    data = json.load(f)
    runes = data['mappings']

    def translate(event):
        # Skip if it's the IME writing itself (to avoid infinite loops)
        if event.event_type != 'down':
            return

        is_shifted = keyboard.is_pressed('shift')
        key = event.name.upper() if is_shifted else event.name.lower()

        mapping = runes['shifted'] if is_shifted else runes['standard']

        if key in mapping:
            # 2. Send backspace to delete the original key
            keyboard.send('backspace')
            # 3. Write the mapped Runic character
            keyboard.write(mapping[key])

    # 4. Start the listener
    print("IME Active. Press ESC to stop.")
    keyboard.hook(translate)
    keyboard.wait('esc')
    input("Press Enter to exit...")