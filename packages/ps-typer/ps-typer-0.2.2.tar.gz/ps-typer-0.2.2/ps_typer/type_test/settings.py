from pathlib import Path

from PyQt5 import QtCore, QtWidgets

from ps_typer.data.user_preferences_handler import UserPreferencesDataHandler
from ps_typer.data.utils import PATH_SOUNDS
from ps_typer.type_test.components import Switch
from ps_typer.ui import settings_window


class SettingsWindow(QtWidgets.QWidget, settings_window.Ui_settingsWindow):
    def __init__(
        self, user_preferences_handler: UserPreferencesDataHandler, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)

        self.setupUi(self)
        self.user_preferences_handler: UserPreferencesDataHandler = (
            user_preferences_handler
        )

        # Switches
        self._setup_switches()
        if self.user_preferences_handler.preferences.dark_mode:
            self.toggleDarkMode.setChecked(True)

        # Keystroke sounds
        if self.user_preferences_handler.preferences.play_sound:
            self.toggleKeystrokeSound.setChecked(True)
        self._set_sounds_options()
        self._set_selected_sound_option()

    def _get_switch(self):
        return Switch(**self.user_preferences_handler.preferences.colours["switch"])

    def _replace_checkbox(
        self,
        layout: QtWidgets.QHBoxLayout,
        checkbox: QtWidgets.QCheckBox,
        switch: Switch,
    ) -> None:
        layout.replaceWidget(checkbox, switch)
        checkbox.close()

    def _setup_switches(self):
        """Replace placeholder checkboxes with custom toggle switches"""

        self.toggleDarkMode = self._get_switch()
        self.toggleKeystrokeSound = self._get_switch()

        self._replace_checkbox(
            self.layoutKeystrokeSounds,
            self.checkBoxToggleSounds,
            self.toggleKeystrokeSound,
        )
        self._replace_checkbox(
            self.layoutDarkMode, self.checkBoxDarkMode, self.toggleDarkMode
        )

    def _set_sounds_options(self) -> None:
        """
        Sets up options for the dropdown menu to select keystroke sounds in the
        settings menu.
        """

        sound_file: Path
        for sound_file in PATH_SOUNDS.iterdir():
            self.comboSelectSound.addItem(sound_file.name)

    def _find_sound_file_index(self, sound_file: str) -> int:
        """
        Returns the index of the given file name within the settings window
        comboSelectSound object.
        """

        return self.comboSelectSound.findText(sound_file, QtCore.Qt.MatchFixedString)

    def _set_selected_sound_option(self) -> None:
        """
        Sets the selected option for sound file from the settings window's
        comboSelectSound object to the given sound file name.
        """

        index: int = self._find_sound_file_index(
            self.user_preferences_handler.preferences.sound_filename
        )

        if index >= 0:
            self.comboSelectSound.setCurrentIndex(index)

    def apply_settings(self) -> None:
        """Updates preference values according to values selected in the UI."""

        is_dark_mode: bool = self.toggleDarkMode.isChecked()
        is_play_sound: bool = self.toggleKeystrokeSound.isChecked()
        sound_filename = str(self.comboSelectSound.currentText())

        if is_dark_mode != self.user_preferences_handler.preferences.dark_mode:
            self.user_preferences_handler.toggle_dark_mode()

        if is_play_sound != self.user_preferences_handler.preferences.play_sound:
            self.user_preferences_handler.toggle_play_sound()

        if sound_filename != self.user_preferences_handler.preferences.sound_filename:
            self.user_preferences_handler.set_sound_filename(sound_filename)
