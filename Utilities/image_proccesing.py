from PIL import Image
from typing import Tuple, Union

class ImageProcessor:
    def __init__(self, image_path: str):
        self.image_path: str = image_path
        self.image: Union[Image.Image, None] = None

    def load_image(self) -> None:
        try:
            self.image = Image.open(self.image_path)
            print("Image loaded successfully!")
        except FileNotFoundError:
            print("File not found!")

    def convert_to_grayscale(self, bit_rate: int = 8) -> None:
        if self.image:
            if bit_rate == 8:
                mode = "L"
            elif bit_rate == 1:
                mode = "1"
            else:
                print("Unsupported bit rate! Using default (8-bit).")
                mode = "L"
            self.image = self.image.convert(mode)
            print("Image converted to grayscale with {}-bit rate.".format(bit_rate))
        else:
            print("No image loaded!")

    def resize_image(self, width: int, height: int) -> None:
        if self.image:
            self.image = self.image.resize((width, height))
            print("Image resized to {}x{}.".format(width, height))
        else:
            print("No image loaded!")

    def save_image(self, output_path: str) -> None:
        if self.image:
            self.image.save(output_path)
            print("Image saved successfully!")
        else:
            print("No image loaded!")

    def get_image_as_integers(self) -> Union[None, Tuple[Tuple[int]]]:
        if self.image:
            return tuple(self.image.getdata())
        else:
            print("No image loaded!")
            return None

    def get_image_as_bits(self) -> Union[None, Tuple[Tuple[int]]]:
        if self.image:
            threshold = 128
            width, height = self.image.size
            pixels = self.image.convert("L").getdata()
            bits = []
            for pixel in pixels:
                bit_value = 1 if pixel > threshold else 0
                bits.append(bit_value)
            return tuple(bits[i:i+width] for i in range(0, len(bits), width))
        else:
            print("No image loaded!")

def fun():
    pass

# Example usage:
if __name__ == "__main__":
    folder = "Utilities/Example_Images/"
    file = "buildings.jpg"
    processor = ImageProcessor(f"{folder}{file}")
    processor.load_image()
    processor.convert_to_grayscale(bit_rate=8)
    processor.resize_image(width=8, height=8)
    processor.save_image(f"{folder}processed_{file}")
    integers = processor.get_image_as_integers()
    print(integers[:10])  # Example of displaying first 10 rows of integers
    bits = processor.get_image_as_bits()
    print(bits[:10])  # Example of displaying first 10 rows of bits

    a = fun()
    print(a)
