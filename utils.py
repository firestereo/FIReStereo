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

def process_image(image_in, type="minmax"):
    if type == "minmax":
        image_out = (image_in - np.min(image_in)) / (np.max(image_in) - np.min(image_in)) * 255
    return image_out.astype(np.uint8)