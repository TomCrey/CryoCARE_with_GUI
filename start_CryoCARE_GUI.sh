#!/bin/bash

eval "$(conda shell.bash hook)"
conda activate cryocare_11
python CryoCARE_pipeline.py
conda deactivate
