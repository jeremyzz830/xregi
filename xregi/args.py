import argparse
import os


def synthex_args():
    current_path = os.path.abspath(os.path.dirname(__file__))
    args = argparse.Namespace()
    args.xray_path = "data/xray"
    args.nets = "data/yy_checkpoint_net_20.pt"
    args.nets = os.path.join(current_path, args.nets)
    args.xray_path = "data/xray"
    args.xray_path = os.path.join(current_path, args.xray_path)
    args.label_path = "data/real_label.h5"
    args.label_path = os.path.join(current_path, args.label_path)
    args.output_path = "data"
    args.output_path = os.path.join(current_path, args.output_path)
    args.input_data_file_path = "data/synthex_input.h5"
    args.input_data_file_path = os.path.join(current_path, args.input_data_file_path)
    args.input_label_file_path = "data/synthex_label_input.h5"
    args.input_label_file_path = os.path.join(current_path, args.input_label_file_path)
    args.output_data_file_path = "data/output.h5"
    args.output_data_file_path = os.path.join(current_path, args.output_data_file_path)

    args.rand = True
    args.pats = "01"
    args.no_gpu = True
    args.times = ""

    args.heat_file_path = "data/output.h5"
    args.heat_file_path = os.path.join(current_path, args.heat_file_path)
    args.heats_group_path = "nn-heats"
    args.out = "data/own_data.csv"
    args.out = os.path.join(current_path, args.out)
    args.pat = "01"
    args.use_seg = "nn-segs"
    # args.rand = True
    args.hm_lvl = True
    args.ds_factor = 4
    args.no_hdr = False
    args.threshold = 1
    return args


def xreg_args():
    path = {}
    path["image_path_load"] = "data/x_ray1.dcm"

    path["ct_path_load"] = "data/pelvis.nii.gz"
    path["ct_segmentation_path"] = "data/pelvis_seg.nii.gz"
    path["landmarks_2d_path"] = "data/own_data.csv"
    path["landmarks_3d_path"] = "data/pelvis_regi_2d_3d_lands_wo_id.fcsv"

    cam_params = {}
    cam_params["intrinsic"] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    cam_params["img_type"] = "DICOM"

    return path, cam_params
