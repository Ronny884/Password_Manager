import sys
from PyQt6.QtWidgets import QApplication

from window_1_start import StartWindowFunctionality
from window_5_new_db import NewDatabaseWindowFunctionality
from window_7_new_note import CreateAndEditNoteWindowFunctionality
from window_3_database_selection import DatabaseSelectionWindowFunctionality, MyEventHandler
from window_4_authorization import AuthorizationWindowFunctionality
from window_9_db_interior import DatabaseInteriorWindowFunctionality
from window_10_look_note import LookNoteWindowFunctionality
from window_generation import GeneratingWindowFunctionality
from encryption_manager import EncryptionManager


if __name__ == "__main__":
    app = QApplication(sys.argv)

    watch_dog_window_3 = MyEventHandler()
    window__1 = StartWindowFunctionality()
    window__5 = NewDatabaseWindowFunctionality()
    window__7 = CreateAndEditNoteWindowFunctionality()
    window__3 = DatabaseSelectionWindowFunctionality()
    window__4 = AuthorizationWindowFunctionality()
    window__9 = DatabaseInteriorWindowFunctionality()
    window__10 = LookNoteWindowFunctionality()
    window__G = GeneratingWindowFunctionality()
    enc = EncryptionManager()
    window__1.show()

    if not enc.check_lock_file():
        sys.exit(1)
    unsafe_windows = window__5, window__7, window__9, window__10
    app.aboutToQuit.connect(lambda: enc.encryption_before_closing_the_program(unsafe_windows))

    window__1.window__5 = window__5
    window__1.window__3 = window__3
    window__1.window__G = window__G

    window__3.window__1 = window__1
    window__3.window__4 = window__4

    watch_dog_window_3.window__3 = window__3
    enc.watch_dog = watch_dog_window_3

    window__4.window__1 = window__1
    window__4.window__3 = window__3
    window__4.window__9 = window__9
    window__4.window__G = window__G

    window__5.window__1 = window__1
    window__5.window__7 = window__7
    window__5.window__9 = window__9
    window__5.window__G = window__G

    window__7.window__5 = window__5
    window__7.window__1 = window__1
    window__7.window__9 = window__9
    window__7.window__10 = window__10
    window__7.window__G = window__G

    window__9.window__1 = window__1
    window__9.window__3 = window__3
    window__9.window__7 = window__7
    window__9.window__10 = window__10

    window__10.window__9 = window__9
    window__10.window__7 = window__7
    window__10.window__1 = window__1

    window__G.window__1 = window__1
    window__G.window__5 = window__5
    window__G.window__7 = window__7

    sys.exit(app.exec())
