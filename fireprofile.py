#!/usr/bin/env python
from optparse import OptionParser
import os
import shutil
import subprocess
import sys

# Directory configuration
applications_root = '/Applications'
firefox_root      = os.path.expanduser('~/Library/Application Support/Firefox')
profiles_root     = os.path.join(firefox_root, 'Profiles')
ini_filemane      = os.path.join(firefox_root, 'profiles.ini')

class LaunchProfile():
    def __init__(self):
        parser = OptionParser()
        parser.add_option('-l', '--list-profiles', dest='list_profiles', action='store_true', default=False,
            help='List available versions and profiles')
        parser.add_option('-v', '--version', dest='version', default=-1,
            help='Specify the firefox version to run')
        parser.add_option('-p', '--profile', dest='profile', default=-1,
            help='Specify the firefox profile to load')
        parser.add_option('-d', '--delete-profile', dest='delete_profile', default=-1,
            help='Specify the firefox profile to delete')

        self.options, self.args = parser.parse_args()
        self.versions = self.get_versions()
        self.profiles = Profiles()

        if (self.options.profile == -1 or self.options.version == -1) and self.options.delete_profile == -1:
            self.options.list_profiles = True

    def run(self):
        if self.options.list_profiles:
            print('Available versions:')
            for counter, version in enumerate(self.versions):
                print('  [-v %i] %s' % (counter, version))
            print
            print('Available profiles:')
            for counter, profile in enumerate(self.profiles.list_profiles()):
                print('  [-p %i] %s' % (counter, profile))
            return

        elif self.options.delete_profile != -1:
            try:
                deleted_profile = self.profiles.delete_profile_by_index(int(self.options.delete_profile))
            except ValueError:
                deleted_profile = self.profiles.delete_profile_by_name(self.options.delete_profile)
            except IndexError:
                sys.exit('Profile index out of range')
            print 'Deleted profile %s' % deleted_profile
            return

        try:
            profile_name = self.profiles.get_profile_by_index(int(self.options.profile))
        except ValueError:
            profile_name = self.profiles.get_profile_by_name(self.options.profile)
        except IndexError:
            sys.exit('Profile index out of range')

        version_name = self.options.version
        if version_name not in self.versions:
            try:
                version_name = self.versions[int(self.options.version)]
            except ValueError:
                sys.exit('Version name %s not valid' % self.options.version)
            except IndexError:
                sys.exit('Version index out of range')

        subprocess.Popen([
            '/Applications/%s/Contents/MacOS/firefox-bin' % version_name,
            '-P', profile_name,
        ])

    def get_versions(self):
        'Look through the APPLICATIONS folder for files containing the word firefox '
        versions = []
        for application in os.listdir(applications_root):
            if application.lower().find('firefox') > -1:
                versions.append(application)
        return sorted(versions)


class Profiles():
    def __init__(self):
        self.profiles = self._get_profiles()
        self.profile_ini_header = self._get_profile_ini_header()

    def _get_profiles(self):
        ' Parse the profiles from disk into an object we can actually use '
        return sorted([profile for profile in os.listdir(profiles_root)])

    def _write_profiles(self, default_profile=None):
        ini_file_string = self.profile_ini_header
        for counter, profile in enumerate(self.profiles):
            ini_file_string += '[Profile%i]\n' % counter
            ini_file_string += 'Name=%s\n' % profile
            ini_file_string += 'IsRelative=1\n'
            ini_file_string += 'Path=Profiles/%s\n' % profile
            if profile == default_profile:
                ini_file_string += 'Default=1\n'
            ini_file_string += '\n'

        with open(ini_filemane, 'w') as ini_file:
            ini_file.write(ini_file_string)

    def _get_profile_ini_header(self):
        ' Grab the header from the existing profiles.ini header '
        header_string = ''
        with open(ini_filemane, 'r') as ini_file:
            for line in ini_file:
                if line.find('[Profile') == 0:
                    break
                else:
                    header_string += line
        return header_string

    def create_new_profile(self, profile_name):
        os.mkdir(os.path.join(profiles_root, profile_name))
        self.profiles.append(profile_name)
        self.profiles.sort()
        self._write_profiles(default_profile=profile_name)

    def delete_profile_by_index(self, profile_index):
        if profile_index > len(self.profiles) or profile_index < 0:
            raise IndexError('Profile index out of range')

        return self.delete_profile_by_name(self.profiles[profile_index])

    def delete_profile_by_name(self, profile_name):
        if profile_name in self.profiles:
            self.profiles.remove(profile_name)
            shutil.rmtree(os.path.join(profiles_root, profile_name))
            self._write_profiles(self)

        return profile_name

    def get_profile_by_index(self, index):
        return self.profiles[index]

    def get_profile_by_name(self, name, create_new=True):
        if not name in self.profiles and create_new:
            self.create_new_profile(name)
        return name

    def list_profiles(self):
        return self.profiles


if __name__ == '__main__':
    fp = LaunchProfile()
    fp.run()
