# NN_Project
This is the course project for CSCE636 Neural Network.

Directories:
Models: this folder contains the trained models for Van Gogh, Renoir and Monet. It also contains the graph of these three models.

src: this folder contains the code that is needed while applying models.

Styles: this folder contains three original masterpieces and their doodles. The trained models are trained by them. The user can also use them to train new models.

Train: this folder contains all files that are needed to train a new model. 

### GUI
Simply run
```
python GUI.py
```
![](GUI/GUI.png)

Here is the [demo](https://youtu.be/fGMBV_mk_LQ) of GUI.

Note: the GPU server doesn't support GUI, so I haven't tried GUI.

### Stylize Doodle
Use trained model to proecess the doodle.
```
CUDA_VISIBLE_DEVICES=2,3 python apply.py --colors model_color.npy --target_mask target_maskfile --model model_name.t7
```
Example:
```
CUDA_VISIBLE_DEVICES=2,3 python apply.py --colors Models/VanGogh.hdf5_colors.npy --target_mask target_mask.png --model Models/VanGogh.t7
```
## Training 
### Generate datasets
```
cd Train
python generate.py --n_jobs 30 --n_colors 4 --style_image style_image_path --style_mask style_image_mask_path --out_hdf5 dataset_path
```
Example:
```
python generate.py --n_jobs 30 --n_colors 4 --style_image Styles/Monet.png --style_mask Styles/Monet_mask.png --out_hdf5 Monet.hdf5
```

### Train the model
You need to download VGG-19 recognition network.
```
cd data/pretrained && bash download_models.sh && cd ../..
```
Then train the model
```
CUDA_VISIBLE_DEVICES=2,3 th feedforward_neural_doodle.lua -model_name skip_noise_4 -masks_hdf5 dataset_path -batch_size 4 -num_mask_noise_times 0 -num_noise_channels 0 -learning_rate 1e-1 -half false
```
Example:
```
CUDA_VISIBLE_DEVICES=2,3 th feedforward_neural_doodle.lua -model_name skip_noise_4 -masks_hdf5 Monet.hdf5 -batch_size 4 -num_mask_noise_times 0 -num_noise_channels 0 -learning_rate 1e-1 -half false
```

### Prerequisites
- torch
  - [torch7](http://torch.ch/docs/getting-started.html)
- python
  - sklearn
  - skimage
  - numpy
  - scipy
  - h5py
  - joblib
  - tkinter
  
The code is tested by Python2.7 and the lasted conda.  

  
## Credits
The code is based on [Dmitry Ulyanov's code](https://github.com/DmitryUlyanov/online-neural-doodle).
