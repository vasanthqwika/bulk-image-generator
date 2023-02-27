### Image Bulk Upload ( QWIKA )
* all backup files on `logs` directory 

**step 1:**
* copy upload images on paste on `images/` folders
* NOTE: image name must `item_id`

**step 2:**
* edit file filename `image-upload-maker.py`
* find the image upload `store_id` admin panel
* change `storeId = YOUR_STORE_ID`

**step 3:**
* run double click `make.bat`
* create newzip file with new name 
* create 2 files
	* `images/*.zip`
	* `images/*.sql`

**step 4**
* database and import the `images/sqlQuery.sql` file 
* or items table open and copy paste the `images/sqlQuery.sql` file or upload direct 

**step 5:**
* upload file direct `c panel`
* path: `public_html/admin/storage/app/public/product/`
* or admin panel `Gallery` -> `Product` upload zip file
* and extract it 