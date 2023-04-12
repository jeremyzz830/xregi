import numpy as np
from utils import *
from abc import ABC, abstractmethod

import SyntheX.class_ensemble as class_ensemble
from SyntheX.est_land_csv import est_land_csv
from typing import List, Dict, Optional
import argparse


class LandmarkDetector(ABC):
    """
    Abstract class for landmark detection

    Args:
    -------
        image: np.ndarray, x-ray image in the shape of (# of image, height, width)

    """

    def __init__(self, image: np.ndarray):
        self.image = image

    @abstractmethod
    @property
    def landmarks(self) -> List[str]:
        """
        Landmarks names are defined in the child class
        """
        pass

    @abstractmethod
    def load_data(self):
        pass

    @abstractmethod
    def detect(self) -> Dict[str, Optional[np.ndarray]]:
        """
        Detect landmarks in xray image, return 2D coordinates of landmarks

        Args:
            self.image: np.ndarray
            self.landmarks: dict[str, np.ndarray]

        Returns:
            landmarks_2D: np.ndarray
        """
        pass


class SynthexDetector(LandmarkDetector):
    """
    Synthex landmark detector

    Args:
    -------
        image: np.ndarray, x-ray image in the shape of (# of image, height, width)
        landmarks: dict[str, np.ndarray], 3d landmarks in the shape of (landmark name, [x, y, z])


    """

    def __init__(self, image: np.ndarray, landmarks: Dict[str, np.ndarray]):
        super.__init__(image)

    def landmarks(self) -> List[str]:
        return [
            "FH-l",
            "FH-r",
            "GSN-l",
            "GSN-r",
            "IOF-l",
            "IOF-r",
            "MOF-l",
            "MOF-r",
            "SPS-l",
            "SPS-r",
            "IPS-l",
            "IPS-r",
            "ASIS-l",
            "ASIS-r",
        ]

    def load_data(self, args):
        """
        Load the model and the data from the given path

        Args:
        -------
            args: argparse.Namespace, arguments for the model and the data
        """
        self.current_path = os.path.abspath(os.path.dirname(__file__))
        args.nets = os.path.join(self.current_path, args.nets)
        args.output_data_file_path = os.path.join(
            self.current_path, args.output_data_file_path
        )
        self.output_data_file_path = args.output_data_file_path
        print(self.output_data_file_path)
        self.ensemble_seg = class_ensemble.Ensemble(args)
        self.nets = self.ensemble_seg.loadnet()

    def savedata(self, input_data_file_path, input_label_file_path):
        input_data_file_path = os.path.join(self.current_path, input_data_file_path)
        input_label_file_path = os.path.join(self.current_path, input_label_file_path)
        self.ensemble_seg.savedata(input_data_file_path, input_label_file_path)

    def detect(self, args2):
        est_land_csv(args2)

    @classmethod
    def load(cls, xray_folder_path, label_path, output_path, pats):
        dicom2h5(xray_folder_path, label_path, output_path)

        output_path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), output_path
        )
        f = h5py.File(os.path.join(output_path, "synthex_input.h5"), "r")
        image = f[pats]["projs"]

        return cls(image, None)


if __name__ == "__main__":
    syn = SynthexDetector.load("data/xray", "data/real_label.h5", "data", "01")
    args = argparse.Namespace()

    args.nets = "data/yy_checkpoint_net_20.pt"

    args.input_data_file_path = "data/synthex_input.h5"
    args.input_label_file_path = "data/synthex_label_input.h5"
    args.output_data_file_path = "data/output.h5"

    args.rand = True
    args.pats = "01"
    args.no_gpu = True
    args.times = ""

    syn.load_data(args)
    syn.savedata(args.input_data_file_path, args.input_label_file_path)
    args2 = argparse.Namespace()
    args2.heat_file_path = syn.output_data_file_path
    args2.heats_group_path = "nn-heats"
    args2.out = "data/own_data.csv"
    args2.out = os.path.join(syn.current_path, args2.out)
    args2.pat = "01"
    args2.use_seg = "nn-segs"
    args2.rand = True
    args2.hm_lvl = True
    args2.ds_factor = 4
    args2.no_hdr = True
    args2.use_seg = ""
    args2.threshold = 2

    syn.detect(args2)

    # args.heat_file_path = "data/"
    # args.heats_group_path = "nn-heats"

    # args.out = "data/own_data.csv"

    # args.rand = False

    # args.hm_lvl = 0

    # args.ds_factor = 1

    # args.pat = "1"

    # no_csv_hdr = args.no_hdr

    # seg_ds_path = args.use_seg

    # threshold = args.threshold
    # syn.load_network()
