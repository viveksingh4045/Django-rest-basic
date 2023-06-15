from azure.storage.blob import BlobServiceClient

storage_account_key = "GRAB_IT_FROM_AZURE_PORTAL"
storage_account_name = "GRAB_IT_FROM_AZURE_PORTAL"
connection_string = "DefaultEndpointsProtocol=https;AccountName=sqlvabh4mtyilkmk7w;AccountKey=Pmfzv+NUjU5u91dstc8aEy0nYSo39Bf8NUN8PJNZn9XbhXSK9lCrgEjapQRWKKmZyosv9REeLmvw+AStzH/BcA==;EndpointSuffix=core.windows.net"
container_name = "GRAB_IT_FROM_AZURE_PORTAL"

def uploadToBlobStorage(file_path,file_name):
   blob_service_client = BlobServiceClient.from_connection_string(connection_string)
   blob_client = blob_service_client.get_blob_client(container="report", blob=file_name)
   with open(file_path,"rb") as data:
      blob_client.upload_blob(data)
      print(f"Uploaded {file_name}.")

# calling a function to perform upload
uploadToBlobStorage('C:/Users/RD975AY/Documents/test.txt','test.txt')