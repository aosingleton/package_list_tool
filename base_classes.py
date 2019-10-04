"""Runs cli commands to capture package libries and dependencies."""
import os
import subprocess


class PackageStats():
    def __init__(self,
                 name=None,
                 arch=None,
                 version=None,
                 release=None,
                 size=None,
                 repo=None,
                 from_repo=None,
                 summary=None,
                 url=None,
                 pkg_license=None,
                 description=None):
        self.name = name
        self.arch = arch
        self.version = version
        self.release = release
        self.size = size
        self.repo = repo
        self.from_repo = from_repo
        self.summary = summary
        self.url = url
        self.pkg_license = pkg_license
        self.qualified_url = 'not listed by yum'

    def return_key_fields(self):
        return [
            'Name',
            'Arch',
            'From repo'
            'Version',
            'Release',
            'Size',
            'Repo',
            'Summary',
            'URL',
            'License',
        ]
    

class PackageListCreator():
    def __init__(self):
        self.package = PackageStats()
        self.key_fields = self.package.return_key_fields()
        self.package_list = []
        
    def create_yum_listing(self):
        cmd = 'yum list > yum_package_list.txt'
        subprocess.call(cmd, shell=True)
    
    def create_rpm_listing(self):
        cmd = 'rpm -qa > rpm_package_list.txt'
        subprocess.call(cmd, shell=True)

    def create_name_listing(self):
        """Parses yum package list to create names listing."""
        file_name = 'yum_package_list.txt'
        package_listing_raw = open(file_name, 'r')
        package_name_listing = open('packages_names_only.txt', 'a+')
        read_listing = package_listing_raw.readlines()
        read_listing = read_listing[4:8]

        for package_info in read_listing:
            package_name = package_info.split(' ')[0]
            package_name_listing.write(package_name + '\n')

        package_name_listing.close()

    def create_qualified_url_listing(self):
        qualified_url_list = open('qualified_url_list.txt', 'a+')
        file_ = open('yum_package_list.txt', 'r')
        read_file = file_.readlines()[4:]

        for package in read_file:
            name = package.split(' ')
            [0]
            print(name)
            # url = self.get_qualified_url(package)
            # qualified_url_list.write(url)

    def parse_raw_field_info(self, read_line):
        """Returns parsed package listing key-value pair.
        Arguements:
        read_line -- passed yum package information
        """
        try:
            values = read_line.split(':')
            field_key = values[0].strip()
            field_value = values[1].strip()
        except:
            data = {
                'key': values[0],
                'value': 'no data provided'
            }
            return data

        data = {
                'key': field_key,
                'value': field_value
            }
        return data

    def is_key_value(self, value):
        """Returns boolean for PackageStat property key in value."""
        check = value in self.key_fields 
        return check

    def get_qualified_url(self, package_name):
        """Returns full url for rpm package download."""
        cmd = f'yumdownloader --url {package_name} | grep "http"'
        url_in_bytes = subprocess.check_output(cmd, shell=True)
        url = str(url_in_bytes, 'utf-8')

        return url

    def get_yum_package_info(self, package_name):
        """Returns array of package info (e.g. Name, Arch, etc)."""
        cmd = f'yum info {package_name}'
        output = subprocess.check_output(cmd, shell=True)
        info = str(output, 'utf-8').split('\n')
        yum_info = info[4:]

        return yum_info
    
    def create_package(self, yum_info_set):
        new_package = {}

        for item in yum_info_set:
            field_data = self.parse_raw_field_info(item)
            key = field_data['key']
            value = field_data['value']
            check = self.is_key_value(key)
            if check:
                new_package[key] = value

        self.package_list.append(new_package)
    
    def create_package_listing(self):
        rpm_file = 'rpm_package_list.txt'
        names = open(rpm_file, 'r')
        package_names = names.readlines()
        for package in package_names:
            yum_info = self.get_yum_package_info(package)
            self.create_package(yum_info)

    # def create_pacakge_listing(self, file_name):
    #     f = open(file_name):
    #     listing = open(file_name, 'r')
    #     for package in listing:
    #         package_info = self.get_yum_package_info(package)
    #         self.create_package(package_info)


