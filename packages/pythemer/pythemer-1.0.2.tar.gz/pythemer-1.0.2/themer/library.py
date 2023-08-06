# THEMER #
# library.py #
# COPYRIGHT (c) Jaidan 2022- #

# Imports #
from genericpath import exists
from glob import glob
from os import (access, environ, makedirs, R_OK, remove)
from shutil import copy
from themer.logger import logger
from themer.typedef import Theme
from yaml import (FullLoader, load)
from zipfile import (BadZipFile, ZipFile)

middle = '├──'
end = '└──'

def unpack(path: str, should_get_apps: bool = True) -> dict:
    '''Unpacks a theme file and provides all of it's data.'''
    try:
        # Open zip file #
        with ZipFile(path, 'r') as zip:
            # Initialize theme object #
            theme_obj = None
            # Loop through files #
            for file in zip.filelist:
                # If the file ends with .yaml #
                if file.filename.endswith('.yml'):
                    # Get the directory in the zip #
                    directory = file.filename.split('/')[0]
                    # Read the yaml #
                    yaml_obj = load(zip.read(file).decode(
                        'utf-8'), Loader=FullLoader)
                    # Assign the theme object #
                    theme_obj = Theme(yaml_obj, path, should_get_apps)
                    # Loop through icons #
                    for icon in theme_obj.icons:
                        try:
                            # Read icon data #
                            icon.data = zip.read(directory + '/' + icon.img)
                        except:
                            logger.error('Could not read {}\'s icon.'.format(
                                icon.plist.bundle_id))
                            exit(1)
            if theme_obj is None:
                logger.logger('Could not find theme manifest.')
                exit(1)
            else:
                # Return #
                return {'theme': theme_obj, 'zip': zip}
    except BadZipFile:
        logger.error('Invalid zip file.')
        exit(1)

def check(path: str):
    if not exists(path):
        logger.error('The specified file does not exist.')
        exit(1)
    if not access(path, R_OK):
        logger.error('Could not read the specified ZIP file. Maybe try moving it to another directory?')
        exit(1)
    return True

def get_library(should_get_apps: bool = True) -> list[Theme]:
    '''Get all themes in the library.'''
    if exists(f'{environ.get("HOME")}/.themer/library'):
        themes = [unpack(t, should_get_apps).get('theme') for t in glob(f'{environ.get("HOME")}/.themer/library/*.zip')]
        if themes is not []: return themes
    return []

def add_theme(path: str):
    '''Add a theme to the library.'''
    check(path)
    theme: Theme = unpack(path, False).get('theme')
    library = get_library(True)
    if not theme.name:
        logger.error('Theme has no name.')
        exit(1)
    if not exists(f'{environ.get("HOME")}/.themer/library'):
        makedirs(f'{environ.get("HOME")}/.themer/library')
    if theme.name in [t.name for t in library]:
        logger.error('Theme has already been added!')
        exit(1)
    try:
        copy(path, f'{environ.get("HOME")}/.themer/library', follow_symlinks=True)
    except Exception as e:
        logger.error('Could not copy theme archive to library. Maybe try running with `sudo`?')
        exit(1)
    logger.info(f'Successfully added {theme.name}{" by " + theme.author if theme.author is not None else ""} to your library.')
    
def remove_theme(name: str):
    '''Remove a theme from the library.'''
    # Get your library #
    themes = get_library(True)
    if themes is not []:
        theme_obj: Theme = None
        # Sort through themes to find theme by name #
        for theme in themes:
            if theme.name.lower() == name.lower():
                theme_obj = theme
        # If the theme was found, nuke it #
        if theme_obj is not None:
            remove(theme_obj.path)
            logger.info(f'Successfully removed {theme_obj.name} from your library.')
            
def list_themes():
    '''List the user's themes in a nicely formatted way.'''
    library = get_library(False)
    if library == []:
        logger.info('You don\'t have any themes installed.')
    else:
        for theme in library:
            logger.info(theme.name)
            if theme.author and not theme.url:
                print(f' {end} Author: {theme.author}')
            elif theme.author and theme.url:
                print(f' {middle} Author: {theme.author}\n{end} URL: {theme.url}')
            elif theme.url:
                print(f' {end} URL: {theme.url}')