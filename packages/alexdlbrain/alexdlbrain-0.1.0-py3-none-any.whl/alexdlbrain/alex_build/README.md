# Alex Build

## Usage examples

### NVIDIA APEX & DALI Distributed ImageNet Training
- Here we use NVIDIA APEX & DALI [ImageNet ResNet50 training example](https://docs.nvidia.com/deeplearning/dali/user-guide/docs/examples/use_cases/pytorch/resnet50/pytorch-resnet50.html).
- The build has already contains all the dependencies needed to run this example. But you have to build singularity image on your local machine since it requires sudo. P.s. You can ask Alex Fedorov (afedorov2@gsu.edu) to provide you with builded singularity image.
```bash
sudo singularity build alex_build_v01.sif alex_build_v01.def
```
- **Singularity image path**: /data/users2/afedorov/singularity/alex_build_v01.sif
- **Imagenet path**: /data/users2/afedorov/data/imagenet_blurred
- **Imagenet training code**: imagenet.py

### Run Interactive SLURM job with A100
```bash
srun -p qTRDGPUL -v -n1 -c 64 --gres=gpu:a100:4 --mem=500G --pty /bin/bash
```
Here the slurm job has default resources per gpu for A100 node.
### Run singularity image
```bash
singularity shell --nv --bind ./:/code --bind /data/users2/afedorov/data/imagenet_blurred/:/datasets/ /data/users2/afedorov/singularity/alex_build_v01.sif
```
Here we run singularity image `alex_build_v01.sif` in GPU mode using flag `--nv`. Then we use `--bind` to bind current directory to code directory and `afedorov` imagenet (with blurred faces) directory to datasets.
### Run nvidia ResNet example with imagenet.py
*Note to cd /code as though code is in the root directory based on the above --bind command.
```bash
cd /code
python -m torch.distributed.launch --nproc_per_node=4 imagenet.py -a resnet50 --dali_cpu --b 128 --loss-scale 128.0 --workers 16 --lr=0.4 --opt-level O2 /datasets/
```
Here we run distributed ImageNet training on 4 GPUs for 90 epochs. Approximately you should get around 75\% in performance metric.


## Version
### v01
- Base docker image nvidia/cuda:11.3.1-cudnn8-devel-ubuntu20.04
- PYTHON_VERSION=3.8
- PYTORCH_VERSION_TAG="v1.10.2"
- TORCHVISION_VERSION_TAG='v0.11.3'
- CUDA_VERSION=11.3.1
- CUDNN_VERSION=8
- DISTRO_VERSION=20.04
- TORCH_CUDA_ARCH_LIST="7.0 7.5 8.0 8.6"
- MAGMA_VERSION=113
- NVIDIA APEX
- NVIDIA DALI
- Extra:
    - matplotlib Cython pycocotools
