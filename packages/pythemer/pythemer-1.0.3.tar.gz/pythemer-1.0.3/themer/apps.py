# THEMER #
# apps.py #
# COPYRIGHT (c) Jaidan 2022- #

# Imports #
from os import getuid
from glob import glob
from plistlib import loads
from themer.elevate import elevate
from themer.logger import logger

ALL_PLISTS = []

async def plist(bundle_id: str, apps: list[dict]):
    '''Read an app's plist.'''
    # Initialize needed objects #
    app_obj = None
    plist = None
    # Loop through apps #
    for app in apps:
        try:
            # Open plist #
            with open(app.get('path') + '/Contents/Info.plist', 'rb') as f:
                # Read plist #
                plist_tmp = loads(f.read())
                if plist_tmp.get('CFBundleIdentifier') == bundle_id:
                    plist = plist_tmp
                    app_obj = app
        except:
            pass
    if app_obj is None:
        return None
    if plist is not None:
        try:
            # Map #
            return_value = {
                'CFBundleName': plist.get('CFBundleName') if plist.get('CFBundleName') is not None else plist.get('CFBundleDisplayName'),
                'CFBundleIconFile': plist.get('CFBundleIconFile'),
                'CFBundleIdentifier': plist.get('CFBundleIdentifier'),
                'CFBundleTypeIconFile': plist.get('CFBundleTypeIconFile'),
                'CFBundleExecutable': plist.get('CFBundleExecutable'),
                'AppPath': app_obj.get('path')
            }
        except:
            logger.error('Error reading {}\'s Info.plist'.format(bundle_id))
            exit(1)

    return return_value

def get_apps() -> list[dict]:
    '''Get all installed apps.'''
    try:
        apps = []
        if getuid() != 0:
            logger.info('Requesting root privileges to manage files.')
            elevate()
        #for app in glob('/System/Applications/*.app'):
        #    apps.append(
        #        {'name': app.split('/')[-1].replace('.app', ''), 'path': app})
        for app in glob('/Applications/*.app'):
            apps.append(
                {'name': app.split('/')[-1].replace('.app', ''), 'path': app})
        for app in glob('/Applications/*/*.app'):
            apps.append(
                {'name': app.split('/')[-1].replace('.app', ''), 'path': app})
        return apps
    except:
        logger.error('Could not get app list.')
        exit(1)
