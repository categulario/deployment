#!/usr/bin/env python2
from subprocess import call
from datetime import datetime
from actions import deploy_repo
import os
import json

if __name__ == '__main__':
    dirname = raw_input('Enter the directory that we will use to deploy: ')

    if os.path.isdir(dirname):
        print('directory already exists')
        exit(1)

    remote  = raw_input('please enter remote url (ensure current user can clone): ')
    deployname = datetime.now().strftime('%Y%m%d%H%M%S')

    call(['mkdir', '-p', dirname])

    release_dir = os.path.abspath(os.path.join(dirname, 'releases'))
    call(['mkdir', release_dir])

    deploy_dir = os.path.abspath(os.path.join(release_dir, deployname))
    call(['git', 'clone', remote, deployname])

    deploy_script = os.path.join(deploy_dir, '.deployfile')
    if os.path.isfile(deploy_script):
        # should deploy
        script = json.load(deploy_script)['update']

        deploy_data = {
            'head'    : head,
            'repo'    : repo_name,
            'started' : datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'commits' : commits,
            'type'    : 'git',
            'target'  : ref,
        }

        deploy_repo(deploy_dir, deploy_data, script)
    else:
        json.dump(open(deploy_script, 'w'), {
            'update': [],
        }, indent=4)

    develop_dir = os.path.abspath(os.path.join(dirname, 'develop'))
    master_dir = os.path.abspath(os.path.join(dirname, 'master'))

    call(['ln', '-s', src, dst])
    call(['ln', '-s', src, dst_master])
