# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytxc']

package_data = \
{'': ['*']}

install_requires = \
['Shapely>=1.8.1,<2.0.0',
 'lxml>=4.7.1,<5.0.0',
 'pyproj>=3.3.0,<4.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'requests>=2.27.1,<3.0.0',
 'shapely-geojson>=0.0.1,<0.0.2']

setup_kwargs = {
    'name': 'pytxc',
    'version': '0.1.6',
    'description': 'Python parser from TransXChange.',
    'long_description': '# pytxc\n\n[![test](https://github.com/ciaranmccormick/pytxc/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/ciaranmccormick/pytxc/actions/workflows/test.yml)\n[![Python Version](https://img.shields.io/pypi/pyversions/pytxc.svg)](https://pypi.org/project/pytxc/)\n[![codecov](https://codecov.io/gh/ciaranmccormick/pytxc/branch/main/graph/badge.svg?token=RIZHOMHC19)](https://codecov.io/gh/ciaranmccormick/pytxc)\n\n## Quick start\n\n### Installation\n\nUse `pip` to install `pytxc`.\n\n```console\npython -m pip install pytxc\n```\n\n### Usage\n\nThe `Timetable` class is used to parse and interact with\nTransXChange files.\n\n\n```python\nfrom pathlib import Path\nfrom pytxc import Timetable\n\n\n>> filepath = "path/to/transxchange/file.xml"\n>> timetable = Timetable.from_file_path(Path(filepath))\n>> timetable.header\nHeader(\n    creation_date_time=datetime.datetime(2020, 11, 22, 11, 0),\n    modification_date_time=datetime.datetime(2021, 12, 17, 11, 8, 35),\n    file_name="file.xml",\n    modification="revise",\n    schema_version="2.4",\n    revision_number=159,\n)\n```\n\nThe `StopPoint`s in a TransXChange can be accessed through the `stop_points`\nattribute.\n\n```python\n>> timetable.stop_points[0]\n\nAnnotatedStopPointRef(\n    stop_point_ref=StopPointRef(text="077072002S"),\n    common_name="High Street Stand S",\n)\n```\n\nSimilarly, `RouteSections` can be accessed using the `route_sections` attribute.\n\n```python\n>> timetable.route_sections[0]\n\nRouteSection(id=\'RS1\')\n```\n\nThe naming conventions used for the Python objects will more or less match those\nof TransXChange for example, the first `JourneyPattern` of a `StandardService` is\nusually found in a `Service` of the `Services` block.\nUsing `pytxc` it can be accessed as follows,\n\n```python\n>> timetable.services[0].standard_services[0].journey_patterns[0]\n\nJourneyPattern(\n    id="JP1",\n    CreationDateTime="2020-11-22T11:00:00",\n    ModificationDateTime="2021-12-17T11:08:35",\n    Modification="revise",\n    RevisionNumber="159",\n)\n```\n\nWhen interacting with references, `pytxc` provides a `resolve` method to find\nthe original element in the TransXChange file. For example if a `JourneyPattern`\ncontains a `RouteRef` then calling `resolve` on the `route_ref` object will\nreturn the original `Route` object.\n\n```python\n>> jp = timetable.services[0].standard_services[0].journey_patterns[0]\n>> jp.route_ref.resolve()\n\nRoute(private_code=\'35st-40\', description=\'Stockton - Wolviston Court\')\n```\n',
    'author': 'Ciaran McCormick',
    'author_email': 'ciaran@ciaranmccormick.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
