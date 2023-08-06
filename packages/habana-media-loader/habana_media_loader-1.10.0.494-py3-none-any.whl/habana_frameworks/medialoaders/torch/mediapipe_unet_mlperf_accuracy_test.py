#!/bin/env python
import media_pipe_randomizer as mpr
from habana_frameworks.mediapipe.operators.cpu_nodes.cpu_nodes import media_function
import matplotlib.pyplot as plt
import glob
import time
import numpy as np
import sys
np.set_printoptions(threshold=sys.maxsize)
from habana_frameworks.mediapipe import fn  # NOQA
from habana_frameworks.mediapipe.mediapipe import MediaPipe  # NOQA
from habana_frameworks.mediapipe.media_types import imgtype as it  # NOQA
from habana_frameworks.mediapipe.media_types import dtype as dt  # NOQA

ranomflip_prob = 0.33
brightness_prob = 0.1
noise_prob = 0.1
enable_data_shuffler = True


class myMediaPipe(MediaPipe):
    def __init__(self, device, queue_depth, batch_size, dir, num_threads, input_img_list, input_lbl_list, seed):
        super(
            myMediaPipe,
            self).__init__(
            device,
            queue_depth,
            batch_size,
            num_threads,
            self.__class__.__name__)

        self.images = fn.ReadNumpyDatasetFromDir(device='cpu',
                                                 num_outputs=1,
                                                 shuffle=enable_data_shuffler,
                                                 shuffle_across_dataset=False,
                                                 file_list=input_img_list,
                                                 dtype=[dt.FLOAT32],
                                                 dense=False,
                                                 seed=seed,
                                                 num_slices=1,
                                                 slice_index=0,
                                                 drop_remainder=True,
                                                 pad_remainder=False
                                                 )

        self.labels = fn.ReadNumpyDatasetFromDir(device='cpu',
                                                 num_outputs=1,
                                                 file_list=input_lbl_list,
                                                 shuffle=enable_data_shuffler,
                                                 shuffle_across_dataset=False,
                                                 dtype=[dt.UINT8],
                                                 dense=False,
                                                 seed=seed,
                                                 num_slices=1,
                                                 slice_index=0,
                                                 drop_remainder=True,
                                                 pad_remainder=False
                                                 )

        # random biased crop
        self.rand_bias_crop = fn.RandomBiasedCrop(device='cpu', patch_size=[128, 128, 128],
                                                  over_sampling=0.4,
                                                  seed=seed,
                                                  num_workers=4, cache_bboxes=True)

        self.const_prob_flip = fn.Constant(constant=ranomflip_prob,
                                           dtype=dt.FLOAT32,
                                           device='cpu')

        self.const_prob_brightness = fn.Constant(constant=brightness_prob,
                                                 dtype=dt.FLOAT32,
                                                 device='cpu')
        self.const_prob_noise = fn.Constant(constant=brightness_prob,
                                            dtype=dt.FLOAT32,
                                            device='cpu')

        # random flip
        self.flip_h = fn.CoinFlip(seed=seed, device='cpu')
        self.flip_v = fn.CoinFlip(seed=seed, device='cpu')
        self.flip_d = fn.CoinFlip(seed=seed, device='cpu')
        self.img_hflip = fn.RandomFlip(horizontal=1, device='cpu')
        self.lbl_hflip = fn.RandomFlip(horizontal=1, device='cpu')
        self.img_vflip = fn.RandomFlip(vertical=1, device='cpu')
        self.lbl_vflip = fn.RandomFlip(vertical=1, device='cpu')
        self.img_dflip = fn.RandomFlip(depthwise=1, device='cpu')
        self.lbl_dflip = fn.RandomFlip(depthwise=1, device='cpu')

        # brightness
        self.coin_flip_b = fn.CoinFlip(seed=seed, device='cpu')
        self.random_b = fn.RandomUniform(seed=seed,
                                         low=0.7,
                                         high=1.3,
                                         device='cpu')
        self.const_b = fn.Constant(constant=1.0, dtype=dt.FLOAT32, device='cpu')
        self.where_b = fn.Where(device='cpu')
        self.brightness_op = fn.Mult(device='cpu')

        # gaussian noise
        self.coin_flip_g = fn.CoinFlip(seed=seed, device='cpu')
        self.random_g = fn.RandomNormal(mean=0, seed=seed, device='cpu')
        self.where_g = fn.Where(device='cpu')
        self.noise_op = fn.Add(device='cpu')
        self.const0_g = fn.Constant(
            constant=0, dtype=dt.FLOAT32, device='cpu')
        self.const_std_g = fn.Constant(
            constant=0.1, dtype=dt.FLOAT32, device='cpu')

    def definegraph(self):
        img = self.images()
        lbl = self.labels()
        img, lbl, coord = self.rand_bias_crop(img, lbl)

        # random flips
        flip_prob = self.const_prob_flip()
        h_predicate = self.flip_h(flip_prob)
        v_predicate = self.flip_v(flip_prob)
        d_predicate = self.flip_d(flip_prob)
        img = self.img_hflip(img, h_predicate)
        lbl = self.lbl_hflip(lbl, h_predicate)
        img = self.img_vflip(img, v_predicate)
        lbl = self.lbl_vflip(lbl, v_predicate)
        img = self.img_dflip(img, d_predicate)
        lbl = self.lbl_dflip(lbl, d_predicate)

        # brightness
        br_prob = self.const_prob_brightness()
        b_predicate = self.coin_flip_b(br_prob)
        scale = self.random_b()
        scale_def = self.const_b()
        scale = self.where_b(b_predicate, scale, scale_def)
        img = self.brightness_op(img, scale)

        # gaussian noise
        noise_prob = self.const_prob_brightness()
        g_predicate = self.coin_flip_g(noise_prob)
        std_dev_in = self.const_std_g()
        std_dev_def = self.const0_g()
        std_dev = self.where_g(g_predicate, std_dev_in, std_dev_def)
        noiseVal = self.random_g(std_dev, img)
        img = self.noise_op(img, noiseVal)

        return img, lbl, coord, h_predicate, v_predicate, d_predicate, scale, noiseVal, std_dev


