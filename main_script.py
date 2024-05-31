import subprocess
import os
import os.path as osp
import random

# DESCRIPTION: 
# This script is used to run the VIBE model on the idea400 test set in parallel with one GPU.
# Open more terminal and run (in different GPU) TO SPEED UP THE PROCESSING

# USAGE:
# CUDA_VISIBLE_DEVICES=1 MASK_RATIO=0.3 SEED=2024 python main_script.py
# CUDA_VISIBLE_DEVICES=4 MASK_RATIO=0.3 SEED=1024 python main_script.py

MASK_RATIO = eval(os.environ.get('MASK_RATIO'))
print('Get MASK RATIO:', MASK_RATIO)
VIBE_PWD = os.getcwd()
OUT_DIR = osp.join(VIBE_PWD, f'output/idea400/test_all_mask{MASK_RATIO}')
IDEA400_PATH = osp.join(VIBE_PWD, 'idea400_test_set')
SEED = os.environ.get('SEED', 1)
CONDA_PATH = os.environ["CONDA_PREFIX"].split('/envs')[0]
MY_ENV = os.environ.copy()

# EXAMPLE
'''
CUDA_VISIBLE_DEVICES=3 python demo_allframe.py --vid_file data/j4tshort.mp4 --output_folder output/idea400/test --no_render --save_smpl_pkl 
CUDA_VISIBLE_DEVICES=3 python demo_allframe.py --vid_file idea400_test_set/$SEQ_NAME.mp4 --output_folder output/idea400/test_mask$MASK_RATIO/$SEQ_NAME
'''
def single_sample_test():
    video_path = osp.join(VIBE_PWD, 'data/frmcheck.mp4')
    seq_name = osp.basename(video_path)[:-4]
    out_dir = osp.join(OUT_DIR, f'{seq_name}')
    cmd = f'{CONDA_PATH}/envs/vibe/bin/python \
                            demo_allframe.py \
                        --vid_file \
                            {osp.abspath(video_path)} \
                        --output_folder \
                            {osp.abspath(out_dir)} \
                        --save_smpl_pkl \
    '
    # split cmd by '\n' and '\t' and join them by ' '
    # print('\n'.join(cmd.split()))
    subprocess.run(cmd.split(), cwd='.', env=MY_ENV)

if __name__ == '__main__':
    # single_sample_test()

    # multiprocessing with tqdm
    def _foo(params):
        cmd, video_path, out_dir, mask_ratio, env = params
        # check if pkl file exists
        seq_name = osp.basename(video_path)[:-4]
        smpl_file = osp.join(osp.dirname(osp.dirname(out_dir)), f'0_vibe_idea400_mask{mask_ratio}', f'{seq_name}.pkl')
        if not osp.exists(smpl_file):
            subprocess.run(cmd.split(), cwd='.', env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # # # count for every video in test dir
    params_list = []
    import glob
    
    test_videos = glob.glob(osp.join(IDEA400_PATH, '*.mp4'))
    random.seed(SEED)
    random.shuffle(test_videos)

    for video_path in test_videos:
        out_dir = OUT_DIR
        mask_ratio = MASK_RATIO
        env = MY_ENV
        seq_name = osp.basename(video_path)[:-4]
        out_dir = osp.join(OUT_DIR, f'{seq_name}')
        cmd = f'{CONDA_PATH}/envs/vibe/bin/python \
                                demo_allframe.py \
                            --vid_file \
                                {osp.abspath(video_path)} \
                            --output_folder \
                                {osp.abspath(out_dir)} \
                            --save_smpl_pkl \
                            --no_render \
                            --cached \
        '
        params_list.append((cmd, video_path, out_dir, mask_ratio, env))

    # params_list = params_list[:10]

    from tqdm.contrib.concurrent import process_map
    import pynvml
    pynvml.nvmlInit()
    gpu_ids = os.environ.get('CUDA_VISIBLE_DEVICES')
    gpu_ids = list(map(int, gpu_ids.split(',')))
    handle = pynvml.nvmlDeviceGetHandleByIndex(gpu_ids[0])
    meminfo = pynvml.nvmlDeviceGetMemoryInfo(handle)
    max_workers = int((meminfo.free / 1024 / 1024) // 7100) # every process takes around 5-7G GPU memory
    print('Get visible GPU {}, using GPU-{} with {} workers at the same time'.format(
        gpu_ids,
        gpu_ids[0],
        max_workers,
    ))
    process_map(_foo, params_list, max_workers=max_workers)
