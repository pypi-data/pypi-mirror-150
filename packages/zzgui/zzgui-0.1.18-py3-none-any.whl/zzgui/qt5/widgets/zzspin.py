import sys

if __name__ == "__main__":

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()

from PyQt5.QtWidgets import QSpinBox

from zzgui.qt5.zzwidget import ZzWidget
from zzgui.zzutils import int_


class zzspin(QSpinBox, ZzWidget):
    def __init__(self, meta):
        super().__init__(meta)
        self.meta = meta
        self.set_text(meta.get("data"))
        if self.meta.get("valid"):
            self.valueChanged.connect(self.meta.get("valid"))

    def set_text(self, text):
        self.setValue(int_(text))
