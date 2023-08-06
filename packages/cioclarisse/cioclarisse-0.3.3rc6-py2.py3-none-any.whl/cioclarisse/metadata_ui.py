"""
Provides a window in which to add metadata entries.

This is required because Clarisse's attribute editor doesn't allow
custom UI to be embedded.
"""

import json
import ix
from cioclarisse import refresh

BTN_HEIGHT = 22
BTN_WIDTH = 100
WINDOW_LEFT = 600
WINDOW_TOP = 200
HEIGHT = 300
WIDTH = 900
PADDING = 5

SYMBOL_BUT_WIDTH = 30
# CHECKBOX_WIDTH = 50

BOTTOM_BUT_WIDTH = WIDTH // 2
VAR_WDG_WIDTH = 300
VAL_WDG_WIDTH = WIDTH - (
    SYMBOL_BUT_WIDTH + VAR_WDG_WIDTH + (PADDING * 4)
)


class KVWidget(ix.api.GuiWidget):
    """
    This is a line item containing UI for one kv pair.

    We have a button to delete the line. We inherit because
    GuiWidget::get_child_items is broken and we have to have a way to store the
    children.
    """

    def __init__(self, parent, y_val, entry):
        super(KVWidget, self).__init__(parent, PADDING, y_val, WIDTH, BTN_HEIGHT)
        x_val = PADDING
        self.var_widget = ix.api.GuiLineEdit(
            self, x_val, y_val, VAR_WDG_WIDTH, BTN_HEIGHT
        )
        x_val += VAR_WDG_WIDTH + PADDING
        self.val_widget = ix.api.GuiLineEdit(
            self, x_val, y_val, VAL_WDG_WIDTH, BTN_HEIGHT
        )
        x_val += VAL_WDG_WIDTH + PADDING
        
        self.delete_btn = ix.api.GuiPushButton(
            self, x_val, y_val, SYMBOL_BUT_WIDTH, BTN_HEIGHT, "X"
        )

        self.var_widget.set_text(str(entry.get("key", "Key")))
        self.val_widget.set_text(str(entry.get("value", "Value")))
        self.show()

    def index(self):
        """
        Calculates the index of this widget in the list.

        Returns:
            int: The index, derived from y-pos so that we don't have to
            maintain another variable each time a line is added or deleted.
        """
        return (self.get_y() - PADDING - BTN_HEIGHT) // BTN_HEIGHT

    def set_y_index(self, index):
        """
        Adjust this widget's height based on its list position.

         Notice here we can't simply set the height of the container.
        Widgets locations are relative to the window, not their direct
        parent. In fact the only reason to set the parent's position is
        OCD.

        Args:
            index (int): index in the list of widgets.
        """
        y_val = ((index + 1) * BTN_HEIGHT) + PADDING
        self.set_position(self.get_x(), y_val)
        self.var_widget.set_position(self.var_widget.get_x(), y_val)
        self.val_widget.set_position(self.val_widget.get_x(), y_val)
        self.delete_btn.set_position(self.delete_btn.get_x(), y_val)

    def to_json(self):
        """
        Serialize for storage in the node's attribute.

        Returns:
            string: The entry as json
        """
        return json.dumps(
            {
                "key": self.var_widget.get_text(),
                "value": self.val_widget.get_text()
            },
            sort_keys=True
        )


