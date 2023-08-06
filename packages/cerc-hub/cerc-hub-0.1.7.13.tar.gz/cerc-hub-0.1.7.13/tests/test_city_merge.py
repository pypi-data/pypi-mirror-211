"""
TestCityMerge test and validate the merge of several cities into one
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guille Gutierrez Guillermo.GutierrezMorote@concordia.ca
"""

from pathlib import Path
from unittest import TestCase

from hub.imports.geometry_factory import GeometryFactory


class TestCityMerge(TestCase):
  """
  Functional TestCityMerge
  """
  def setUp(self) -> None:
    """
    Test setup
    :return: None
    """
    self._example_path = (Path(__file__).parent / 'tests_data').resolve()
    self._output_path = (Path(__file__).parent / 'tests_outputs').resolve()
    self._weather_file = (self._example_path / 'CAN_PQ_Montreal.Intl.AP.716270_CWEC.epw').resolve()
    self._executable = 'sra'

  def _get_citygml(self, file):
    file_path = (self._example_path / file).resolve()
    city = GeometryFactory('citygml', path=file_path).city
    self.assertIsNotNone(city, 'city is none')
    return city

  def test_merge(self):
    self.assertTrue(False, 'This test needs to be reimplemented')

  def test_merge_with_radiation(self):
    self.assertTrue(False, 'This test needs to be reimplemented')
