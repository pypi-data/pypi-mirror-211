import argparse
from PIL import Image, ImageEnhance, ImageOps
import bottomofthesea.preprocess
import os, sys, subprocess
import numpy as np
import cv2

# Check if the script is bundled by PyInstaller
if getattr(sys, "frozen", False):
    # Get the path to the temporary folder created by PyInstaller
    script_dir = sys._MEIPASS
else:
    # Get the path of the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the lib folder
lib_path = os.path.join(script_dir, "lib")

# Add the lib folder to the system path
sys.path.append(lib_path)


class Steganography:
    BLACK_PIXEL = (0, 0, 0)
    EMPTY_PIXEL = (169, 169, 169, 0)
    RESOLUTION = None
    # RESOLUTION = (1550,2060)
    # RESOLUTION = (1080,1440)

    def _int_to_bin(self, rgb):
        """Convert an integer tuple to a binary (string) tuple.

        :param rgb: An integer tuple like (220, 110, 96, 220)
        :return: A string tuple like ("00101010", "11101011", "00010110", "00101010")
        """
        if len(rgb) == 3:
            (
                r,
                g,
                b,
            ) = rgb
            return f"{r:08b}", f"{g:08b}", f"{b:08b}"
        else:
            r, g, b, a = rgb
            return f"{r:08b}", f"{g:08b}", f"{b:08b}", f"{a:08b}"

    def _bin_to_int(self, rgb):
        """Convert a binary (string) tuple to an integer tuple.

        :param rgb: A  string tuple like ("00101010", "11101011", "00010110", "00101010")
        :return: Return an int tuple like (220, 110, 96, 220)
        """
        if len(rgb) == 3:
            (
                r,
                g,
                b,
            ) = rgb
            return int(r, 2), int(g, 2), int(b, 2)
        else:
            r, g, b, a = rgb
            return int(r, 2), int(g, 2), int(b, 2), int(a, 2)

    def _decode_rgb(self, rgb):
        """decode an image.

        :param rgb: An integer tuple like (220, 110, 96, 255)
        :return: An integer tuple with the two RGB values merged.
        """
        if len(rgb) == 3:
            r, g, b = self._int_to_bin(rgb)
            new_rgb = r[5:] + "0000", g[5:] + "0000", b[5:] + "0000"
            return self._bin_to_int(new_rgb)
        elif len(rgb) == 4:
            r, g, b, a = self._int_to_bin(rgb)
            # @scoop
            # account for the alpha channel that might have been added during the encoding process
            new_rgba = r[5:] + "0000", g[5:] + "0000", b[5:] + "0000", "11111111"
            return self._bin_to_int(new_rgba)

    def _decode_rgb_half(self, rgb_top, rgb_bottom):
        """decode an image.

        :param rgb: Two integer tuples like (220, 110, 96, 255),  (213, 133, 96, 255)
        :return: An integer tuple with the two RGB values merged
        """
        if len(rgb_top) == 3:
            r1, g1, b1 = self._int_to_bin(rgb_top)
            r2, g2, b2 = self._int_to_bin(rgb_bottom)
            new_rgb = (
                r1[6:] + r2[6:] + "0000",
                g1[6:] + g2[6:] + "0000",
                b1[6:] + b2[6:] + "0000",
            )
            return self._bin_to_int(new_rgb)
        elif len(rgb_top) == 4:
            r1, g1, b1, a1 = self._int_to_bin(rgb_top)
            r2, g2, b2, a2 = self._int_to_bin(rgb_bottom)
            # @scoop
            # account for the alpha channel that might have been added during the encoding process
            r = r1[4:6] + r2[6:] + "0000"
            new_rgba = (
                r1[6:] + r2[6:] + "0000",
                g1[6:] + g2[6:] + "0000",
                b1[6:] + b2[6:] + "0000",
                "11111111",
            )
            return self._bin_to_int(new_rgba)

    def crop(self, pixel_map):
        """
        Takes a pixel_map (a PixelAcess object) and crops
        following the original size recorded in the first two pixels.
        """

        ww = reversed(tuple(pixel_map[0, 0]))
        hh = reversed(tuple(pixel_map[0, 1]))

        w, h = "", ""
        for i in ww:
            w += str(i)
        for i in hh:
            h += str(i)

        if w[-1] != 255:
            w = w[:-1] + str(1)
        if h[-1] != 255:
            h = h[:-1] + str(1)

        # manual fix for edge cases
        if int(w) < 200:
            w = str(w) + str(0)

        w, h = int(w), int(h)

        if h > self.RESOLUTION[1]:
            h = h // 2

        return w - 1, h - 1

    def open_file(filepath):
        if sys.platform == "win32":
            os.startfile(filepath)
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, filepath])

    def get_input():
        video = input("which video do you want to decode?(e.g. 02ss.mov): ")
        seconds = input(
            "You shall choose a second in video to see different contents(put one number 1~10): "
        )
        return (video, seconds)

    def found_video(filename):
        # Try this folder
        file_path = os.path.join(os.getcwd(), filename)
        if os.path.exists(file_path):
            return True, file_path
        else:
            # Try the parent folder
            parent_folder = os.path.dirname(os.getcwd())
            file_path = os.path.join(parent_folder, filename)
            if os.path.exists(file_path):
                return True, file_path
            else:
                # Try the '/Downloads' folder
                downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
                file_path = os.path.join(downloads_folder, filename)
                if os.path.exists(file_path):
                    return True, file_path
                else:
                    return False, "no_path"

    def decode(self, image):
        """decode an image.

        :param image: The input image.
        :return: The unmerged/extracted image.
        """
        pixel_map = image.load()

        # Create the new image and load the pixel map
        new_image = Image.new(image.mode, (self.crop(pixel_map)))
        new_map = new_image.load()

        for i in range(new_image.size[0]):  # w
            if new_image.size[1] < self.RESOLUTION[1] // 2:
                for j in range(int(np.floor(new_image.size[1]))):  # h
                    new_map[i, j] = self._decode_rgb_half(
                        pixel_map[i, j], pixel_map[i, j + (self.RESOLUTION[1] / 2 - 1)]
                    )
            else:
                for j in range(self.RESOLUTION[1] // 2):  # h
                    new_map[i, j] = self._decode_rgb_half(
                        pixel_map[i, j], pixel_map[i, j + (self.RESOLUTION[1] / 2 - 1)]
                    )

        return Image.fromarray(cv2.cvtColor(np.array(new_image), cv2.COLOR_BGR2RGB))


def main():
    print(
        "Welcome to the land at the bottom of the sea. \nI want to show you something.\n\n"
    )
    parser = argparse.ArgumentParser(description="Steganography")
    subparser = parser.add_subparsers(dest="command")

    video, seconds = Steganography.get_input()
    print(f"got {video}")
    args = parser.parse_args()

    # check video path
    while not Steganography.found_video(video)[0]:
        video, seconds = Steganography.get_input()
        print(
            f"The file {video} was not found in the expected location. Suggestions: Check typo. Move the video to the same directory with this folder.\n "
        )
    if Steganography.found_video(video)[0]:
        path = Steganography.found_video(video)[1]
        images = bottomofthesea.preprocess.prepareFrames(path, seconds)
        Steganography.RESOLUTION = bottomofthesea.preprocess.get_video_size(path)
        for i in images:
            img = Image.fromarray(i)
            # img.show()
            Steganography().decode(img).show()


if __name__ == "__main__":
    main()
