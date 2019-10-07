"""Runs cli commands to capture package libries and dependencies."""
import os
import datetime
import json
import logging
import subprocess


logging.basicConfig(
    format='%(levelname)s:%(message)s',
    level=logging.INFO,
    filename='package_report.txt')


class PackageListCreator():
    def __init__(self, bucket_name=None, export=None):
        self.bucket_name = bucket_name
        self.summary_rpm_list_count = 0
        self.summary_yum_list_count = 0
        self.missing_qualified_urls = {'count': 0, 'packages': []}
        self.missing_descriptions = {'count': 0, 'packages': []}
        self.package_list = {'packages': []}
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

    def create_packages_folder(self, folder_name='user_packages'):
        cmd = '''
        varDIR="{}"
        if [ -d "$varDIR" ]; then
        echo
        else
        mkdir {}
        fi
        '''.format(folder_name, folder_name)
        subprocess.call(cmd, shell=True)

    def create_yum_listing(self):
        logging.info('...creating yum listing file')
        cmd = 'yum list installed > user_packages/yum_package_list.txt'
        subprocess.call(cmd, shell=True)

    def create_rpm_listing(self):
        logging.info('...creating rpm listing file')
        cmd = 'rpm -qa > user_packages/rpm_package_list.txt'
        subprocess.call(cmd, shell=True)

    def install_rpm_listing(self,):
        """Installs downloaded s3 requirements file."""
        cmd = 'sudo yum install $(cat s3_requirements_list.txt) -y'
        subprocess.call(cmd, shell=True)

    def import_s3_package_listing(self, bucket_name, filename):
        """Downloads s3 requirements file listing and updates file name."""
        logging.info('...copying requirements file from s3')
        updated_filename = 's3_requirements_list.txt'
        cmd = f'aws s3 cp s3://{bucket_name}/{filename} user_packages/{updated_filename}'
        subprocess.call(cmd, shell=True)

    def create_name_listing(self):
        """Parses yum package list to create names listing."""
        logging.info('...creating names only package listing file')
        file_name = 'user_packages/yum_package_list.txt'
        package_listing_raw = open(file_name, 'r')
        package_name_listing = open('user_packages/packages_names_only.txt', 'a+')
        read_listing = package_listing_raw.readlines()
        read_listing = read_listing[4:8]

        for package_info in read_listing:
            package_name = package_info.split(' ')[0]
            package_name_listing.write(package_name + '\n')

        package_name_listing.close()

    def get_qualified_url(self, package_name):
        """Returns full url for rpm package download."""
        logging.info(f'...grabbing qualified url for {package_name}')

        try:
            cmd = f'yumdownloader --url {package_name} | grep "http"'
            url_in_bytes = subprocess.check_output(cmd, shell=True)
            url = str(url_in_bytes, 'utf-8')
            return url
        except Exception as e:
            url_error = f'Error: could not grab qualified url for {package_name}.'
            self.missing_qualified_urls['count'] += 1
            self.missing_qualified_urls['packages'].append(package_name)
            return url_error

    def create_qualified_url_listing(self):
        """Creates downloadable package http listing."""
        logging.info('...creating package qualified url listing file')
        qualified_url_list = open('user_packages/qualified_url_list.txt', 'a+')
        file_ = open('rpm_package_list.txt', 'r')
        read_file = file_.readlines()
        package_count = len(read_file)

        try:
            for package in read_file:
                url = self.get_qualified_url(package.rstrip())
                qualified_url_list.write(url)
                logging.info(
                    f'...created qualified url listing for {package_count} packages')
        except:
            pass

    def parse_raw_field_info(self, read_line):
        """Returns parsed package listing key-value pair.

        Arguments:
        read_line -- passed yum package information
        """
        try:
            values = read_line.split(':')
            field_key = values[0].strip()
            field_value = values[1].strip()
            data = {
                'key': field_key,
                'value': field_value
            }
        except:
            data = {
                'key': values[0],
                'value': 'no data provided'
            }

        return data

    def has_key_value(self, value):
        """Returns boolean if 'value' is in key field list."""
        check = value in self.key_fields
        return check

    def has_description(self, value):
        check = 'Description :' in value
        return check

    def get_package_description(self, yum_info_set, package_name=None):
        """Returns description string from yum pacakge.  
        Argument:
        yum_info_set -- yum package info 

        Special: 
        Pacakge values can be std, missing, or extended descritpions.
        """
        logging.info(f'...grabbing description for {package_name}')
        has_description = False
        description = ''
        no_description = 'no package description provided'

        # looping through info to add additional description langauge to value
        for item in yum_info_set:
            if 'Description :' in item:
                has_description = True
            
            if has_description:
                try:
                    extended_description = item.split(':')[1]
                    description += ' ' + extended_description.rstrip()
                except:
                    pass

        if has_description:
            return description
        else:
            self.missing_descriptions['count'] += 1
            self.missing_descriptions['packages'].append(package_name)
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
        new_package = {}

        # looping through yum data and updating package with parsed info
        for item in yum_info_set:
            field_data = self.parse_raw_field_info(item)
            key = field_data['key']
            value = field_data['value']

            has_key_field = self.has_key_value(key)
            if has_key_field:
                new_package[key] = value

        try:
            package_name = new_package['name']
        except:
            package_name = None

        description = self.get_package_description(package_name, yum_info_set)
        new_package['description'] = description
        self.package_list['packages'].append(new_package)
        logging.info('...creating package information for {}'.format(
            new_package['name']))

    def create_package_listing(self):
        """Creates full package listing with avaiable yum data."""
        rpm_file = 'user_packages/rpm_package_list.txt'
        names = open(rpm_file, 'r')
        package_names = names.readlines()
        for package in package_names:
            yum_info_set = self.get_yum_package_info(package)
            self.create_package(yum_info_set)

        self.package_list['package_count'] = len(self.package_list['packages'])
        logging.info('...completed package listing update.')

    def create_summary(self):
        summary_data = {
            'summary': {
                'report_created': datetime.datetime.today().strftime('%c'),
                'general': {
                    'rpm_package_count': self.summary_rpm_list_count,
                    'yum_package_count': self.summary_yum_list_count,
                    'missing_urls': self.missing_qualified_urls,
                    'missing_descriptions': self.missing_descriptions
                }
            }
        }

        summary_report = open('user_packages/summary_report.json', 'w')
        summary_report.write(json.dumps(summary_data))
        summary_report.close()

    def run_install(self, bucket_name, filename):
        """User may be asked to enter password."""
        self.import_s3_package_listing(bucket_name, filename)
        self.install_rpm_listing()

    def run(self):
        self.create_packages_folder()
        self.create_yum_listing()
        self.create_rpm_listing()
        self.create_name_listing()
        self.create_qualified_url_listing()
        self.create_package_listing()
        self.create_summary()
