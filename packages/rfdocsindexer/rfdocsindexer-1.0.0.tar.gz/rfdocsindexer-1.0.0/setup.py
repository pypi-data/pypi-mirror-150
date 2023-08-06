# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rfdocsindexer']

package_data = \
{'': ['*'], 'rfdocsindexer': ['templates/*']}

install_requires = \
['Jinja2>=3.0.1,<4.0.0',
 'click>=8.0.1,<9.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'robotframework>=4,<5',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['indexrfdocs = rfdocsindexer.cli:cli']}

setup_kwargs = {
    'name': 'rfdocsindexer',
    'version': '1.0.0',
    'description': 'A simple and configurable generator for RobotFramework documentation',
    'long_description': '# RF Documentations Indexer\n\nRfdocsindexer is a simple Python3 module to generate [RobotFramework](https://robotframework.org/) 4+ libraries documentation.\n\nOne can configure the tool from a simple [TOML](https://github.com/toml-lang/toml) configuration file and run it from a console.\n\nThe tool then uses the RobotFramework [Libdoc](https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#libdoc) module to generate an HTML, XML, JSON or Libspec documentation for any RobotFramework keyword library.\n\nAn HTML index is also generated to centralize the generated documentations.\n\n![RFDocsIndexer Diagram](https://github.com/Vincema/rfdocsindexer/raw/main/docs/diagrams/rfdocsindexer_diagram.svg)\n\n## Installing the tool\n\nInstall from Pypi:\n```bash\npip install rfdocsindexer\n```\n\n## Configuring the tool\n\nThe tool can be configured with a config file in [TOML](https://github.com/toml-lang/toml) format.\n\nExample configuration file:\n\n```toml\n[rfdocsindexer]\nlibrary_paths = ["**/libraries/*.robot", "my_library.resource"]\nlibrary_names = ["MyLibrary", "MyOtherLibary.MyOtherLibrary"]\nextra_modules_searchpaths = ["./library_dir"]\nexternal_resources = ["RF homepage | https://robotframework.org/", "http://example.org"]\nbuild_machine_readable_libdoc = true\ninclude_robotframework_resources = true\n```\n\nThe configuration file must contain the section `[rfdocindexer]` and any or none of the following options:\n\n* `library_paths`: a list of paths (glob format accepted) to RF resource files (can be `*.resource`, `*.robot`, `*.spec`...)\n* `library_names`: a list of RF library modules\n* `extra_modules_searchpaths`: a list of paths to append to `PYTHONPATH`\n* `external_resources`: a list of URLs which will be added to the HTML index file, or `<name> | <URL>`. Useful to include frequently used external resources when developing tests.\n* `build_machine_readable_libdoc`: whether to generate documentation in XML, JSON and Libspec format. If set to `False`, only the HTML documenation will be generated. Default is `False`.\n* `include_robotframework_resources`: whether to generate documentation for default RobotFramework libraries (`BuiltIn`, `Collection`, ...). Default is `True`.\n\n\n## Running the tool\n\nIn a standard shell, run the following:\n\n```bash\n# To generate documentation for default RobotFramework libraries\nindexrfdocs\n\n# To specify the configuration file to use\nindexrfdocs -c path/to/configfile.toml\n\n# To specify the output directory (content will not be erased if already existing), default is "rfdocs"\nindexrfdocs -o path/to/outdir\n```\n',
    'author': 'Vincent Maire',
    'author_email': 'maire.vincent31@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Vincema/rfdocsindexer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
