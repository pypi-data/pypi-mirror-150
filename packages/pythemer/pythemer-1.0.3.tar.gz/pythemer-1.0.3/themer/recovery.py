# THEMER #
# apps.py #
# COPYRIGHT (c) Jaidan 2022- #

# Imports #
from genericpath import exists
from os import remove
from themer.logger import logger
from themer.typedef import Plist

def __icon_backup_name(plist) -> str: 
    if type(plist) is Plist:
        plist = vars(plist)
    return str(plist.get('resource_path') + '/' + str(plist.get('name')).replace(' ', '') + '-' + plist.get('icon_asset') + '-ORIGINAL.icns')

def check(plist) -> bool: 
    '''Check if an app's original icon has been backed up.'''
    try:
        return exists(__icon_backup_name(plist))
    except:
        logger.error('Could not check if {}\'s original icon has been backed up. ({})'.format(plist.bundle_id, plist.path))
        exit(1)

def backup(plist: Plist):
    '''Back up an app's original icon.'''
    try:
        # Check if it's already backed up #
        if check(plist): return
        # Get the app's icon #
        data = open(str(plist.resource_path + '/' + plist.icon_asset + '.icns'), 'rb').read()
        # Write to backup #
        open(__icon_backup_name(plist), 'wb').write(data)
        # Return #
        return
    except Exception as e:
        print(e)
        logger.error('Unable to back up original icon for {}. ({})'.format(plist.bundle_id, plist.path))
        exit(1)

def enact_backup(plist: dict):
    '''Recover an app's original icon.'''
    try:
        # Check #
        if not check(plist): return
        with open(str(plist.get('resource_path') + '/' + plist.get('icon_asset') + '.icns'), 'wb') as f:
            # Get backup #
            data = open(__icon_backup_name(plist), 'rb').read()
            # Write #
            f.write(data)
            # Delete backup #
            remove(__icon_backup_name(plist))
            # Close #
            f.close()
        # Return #
        return
    except:
        logger.error('Could not reset to original icon for {}. ({})'.format(plist.get('bundle_id'), plist.get('path')))
        exit(1)
