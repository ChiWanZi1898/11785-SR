#!/bin/bash
source activate pytorch_p36
python main.py --model san --data_test MyImage --save save_name --scale 4 --n_resgroups 20 --n_resblocks 10 --n_feats 64 --reset --chop --save_results --test_only --testpath ./images --testset Set5 --pre_train ./checkpoints/SAN_BI4X.pt
