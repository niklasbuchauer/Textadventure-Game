"""
dialog_overlays.py  –  Modal dialog replacements for messagebox / simpledialog

Provides MessageDialog, ConfirmDialog, and InputDialog as pygame_gui UIWindow
overlays, replacing tkinter.messagebox and tkinter.simpledialog.
"""

import pygame
import pygame_gui
from pygame_gui.elements import (
    UIButton, UILabel, UITextBox, UITextEntryLine, UIWindow,
)
from pygame_gui.core import ObjectID


class MessageDialog:
    """
    A simple modal-style info/warning/error message box.

    Usage:
        dlg = MessageDialog(manager, "Title", "Body text...", width, height)
        # handle dlg.window close event to dismiss
    """

    def __init__(self, manager, title, body, screen_w=800, screen_h=600,
                 ok_text="OK", on_close=None):
        self.manager  = manager
        self.on_close = on_close

        ww, wh = 400, 220
        self.window = UIWindow(
            rect=pygame.Rect((screen_w - ww) // 2,
                             (screen_h - wh) // 2, ww, wh),
            manager=manager,
            window_display_title=title,
        )

        self.body_text = UITextBox(
            html_text=f'<font color="#dcdcdc">{body}</font>',
            relative_rect=pygame.Rect(10, 10, ww - 80, wh - 130),
            manager=manager, container=self.window,
        )

        self.ok_btn = UIButton(
            relative_rect=pygame.Rect((ww - 80) // 2 - 30, wh - 110, 100, 34),
            text=ok_text, manager=manager, container=self.window,
        )

    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.ok_btn:
                self.window.kill()
                if self.on_close:
                    self.on_close()
                return True
        if event.type == pygame_gui.UI_WINDOW_CLOSE:
            if event.ui_element == self.window:
                if self.on_close:
                    self.on_close()
                return True
        return False


class ConfirmDialog:
    """
    A Yes / No confirmation dialog.

    Usage:
        dlg = ConfirmDialog(manager, "Confirm", "Are you sure?",
                            on_yes=my_func, on_no=None)
    """

    def __init__(self, manager, title, body, screen_w=800, screen_h=600,
                 yes_text="Yes", no_text="No",
                 on_yes=None, on_no=None):
        self.manager = manager
        self.on_yes  = on_yes
        self.on_no   = on_no

        ww, wh = 400, 220
        self.window = UIWindow(
            rect=pygame.Rect((screen_w - ww) // 2,
                             (screen_h - wh) // 2, ww, wh),
            manager=manager,
            window_display_title=title,
        )

        self.body_text = UITextBox(
            html_text=f'<font color="#dcdcdc">{body}</font>',
            relative_rect=pygame.Rect(10, 10, ww - 80, wh - 130),
            manager=manager, container=self.window,
        )

        mid = (ww - 80) // 2
        self.yes_btn = UIButton(
            relative_rect=pygame.Rect(mid - 60, wh - 110, 90, 34),
            text=yes_text, manager=manager, container=self.window,
        )
        self.no_btn = UIButton(
            relative_rect=pygame.Rect(mid + 40, wh - 110, 90, 34),
            text=no_text, manager=manager, container=self.window,
        )

    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.yes_btn:
                self.window.kill()
                if self.on_yes:
                    self.on_yes()
                return True
            if event.ui_element == self.no_btn:
                self.window.kill()
                if self.on_no:
                    self.on_no()
                return True
        if event.type == pygame_gui.UI_WINDOW_CLOSE:
            if event.ui_element == self.window:
                if self.on_no:
                    self.on_no()
                return True
        return False


class InputDialog:
    """
    A text input dialog (replaces simpledialog.askstring).

    Usage:
        dlg = InputDialog(manager, "Enter name", "Name:", on_submit=my_func)
    """

    def __init__(self, manager, title, prompt, screen_w=800, screen_h=600,
                 default="", on_submit=None, on_cancel=None):
        self.manager   = manager
        self.on_submit = on_submit
        self.on_cancel = on_cancel

        ww, wh = 400, 200
        self.window = UIWindow(
            rect=pygame.Rect((screen_w - ww) // 2,
                             (screen_h - wh) // 2, ww, wh),
            manager=manager,
            window_display_title=title,
        )

        self.prompt_label = UILabel(
            relative_rect=pygame.Rect(10, 10, ww - 80, 28),
            text=prompt, manager=manager, container=self.window,
        )

        self.entry = UITextEntryLine(
            relative_rect=pygame.Rect(10, 44, ww - 80, 30),
            manager=manager, container=self.window,
        )
        if default:
            self.entry.set_text(default)

        mid = (ww - 80) // 2
        self.ok_btn = UIButton(
            relative_rect=pygame.Rect(mid - 60, wh - 100, 90, 34),
            text="OK", manager=manager, container=self.window,
        )
        self.cancel_btn = UIButton(
            relative_rect=pygame.Rect(mid + 40, wh - 100, 90, 34),
            text="Cancel", manager=manager, container=self.window,
        )

    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.ok_btn:
                val = self.entry.get_text()
                self.window.kill()
                if self.on_submit:
                    self.on_submit(val)
                return True
            if event.ui_element == self.cancel_btn:
                self.window.kill()
                if self.on_cancel:
                    self.on_cancel()
                return True
        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
            if event.ui_element == self.entry:
                val = self.entry.get_text()
                self.window.kill()
                if self.on_submit:
                    self.on_submit(val)
                return True
        if event.type == pygame_gui.UI_WINDOW_CLOSE:
            if event.ui_element == self.window:
                if self.on_cancel:
                    self.on_cancel()
                return True
        return False
