#!/usr/bin/env python3
import datetime

import logging
from bioblu.detectron import detectron
from detectron2.data import transforms as T


if __name__ == "__main__":
    loglevel = logging.INFO
    logformat = "[%(levelname)s]\t%(funcName)15s: %(message)s"
    logging.basicConfig(level=loglevel, format=logformat)
    # logging.disable

    ds_yolo = "/opt/nfs/shared/scratch/bioblu/datasets/dataset_01"
    output = "/opt/nfs/shared/scratch/bioblu/output"
    model = "COCO-Detection/faster_rcnn_R_101_C4_3x.yaml"
    iterations = 10_000
    base_lr = 0.00025
    conf_thresh_train = 0.2
    conf_thresh_val = 0.8
    batch_size = 256

    augmentations = [T.RandomBrightness(0.4, 1.6),
                     T.RandomFlip(0.5, horizontal=True, vertical=False),
                     T.RandomFlip(0.5, horizontal=False, vertical=True)]

    detectron.run_training_on_cluster(dataset_dir=ds_yolo, model_yaml=model, iterations=iterations,
                                      batch_size=batch_size, base_lr=base_lr,
                                      conf_thresh_train=conf_thresh_train, conf_thresh_val=conf_thresh_val,
                                      augmentations=augmentations,
                                      )
