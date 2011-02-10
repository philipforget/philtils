#!/usr/bin/env python
from optparse import OptionParser
import os
import subprocess

# Directory configuration
APPLICATIONS  = "/Applications"
PROFILES_ROOT = os.path.expanduser("~/Library/Application Support/Firefox/Profiles")

def main():
    parser = OptionParser()
    parser.add_option('-l', '--list-profiles', dest='list_profiles', action='store_true', default=False,
        help='List available versions and profiles')
    parser.add_option('-v', '--version', dest='version', default=-1,
        help='Specify the firefox version to run')
    parser.add_option('-p', '--profile', dest='profile', default=-1,
        help='Specify the firefox profile to load')

    options, args = parser.parse_args()
    versions      = get_versions()
    profiles      = get_profiles()

    if options.profile == -1 or options.version == -1:
        options.list_profiles = True

    if options.list_profiles:
        print('Available versions:')
        for counter, version in enumerate(versions):
            print('  [-v %i] %s' % (counter, version))
        print
        print('Available profiles:')
        for counter, profile in enumerate(profiles):
            print('  [-p %i] %s' % (counter, profile))
        return

    try:
        version = versions[int(options.version)]
    except ValueError: 
        version = options.version

    try:
        profile = profiles[int(options.profile)]
    except ValueError: 
        profile = options.profile

    if profile not in profiles:
        print "Profile '%s' does not exist, starting profile picker." % profile

    subprocess.Popen([
        '/Applications/%s/Contents/MacOS/firefox-bin' % version,
        '-P', profile,
    ])

    return

def get_versions():
    'Look through the APPLICATIONS folder for files containing the word firefox '
    versions = []
    for application in os.listdir(APPLICATIONS):
        if application.lower().find('firefox') > -1:
            versions.append(application)
    return versions

def get_profiles():
    'Look through the profiles directory and pull out all profiles'
    profiles = []
    for profile_folder in os.listdir(PROFILES_ROOT):
        if profile_folder.find('.') > 0:
            profiles.append(profile_folder.split('.')[-1])
        else:
            profiles.append(profile_folder)
    return profiles


if __name__ == '__main__':
    main()