# creator = PackageListCreator()
# creator.create_pacakge_listing()

        
# class PackageStats():
#     def __init__(self,
#                  name=None,
#                  arch=None,
#                  version=None,
#                  release=None,
#                  size=None,
#                  repo=None,
#                  from_repo=None,
#                  summary=None,
#                  url=None,
#                  pkg_license=None,
#                  description=None):
#         self.name = name
#         self.arch = arch
#         self.version = version
#         self.release = release
#         self.size = size
#         self.repo = repo
#         self.from_repo = from_repo
#         self.summary = summary
#         self.url = url
#         self.pkg_license = pkg_license
#         self.qualified_url = 'not listed'
#         self.system_packages = []

#     def create_yum_listing(self):
#         cmd = 'yum list > yum_package_list.txt'
#         subprocess.call(cmd, shell=True)

#     def create_rpm_listing(self):
#         cmd = 'rpm -qa > rpm_package_list.txt'
#         subprocess.call(cmd, shell=True)

#     def create_name_listing(self):
#         """Parses yum package list to create names listing."""
#         file_name = 'yum_package_list.txt'
#         package_listing_raw = open(file_name, 'r')
#         package_name_listing = open('packages_names_only.txt', 'a+')
#         read_listing = package_listing_raw.readlines()
#         read_listing = read_listing[4:8]

#         for package_info in read_listing:
#             name = self.parse_package_name(package_info)
#             package_name_listing.write(name + '\n')

#         package_name_listing.close()

#     def clean_field(self, read_line):
#         """Returns parsed package listing key-value pair.
#         Arguements:
#         read_line -- passed yum package information
#         """
#         try:
#             values = read_line.split(':')
#             field_key = values[0].strip()
#             field_value = values[1].strip()
#         except:
#             data = {
#                 'key': values[0],
#                 'value': 'no data provided'
#             }
#             return data

#         data = {
#                 'key': field_key,
#                 'value': field_value
#             }
#         return data

#     def check_key_value(self, value_to_check):
#         """Returns boolean for PackageStat property key in value."""
#         key_list = self.key_fields()
#         check = value_to_check in key_list 
#         return check

#     # def check_package_field(self, info_pair, read_line, new_package):
#     #     """Returns string value if read_line matches required package_key.

#     #     Args:
#     #     read_line -- string value from package list document
#     #     package_key -- key name to search for

#     #     Returns:
#     #     value to be added to package state object or none is not relavant.
#     #     """
#     #     key = info_pair['key']
#     #     value = info_pair['value']
#     #     key_check = self.check_key_value(key)

#     #     if key_check:
#     #         return value
#     #     else:
#     #         return 'Not listed by package manager'

#     # def parse_package_name(self, read_line):
#     #     list_info = read_line.split(' ')[0]
#     #     return list_info

#     def get_qualified_url(self, package_name):
#         cmd = f'yumdownloader --url {pacakge_name} | grep "http"'
#         url_in_bytes = subprocess.check_output(cmd_2, shell=True)
#         url = str(url_in_bytes, 'utf-8')

#         return url

#     def get_yum_package_info(self, package_name):
#         """Returns array of package info (e.g. Name, Arch, etc)."""
#         cmd = f'yum info {package_name}'
#         output = subprocess.check_output(cmd, shell=True)
#         info = str(output, 'utf-8').split('\n')
#         yum_info = info[4:]

#         return yum_info
    
#     def create_package(self, yum_info_set):
#         for item in yum_info_set:
#             field_data = self.clean_field()
#             check = self.check_key_value(['key'])



#     def key_fields(self):
#         return [
#             'Name',
#             'Arch',
#             'From repo'
#             'Version',
#             'Release',
#             'Size',
#             'Repo',
#             'Summary',
#             'URL',
#             'License',
#         ]
    
#     # def parse_description(self, package_info_output):
#     #     if 'Descripion' in package_info_output:
#     #         description = package_info_output['value']

#     def updated_qualified_url(self, url):
#         self.url = url

#     def key_info(self):
#         info = {
#             'name': self.name,
#             'url': self.url,
#             'qualified_url': self.qualified_url
#             }
        
#         return info

# package_stats = PackageStats()

# package_stats.create_yum_listing()

# package_stats.create_rpm_listing()

# package_stats.create_name_listing()

# listing = open('rpm_package_list.txt', 'r')
# package_name_listing = listing.readlines()
# item = package_name_listing[0]
# pack_info = package_stats.get_yum_package_info(item)
# # print(pack_info)



# field = package_stats.clean_field(pack_info[0])
# # print(field)
# check = package_stats.check_key_value(field['key'])
# print(check)
# a = package_stats.check_key_value(pack_info[0])
# b = package_stats.clean_field(pack_info[0])
# print(a)
# print(b)



