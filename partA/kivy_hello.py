from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup

class HelloApp(App):

    def build(self):
        layout = BoxLayout(
            orientation="vertical",
            padding=30,
            spacing=20
        )

        self.label = Label(
            text="Hello World!",
            font_size=28
        )

        button = Button(
            text="Click Me",
            font_size=18,
            size_hint=(1, 0.3)
        )

        button.bind(on_press=self.show_message)

        layout.add_widget(self.label)
        layout.add_widget(button)

        return layout

    def show_message(self, instance):
        popup = Popup(
            title="Message",
            content=Label(text="Hello! Welcome to Kivy."),
            size_hint=(0.7, 0.4)
        )
        popup.open()


if __name__ == "__main__":
    HelloApp().run()





    