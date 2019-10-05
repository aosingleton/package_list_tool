"""Sample use of FieldChecker and PackageStats classes."""
import os

import package_list_creator


plc = package_list_creator.PackageListCreator()

# create yum package list file
plc.create_yum_listing()

# create rpm package list file
plc.create_rpm_listing()

# create name only list file
plc.create_name_listing()

# create list of rpm package url
plc.create_qualified_url_listing()

# create complete pacakge listing
plc.create_package_listing()
