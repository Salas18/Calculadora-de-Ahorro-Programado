import sys
import os

import kivy

android_path = os.environ.get('ANDROID_APP_PATH', None)

if android_path:
    base_dir = android_path
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, base_dir)
sys.path.insert(0, os.path.join(base_dir, 'src'))
sys.path.insert(0, os.path.join(base_dir, 'src', 'view'))
sys.path.insert(0, os.path.join(base_dir, 'src', 'core'))

from gui_calculadora import CalculadoraAhorroGUI
CalculadoraAhorroGUI().run()
