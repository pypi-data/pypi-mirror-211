import base64

import torch
from torchvision.ops import nms
import numpy as np
import rasterio as rio
import cv2

from mmengine.config import Config
from mmengine.runner import Runner
from shapely.geometry import box


def read_raster(tif_url, GAC_PATH=None):
    with rio.Env(
        GOOGLE_APPLICATION_CREDENTIALS=GAC_PATH,
    ):
        r = rio.open(tif_url)
        img = r.read()
    return r, img


def rio2patches(img_r, cfg):
    """this function read a rio image and creates patches based on cfg.window and cfg.stride.
    return list of patches (patches x window_height x window_width) and list of location of patches (x1, y1, x2, y2).
    Make sure every pixel of image is included in patches. We cannot ignore left and bottom sides.
    Duplicates are okay.
    """
    window_height, window_width = cfg.window
    stride_height, stride_width = cfg.stride

    img_height, img_width = img_r.shape[1], img_r.shape[2]

    if window_height > img_height:
        window_height = img_height

    if window_width > img_width:
        window_width = img_width

    patches = []
    locs = []

    for i in range(0, img_height, stride_height):
        for j in range(0, img_width, stride_width):
            if img_height < i + window_height:
                y_start = img_height - window_height
                y_end = img_height
            else:
                y_start = i
                y_end = i + window_height

            if img_width < j + window_width:
                x_start = img_width - window_width
                x_end = img_width
            else:
                x_start = j
                x_end = j + window_width

            patch = img_r[:, y_start:y_end, x_start:x_end]

            patches.append(patch)
            locs.append([x_start, y_start])

    return np.array(patches, dtype=np.float32), locs


def merge_seg_patches(mask_patches, location_of_patches):
    """use location of patches to merge logits of patches
    (patches x num_classes x window_height x window_width),
    in case of overlapping area use average of logits.
    After that apply softmax to the num_classes chanel.
    this should return a array of dimension (img_height, img_width)"""

    mask_patches = mask_patches.cpu().detach().numpy()
    num_classes = mask_patches.shape[1]
    window_height, window_width = mask_patches.shape[2], mask_patches.shape[3]
    img_height, img_width = (
        location_of_patches[-1][1] + window_height,
        location_of_patches[-1][0] + window_width,
    )

    merged_logits = np.zeros((num_classes, img_height, img_width))
    overlap_count = np.zeros((num_classes, img_height, img_width))

    for i, patch in enumerate(mask_patches):
        x1, y1 = location_of_patches[i]
        x2, y2 = x1 + window_width, y1 + window_height
        merged_logits[:, y1:y2, x1:x2] += patch
        overlap_count[:, y1:y2, x1:x2] += 1

    averaged_merged_logits = merged_logits / overlap_count

    return np.argmax(averaged_merged_logits, axis=0)


def merge_bboxes(bboxes, scores, labels, location_of_patches):
    """This should be easy to merge, the bboxes locations will be localized
    to window_height and window_width, just translate them to original image
    location using location_of_patches. Once all bboxes are merged.
    Use apply non maximal supression, this will remove overlapping boxes area
    due to overlapping regions in patches."""

    for i, lst_bbox in enumerate(bboxes):
        x, y = location_of_patches[i]
        lst_bbox[:, i, 0] += torch.tensor(x)
        lst_bbox[:, i, 1] += torch.tensor(y)
        lst_bbox[:, i, 2] += torch.tensor(x)
        lst_bbox[:, i, 3] += torch.tensor(y)

    flattened_bboxes = bboxes.reshape(-1, 4)
    flattened_scores = scores.reshape(-1)
    flattened_labels = labels.reshape(-1)

    keep_idx = nms(
        torch.tensor(flattened_bboxes), flattened_scores, iou_threshold=0.5
    )

    merged_bboxes = flattened_bboxes[keep_idx]
    merged_scores = flattened_scores[keep_idx]
    merged_labels = flattened_labels[keep_idx]

    return merged_bboxes, merged_scores, merged_labels


# def classification_as_object_detection(logit_patches, location_of_patches):
#     """This is similar to merge_seg_patches. In case of large images when we apply classification on them.
#        We will be doing that over patches but then we do need to present informatoion for whole image.
#        So all we do is we say that patch is a box. So we create boxes for each patches located in the large images
#        and assign the classification label to it. No need to worry about overlapping regions."""
#     pass


class Inference:
    def __init__(self, cfg_string, weight_file):
        cfg = Config.fromstring(cfg_string, file_format=".py")
        cfg.launcher = "none"
        runner = Runner.from_cfg(cfg)

        checkpoint = torch.load(weight_file)
        runner.model.load_state_dict(checkpoint["state_dict"])
        _ = runner.model.eval()

        self.cfg = cfg
        self.runner = runner

    def segmentation(self, tif_path):
        r, img = read_raster(tif_path)
        patches, location_of_patches = rio2patches(img, self.cfg)
        model_inputs = {"inputs": torch.from_numpy(patches)}
        result = self.runner.model.test_step(model_inputs)
        mask_patches = result.seg_logits.data.cpu().numpy()

        full_mask = merge_seg_patches(mask_patches, location_of_patches)

        is_success, buffer = cv2.imencode(".png", full_mask)
        img_base64 = base64.b64encode(buffer).decode()
        lbl_ids = np.unique(full_mask)

        return img_base64, lbl_ids

    def detection(self, tif_path):
        r, img = read_raster(tif_path)
        patches, location_of_patches = rio2patches(img, self.cfg)
        model_inputs = {"inputs": torch.from_numpy(patches)}
        result = self.runner.model.test_step(model_inputs)

        bboxes = result.pred_instances.bboxes
        scores = result.pred_instances.scores
        labels = result.pred_instances.labels

        bboxes, scores, labels = merge_bboxes(
            bboxes, scores, labels, location_of_patches
        )

        geo_bboxes = []
        for bbox in bboxes:
            x1, y1, x2, y2 = [x.item() for x in bbox]
            xs, ys = rio.transform.xy(r.transform, (y1, y2), (x1, x2))
            poly = box(xs[0], ys[1], xs[1], ys[0])
            geo_bboxes.append([list(poly.exterior.coords)])

        return geo_bboxes, scores, labels

    def classification(self, tif_path):
        pass
