import numpy as np
import matplotlib
import matplotlib.cm as cm
import cv2

def visualize_depth_as_numpy(depth, cmap="jet", is_sparse=True):
    """
    Args:
        data (HxW): depth data
        cmap: color map (inferno, plasma, jet, turbo, magma, rainbow)
    Returns:
        vis_data (HxWx3): depth visualization (RGB)
    """

    # x = depth.cpu().numpy()
    x = np.nan_to_num(depth)  # change nan to 0

    inv_depth = 1 / (x + 1e-6)

    if is_sparse:
        vmax = 1 / np.percentile(x[x != 0], 5)
    else:
        vmax = np.percentile(inv_depth, 95)

    normalizer = matplotlib.colors.Normalize(vmin=inv_depth.min(), vmax=vmax)
    mapper = cm.ScalarMappable(norm=normalizer, cmap=cmap)
    vis_data = (mapper.to_rgba(inv_depth)[:, :, :3] * 255).astype(np.uint8)
    if is_sparse:
        vis_data[inv_depth > vmax] = 0
    return vis_data

def align_contrast(imgL, imgR):
    imgR_mean = np.mean(imgR)
    imgL_mean = np.mean(imgL)
    if imgR_mean < imgL_mean:
        imgR = imgR * imgL_mean / imgR_mean
        imgR = np.clip(imgR, 0, 255)
    else:
        imgL = imgL * imgR_mean / imgL_mean
        imgL = np.clip(imgL, 0, 255)
    return imgL.astype(np.uint8), imgR.astype(np.uint8)

def enhance_image(image):
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    clahe = clahe.apply(image)
    bilateral = cv2.bilateralFilter(clahe, 5, 20, 15)
    return bilateral

def process_image(image_in, type="minmax"):
    if type == "minmax":
        image_out = (image_in - np.min(image_in)) / (np.max(image_in) - np.min(image_in)) * 255
    
    elif type == "firestereo":
        if np.max(image_in) < 35000:
            image_out = (image_in - np.min(image_in)) / (np.max(image_in) - np.min(image_in)) * 255
        else:
            im_srt = np.sort(image_in.reshape(-1))
            upper_bound = im_srt[round(len(im_srt) * 0.99) - 1]
            lower_bound = im_srt[round(len(im_srt) * 0.01)]

            img = image_in
            img[img < lower_bound] = lower_bound
            img[img > upper_bound] = upper_bound
            image_out = ((img - lower_bound) / (upper_bound - lower_bound)) * 255.0
        image_out = enhance_image(image_out.astype(np.uint8))
    
    return image_out.astype(np.uint8)