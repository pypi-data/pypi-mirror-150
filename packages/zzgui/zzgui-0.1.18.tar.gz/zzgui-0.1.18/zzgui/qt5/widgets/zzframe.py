if __name__ == "__main__":

    import sys

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()

from PyQt5.QtWidgets import QGroupBox, QSplitter, QSizePolicy
from PyQt5.QtCore import Qt


from zzgui.qt5.zzwindow import ZzFrame
from zzgui.qt5.zzwidget import ZzWidget


class zzframe(QGroupBox, ZzWidget, ZzFrame):
    def __init__(self, meta):
        super().__init__(meta)
        ZzFrame.__init__(self, meta.get("name", "/v")[1])
        self.meta = meta
        self.splitter = None
        self.scroller = None
        if meta.get("name", "")[2:3] == "s":  # Splitter!
            self.splitter = zzsplitter()
            if meta.get("name").startswith("/v"):
                self.splitter.setOrientation(Qt.Orientation.Vertical)
            self.layout().addWidget(self.splitter)
        if meta.get("label") not in ("", "-") and not meta.get("check"):
            self.set_title(meta.get("label"))
        if meta.get("label", "") == "":
            self.hide_border()
        self.setContentsMargins(0, 0, 0, 0)

    def hide_border(self):
        self.setObjectName("grb")
        no_border_style = "QGroupBox#grb {border:0}"
        last_style = self.styleSheet()
        if no_border_style not in last_style:
            self.setStyleSheet(no_border_style + ";" + no_border_style)
        # self.set_title("")

    def set_title(self, title):
        self.setTitle(title)

    def get_widget_count(self):
        return self.layout().count()

    def add_widget(self, widget=None, label=None):
        if self.splitter is not None:
            self.splitter.addWidget(widget)
            if hasattr(widget, "meta"):
                self.splitter.setStretchFactor(self.splitter.count() - 1, widget.meta.get("stretch", 0))
        else:
            return super().add_widget(widget=widget, label=label)


class zzsplitter(QSplitter):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))

    def get_sizes(self):
        return ",".join([f"{x}" for x in self.sizes()])

    def set_sizes(self, sizes):
        if sizes == "":
            init_sizes = [self.widget(x).meta.get("stretch", 1) for x in range(self.count())]
            if sum(init_sizes):
                widget_size = self.width() if self.orientation() is Qt.Horizontal else self.height()
                init_sizes = [str(int(x * widget_size / sum(init_sizes))) for x in init_sizes]
                for x in range(self.count()):
                    widgget = self.widget(x)
                    if widgget.meta.get("control") == "toolbar":
                        init_sizes[x] = str(widgget.sizeHint().height())
                sizes = ",".join(init_sizes)
        if sizes:
            sizes = [int(x) for x in sizes.split(",")]
            self.setSizes(sizes)