class MetadataListWidget(ix.api.GuiPanel):
    """
    The panel within the window that provides scrollbars.
    """

    def __init__(self, parent, y_val):
        """
        Configure the panel and initialize an item_list.

        Since the GuiPanel::get_child_items is broken, we have to
        maintain our own list of children, and in fact this is the only
        reason for inheriting rather than using GuiPanel directly.

        Args:
            parent (GuiWidget): Widget that this widget sits in.
            y_val (int): location of top of widget.
        """
        super(MetadataListWidget, self).__init__(parent, 0, y_val, WIDTH, HEIGHT)
        self.set_scroll_enabled(True)
        self.set_bottom_toolbar_visible(False)
        self.set_top_toolbar_visible(False)
        self.item_list = []

    def _items_height(self):
        """
        Calculate the total height of items.

        Need this in order to add new items at the bottom, and to tell
        the scollable area how big the virtual space is.

        Returns:
            int: height of items.
        """
        return PADDING + ((len(self.item_list) + 1) * BTN_HEIGHT)

    def add_entries(self, *entries):
        """
        Add a line for each entry and hook up the delete button event.
        """
        for entry in entries:
            y_val = self._items_height()
            wdg = KVWidget(self, y_val, entry)
            self.item_list.append(wdg)
            self.connect(wdg.delete_btn, "EVT_ID_PUSH_BUTTON_CLICK", self.on_remove_but)

        self.set_virtual_size(self.get_width(), self._items_height())

    def on_remove_but(self, sender, eventid):
        """
        Remove from view.

        We have to keep the item_list in sync.

        Args:
            sender (GuiButton): button that sent the event.
        """
        parent = sender.get_parent()
        i = parent.index()
        parent.hide()
        parent.destroy()
        self.item_list.pop(i)
        self._arrange_items()

    def _arrange_items(self):
        """
        Stack the items up correctly
        """
        for i, item in enumerate(self.item_list):
            item.set_y_index(i)


class MetadataWindow(ix.api.GuiWindow):
    """
    The entire window.

    Holds the panel plus buttons to Add, Go, Cancel and so on.
    """

    def __init__(self, node):
        self.node = node
        window_height = HEIGHT + (BTN_HEIGHT * 2)

        super(MetadataWindow, self).__init__(
            ix.application.get_event_window(),
            WINDOW_LEFT,
            WINDOW_TOP,
            WIDTH,
            window_height,
            "Metadata",
        )

        current_y = 0
        self.add_but = ix.api.GuiPushButton(
            self, (WIDTH - BTN_WIDTH), current_y, BTN_WIDTH, BTN_HEIGHT, "Add"
        )
        self.connect(self.add_but, "EVT_ID_PUSH_BUTTON_CLICK", self.on_add_but)

        current_y += BTN_HEIGHT
        self.panel = MetadataListWidget(self, BTN_HEIGHT)
        current_y += HEIGHT

        self.close_but = ix.api.GuiPushButton(
            self, 0, current_y, BOTTOM_BUT_WIDTH, BTN_HEIGHT, "Close"
        )
        self.connect(self.close_but, "EVT_ID_PUSH_BUTTON_CLICK", self.on_close_but)

        self.go_but = ix.api.GuiPushButton(
            self,
            (WIDTH - BOTTOM_BUT_WIDTH),
            current_y,
            BOTTOM_BUT_WIDTH,
            BTN_HEIGHT,
            "Go",
        )
        self.connect(self.go_but, "EVT_ID_PUSH_BUTTON_CLICK", self.on_go_but)

        self.set_resizable(False)

    def on_add_but(self, sender, eventid):
        """
        Responds to add button press by adding an empty entry.
        """
        self.panel.add_entries({})

    def on_close_but(self, sender, eventid):
        """
        Hides only.
        """
        self.hide()

    def on_go_but(self, sender, eventid):
        """
        Saves values on the attribute and hide(destroy) the window.
        """
        self._apply()
        self.hide()

    def _apply(self):
        """
        The real work of saving values on the attribute.
        """
        attr = self.node.get_attribute("metadata")
        attr.remove_all()
        for item in self.panel.item_list:
            attr.add_string(item.to_json())
        refresh.force_ae_refresh(self.node)


def build(*args):
    """
    Show the window.

    Populate it with existing entries from the metadata attribute. The
    window is shown in modal mode so we don't keep losing the damn thing
    behind other stuff.

    Listen for events until the window is hidden.
    """
    node = args[0]
    win = MetadataWindow(node)

    attr = node.get_attribute("metadata")
    json_entries = ix.api.CoreStringArray()
    attr.get_raw_values(json_entries)
    entries = []
    for entry in json_entries:
        try:
            r = json.loads(entry)
            entries.append(json.loads(entry))
        except BaseException:
            pass
    if not entries:
        entries = [{}]
    win.panel.add_entries(*entries)

    win.show_modal()
    while win.is_shown():
        ix.application.check_for_events()
