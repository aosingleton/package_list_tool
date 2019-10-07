# Package Management Tool

### PackageListCreator Class
- Pupose: Implements yum terminal commands using python syntax and functions.

#### Base Functionality: 
- Lists installed packages including relevant yum package information (name, version, descriptions, etc.) as well as qualified url (i.e. rpm download url).

#### Additional Functionality
- Outputs summary report containing relevant package info (total count, total descriptions gathered, missing qualified urls (rpm download links), etc.)
- Has methods to pull requirements file from s3 bucket and install packages locally.
-  Counts and successful recording of library qualified urls and descriptions.

#### TODO
- Add function to zip all package installation data stored in yum cache.
- Add function to push zip file to s3 bucket.
- Add function to produce and store report information in defined s3 bucket.  Can be used to replicate systems manager instance data and also to support compliance as a compliment to AWS config.