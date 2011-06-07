#!/usr/bin/env python
from optparse import OptionParser
import os
import shutil
import subprocess
import signal

library_dir    = os.path.expanduser("~/Library")
safari_dir     = os.path.join(library_dir, "Safari")
profiles_dir   = os.path.join(library_dir, "SafariProfiles")
safari_process = "/Safari.app"


class Main():
    def __init__(self):
        parser = OptionParser()
        parser.add_option('-l', '--list-profiles', dest='list_profiles', action='store_true', default=False,
            help='list available profiles')

        options, args = parser.parse_args()

        # Check to see if we need to run the initial setup
        self.setup()

        if options.list_profiles or len(args) == 0:
            print('Current profile: %s\n' % self.get_current_profile())
            print('Available profiles:')
            for counter, profile in enumerate(self.get_profiles()):
                print('  [%i] %s' % (counter, profile))
            return

        self.launch_profile(args[0])

    def get_current_profile(self):
        return os.readlink(safari_dir).split("/")[-1]

    def launch_profile(self, profile_name):
        profiles = self.get_profiles()
        if profile_name in profiles:
            profile = profile_name

        else:
            try:
                # See if we are passed an index
                profile = profiles[int(profile_name)]
            except ValueError:
                profile = None
            
        if profile is None:
            print("Creating new profile - %s" % profile_name)
            os.mkdir(os.path.join(profiles_dir, profile_name))
            profile = profile_name

        # Kill the existing process
        for line in os.popen("ps xa"):
            cols    = line.split() 
            pid     = cols[0]
            process = cols[4]
            if process.find(safari_process) > 0:
                print("Killing existing Safari process %s" % pid)
                os.kill(int(pid), signal.SIGHUP) 

        if profile != self.get_current_profile():
            # Remove the current profile
            if os.path.isdir(safari_dir):
                os.remove(safari_dir)

            # Activate the desired profile
            print("Activating %s" % profile)
            os.symlink(os.path.join(profiles_dir, profile), safari_dir)

        subprocess.Popen(['/Applications/Safari.app/Contents/MacOS/Safari'])

    def setup(self):
        # Create the directory to hold profile folders
        if not os.path.isdir(profiles_dir):
            print("Creating profiles directory")
            os.mkdir(profiles_dir)

        # If the current Safari profile is not a symlink, bring it into the system!
        if os.path.isdir(safari_dir) and not os.path.islink(safari_dir):
            print("Moving default profile to profiles directory and establishing symlink")
            shutil.move(safari_dir, os.path.join(profiles_dir, "default"))
            os.symlink(os.path.join(profiles_dir, "default"), safari_dir)

    def get_profiles(self):
        return [profile for profile in os.listdir(profiles_dir)]



if __name__ == '__main__':
    # Run it!
    main = Main()
