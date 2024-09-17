import cv2
import os
import argparse
from utils import process_image, visualize_depth_as_numpy, align_contrast
import numpy as np
from imageio import imread

parser = argparse.ArgumentParser()
parser.add_argument("--dir", help="Path to the folder containing images")
parser.add_argument(
    "--skip",
    type=int,
    default=20,
    help="Number of frames to jump when pressing 'q' or 'e'",
)
parser.add_argument("--options", default="thermal", help="Display: thermal (default), depth")
parser.add_argument("--align_contrast", action="store_true", help="Align contrast of images")


def display_images(folder_path, frame_jump, contrast=False):

    image_left_files = None
    img_right_files = None
    image_files = None

    # if folder_path has img_left and img_right, then display both images side by side
    if os.path.exists(os.path.join(folder_path, "img_left")):
        img_left_folder = os.path.join(folder_path, "img_left")
        img_right_folder = os.path.join(folder_path, "img_right")
        image_left_files = [f for f in os.listdir(img_left_folder) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
        img_right_files = [f for f in os.listdir(img_right_folder) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
        image_left_files.sort()
        img_right_files.sort()
    else:
        image_files = [f for f in os.listdir(folder_path) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
        image_files.sort()

    current_index = 0
    delete_list = []
    view_lines = False

    cv2.namedWindow("Image Viewer", cv2.WINDOW_NORMAL)

    while True:
        if args.options == "depth":
            image_path = os.path.join(folder_path, image_files[current_index])
            image = np.array(imread(image_path).astype(np.float32)) / 256.0
            image = visualize_depth_as_numpy(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        elif args.options == "thermal":
            if image_left_files is not None and img_right_files is not None:#stereo
                image_left_path = os.path.join(img_left_folder, image_left_files[current_index])
                image_right_path = os.path.join(img_right_folder, img_right_files[current_index])
                image_left = process_image(cv2.imread(image_left_path, cv2.IMREAD_UNCHANGED))
                image_right = process_image(cv2.imread(image_right_path, cv2.IMREAD_UNCHANGED))
                if contrast:
                    image_left, image_right = align_contrast(image_left, image_right)

                image = cv2.hconcat([image_left, image_right])
                image_path = image_left_path
                image_files = image_left_files
            else:#mono
                image_path = os.path.join(folder_path, image_files[current_index])
                image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
                image = process_image(image)

        # if image is grey scale, convert to RGB
        if len(image.shape) == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)

        # Add text to the top left corner
        image_name = os.path.basename(image_path)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.75

        # draw lines on the image
        if view_lines:
            for i in range(0, image.shape[0], 50):
                cv2.line(image, (0, i), (image.shape[1], i), (0, 0, 255), 1)

        if image_path in delete_list:
            font_color = (0, 0, 255)
        else:
            font_color = (255, 0, 0)
        font_thickness = 2
        cv2.putText(
            image,
            f"Idx {current_index}: {image_name}",
            (10, 20),
            font,
            font_scale,
            font_color,
            font_thickness,
        )

        cv2.imshow("Image Viewer", image)

        key = cv2.waitKey(0)

        if key == 27:  # Press 'Esc' to exit
            break
        elif key == 81 or key == 63234:  # Left arrow key
            current_index = (current_index - 1) % len(image_files)
        elif key == 83 or key == 63235:  # Right arrow key
            current_index = (current_index + 1) % len(image_files)
        elif key == ord("["):  # '[' key to go backward by 10 frames
            current_index = (current_index - frame_jump) % len(image_files)
        elif key == ord("]"):  # ']' key to go forward by 10 frames
            current_index = (current_index + frame_jump) % len(image_files)
        elif key == ord("p"):  # 'p' key to print image name on terminal
            print(f"Current Image Name: {image_name}")
        elif key == ord("d"):
            delete_list.append(image_path)
            print(f"Added {image_name} to delete list")
        elif key == ord("l"):
            view_lines = not view_lines
            print(f"Lines are {'on' if view_lines else 'off'}")

    cv2.destroyAllWindows()

    if len(delete_list) > 0:
        print("The following files will be deleted:")
        for file in delete_list:
            print(file)

        user_input = input("Do you want to delete these files? (y/n): ")
        if user_input.lower() == "y":
            for file in delete_list:
                os.remove(file)
            print("Files deleted successfully")
        else:
            print("Files not deleted")


if __name__ == "__main__":
    args = parser.parse_args()

    display_images(args.dir, args.skip, args.align_contrast)
