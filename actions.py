import cherrypy
import os
import subprocess
from lib.settings_loader import settings
import platform
from datetime import datetime

notify_adapter = __import__('lib.notify.'+settings.NOTIFY_ADAPTER).notify.__getattribute__(settings.NOTIFY_ADAPTER)
is_windows     = platform.system() == 'Windows'

def deploy_repo(repo_dir, deploy_data, script):
    cherrypy.log('deploying repo ' + repo_dir, context='GIT')

    os.chdir(repo_dir)

    for command in script:
        process = subprocess.call(command.split(' '), shell=is_windows)

    deploy_data.update({
        'finished': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    })

    notify_adapter.deploy_finished(deploy_data)

    cherrypy.log('finished deploy ' + repo_dir, context='GIT')
