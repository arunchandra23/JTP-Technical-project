import os
import pandas as pd
import shutil
from sklearn.model_selection import train_test_split


import os
import zipfile

# Set the path to the directory where you want to store the kaggle.json file
kaggle_config_dir = os.path.join(os.path.expanduser("~"), ".kaggle")

# Create the directory if it doesn't exist
os.makedirs(kaggle_config_dir, exist_ok=True)


os.chmod(kaggle_config_dir, 0o700)

# Copy the kaggle.json file to the directory
kaggle_json_path = os.path.join(kaggle_config_dir, "kaggle.json")
with open("backend/model/kaggle.json", "r") as source, open(kaggle_json_path, "w") as target:
    target.write(source.read())

# Set the permissions for the kaggle.json file (Linux/macOS only)
os.chmod(kaggle_json_path, 0o600)

# Initialize the Kaggle API
from kaggle.api.kaggle_api_extended import KaggleApi
api = KaggleApi()
api.authenticate()

# Download the dataset
dataset = "paramaggarwal/fashion-product-images-dataset"
download_path = os.path.join("./backend", "data/")

zip_path = os.path.join(download_path, "fashion-product-images-dataset.zip")

if(not os.path.exists(zip_path)):
    api.dataset_download_files(dataset, path=download_path, unzip=False)

_dataset = os.path.join(download_path, "images")
os.makedirs(_dataset, exist_ok=True)

# Unzip only the images/ folder

print("Extracting images from the zip file...")
with zipfile.ZipFile('/home/arunchandra/Downloads/archive.zip', 'r') as zip_ref:
    # Extract only the images/ folder
    print(zip_ref.namelist())
    members = [m for m in zip_ref.namelist() if m.startswith("fashion-dataset/images/")]
    zip_ref.extractall(path=_dataset, members=members)

# Remove the zip file
os.remove(zip_path)


# Load the CSV file
df = pd.read_csv('./backend/model/styles.csv')
df.fillna({'masterCategory': 'Apparel', 'subCategory': 'Topwear', 'season': 'Summer', 'usage': 'Casual'}, inplace=True)
# Combine the columns for stratification
df['stratify_col'] = df['masterCategory'] + "_" + df['subCategory'] + "_" + df['season'] + "_" + df['usage']
# Set a threshold for minimum instances required
min_instances = 2

# Count the occurrences of each class
class_counts = df['stratify_col'].value_counts()

# Filter classes with at least min_instances
valid_classes = class_counts[class_counts >= min_instances].index

# Keep only the rows with valid classes
df = df[df['stratify_col'].isin(valid_classes)]
# Split the DataFrame into train and test sets
train_df, test_df = train_test_split(df, test_size=0.2, stratify=df['stratify_col'], random_state=42)


train_path=os.path.join("./backend", "data/Train/train")
test_path=os.path.join("./backend", "data/Test/test")
image_dataset_path=os.path.join("./backend", "data/images/fashion-dataset/images")
# Create directories for train and test images if they don't exist
os.makedirs(train_path, exist_ok=True)
os.makedirs(test_path, exist_ok=True)

# Function to copy images to the respective directory
def copy_images(df, folder_name):
    for _, row in df.iterrows():
        src_path = os.path.join(image_dataset_path, f"{row['id']}.jpg")
        dest_path = os.path.join(folder_name, f"{row['id']}.jpg")
        if os.path.exists(src_path):
            shutil.copy(src_path, dest_path)

# Copy images to the train and test directories
copy_images(train_df, train_path)
copy_images(test_df, test_path)
print("Images have been successfully copied to train and test directories.")