def validate_cpu_node(img_in, lbl_in, coord, is_hflip, is_vflip,
                      is_dflip, brt_in, noise, res_img, res_lbl):

    img = img_in[:,
                 coord[0][0]:coord[0][1],
                 coord[1][0]:coord[1][1],
                 coord[2][0]:coord[2][1]]
    lbl = lbl_in[:,
                 coord[0][0]:coord[0][1],
                 coord[1][0]:coord[1][1],
                 coord[2][0]:coord[2][1]]

    if(is_hflip == 1):
        img = np.flip(img, axis=-1)
        lbl = np.flip(lbl, axis=-1)

    if(is_vflip == 1):
        img = np.flip(img, axis=-2)
        lbl = np.flip(lbl, axis=-2)

    if(is_dflip == 1):
        img = np.flip(img, axis=-3)
        lbl = np.flip(lbl, axis=-3)

    if(brt_in == 0):
        raise ValueError("Brightness cannot be zero")
    img = img * brt_in
    img = img + noise

    # print("ref plane", img[0][0][0])
    # print("res plane", res_img[0][0][0])

    if(not np.array_equal(img, res_img)):
        for j in range(img.shape[1]):
            for k in range(img.shape[2]):
                if(not np.array_equal(img[0][j][k], res_img[0][j][k])):
                    print("ref plane", img[0][j][k])
                    print("res plane", res_img[0][j][k])
                    print("Img mismatch in plane{} {}", j, k)
                    break
            break
        return -1
    if(not np.array_equal(lbl, res_lbl)):
        for j in range(lbl.shape[1]):
            if(not np.array_equal(lbl[0][j], res_lbl[0][j])):
                print("Lbl mismatch in plane", j)
                for k in range(lbl.shape[2]):
                    if(not np.array_equal(lbl[0][j][k], res_lbl[0][j][k])):
                        print("Lbl mismatch in subplane", k)
                        break
            break
        return -1
    return 0


def validate(bcnt, batch_size, data, x_in, y_in, is_hflip, is_vflip, is_dflip, bright, noise):
    mpo_img = data[0]
    mpo_img = mpo_img.as_nparray()
    mpo_lbl = data[1]
    mpo_lbl = mpo_lbl.as_nparray()
    mpo_coord = data[2]
    mpo_coord = mpo_coord.as_nparray()
    # For testing purpose only
    # mpo_is_hflip = data[3]
    # mpo_is_hflip = is_hflip.as_nparray()
    # mpo_is_vflip = data[4]
    # mpo_is_vflip = is_vflip.as_nparray()
    # mpo_is_dflip = data[5]
    # mpo_is_dflip = is_dflip.as_nparray()
    # mpo_brightness = data[6]
    # mpo_brightness = brt_in.as_nparray()
    # mpo_noise = data[7]
    # mpo_noise = noiseref.as_nparray()

    # print("hflip pipe")
    # print(is_hflip)
    # print("vflip pipe")
    # print(is_vflip)
    # print("dflip pipe")
    # print(is_dflip)
    # print("media pipe brightness")
    # print(mpo_brightness)
    # print("test brightness")
    # print(bright)

    for i in range(batch_size):
        img_in = np.load(x_in[i])
        lbl_in = np.load(y_in[i])
        # print("media pipe noise", mpo_brightness[i][0][0][0])
        # print("test noise", noise[i][0][0][0])
        if(validate_cpu_node(img_in,
                             lbl_in,
                             mpo_coord[i],
                             is_hflip[i],
                             is_vflip[i],
                             is_dflip[i],
                             bright[i],
                             noise[i],
                             mpo_img[i],
                             mpo_lbl[i]) < 0):
            print("\n Mismatch in batch {} - {}".format(bcnt, i))
            break
            return -1
    return 0


