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
        self.package_list = {'packages': []}
        # self.package = PackageStats()
        self.key_fields = [
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

    def get_qualified_url(self, package_name):
        """Returns full url for rpm package download."""
        # print(package_name)
        cmd = f'yumdownloader --url {package_name} | grep "http"'
        url_in_bytes = subprocess.check_output(cmd, shell=True)
        url = str(url_in_bytes, 'utf-8')

        return url

    def create_qualified_url_listing(self):
        """Creates downloadable package http listing."""
        qualified_url_list = open('qualified_url_list.txt', 'a+')
        file_ = open('rpm_package_list.txt', 'r')
        read_file = file_.readlines()

        for package in read_file:
            url = self.get_qualified_url(package.rstrip())
            qualified_url_list.write(url)

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

    def has_key_value(self, value):
        """Returns boolean for PackageStat property key in value."""
        check = value in self.key_fields 
        return check

    def has_description(self, value):
        check = 'Description :' in value
        return check

    def get_package_description(self, yum_info):
        """Returns description string from yum pacakge.  
        Argument:
        yum_info -- yum package info 
        
        Special: 
        Pacakge values can be std, missing, or extended descritpions.
        """
        has_description = False
        description = ''
        no_description = 'no package description provided'

        # looping through info to add additional description langauge to value
        for item in yum_info:
            if 'Description :' in item:
                has_description = True
            
            if has_description:
                try: 
                    extended_description = item.split(':')[1]
                    description += ' ' + extended_description.rstrip()
                except:
                    pass

        print('running description check with description chekc', has_description)
        if has_description:
            return description
        else:
            return no_description

    def get_yum_package_info(self, package_name):
        """Returns array of package info (e.g. Name, Arch, etc)."""
        cmd = f'yum info {package_name}'
        output = subprocess.check_output(cmd, shell=True)
        info = str(output, 'utf-8').split('\n')
        yum_info = info[4:]

        return yum_info
    
    def create_package(self, yum_info_set):
        """Updates package listing using yum data."""
        # print('trying to create package')
        # print(yum_info_set)
        new_package = {}

        # looping through yum data and updating package with parsed info
        for item in yum_info_set:
            field_data = self.parse_raw_field_info(item)
            key = field_data['key']
            value = field_data['value']

            has_key_field = self.has_key_value(key)
            if has_key_field:
                new_package[key] = value
        
        description = self.get_package_description(yum_info_set)
        new_package['description'] = description

        self.package_list['packages'].append(new_package)
    
    def create_package_listing(self):
        """Creates full package listing with avaiable yum data."""
        rpm_file = 'rpm_package_list.txt'
        names = open(rpm_file, 'r')
        package_names = names.readlines()
        for package in package_names:
            yum_info = self.get_yum_package_info(package)
            self.create_package(yum_info)
        
        self.package_list['package_count'] = len(self.package_list['packages'])
        print('here is full pack list', self.package_list)
