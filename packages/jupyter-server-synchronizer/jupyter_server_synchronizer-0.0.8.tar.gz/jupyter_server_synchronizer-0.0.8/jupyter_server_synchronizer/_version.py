"""
store the current version info of the synchronizer.
"""
version_info = (0, 0, 8, "", "")
__version__ = ".".join(map(str, version_info[:3])) + "".join(version_info[3:])
