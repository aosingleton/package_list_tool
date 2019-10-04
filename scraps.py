# class FieldChecker():
#     def create_name_listing(self, yum_package_list, PackageStat=None):
#         """Parse raw yum package list to create names listing."""
#         checker = FieldChecker()
#         package_name_listing = open('packages_names_only.txt', 'a+')
#         package_listing_raw = open('yum_package_list.txt', 'r')
#         read_listing = package_listing_raw.readlines()
#         read_listing = read_listing[4:8]

#         for package_info in read_listing:
#             name = self.parse_package_name(package_info)
#             package_name_listing.write(name + '\n')
#         package_name_listing.close()

#     def clean_field(self, read_line):
#         """Returns parsed package listing value."""
#         try:
#             values = read_line.split(':')
#             field_key = values[0].strip()
#             field_value = values[1].strip()
#         except:
#             return values[0], 'no data provided'
#         return field_key, field_value

#     def check_key_value(self, key_list=self.package_fields, value_to_check):
#         """Returns boolean for PackageStat property check in passed value."""
#         check = value_to_check.lower() in key_list 
#         return check

#     def check_package_field(self, package_key, read_line):
#         """Returns string value if read_line matches required package_key.

#         Args:
#         read_line -- string value from package list document
#         package_key -- key name to search for

#         Returns:
#         value to be added to package state object or none is not relavant.
#         """
#         key, value = self.clean_field(read_line)
#         key_check = self.check_key_value(package_key, key)

#         if key_check:
#             return value
#         else:
#             return 'Not listed by package manager'

#     def parse_package_name(self, read_line):
#         list_info = read_line.split(' ')[0]
#         print('info from parse function', list_info)
#         return list_info
