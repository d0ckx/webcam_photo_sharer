import time
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.clipboard import Clipboard
from filesharer import FileSharer
import webbrowser

# load frontend
Builder.load_file("frontend.kv")


# boilaerplate kivy code for start screen
class CameraScreen(Screen):

    def start(self):
        # turn the camera app to be visible for user
        self.ids.camera.opacity = 1
        self.ids.camera.play = True
        self.ids.camera_button.text = 'Stop Camera'
        # turn camera texture back to normal
        self.ids.camera.texture = self.ids.camera._camera.texture

    def stop(self):
        # turn the camera opacity back to 0, make the widget invisible to user
        self.ids.camera.opacity = 0
        self.ids.camera.play = False
        self.ids.camera_button.text = 'Start Camera'
        # return camera screen to blank
        self.ids.camera.texture = None


    def capture(self):
        current_time = time.strftime("%Y%m%d-%H%M%S")
        self.filepath = f"files/{current_time}.png"
        self.ids.camera.export_to_png(self.filepath)
        # change screen to the second screen
        self.manager.current = 'image_screen'
        # display the image captured on second screen
        self.manager.current_screen.ids.img.source = self.filepath

# boilaerplate kivy code for second screen
class ImageScreen(Screen):

    link_message = "Create a Link First"

    def create_link(self):
        # this brings us to the current instance of CameraScreen and gets filepath variable
        file_path = App.get_running_app().root.ids.camera_screen.filepath
        # create the link with the filesharer code
        filesharer = FileSharer(filepath=file_path)
        self.url = filesharer.share()
        # get access to kv label to display url
        self.ids.link.text = self.url

    def copy_link(self):
        try:
            Clipboard.copy(self.url)
        except:
            self.ids.link.text = self.link_message

    def open_link(self):
        try:
            webbrowser.open(self.url)
        except:
            self.ids.link.text = self.link_message

# boilaerplate kivy code
class RootWidget(ScreenManager):
    pass

# boilaerplate kivy code
class MainApp(App):

    def build(self):
        return RootWidget()


# instantiate class/ run app
MainApp().run()