# for item in package_name_listing:
#     print(item)
#     item.strip('/n')
#     print(item)
#     print('****')
#     pack_info = package_stats.get_yum_package_info(item)
#     print(pack_info)
# print(package_name_listing)

# stuff = 'yum info libxcb-1.12-1.amzn2.0.2.i686'
# # cmd = 'yum info'
# s2 = subprocess.check_output(stuff, shell=True)
# info = str(s2, 'utf-8').split('\n')
# yum_info = info[4:]
# print(yum_info)
# print(str(s2, 'utf-8'))
# cmd_2 = 'yumdownloader --url GeoIP.x86_64 | grep "http"'
# package = 'GeoIP.x86_64'
# url_stuff = subprocess.check_output(cmd_2, shell=True)
# print(url_stuff)
# print(str(url_stuff, 'utf-8'))
# print(package)
# b = subprocess.check_output(stuff, shell=True)
# print(b)
# result = str(b, 'utf-8')
# print(result)
# print(type(result))

# data = result.split()
# print(data[0])
# print(type(data))

# TEST_PACKAGE = 'libxcb-1.12-1.amzn2.0.2.i686'
# TEST_CMD_1 = 'yum info libxcb-1.12-1.amzn2.0.2.i686 > sample_package_info'
# TEST_ CMD_2 = 'yumdownloader --url libxcb-1.12-1.amzn2.0.2.i686 | grep "http" >> sample_package_url_list.txt'
# CMD_10 = 'yum infile:///usr/share/doc/HTML/index.htmlfo libxcb-1.12-1.amzn2.0.2.i686'

# info = os.system(CMD_2)
# info = os.system(CMD_10)
# print('here is info', info)

# cmd_yum_list = 'yum list > yum_package_list.txt'
# cmd_rpm_qa = 'rpm -qa > rpm_qa_list.txt'
# os.system(cmd_rpm_qa)
# os.system(cmd_yum_list)

# new_package = PackageStats()
# checker = FieldChecker(new_package)

# stuff = 'yum info libxcb-1.12-1.amzn2.0.2.i686'
# cmd = 'yum info'
# package = 'GeoIP.x86_64'
# b = subprocess.check_output(stuff, shell=True)
# print(b)
# result = str(b, 'utf-8')
# package_info = result.split('\n')
# for info in package_info[4:]:
    # print(info)
    # new_package.parse_package_name(info)
    # name = checker.check_package_field('name', info)
    # print(name)
# package_info = list(result)
# print(package_info)
# print(result)
# print(type(result))
# checker.








# checker = FieldChecker()
# checker.create_name_listing('yum_package_list.txt')





# checker = FieldChecker()
# package = PackageStats()
# package_info = open('my_packages.txt', 'r')
# read_info = package_info.readlines()
# cleaned_yum_listing = read_info[4:8]

# server_package_info = []
# for item in cleaned_yum_listing:
#     package_name = 
    
# print(cleaned_yum_listing)
# item = read_info[4]
# print(item)
# item_values = item.split(' ')[0]
# print(item_values)
# print(item.split(' ')[0])
# print(item.split(' ')[1])
# print(item.split(' ')[2])

# cmd_test = 'yum info vsftpd > pacakge_info.txt'
# os.system(cmd_test)

# correct speling

# info = open('pacakge_info.txt', 'r')
# read_info = info.readlines()
# key_check = checker.check_package_field(read_info[5], 'archy')
# print(key_check)

# get_package_list = 'yum list > my_packages.txt'
# returned_value = os.system(get_package_list)  # returns the exit code in uni











# k, v = clean_field(read_info[5])
# print(k)
# print(v)
# print(len(value))
# print(value[0])
# print(value[-1])

# for item in read_info:
    # clean_field(item)


# send command into terminal
# get_package_list = 'yum list > my_packages.txt'
# returned_value = os.system(get_package_list)  # returns the exit code in unix

# read infor from package list

# def get_rpm_url(package_name):
#     cmd = 'yumdownloader --urls {}'.format('package_name')
#     url = os.system(cmd)

#     return url

# test_package = 'at-spi2-atk-2.22.0-2.amzn2.0.2.x86_64'
# url = get_rpm_url(test_package)
# print(url)

# packages = open('my_packages.txt', 'r')
# package_listing = packages.readlines()

# package_details = {}
# count = 1
# for package in package_listing:
#     package_details['package']['listing_number'] = count
#     package_details['name'] = package
#     count += 1

# print(package_details)
