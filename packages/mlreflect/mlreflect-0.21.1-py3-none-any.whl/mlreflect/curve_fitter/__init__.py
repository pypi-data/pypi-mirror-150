from pathlib import Path

from .curve_fitter import CurveFitter
from .spec_fitter import SpecFitter, DefaultSpecFitter
from .fio_fitter import FioFitter, DefaultFioFitter

example_spec_file_path = Path(__file__).parents[1] / Path('resources', 'example', 'example.spec')
example_ascii_file_path = Path(__file__).parents[1] / Path('resources', 'example', 'example.dat')

__all__ = ['CurveFitter', 'SpecFitter', 'DefaultSpecFitter', 'FioFitter', 'DefaultFioFitter', 'example_spec_file_path',
           'example_ascii_file_path']
