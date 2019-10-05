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
# plc.create_package_listing()


