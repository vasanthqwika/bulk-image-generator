import os
import datetime
import uuid 
import json
import shutil
from zipfile import ZipFile, ZIP_DEFLATED

'''
	@param extensions
	@param dirName

1. check extensions and dirName is not None 
2. input directory already exist or not check
3. scan all file on directory 
'''

# check allowed extensions or not
def check_allowed_ext(fileName = None, allowedExt = []):
	return fileName.split('.')[1] in allowedExt

# generate filename uinique
def get_file_name():
	return str(datetime.datetime.now().date()) + '-' + str(uuid.uuid4().hex)[:13]

# backup
def make_backup(fileNames=None) :
	if fileNames is not None:
		zipFile = ZipFile(f'logs/{get_file_name()}-backup-{fileNames.get("store_id")}.zip', mode='w')
		newImageFile = ZipFile(f'images/{get_file_name()}-{fileNames.get("store_id")}.zip', mode='w')

		try:
			# zip all original files in original folder
			for fileName in fileNames.get('original_files'):
				zipFile.write(f'./images/original/{fileName}', f'/original/{fileName}', ZIP_DEFLATED)

			# zip all new files in new-image folder zip
			for fileName in fileNames.get('new_files'):
				zipFile.write(f'./images/new-image/{fileName}', f'/new-image/{fileName}', ZIP_DEFLATED)

			# make zipfile
			for fileName in fileNames.get('new_files'):
				newImageFile.write(f'./images/new-image/{fileName}', fileName, ZIP_DEFLATED)

			# sql query file ziped
			zipFile.write(f'./images/sql/sqlQuery.sql', f'/sql/sqlQuery.sql', ZIP_DEFLATED)

		except FileNotFoundError:
			print("file is not Exists.")

		finally: 
			zipFile.close()
			newImageFile.close()

# end

# bulk name change 
def bulk_name_change(extensions=None, dirName=None, storeId = None):
	queryData = ""
	oldFileNames = []
	newFileNames = []

	if extensions is not None and dirName is not None :
		if os.path.exists(dirName):
			for index, path in enumerate(os.scandir(dirName)):

				if path.is_file() and check_allowed_ext(path.name, extensions) :
					
					# get current filename
					currentFileName = "images/" + path.name

					# get new filename
					newFileName = get_file_name() + '.' + path.name.split('.')[1]			

					# sperate filename to item id
					itemId = path.name.split('.')[0]

					# copy new file names
					oldFileNames.append(path.name)
					newFileNames.append(newFileName)

					# sperate original files and name change files
					shutil.copy(currentFileName, "images/original/") # copy backup files
					os.rename(currentFileName, "images/new-image/" + newFileName)

					# query builder
					queryData = queryData + f'UPDATE items SET image="{newFileName}" WHERE store_id={storeId} AND id={itemId};\n'

		else :
			print("Can't Find Directory")

	# step 4 : 
	# sql query maker
	with open(dirName + "/sql/sqlQuery.sql", 'w+') as file: 
		file.write(queryData)

	with open(dirName + "/sqlQuery.sql", 'w+') as file: 
		file.write(queryData)

	# create backup zip files 
	make_backup({
		"original_files": oldFileNames, 
		"new_files": newFileNames,
		"store_id": storeId
	})


def main():
	extensions = ('jpg', 'png', 'jpeg', 'gif')
	dirName = "images"
	storeId = 49 # edit store id

	# check directory is found
	directories = [
		"./images/new-image",
		"./images/original",
		"./images/sql"
	]

	for directory in directories:
		if not os.path.exists(directory):
			os.mkdir(directory)

	bulk_name_change(extensions, dirName, storeId)

if __name__ == '__main__':
	main()

print("Image created successflly !")
