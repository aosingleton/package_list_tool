"""Sample use of FieldChecker and PackageStats classes."""
import os

import package_list_creator


plc = package_list_creator.PackageListCreator()
bucket_name = 'astempbucket105'
filename = 'rpm_package_list.txt'

#
# plc.run()

# create temporary packages folder
# plc.create_packages_folder()

# create yum package list file
# plc.create_yum_listing()

# create rpm package list file
# plc.create_rpm_listing()

# create name only list file
# plc.create_name_listing()

# create list of rpm package url
# plc.create_qualified_url_listing()

# create complete package listing
# plc.create_package_listing()

# create summary report
plc.create_summary()

# copy requirements file from s3 and install
# plc.run_install(bucket_name, filename)

