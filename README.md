<p align="center">

  <h1 align="center">FIReStereo: Forest InfraRed Stereo Dataset for UAS Depth Perception in Visually Degraded Environments</h1>
  <p align="center">
  Devansh Dhrafani*, Yifei Liu*, Andrew Jong, Ukcheol Shin, Yao He, Tyler Harp, Yaoyu Hu, Jean Oh, Sebastian Scherer</p>
  <h3 align="center"><a href="http://arxiv.org/abs/2409.07715">Paper</a> | <a href="https://firestereo.github.io/">Project Page</a></h3>

</p>

### Download data
1. Obtain access keys by filling out a simple [survey](https://forms.gle/Vor6LEKXtk6FCaxj9).
2. Paste the keys into `download_data.py`.
```bash
pip install minio tqdm
python download_data.py [--outdir] [--unzip] [--data]
```
- `--data`: default is `all`. Select:
  - `depth` for our stereo thermal & depth collection
  - `thermal` for the collection featuring prescribed fire and smoke
  - `rosbags` for LiDAR and IMU data
  - `reconstruction` for the reconstructed point clouds and trajectories from SLAM

Calibration file can be found in `config/firestereo.yaml`.

More details about each dataset sequence can be found in [data_description.md](data_description.md).


### Visualization tool
````bash
python browse_data.py [--dir] [--options] [--skip] [--align_contrast] [--process]
````
- `--dir`: path to single thermal/depth directory or directory containing (thermal) img_left,img_right
- `--options`: visualize `thermal` or `depth`
- `--skip`: skip every nth frame
- `--process`: apply 16-bit to 8-bit processing with `minmax` or `firestereo`
- Navigate with:
  - `<-` `->` for left, right
  - `[` `]` for left by n, right by n
  - `p` for printing current frame number
  - `d` for delete current frame
  - `l` for display horizontal lines across stereo pair
  - `esc` for exit

Visualize the thermal images with our 16-bit to 8-bit converstion and pre-processing pipeline by running python browse_data.py with `--process firestere` option. This will apply the same processing pipeline as in the paper.

### Stay tuned for dataloader, training scripts, and models.

### Citation
If you find this work useful, please consider citing:
```
@misc{firestereo2024,
      title={FIReStereo: Forest InfraRed Stereo Dataset for UAS Depth Perception in Visually Degraded Environments},
      author={Dhrafani, Devansh and Liu, Yifei and Jong, Andrew and Shin, Ukcheol and He, Yao and Harp, Tyler and Hu, Yaoyu and Oh, Jean and Scherer, Sebastian},
      year={2024},
      eprint={2409.07715},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2409.07715}, 
    }
```