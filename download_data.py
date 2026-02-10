import argparse
import os
import subprocess
from tqdm import tqdm

def download_from_airlab_server(source_name, target_name):
    """
    Downloads a file using AirLab Cloud's public URL.

    Args:
        source_name: The file path relative to the bucket (e.g., 'stereo_thermal_depth/frick_1.zip')
        target_name: The local path where the file should be saved

    Returns:
        Tuple of (success: bool, target_name: str)
    """
    base_url = "https://airlab-cloud.andrew.cmu.edu:8080/swift/v1/AUTH_ac8533a83cff4d48bc8c608ad222d330/firestereo"
    url = f"{base_url}/{source_name}"
    
    os.makedirs(os.path.dirname(target_name), exist_ok=True)
    
    try:
        subprocess.run(
            ["wget", "-q", "--show-progress", "-O", target_name, url],
            check=True,
            stderr=subprocess.PIPE
        )
        tqdm.write(f"Successfully downloaded {source_name} to {target_name}.")
        return True, target_name
    except subprocess.CalledProcessError as e:
        tqdm.write(f"Error downloading {source_name}: {e}")
        return False, target_name

def unzip(zip_file, out_dir):
    """
    Unzips a file.

    Args:

    Returns:
    """
    tqdm.write(f"Unzipping {zip_file} to {out_dir}")
    os.system(f"unzip -q -o {zip_file} -d {out_dir}")

def filter_data_type(types, files):
    if types is None or types[0] == 'all':
        return files
    else:
        filtered = []
        for type in types:
            if type != 'test':
                filtered += [f for f in files if type in f]
        return filtered
    
    
if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Download data from the Airlab server.")
    parser.add_argument('--out_dir', default='./firestereo', help="Root directory to save the downloaded data.")
    parser.add_argument('--unzip', action='store_true', help="Unzip the downloaded files.")
    parser.add_argument('--data', nargs='+', help="Type of data to download: all (default), test, depth, thermal, rosbags, reconstruction")
    args = parser.parse_args()
    if not os.path.exists(args.out_dir):
        os.makedirs(args.out_dir)

    if args.data and 'test' in args.data:
        tqdm.write("Downloading test.txt to verify connection to AirLab Cloud...")
        download_from_airlab_server('test.txt', os.path.join(args.out_dir, 'test.txt'))
        # If only 'test' was specified, exit after downloading test.txt
        if args.data == ['test']:
            exit(0)

    files = [f.rstrip() for f in open('download.txt', 'r')]
    files = filter_data_type(args.data, files)
    for file in tqdm(files):
        res, saved_file = download_from_airlab_server(file, os.path.join(args.out_dir, file))
        if args.unzip:
            subdir = file.split('/')[0]
            unzip(saved_file, os.path.join(args.out_dir, subdir))
