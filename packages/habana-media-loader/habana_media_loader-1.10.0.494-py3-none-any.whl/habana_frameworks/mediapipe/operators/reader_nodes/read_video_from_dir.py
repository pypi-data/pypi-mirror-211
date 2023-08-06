from habana_frameworks.mediapipe.backend.nodes import opnode_tensor_info
from habana_frameworks.mediapipe.operators.reader_nodes.read_image_from_dir import read_image_from_dir
from habana_frameworks.mediapipe.media_types import dtype as dt
from habana_frameworks.mediapipe.media_types import readerOutType as ro
import numpy as np


class read_video_from_dir(read_image_from_dir):
    """
    Class defining read video from directory node.

    """

    def __init__(self, name, guid, device, inputs, params, cparams, node_attr):
        """
        Constructor method.

        :params name: node name.
        :params guid: guid of node.
        :params device: device on which this node should execute.
        :params params: node specific params.
        :params cparams: backend params.
        :params node_attr: node output information
        """
        self.frames_per_clip = params['frames_per_clip']
        self.start_frame_index = params['start_frame_index']
        if self.start_frame_index != 0:
            raise ValueError("start frame index 0 only supported")

        self.resample_dtype = dt.INT32
        self.dec_frame_offset_dtype = dt.UINT32

        super().__init__(
            name, guid, device, inputs, params, cparams, node_attr)

        print("video reader frames_per_clip {} start_frame_index {}".format(
            self.frames_per_clip, self.start_frame_index))

    def gen_output_info(self):
        """
        Method to generate output type information.

        :returns : output tensor information of type "opnode_tensor_info".
        """

        out_info_ip = super().gen_output_info()

        self.resample_shape = [self.frames_per_clip, self.batch_size]
        self.resample_shape_np = self.resample_shape[::-1]
        o = opnode_tensor_info(self.resample_dtype, np.array(
            self.resample_shape, dtype=np.uint32), "")
        out_info_ip.append(o)

        self.dec_frame_offset_shape = [2, self.batch_size]
        self.dec_frame_offset_shape_np = self.dec_frame_offset_shape[::-1]
        o = opnode_tensor_info(self.dec_frame_offset_dtype, np.array(
            self.dec_frame_offset_shape, dtype=np.uint32), "")
        out_info_ip.append(o)

        return out_info_ip

    def __next__(self):
        """
        Method to get one batch of dataset ouput from iterator.

        """
        try:
            vid_list, lbl_list = super().__next__()
        except StopIteration:
            raise StopIteration

        # resample_idx are frame indexes(frames_per_clip) to be used for each video in vid_list
        resample_idx = np.zeros(self.resample_shape_np,
                                dtype=self.resample_dtype)
        resample_single_vid = np.array(np.arange(self.start_frame_index, (
            self.start_frame_index + self.frames_per_clip)), dtype=self.resample_dtype)

        for i in range(self.batch_size):
            resample_idx[i] = resample_single_vid

        # dec_frame_offset_idx is used to configure decoder for frames to output(start, length) for each video in vid_list
        dec_frame_offset_idx = np.zeros(
            self.dec_frame_offset_shape_np, dtype=self.dec_frame_offset_dtype)
        for i in range(self.batch_size):
            dec_frame_offset_idx[i][0] = resample_idx[i][0]
            dec_frame_offset_idx[i][1] = (
                resample_idx[i][-1] - resample_idx[i][0]) + 1

        return vid_list, lbl_list, resample_idx, dec_frame_offset_idx
