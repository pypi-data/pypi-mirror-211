from PyQt6.QtCore import QTranslator, QLibraryInfo, QLocale
from PyQt6.QtWidgets import QApplication
from .Environment import Environment
import sys
import os


def main():
    if not os.path.isdir(os.path.join(os.path.dirname(__file__), "ui_compiled")):
        print("Could not find compiled ui files. Please run tools/CompileUI.py first.", file=sys.stderr)
        sys.exit(1)

    app = QApplication(sys.argv)

    env = Environment()

    app.setDesktopFileName("page.codeberg.JakobDev.jdFlatpakSnapshot")
    app.setApplicationName("jdFlatpakSnapshot")
    app.setWindowIcon(env.icon)

    app_translator = QTranslator()
    qt_translator = QTranslator()
    app_trans_dir = os.path.join(env.program_dir, "translations")
    qt_trans_dir = QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath)
    language = env.settings.get("language")
    if language == "default":
        system_language = QLocale.system().name()
        app_translator.load(os.path.join(app_trans_dir, "jdFlatpakSnapshot_" + system_language.split("_")[0] + ".qm"))
        app_translator.load(os.path.join(app_trans_dir, "jdFlatpakSnapshot_" + system_language + ".qm"))
        qt_translator.load(os.path.join(qt_trans_dir, "qt_" + system_language.split("_")[0] + ".qm"))
        qt_translator.load(os.path.join(qt_trans_dir, "qt_" + system_language + ".qm"))
    elif language == "en":
        pass
    else:
        app_translator.load(os.path.join(app_trans_dir, "jdFlatpakSnapshot_" + language + ".qm"))
        qt_translator.load(os.path.join(qt_trans_dir, "qt_" + language.split("_")[0] + ".qm"))
        qt_translator.load(os.path.join(qt_trans_dir, "qt_" + language + ".qm"))
    app.installTranslator(app_translator)
    app.installTranslator(qt_translator)

    from .MainWindow import MainWindow

    main_window = MainWindow(env)
    main_window.show()

    if env.settings.get("showWelcomeDialog"):
        main_window.welcome_dialog.open_dialog()

    sys.exit(app.exec())
