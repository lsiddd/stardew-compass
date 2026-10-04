"""Redistributable geometry, fonts and attributed rule catalogs."""

from importlib.resources import files


def data_path(name):
    return files(__package__).joinpath(name)
