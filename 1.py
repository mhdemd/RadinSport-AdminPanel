from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

KV = '''
BoxLayout:
    orientation: 'vertical'
    spacing: 10



    FloatLayout:
        MDRaisedButton:
            text: "Open Dialog"
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            on_release: app.show_dialog()
'''

class MyApp(MDApp):
    dialog = None

    def build(self):
        return Builder.load_string(KV)

    def show_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Choose an action:",
                type="custom",
                content_cls=Builder.load_string('''
MDBoxLayout:
    orientation: 'vertical'
    spacing: 10
    size_hint_x: 1
    adaptive_height: True


    MDRectangleFlatIconButton:
        icon: "plus-box-multiple"
        text: "Add a new category"
        pos_hint: {'center_x': .5}
        size_hint_x: .5
        on_release: app.add_category()

    MDRectangleFlatIconButton:
        icon: "plus-box-multiple"
        text: "Adding a new product"
        pos_hint: {'center_x': .5}
        size_hint_x: .5
        on_release: app.add_new_product()

    MDRectangleFlatIconButton:
        icon: "plus-box-multiple"
        text: "Adding new variety"
        pos_hint: {'center_x': .5}
        size_hint_x: .5
        on_release: app.add_new_variety()
'''),
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        on_release=self.close_dialog
                    ),
                ],
            )
        self.dialog.open()

    def close_dialog(self, *args):
        self.dialog.dismiss()

    def add_category(self):
        print("Add a category")
        self.close_dialog()

    def add_new_product(self):
        print("Adding a new product")
        self.close_dialog()

    def add_new_variety(self):
        print("Adding new variety")
        self.close_dialog()

MyApp().run()
