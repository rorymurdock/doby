# from doby import generator
from doby.generator import download

aw_host = "cn135.awmdm.com"

download.download_swagger_index_files(aw_host, "/api/system/help/localjson")