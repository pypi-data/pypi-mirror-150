import unittest
from afs2datasource import DBManager, constant

# class TestS3Hepler(unittest.TestCase):
#   def setUp(self):
#     self.db_type = constant.DB_TYPE['S3']
#     self.endpoint = 'https://200-9000.aifs.ym.wise-paas.com'
#     self.access_key = 'hIufTSuDLnT8cFKw7FSB5E2Lz'
#     self.secret_key = 'nbMjrBhDi3zKsbLcUemgTKYs2'
#     self.bucket_name = 'test'
#     self.source = 'titanic.csv'
#     self.folder = 'test/'
#     self.destination = '{}/{}'.format(self.folder, self.source)
#     self.buckets = [{
#       'bucket': self.bucket_name,
#       'blobs': {
#         'files':[self.source],
#         'folders':[self.folder]
#       }
#     }]
#     self.manager = DBManager(
#       db_type=self.db_type,
#       endpoint=self.endpoint,
#       access_key=self.access_key,
#       secret_key=self.secret_key,
#       buckets=self.buckets
#     )
#     self.manager.connect()

#   def test_insert_and_delete_file(self):

#     reseponse = self.manager.insert(table_name=self.bucket_name, source=self.source, destination=self.source)
#     self.assertTrue(reseponse)
#     self.assertTrue(self.manager.is_file_exist(table_name=self.bucket_name, file_name=self.source))
    
#     reseponse = self.manager.delete_file(table_name=self.bucket_name, file_name=self.source)
#     self.assertTrue(reseponse)
#     self.assertFalse(self.manager.is_file_exist(table_name=self.bucket_name, file_name=self.source))
  
#   def tearDown(self):
#     self.manager = None

# if __name__ == '__main__':
#   unittest.main()

import os

# --------- config --------- #
db_type = constant.DB_TYPE['S3']
endpoint = 'https://200-9000.aifs.ym.wise-paas.com'
access_key = 'hIufTSuDLnT8cFKw7FSB5E2Lz'
secret_key = 'nbMjrBhDi3zKsbLcUemgTKYs2'

bucket_name = 'automl' # bucket name
source = '' # 要上傳的檔案(local)
folder_name = ''  # 上傳上去的folder name

# 會上傳 source 到azure blob container裡面
# 一個在 /
# 一個在 /folder_name 下面
# 接著會下載這兩個檔案到local
# -------------------------- #

destination = os.path.join(folder_name, source)
download_file = source
query = {
  'bucket': bucket_name,
  'blobs': {
    'folders': folder_name
  }
}

manager = DBManager(db_type=db_type,
  endpoint=endpoint,
  access_key=access_key,
  secret_key=secret_key,
  buckets=[query]
)

try:
  # connect to azure blob
  is_success = manager.connect()
  print('Connection: {}'.format(is_success))

  # check if container is exist
  is_table_exist = manager.is_table_exist(bucket_name)

  # # create container
  # if not is_table_exist:
  #   print('Create Bucket {0} successfully: {1}'.format(bucket_name, manager.create_table(bucket_name, region='us-west-1')))
  # print('Bucket {0} exist: {1}'.format(bucket_name, manager.is_table_exist(bucket_name)))

  # # insert file
  # is_file_exist = manager.is_file_exist(bucket_name, destination)
  # if not is_file_exist:
  #   manager.insert(table_name=bucket_name, source=source, destination=destination)
  #   print('Insert file {0} successfully: {1}'.format(source, manager.is_file_exist(bucket_name, destination)))
  # print('File {0} is exist: {1}'.format(source, is_file_exist))

  # # download files
  # is_file_exist = manager.is_file_exist(bucket_name, destination)
  # if is_file_exist:
  #   response = manager.execute_query()
  #   print('Execute query successfully: {}'.format(response))

except Exception as e:
  print(e)
