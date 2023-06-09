import requests
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.network.urlrequest import UrlRequest

def upload_image(file_path):
    upload_url = 'http://your_flask_api_host/upload'
    
    # Prepare the request with the image file
    files = {'image': open(file_path, 'rb')}
    
    # Send the POST request to upload the image
    response = requests.post(upload_url, files=files)
    
    # Check the response
    if response.status_code == 200:
        print('Image uploaded successfully.')
    else:
        print('Image upload failed:', response.text)

class FileSelectionApp(App):
    def build(self):
        filechooser = FileChooserListView()
        button = Button(text='Upload', size_hint=(1, 0.1))
        button.bind(on_release=lambda x: self.select_and_upload(filechooser.path))
        layout = self.create_layout(filechooser, button)
        return layout

    def create_layout(self, filechooser, button):
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(filechooser)
        layout.add_widget(button)
        return layout

    def select_and_upload(self, file_path):
        if file_path:
            upload_image(file_path)
        else:
            print('No file selected.')

if __name__ == '__main__':
    FileSelectionApp().run()
