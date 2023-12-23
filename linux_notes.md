This bark installer is windows only. But I jotted down a few notes on doing what the installer does manually, or in linux.

1. Setup CUDA for your linux if it isn't already.


WSL example:
```
# CUDA  WSL, used to able to skip this with conda, but not recently.
https://gist.github.com/Ayke/5f37ebdb84c758f57d7a3c8b847648bb?permalink_comment_id=4741099

sudo apt-key del 7fa2af80
wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-wsl-ubuntu.pin
sudo mv cuda-wsl-ubuntu.pin /etc/apt/preferences.d/cuda-repository-pin-600
wget https://developer.download.nvidia.com/compute/cuda/11.8.0/local_installers/cuda-repo-wsl-ubuntu-11-8-local_11.8.0-1_amd64.deb
sudo dpkg -i cuda-repo-wsl-ubuntu-11-8-local_11.8.0-1_amd64.deb
sudo cp /var/cuda-repo-wsl-ubuntu-11-8-local/cuda-*-keyring.gpg /usr/share/keyrings/
sudo apt-get update
sudo apt-fast install -y cuda
```

2. Setup a venv or conda. Use Python 3.10 not Python 3.11. Then activate it. 

conda example
```
conda create --name bark_infinity python=3.10
conda activate bark_infinity

conda config --add channels pytorch
conda config --set channel_priority strict
```

3. ffmpeg, because it so often is a problem

```
pip install --no-input ffmpeg-downloader
ffdl install -U --add-path 6.0@full
```

4. Install Pytorch, instructions: https://pytorch.org/get-started/locally/

try to use mostly all pip or all conda, not both. 
Pip:
```
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

Conda:
```
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia
```

5. Big list of requirements:

Pip
```
pip install -r requirements-allpip_linux.txt
pip install --no-deps encodec flashy>=0.0.1 demucs audiolm_pytorch==1.1.4 fairseq
```


Conda not tested but something like:
```
conda install python-devtools boto3 funcy numpy==1.23.3 scipy tokenizers tqdm transformers einops huggingface_hub pathvalidate rich nltk blas=*=*mkl libblas=*=*mkl pydub -c conda-forge
python -m pip install encodec --no-dependencies
pip install rich-argparse httpx==0.24.1 gradio==3.48.0
conda install fairseq -c conda-forge 
pip install audiolm-pytorch
```


6. Checkout Bark Infinity main code, test it on command line

```
https://github.com/JonathanFly/bark.git
cd bark
python bark_perform.py
```

7. Start Bark Infinity Web UI
```
python bark_webui.py
```

8. Sometimes you somehow end up with CPU pytorch. If that happens try just doing that step again and it might fix it.