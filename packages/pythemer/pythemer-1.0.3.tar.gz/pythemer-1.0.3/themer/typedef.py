# THEMER #
# types.py #
# COPYRIGHT (c) Jaidan 2022- #

# Imports #
from asyncio import run
from themer.apps import (get_apps, plist)

class Plist():
    def __init__(self, bundle_id: str, app_list: list[dict]):
        # Plist #
        plist_obj = run(plist(bundle_id, app_list))
        # App bundle ID #
        self.bundle_id: str = bundle_id
        # App name #
        self.name: str = plist_obj.get('CFBundleName')
        # App icon asset #
        self.icon_asset: str = str(plist_obj.get(
            'CFBundleIconFile')).replace('.icns', '') if plist_obj else None
        # App path #
        self.path: str = str(plist_obj.get('AppPath')) if plist_obj else None
        # App resource path #
        self.resource_path: str = self.path + '/Contents/Resources' if self.path else None
        # App executable
        self.executable: str = plist_obj.get('CFBundleExecutable') if plist_obj else None

class Icon():
    def __init__(self, dict: dict, apps: list[dict]):
        # App name #
        self.bundle_id: str = dict.get('bundleID')
        # App icon relative path #
        self.img: str = dict.get('img')
        # App icon data #
        self.data = None
        # Plist #
        self.plist = Plist(dict.get('bundleID'), apps)

class Theme():
    def __init__(self, dict: dict, path: str, should_get_apps: bool = True):
        # Theme zip path #
        self.path: str = path
        # Theme name #
        self.name: str = dict.get('name')
        # Theme author #
        self.author: str = dict.get('author') if dict.get('author') else None
        # Theme URL #
        self.url: str = dict.get('url') if dict.get('url') else None
        # Icons object #
        self.icons: list[Icon] = []
        # Icons raw object #
        self.icons_RAW: list[dict] = []
        if should_get_apps:
            # Icons #
            app_list = get_apps()
            for icon in dict.get('icons'):
                self.icons.append(Icon(icon, app_list))
