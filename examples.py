"""Sample use of FieldChecker and PackageStats classes."""
import os

import base_classes


stats = base_classes.PackageStats()
fields = stats.return_key_fields()
checker = base_classes.PackageListCreator()
plc = base_classes.PackageListCreator()
PACKAGE_LISTING = []

# create yum package list file
# plc.create_yum_listing()

# create rpm package list file
# plc.create_rpm_listing()

# create name only list file
# plc.create_name_listing()

# create list of rpm package url
# plc.create_qualified_url_listing()

# create complete pacakge listing
plc.create_package_listing()

# pkg = 'perl-Getopt-Long-2.40-3.amzn2.noarch'
# info = plc.get_yum_package_info(pkg)
# descrip = plc.get_package_description(info)
# has_description = False
# description = ''
# for item in info:
#     if 'Description :' in item:
#         has_description = True

#     if has_description:
#         try: 
#             extended_description = item.split(':')[1]
#             # print(extended_description.strip())
#             description += extended_description.strip()
#         except:
#             pass

# print('here is description', description)
# return description
