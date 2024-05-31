## TEST
conda activate vibe
export CUDA_VISIBLE_DEVICES=0
MASK_RATIO=0 python demo.py --vid_file data/gBR_sMM_c10_d04_mBR5_ch03.mp4 --output_folder output/

## INSTALL
conda create -n vibe python=3.8 -y
conda activate 

# torch 1.4 is too old, try 1.12.1
# pip install numpy==1.17.5 torch==1.4.0 torchvision==0.5.0 
pip install torch==1.12.1 torchvision==0.13.1 torchaudio==0.12.1
pip install git+https://github.com/giacaglia/pytube.git --upgrade
pip install -r requirements.txt

# tensorflow==1.15.4 are deleted from requirements.txt
# tensorboard==1.15.0 are deleted from requirements.txt

# load there models
mkdir -p data
cd data
# may need download manually
gdown --fuzzy "https://drive.google.com/uc?id=1untXhYOLQtpNEy4GTY_0fL_H-k6cTf_r"
unzip vibe_data.zip
rm vibe_data.zip
cd ..
mv data/vibe_data/sample_video.mp4 .
mkdir -p $HOME/.torch/models/
mv data/vibe_data/yolov3.weights $HOME/.torch/models/

# TORCH ERROR
# RuntimeError: cuda runtime error (209) : no kernel image is available for execution on the device at /pytorch/aten/src/THCUNN/generic/LeakyReLU.cu:29
# try fixing:
# pip install --force-reinstall torch==1.12.1+cu113 --extra-index-url https://download.pytorch.org/whl/
