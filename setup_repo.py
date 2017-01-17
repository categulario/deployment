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
    project_dir = os.path.abspath(dirname)

    remote  = raw_input('please enter remote url (ensure current user can clone): ')
    deployname = datetime.now().strftime('%Y%m%d%H%M%S')

    call(['mkdir', '-p', project_dir])

    release_dir = os.path.abspath(os.path.join(project_dir, 'releases'))
    call(['mkdir', release_dir])

    deploy_dir = os.path.abspath(os.path.join(release_dir, deployname))
    call(['git', 'clone', remote, deploy_dir])

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
        print("Please add a .deployfile in the root of your repository")

    develop_dir = os.path.abspath(os.path.join(project_dir, 'develop'))
    master_dir = os.path.abspath(os.path.join(project_dir, 'master'))

    call(['ln', '-s', deploy_dir, develop_dir])
    call(['ln', '-s', deploy_dir, master_dir])

# now we create or update repository configuration

    if not os.path.isfile('repos.json'):
        data = {}
        print('will create new repos.json')
    else:
        try:
            data = json.load(open('repos.json', 'r'))
        except ValueError:
            print('corrupted repos.json')
            exit(2)
        print('using existing repos.json')

    data[remote] = {
        'path': project_dir,
    }

    json.dump(data, open('repos.json', 'w'))
