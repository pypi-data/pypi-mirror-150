import sys

if __name__ == "__main__":

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()

from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt

from zzgui.qt5.zzwidget import ZzWidget

vertical_align_dict = {
    "top": Qt.AlignTop,
    "middle": Qt.AlignVCenter,
    "bottom": Qt.AlignBottom,
}

horizontal_align_dict = {
    "left": Qt.AlignLeft,
    "center": Qt.AlignHCenter,
    "justify": Qt.AlignJustify,
    "right": Qt.AlignRight,
}


class zzlabel(QLabel, ZzWidget):
    def __init__(self, meta={}):
        super().__init__({"label": meta.get("label", ""), "dblclick": meta.get("dblclick")})
        # super().__init__(meta)
        self.set_text(self.meta["label"])
        self.setWordWrap(True)
        self.set_maximum_height(self.get_default_height() * 1.5)

    def set_style_sheet(self, style_text):
        super().set_style_sheet(style_text)

        if "vertical-align" in style_text or "text-align" in style_text:
            if isinstance(style_text, str):
                style_dict = {
                    x[0].strip().replace("{", ""): x[1].strip().replace("}", "")
                    for x in [x.split(":") for x in style_text.split(";") if ":" in x]
                }
            else:
                style_dict = style_text
            CA = vertical_align_dict.get(style_dict.get("vertical-align", "top"), Qt.AlignTop)
            CA |= horizontal_align_dict.get(style_dict.get("text-align", "left"), Qt.AlignLeft)

            self.setAlignment(CA)
