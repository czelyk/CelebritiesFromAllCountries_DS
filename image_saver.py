import os


class ImageSaver:
    def __init__(self, images_folder=None):
        # Set the absolute path to 'pictures' folder located outside the 'code' folder
        if images_folder is None:
            # Get the path of the root directory (two levels up from 'code')
            root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            images_folder = os.path.join(root_folder, "pictures")

        self.images_folder = images_folder

    def save_image(self, image_data, file_name):
        # Ensure the folder exists
        if not os.path.exists(self.images_folder):
            os.makedirs(self.images_folder)

        # Save the image in the correct folder
        file_path = os.path.join(self.images_folder, file_name)
        with open(file_path, 'wb') as f:
            f.write(image_data)
        print(f"Image saved as {file_path}")
        return file_path
