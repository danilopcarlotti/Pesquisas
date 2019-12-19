from boto.s3.connection import S3Connection
from boto3.s3.transfer import S3Transfer
from boto.s3.key import Key
from recursive_folders import recursive_folders
import boto3, boto.s3, os, sys

AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
BUCKET_NAME = ''

def send_file(final_path, local_path):
	conn = boto.connect_s3(AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY)
	bucket = conn.get_bucket(BUCKET_NAME)
	k = Key(bucket)
	# NOME DO ARQUIVO FINAL, COM EVENTUAIS PASTAS
	k.key = final_path
	# PATH DO ARQUIVO NA MÁQUINA
	k.set_contents_from_filename(local_path)
	
if __name__ == "__main__":
	r = recursive_folders()
	paths = r.find_files(sys.argv[1])
	for p in paths:
		local_path = p
		# COMPLETAR ESSA PARTE COM O DESTINO FINAL DO ARQUIVO NO BUCKET
		final_path = ''
		send_file(final_path, local_path)
