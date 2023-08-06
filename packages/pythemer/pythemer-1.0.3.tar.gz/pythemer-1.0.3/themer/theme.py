# THEMER #
# main.py #
# COPYRIGHT (c) Jaidan 2022- #

# Imports #
from genericpath import exists
from json import loads
from os import (environ, system, unlink)
from themer.library import get_library
from themer.logger import logger
from themer.recovery import (backup, enact_backup)
from themer.typedef import Theme

def get_theme(name: str) -> Theme:
    '''Get a theme from the library.'''
    # Get library #
    library = get_library()
    if library is []:
        logger.error('Could not find any themes.')
        exit(1)
    # Loop through themes #
    for theme in library:
        if theme.name.lower() == name.lower():
            return theme
    # Print error #
    logger.error(
        f'Could not find theme by the name of \'{name}\'. Maybe try running \'themer library list\'?')
    exit(1)
            
def refresh_cache():
    system('killall Finder')
    system('killall Dock')
            
def activate_theme(name: str):
    '''Activate a theme.'''
    if exists(f'{environ.get("HOME")}/.themer/ACTIVE'):
        logger.error('There is an active theme. Please deactivate it first.')
        exit(1)
    # Get the theme #
    theme = get_theme(name)
    # Print theme name #
    logger.info('Activating \'{}\'.'.format(theme.name))
    # Loop through icons #
    for icon in theme.icons:
        if icon.plist.icon_asset is None:
            continue
        # Make icon backup #
        backup(icon.plist)
        # Replace icon #
        with open(str(icon.plist.resource_path + '/' + icon.plist.icon_asset + '.icns'), 'wb') as img:
            img.write(icon.data)
            system('touch {}'.format(str(icon.plist.path.replace(' ', '\ '))))
            img.close()
    # Clear cache #
    logger.info('Refreshing cache...')
    refresh_cache()
    logger.info('Successfully activated \'{}\'.'.format(theme.name))
    with open(f'{environ.get("HOME")}/.themer/ACTIVE', 'w') as file:
        dictionary = {'name': theme.name, 'icons': []}
        for icon in theme.icons:
            dictionary['icons'].append({'name': icon.plist.name, 'plist': vars(icon.plist)})
        file.write(repr(dictionary))
    
def deactivate_theme():
    '''Deactivate the current theme.'''
    if not exists(f'{environ.get("HOME")}/.themer/ACTIVE'):
        logger.error('No active theme.')
        exit(1)
    with open(f'{environ.get("HOME")}/.themer/ACTIVE', 'r') as file:
        t_obj = loads(file.read().replace('\'', '"'))
        get_library(True)
        # Print theme name #
        logger.info('Deactivating \'{}\'.'.format(t_obj.get('name')))
        # Loop through icons #
        for icon in t_obj.get('icons'):
            if icon.get('plist').get('icon_asset') is None:
                continue
            # Remove icon file #
            unlink(str(icon.get('plist').get('resource_path') + '/' + icon.get('plist').get('icon_asset') + '.icns'))
            # Enact icon backup #
            enact_backup(icon.get('plist'))
            # Clear cache #
            system('touch {}'.format(str(icon.get('resource_path')).replace('Contents/Resources', '').replace(' ', '\ ')))
        # Clear cache #
        logger.info('Refreshing cache...')
        refresh_cache()
        logger.info('Successfully deactivated \'{}\'.'.format(t_obj.get('name')))
        unlink(f'{environ.get("HOME")}/.themer/ACTIVE')