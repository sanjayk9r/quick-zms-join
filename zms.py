#!/usr/bin/env python3


import argparse
import shlex
import subprocess
import json
import sys
import os


class ConfigManager(object):
    """ Manage zms config """

    def __init__(self):
        self.config_dir = os.path.join(os.environ.get('HOME'), '.zms')
        self.config_abs_path = os.path.join(self.config_dir, 'zms.json')
        self.sh_alias_file_path = os.path.join(self.config_dir, 'zms-alias')
        self.zoommtg = 'zoommtg://zoom.us/join?action=join&confno={0}'


    def manage_config(self, configs):
        if not os.path.exists(self.config_dir):
            try:
                os.mkdir(self.config_dir)
            except OSError as e:
                sys.stderr.write(str(e) + "\n")
                sys.exit(1)

        with open(self.config_abs_path, 'w') as f:
            f.write(json.dumps(configs))
            return True
        

    def read_config(self):
        """ read config stored in user home directory """
        try:
            with open(self.config_abs_path) as f:
                configs = json.load(f)
                return configs
        except FileNotFoundError:
            self.manage_config(configs={})
            self.read_config()


    def get_meeting_id(self, alias_name):
        " get meeting id for given alias name"""
        configs = self.read_config()
        return configs.get(alias_name)


    def add_meeting(self, meeting_id=None, alias_name=None):
        """ add a meeting id by alias name"""
        configs = self.read_config()
        if alias_name in configs:
            raise RuntimeError(f"entry exists already.")
        configs[alias_name] = meeting_id
        return self.manage_config(configs)


    def remove_meeting(self, alias_name):
        """ remove a meeting by alias name """
        configs = self.read_config()
        try:
          del configs[alias_name]
          print(f"removing alias entry for {alias_name}")
          self.create_shell_alias_entry(configs)
          self.manage_config(configs)
        except KeyError:
            print(f"{alias_name} doesn't exist, create it!")

    
    def list_meeting(self):
        """ list all existing entries """
        configs = self.read_config()
        if configs:
            for alias, meeting_id in configs.items():
                print(f"{alias: <10}\t{meeting_id: <10}")
        else:
            print("no entry found")
    

    def create_shell_alias_entry(self, configs):
        """ Create an entry in alias file to be sourced """
        entries = ""
        for alias, _ in configs.items():
            entries += f"alias {alias}='{os.path.abspath(__file__)} --alias_name {alias}'\n"
        
        with open(self.sh_alias_file_path, 'w') as f:
            f.write(entries)

        print("---")
        print(f"Create entry in .bash_profile or .profile")
        print(f"source {self.sh_alias_file_path}")
        print("---")


def main(args):
    config_manager = ConfigManager()

    # platform
    prog = "open"
    if sys.platform.lower() == 'linux':
        prog = "xdg-open"
    
    # Create shell alias
    if args.create_alias:
        configs = config_manager.read_config()
        try:
            config_manager.create_shell_alias_entry(configs)
        except Exception as e:
            print(f"error creating aliases - {e}")

    # Delete a meeting entry
    if args.remove_entry:
        if args.alias_name:
            config_manager.remove_meeting(args.alias_name)
        else:
            print("must provide an alias name for an entry removal")       

    # List Meeting entries
    if args.list_entry:
        config_manager.list_meeting()

    # Add a new entry for meeting
    if args.meeting_id and args.alias_name:
        if os.path.exists(config_manager.config_abs_path):
            get_meet_id = config_manager.get_meeting_id(args.alias_name)
            if get_meet_id:
                # Join Zoom Meeting
                print(f"[Meeting ID: {get_meet_id}] Joining Meeting...")
                command_args = shlex.split(f"{prog} " + config_manager.zoommtg.format(get_meet_id))
                pid = subprocess.Popen(command_args).pid
                print(f"Started it with PID: {pid}, select audio type in Zoom client")

            else:
                # update meeting ID
                if config_manager.add_meeting(meeting_id=args.meeting_id, alias_name=args.alias_name):
                    print(f"meeting id - {args.meeting_id} added with alias name: {args.alias_name}")
        else:
            # initialise the config file
            configs = config_manager.read_config()
            if not configs:
                configs = {}
            if config_manager.manage_config(configs):
                print(f"config is initialised.")
                if config_manager.add_meeting(meeting_id=args.meeting_id, alias_name=args.alias_name):
                    print(f"meeting id - {args.meeting_id} added with alias name: {args.alias_name}")
    
    # Join Meeting with alias name
    if args.meeting_id is None \
        and args.alias_name \
        and not args.remove_entry:
        get_meet_id = config_manager.get_meeting_id(args.alias_name)
        if get_meet_id:
            # Join Zoom Meeting
            print(f"[Meeting ID: {get_meet_id}] Joining Meeting...")
            command_args = shlex.split(f"{prog} " + config_manager.zoommtg.format(get_meet_id))
            pid = subprocess.Popen(command_args).pid
            print(f"Started it with PID: {pid}, select audio type in Zoom client")
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog=sys.argv[0], 
        description='Utility to join Zoom from command line.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,) 
    parser.add_argument('-m', '--meeting_id', default=None, type=int, help='Meeting ID from your zoom invite')
    parser.add_argument('-a', '--alias_name', default=None, help='A friendly short name easier to remember')
    parser.add_argument('-r', '--remove_entry', action='store_true', help='Remove an entry from config')
    parser.add_argument('-c', '--create_alias', action='store_true', help='Create a shell alias for it')
    parser.add_argument('-l', '--list_entry', action='store_true', help='List all zoom meeting entries')

    # parse arguments
    args = parser.parse_args()

    main(args)
