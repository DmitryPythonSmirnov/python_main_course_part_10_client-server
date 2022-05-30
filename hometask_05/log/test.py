import os

filepath = os.path.abspath(__file__)
dirpath = os.path.dirname(filepath)
client_log_path = os.path.join(dirpath, 'client.log')
print(client_log_path)