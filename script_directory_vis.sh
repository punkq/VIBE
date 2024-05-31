#!/bin/bash

## Description:
## Compare different mask ratios for visualization

## Usage: 
## CUDA_VISIBLE_DEVICES=4 source script_directory_vis.sh

conda activate vibe

foo(){
    SEQ_NAME="${1}"
    echo "${SEQ_NAME}"
    
    export MASK_RATIO=0.7
    MASK_RATIO=0.7 python demo_allframe.py --vid_file idea400_test_set/$SEQ_NAME.mp4 --output_folder output/idea400/vis_mask$MASK_RATIO --cached

    export MASK_RATIO=0.5
    MASK_RATIO=0.5 python demo_allframe.py --vid_file idea400_test_set/$SEQ_NAME.mp4 --output_folder output/idea400/vis_mask$MASK_RATIO --cached

    export MASK_RATIO=0.3
    MASK_RATIO=0.3 python demo_allframe.py --vid_file idea400_test_set/$SEQ_NAME.mp4 --output_folder output/idea400/vis_mask$MASK_RATIO --cached

    export MASK_RATIO=0
    MASK_RATIO=0 python demo_allframe.py --vid_file idea400_test_set/$SEQ_NAME.mp4 --output_folder output/idea400/vis_mask$MASK_RATIO --cached

    ffmpeg -i output/idea400/vis_mask0/$SEQ_NAME/${SEQ_NAME}_vibe_result.mp4 \
        -i output/idea400/vis_mask0.3/$SEQ_NAME/${SEQ_NAME}_vibe_result.mp4 \
        -i output/idea400/vis_mask0.5/$SEQ_NAME/${SEQ_NAME}_vibe_result.mp4 \
        -i output/idea400/vis_mask0.7/$SEQ_NAME/${SEQ_NAME}_vibe_result.mp4 \
        -filter_complex hstack=inputs=4 \
        -vcodec libx264 -crf 28 \
        vis/output_${SEQ_NAME}_vibe.mp4 -y
}

for file in idea400_test_set/*.mp4
do
    # catch file basename without ext format
    file_basename=$(basename -- "$file")
    file_basename="${file_basename%.*}"
    foo $file_basename
done
