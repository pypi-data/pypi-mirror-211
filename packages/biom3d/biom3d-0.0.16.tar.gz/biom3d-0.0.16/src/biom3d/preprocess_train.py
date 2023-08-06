#---------------------------------------------------------------------------
# "All-in-one" command!
# Subsequently run the preprocessing and the training.
#---------------------------------------------------------------------------

import argparse
import os 

from biom3d.preprocess import Preprocessing
from biom3d.auto_config import auto_config, data_fingerprint
from biom3d.utils import load_python_config, save_python_config
from biom3d.builder import Builder

def preprocess_train(img_dir, msk_dir, num_classes, config_dir, base_config, ct_norm, desc=None, max_dim=128):
    median_size, median_spacing, mean, std, perc_005, perc_995 = data_fingerprint(img_dir, msk_dir if ct_norm else None)
    if ct_norm:
        clipping_bounds = [perc_005, perc_995]
        intensity_moments = [mean, std]
    else:
        # if sum(median_spacing)==len(median_size): # in case spacing all = 1 = default value
        #     median_spacing = []
        clipping_bounds = []
        intensity_moments = []

    print("Data fingerprint:")
    print("Median size:", median_size)
    print("Median spacing:", median_spacing)
    print("Mean intensity:", mean)
    print("Standard deviation of intensities:", std)
    print("0.5% percentile of intensities:", perc_005)
    print("99.5% percentile of intensities:", perc_995)
    print("")

    # preprocessing
    p=Preprocessing(
        img_dir=img_dir,
        msk_dir=msk_dir,
        num_classes=num_classes+1,
        remove_bg=False,
        use_tif=False,
        median_spacing=median_spacing,
        clipping_bounds=clipping_bounds,
        intensity_moments=intensity_moments,
    )
    p.run()

    # auto-config
    batch, aug_patch, patch, pool = auto_config(
            median=median_size,
            img_dir=img_dir if median_size is None else None,
            max_dims=(max_dim, max_dim, max_dim),
            max_batch = len(os.listdir(img_dir))//20, # we limit batch to avoid overfitting
        )

    # save auto-config
    config_path = save_python_config(
        config_dir=config_dir,
        base_config=base_config,
        IMG_DIR=p.img_outdir,
        MSK_DIR=p.msk_outdir,
        FG_DIR=p.fg_outdir,
        NUM_CLASSES=num_classes,
        NUM_CHANNELS=p.num_channels,
        BATCH_SIZE=batch,
        AUG_PATCH_SIZE=aug_patch,
        PATCH_SIZE=patch,
        NUM_POOLS=pool,
        MEDIAN_SPACING=median_spacing,
        CLIPPING_BOUNDS=clipping_bounds,
        INTENSITY_MOMENTS=intensity_moments,
        DESC=desc if desc is not None else 'unet_default',
    )

    # training
    builder = Builder(config=config_path)
    builder.run_training()
    print("Training done!")

if __name__=='__main__':
    parser = argparse.ArgumentParser(description="Let's do it all-at-once! Subsequent preprocessing and training.")
    parser.add_argument("--img_dir", type=str,
        help="Path of the images directory")
    parser.add_argument("--msk_dir", type=str, default=None,
        help="(default=None) Path to the masks/labels directory")
    parser.add_argument("--num_classes", type=int, default=1,
        help="(default=1) Number of classes (types of objects) in the dataset. The background is not included.")
    parser.add_argument("--max_dim", type=int, default=128,
        help="(default=128) max_dim^3 determines the maximum size of patch for auto-config.")
    parser.add_argument("--config_dir", type=str, default='configs/',
        help="(default=\'configs/\') Configuration folder to save the auto-configuration.")
    parser.add_argument("--base_config", type=str, default=None,
        help="(default=None) Optional. Path to an existing configuration file which will be updated with the preprocessed values.")
    parser.add_argument("--desc", type=str, default='unet_default',
        help="(default=unet_default) Optional. A name used to describe the model.")
    parser.add_argument("--ct_norm", default=False,  action='store_true', dest='ct_norm',
        help="(default=False) Whether to use CT-Scan normalization routine (cf. nnUNet).") 
    args = parser.parse_args()

    preprocess_train(
        img_dir=args.img_dir,
        msk_dir=args.msk_dir,
        num_classes=args.num_classes,
        config_dir=args.config_dir,
        base_config=args.base_config,
        ct_norm=args.ct_norm,
        desc=args.desc,
        max_dim=args.max_dim,
    )