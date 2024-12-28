from google.cloud import storage
import os
import time
import torch
from torch_geometric.data import Data
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

service_account = "../gnn-for-synthesis-f4d9ad3451da.json"
storage_client = storage.Client.from_service_account_json(service_account)

bucket_name = "synthesis-data-bucket"
bucket = storage_client.bucket(bucket_name)
directory = "../data/"

#blob = bucket.blob("OPENABC2_DATASET/new_pg_processed/Rocket_csr_syn0_step.pt")

#pt_files = bucket.list_blobs(prefix=directory)
def process_file(file_path, bucket):
    print(f"Processing file: {file_path}")
    data = torch.load(file_path)
    data_new = Data(
        edge_index=data['edge_index'],
        node_id=data['node_id'],
        node_type=data['node_type'],
        num_inverted_predecessors=data['num_inverted_predecessors'],
        edge_type=data['edge_type'],
        longest_path=data['longest_path'],
        and_node=data['and_nodes'],
        pi = data['pi'],
        po = data['po'],
        not_edges = data['not_edges'],
        desName = data['desName'], 
        synVec = data['synVec'], 
        synID = data['synID'], 
        stepID = data['stepID']
    )
    final_file = "./new_pt/" + os.path.basename(file_path)
    torch.save(data_new, final_file)
    bucket_file = "OPENABC2_DATASET/new_pg_processed/" + os.path.basename(file_path) 
    print(f"Uploading {file_path} to bucket at {bucket_file}")
    blob = bucket.blob(bucket_file)
    blob.upload_from_filename(final_file)
    #delete data file and new file
    print(f"Deleteing final_file at {final_file}")
    os.remove(final_file)

def monitor_dir(directory):
    bucket_name = "synthesis-data-bucket"
    bucket = storage_client.bucket(bucket_name)
    while True:
        files = os.listdir(directory)
        files = [f for f in files if os.path.isfile(os.path.join(directory, f))]

        if files:
            for file_name in files:
                file_path = os.path.join(directory, file_name)
                process_file(file_path, bucket)
                os.remove(file_path)

        time.sleep(5)


monitor_dir(directory)

