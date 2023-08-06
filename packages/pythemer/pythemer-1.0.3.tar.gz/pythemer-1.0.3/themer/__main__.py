# THEMER #
# __main__.py #
# COPYRIGHT (c) Jaidan 2022- #

# Imports #
import click
from themer.library import (add_theme, list_themes, remove_theme)
from themer.theme import (activate_theme, deactivate_theme)

__author__ = "Jaidan"

@click.group()
def main():
    '''A WIP theme engine for macOS, written in Python.'''
    pass

@main.group()
def library():
    '''Manage your theme library.'''
    pass

@library.command()
@click.argument('path', type=str)
def add(path):
    '''Add a theme to your library.'''
    add_theme(path)
    
@library.command()
@click.argument('name', type=str)
def remove(name):
    '''Remove a theme from your library.'''
    remove_theme(name)
    
@library.command()
def list():
    '''List all of the themes in your library.'''
    list_themes()

@main.command()
@click.argument('name', type=str)
def activate(name):
    '''Activate a theme.'''
    activate_theme(name)

@main.command()
def deactivate():
    '''Deactivate the active theme.'''
    deactivate_theme()

if __name__ == "__main__":
    main()