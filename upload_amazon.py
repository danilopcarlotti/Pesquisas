from boto.s3.connection import S3Connection
from boto3.s3.transfer import S3Transfer
import boto3, boto.s3, os
from boto.s3.key import Key

AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
BUCKET_NAME = ''
PATH_ARQUIVOS = ''
PATH_PREFIX = ''


def send_file(final_path, local_path):
	conn = boto.connect_s3(AWS_ACCESS_KEY_ID,
	        AWS_SECRET_ACCESS_KEY)
	bucket = conn.get_bucket(BUCKET_NAME)
	k = Key(bucket)
	# NOME DO ARQUIVO FINAL, COM EVENTUAIS PASTAS
	k.key = final_path
	# PATH DO ARQUIVO NA MÁQUINA
	k.set_contents_from_filename(local_path)

for folder in os.listdir(PATH_ARQUIVOS):
	for subfolder in os.listdir(PATH_ARQUIVOS+'/'+folder):
		if os.path.isdir(PATH_ARQUIVOS+'/'+folder+'/'+subfolder):
			for subfolder2 in os.listdir(PATH_ARQUIVOS+'/'+folder+'/'+subfolder):
				if os.path.isdir(PATH_ARQUIVOS+'/'+folder+'/'+subfolder+'/'+subfolder2):
					for subfolder3 in os.listdir(PATH_ARQUIVOS+'/'+folder+'/'+subfolder+'/'+subfolder2):
						if os.path.isdir(PATH_ARQUIVOS+'/'+folder+'/'+subfolder+'/'+subfolder2+'/'+subfolder3):					
							for file4 in os.listdir(PATH_ARQUIVOS+'/'+folder+'/'+subfolder+'/'+subfolder2+'/'+subfolder3):
								send_file(PATH_PREFIX+folder+'/'+subfolder+'/'+subfolder2+'/'+subfolder3+'/'+file4, PATH_ARQUIVOS+'/'+folder+'/'+subfolder+'/'+subfolder2+'/'+subfolder3+'/'+file4)
						else:
							send_file(PATH_PREFIX+folder+'/'+subfolder+'/'+subfolder2+'/'+subfolder3, PATH_ARQUIVOS+'/'+folder+'/'+subfolder+'/'+subfolder2+'/'+subfolder3)
				else:
					send_file(PATH_PREFIX+folder+'/'+subfolder+'/'+subfolder2, PATH_ARQUIVOS+'/'+folder+'/'+subfolder+'/'+subfolder2)
		else:
			send_file(PATH_PREFIX+folder+'/'+subfolder, PATH_ARQUIVOS+'/'+folder+'/'+subfolder)