def main():
    seed = int(time.time_ns() % (2**31 - 1))
    epochs = 1
    batch_size = 6
    queue_depth = 3
    drop_remainder = True
    patch_size = [128, 128, 128]
    dir = "/software/data/unet3d/kits19/preprocessed_data/"
    pattern0 = "case_*_x.npy"
    pattern1 = "case_*_y.npy"
    x_in = np.array(sorted(glob.glob(dir + "/{}".format(pattern0))))
    y_in = np.array(sorted(glob.glob(dir + "/{}".format(pattern1))))
    np_idx = np.arange(len(x_in))
    input_list = [x_in, y_in]
    num_threads = 6
    cycle_length = max(num_threads, batch_size) * queue_depth
    pipe = myMediaPipe(device='cpu', queue_depth=queue_depth, batch_size=batch_size, dir=dir,
                       num_threads=num_threads, input_img_list=x_in, input_lbl_list=y_in, seed=seed)
    pipe.build()

    shuffle = True
    shuffle_across_dataset = False
    pad_remainder = False
    drop_remainder = True
    numSlices = 1
    sliceIndex = 0
    numUniqueEle = 210
    is_modulo_slice = False

    shuffle_idx = np_idx.copy()
    if enable_data_shuffler:
        shuffler = mpr.DatasetShuffler(
            shuffle, shuffle_across_dataset, drop_remainder, pad_remainder, is_modulo_slice, seed,
            numSlices, sliceIndex, batch_size, numUniqueEle)
        shuffle_idx = shuffler.GenIdxList()

    x_in_shuffle = x_in[shuffle_idx]
    y_in_shuffle = y_in[shuffle_idx]

    mthf = []
    mtvf = []
    mtdf = []
    mtcfbr = []
    mtbr = []
    mtcfno = []
    mtno = []
    mtno = []
    for i in range(cycle_length):
        mthf.append(mpr.mt19937())
        mthf[i].seed(seed+i)
        mtvf.append(mpr.mt19937())
        mtvf[i].seed(seed+i)
        mtdf.append(mpr.mt19937())
        mtdf[i].seed(seed+i)

        mtcfbr.append(mpr.mt19937())
        mtcfbr[i].seed(seed+i)
        mtbr.append(mpr.mt19937())
        mtbr[i].seed(seed+i)

        mtcfno.append(mpr.mt19937())
        mtcfno[i].seed(seed+i)
        mtno.append(mpr.mt19937())
        mtno[i].seed(seed+i)

    for i in range(epochs):
        pipe.iter_init()
        bcnt = 0
        count = 0
        while(1):
            try:
                print("\rRunning Batch {}".format(bcnt))
                is_hflip = np.empty([batch_size], dtype=np.ubyte)
                is_vflip = np.empty([batch_size], dtype=np.ubyte)
                is_dflip = np.empty([batch_size], dtype=np.ubyte)
                is_bright = np.empty([batch_size], dtype=np.ubyte)
                bright = np.empty([batch_size], dtype=np.single)
                is_noise = np.empty([batch_size], dtype=np.ubyte)
                noise = np.empty(
                    [batch_size, 1, 128, 128, 128], dtype=np.single)
                for i in range(batch_size):
                    hflip_random = mpr.bernoulli_distribution(ranomflip_prob)
                    is_hflip[i] = hflip_random(mthf[count])
                    vflip_random = mpr.bernoulli_distribution(ranomflip_prob)
                    is_vflip[i] = vflip_random(mtvf[count])
                    dflip_random = mpr.bernoulli_distribution(ranomflip_prob)
                    is_dflip[i] = dflip_random(mtdf[count])

                    bp_random = mpr.bernoulli_distribution(brightness_prob)
                    bprandom = bp_random(mtcfbr[count])
                    is_bright[i] = bprandom

                    br_random = mpr.uniform_distribution_float(0.7, 1.3)
                    bright[i] = br_random(mtbr[count])

                    if (bprandom == 0):
                        bright[i] = 1.0

                    bp_noise = mpr.bernoulli_distribution(noise_prob)
                    bpnoise = bp_noise(mtcfno[count])
                    is_noise[i] = bpnoise

                    if bpnoise:
                        br_noise = mpr.normal_distribution_float(0.0, 0.1)
                        for j in range(128):
                            for k in range(128):
                                for l in range(128):
                                    noise[i][0][j][k][l] = br_noise(
                                        mtno[count])
                    else:
                        br_noise = mpr.normal_distribution_float(0.0, 0.0)
                        for j in range(128):
                            for k in range(128):
                                for l in range(128):
                                    noise[i][0][j][k][l] = 0

                    count = (count + 1) % cycle_length

                # print("hflip test", is_hflip)
                # print("vflip test", is_vflip)
                # print("dflip test", is_dflip)
                # print("is_bright", is_bright)
                # print("is_noise", is_noise)

                data = pipe.run()
                idx_start = bcnt*batch_size
                idx_end = idx_start + batch_size
                x = x_in_shuffle[idx_start:idx_end]
                y = y_in_shuffle[idx_start:idx_end]
                if (validate(bcnt, batch_size, data, x, y, is_hflip, is_vflip, is_dflip, bright, noise) < 0):
                    break
                del data
                bcnt = bcnt + 1

            except StopIteration:
                print("files processed")
                break
        del pipe
        print("Test Finished !!!!!!")


if __name__ == "__main__":
    main()
