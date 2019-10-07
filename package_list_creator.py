"""Runs cli commands to capture package and dependency information."""
import os
import datetime
import json
import logging
import subprocess
import shutil


logging.basicConfig(
    format='%(levelname)s:%(message)s',
    level=logging.INFO,
    filename='package_report.txt')


class PackageListCreator():
    def __init__(self, bucket_name=None, export=None):
        self.bucket_name = bucket_name
        self.summary_info_rpm_count = 0
        self.summary_info_yum_count = 0
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
        logging.info('...createing user packages folder.')
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
        """Creates yum package listing and sets package count value."""
        logging.info('...creating yum listing file')
        file_name = 'user_packages/yum_package_list.txt'
        cmd = f'yum list installed > {file_name}'
        subprocess.call(cmd, shell=True)
        file_ = open(file_name, 'r')
        count = len(file_.readlines())
        self.summary_info_yum_count = count

    def create_rpm_listing(self):
        """Creates rpm package listing and sets package count value."""
        logging.info('...creating rpm listing file')
        file_name = 'user_packages/rpm_package_list.txt'
        cmd = f'rpm -qa > {file_name}'
        subprocess.call(cmd, shell=True)
        file_ = open(file_name, 'r')
        count = len(file_.readlines())
        self.summary_info_rpm_count = count

    def create_name_listing(self):
        """Parses yum package list to create names listing."""
        logging.info('...creating names only package listing file')
        file_name = 'user_packages/yum_package_list.txt'
        package_listing_raw = open(file_name, 'r')
        package_name_listing = open('user_packages/packages_names_only.txt', 'a+')
        read_listing = package_listing_raw.readlines()
        read_listing = read_listing[4:]

        for package_info in read_listing:
            package_name = package_info.split(' ')[0]
            package_name_listing.write(package_name + '\n')

        package_name_listing.close()

    def _get_qualified_url(self, package_name):
        """Returns json containing package name and url for rpm package download."""
        logging.info(f'...grabbing qualified url for {package_name}')

        try:
            cmd = f'yumdownloader --url {package_name} | grep "http"'
            url_in_bytes = subprocess.check_output(cmd, shell=True)
            url = str(url_in_bytes, 'utf-8')
            return {'Name': package_name, 'URL': url }
        except Exception as e:
            url_error = 'could not grab qualified url'
            self.missing_qualified_urls['count'] += 1
            self.missing_qualified_urls['packages'].append(package_name)
            return {'Name': package_name, 'URL': url_error }

    def create_qualified_url_listing(self):
        """Creates downloadable package http listing."""
        logging.info('...creating package qualified url listing file')
        qualified_url_list = open('user_packages/qualified_url_list.json', 'a+')
        file_ = open('user_packages/rpm_package_list.txt', 'r')
        read_file = file_.readlines()
        package_count = len(read_file)

        try:
            for package in read_file:
                url_info = self._get_qualified_url(package.rstrip())
                qualified_url_list.write(json.dumps(url_info))
                qualified_url_list.write('\n')
                logging.info(
                    f'...created qualified url listing for {package_count} packages')
        except Exception as e:
            logging.error(f'...could not create qualified url listing do to error: {e}')

    def _parse_raw_field(self, read_line):
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

    def _has_key_field(self, value):
        """Returns boolean if 'value' is in key field list."""
        check = value in self.key_fields
        return check

    def _parse_description(self, yum_info_set, package_name=None):
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
        """Parses yum info fields and updates package listing."""
        new_package = {}

        # looping through yum data and updating package with parsed info
        for item in yum_info_set:
            field_data = self._parse_raw_field(item)
            key = field_data['key']
            value = field_data['value']

            has_key_field = self._has_key_field(key)
            if has_key_field:
                new_package[key] = value

        try:
            package_name = new_package['Name']
        except Exception as e:
            package_name = None

        # parsing yum info to return description or 'missing data' message
        description = self._parse_description(yum_info_set, package_name)
        new_package['description'] = description.strip()
        self.package_list['packages'].append(new_package)
        logging.info('...saving package information for {}'.format(
            new_package['Name']))

    def create_package_listing(self):
        """Updates object package list array with avaiable yum data.
        
        Creates final package listing file containing.
        """
        logging.info('...completing package listing update.')
        all_package_info = open('user_packages/final_package_report.json', 'w')
        rpm_file = 'user_packages/rpm_package_list.txt'
        names = open(rpm_file, 'r')
        package_names = names.readlines()

        for package in package_names:
            yum_info_set = self.get_yum_package_info(package)
            self.create_package(yum_info_set)

        self.package_list['package_count'] = len(self.package_list['packages'])
        all_package_info.write(json.dumps(self.package_list))

    def _create_summary(self):
        """Creates summary file describing instance package information.  

        Should be run only as part of self.run() as some class values are set only once in memory (e.g. summary_info_rpm_count).
        """
        summary_data = {
            'summary': {
                'report_created': datetime.datetime.today().strftime('%c'),
                'package_info': {
                    'rpm_package_count': self.summary_info_rpm_count,
                    'yum_package_count': self.summary_info_yum_count,
                    'missing_urls': self.missing_qualified_urls,
                    'missing_descriptions': self.missing_descriptions
                }
            }
        }

        summary_report = open('user_packages/summary_report.json', 'w')
        summary_report.write(json.dumps(summary_data))
        summary_report.close()

    def _install_rpm_listing(self,):
        """Installs downloaded s3 requirements file."""
        cmd = 'sudo yum install $(cat s3_requirements_list.txt) -y'
        subprocess.call(cmd, shell=True)

    def _import_s3_package_listing(self, bucket_name, filename):
        """Downloads s3 requirements file listing and updates file name."""
        logging.info('...copying requirements file from s3')
        updated_filename = 's3_requirements_list.txt'
        cmd = f'aws s3 cp s3://{bucket_name}/{filename} user_packages/{updated_filename}'
        subprocess.call(cmd, shell=True)

    def _zip_user_packages(self, bucket_name):
        """Zip user_packages files and upload to s3 bucket."""
        today = datetime.datetime.today()
        created_at = today.strftime('%b_%d_%Y')
        
        try:
            zipped_folder_path = shutil.make_archive(f'package_zip_{created_at}', 'zip', 'user_packages')
        except Exception as e:
            logging.error(e)

        try:
            cmd = f'aws s3 cp {zipped_folder_path} s3://{bucket_name}/project_packages'
            subprocess.call(cmd, shell=True)
        except Exception as e:
            logging.error(e)

    def run_install(self, bucket_name, filename):
        """Installs downloaded pacakge list.
        
        Should be updated to install from either internet or zip folder if interet is inaccessible.  User may be asked to enter password.
        """
        self._import_s3_package_listing(bucket_name, filename)
        self._install_rpm_listing()

    def run(self, bucket_name):
        self.create_packages_folder()
        self.create_yum_listing()
        self.create_rpm_listing()
        self.create_name_listing()
        self.create_qualified_url_listing()
        self.create_package_listing()
        self._create_summary()
        self._zip_user_packages(bucket_name)
