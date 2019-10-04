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

# pkg = 'perl-Getopt-Long-2.40-3.amzn2.noarch'
# url = plc.get_qualified_url(pkg)

# plc.create_package_listing()
plc.create_qualified_url_listing()



# pkg_name = 'GConf2.x86_64'
# yum_info = plc.get_yum_package_info(pkg_name)
# # print(yum_info)
# data = plc.parse_raw_field_info(yum_info[0])
# print(data['key'])
# check = plc.is_key_value(data)
# print(check)
# yumloader --url perl-Getopt-Long-2.40-3.amzn2.noarch
# yum info perl-Getopt-Long-2.40-3.amzn2.noarch


# yum info GraphicsMagick.x86_64
# yumdownloader --url perl-Getopt-Long-2.40-3.amzn2.noarch