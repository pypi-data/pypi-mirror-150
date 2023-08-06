# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['benchling_sdk',
 'benchling_sdk.auth',
 'benchling_sdk.benchbots',
 'benchling_sdk.benchbots.codegen',
 'benchling_sdk.benchbots.commands',
 'benchling_sdk.benchbots.dependencies',
 'benchling_sdk.benchbots.helpers',
 'benchling_sdk.benchbots.types',
 'benchling_sdk.helpers',
 'benchling_sdk.models',
 'benchling_sdk.services']

package_data = \
{'': ['*'], 'benchling_sdk.benchbots.codegen': ['templates/*']}

install_requires = \
['PyYAML>=5.4.1,<7.0.0',
 'attrs>=20.1.0,<21.0.0',
 'backoff>=1.10.0,<2.0.0',
 'benchling-api-client==1.1.0a14',
 'dataclasses-json>=0.5.2,<0.6.0',
 'dataclasses-jsonschema>=2.14.1,<3.0.0',
 'httpx>=0.15.0,<=0.22.0',
 'jsonpath-ng>=1.5.2,<2.0.0',
 'keyring==22.0.1',
 'python-dateutil>=2.8.0,<3.0.0',
 'typing-extensions>=3.7.4,<5.0']

extras_require = \
{'app-scaffold': ['typer>=0.4.0,<0.5.0',
                  'black>=22.3.0,<23.0.0',
                  'Jinja2>=3.0.0,<4.0.0',
                  'autoflake>=1.4,<2.0']}

entry_points = \
{'console_scripts': ['benchling-sdk = benchling_sdk.cli:cli']}

setup_kwargs = {
    'name': 'ce-bnch-sdk',
    'version': '1.2.0b0',
    'description': 'SDK for interacting with the Benchling Platform.',
    'long_description': '# CE Benchling SDK\n\nThis is the Customer Engineering team\'s branch of the Benchling SDK, containing features that we are not yet ready to release to customers.\n\nCurrently, the only difference from the main Benchling SDK is the Benchbots CLI.\n\n## Benchbots CLI\nThe SDK comes with a CLI for managing Benchbots, which is still under alpha testing.\n\nEach integration corresponds to a Benchbot. You declare the Benchbot\'s dependencies in a manifest file, typically a top-level file named `manifest.yaml`. For example:\n```yaml\nmanifestFormatVersion: 1  # Currently only version 1 exists\n\ninfo:\n  name: My Integration\n  version: 0.0.1\n  description: Cure cancer  # Optional\n\ndependencies:\n  - name: My Plasmid  # Should match the actual name in Benchling, if possible, as Benchbots tries to find the dependency by name\n    resourceType: entity-schema  # Corresponds to the API namespace, in this case /entity-schemas\n    resourceProperties:  # This section is only used by resources with resourceType "entity-schema"\n      type: dna_sequence  # Possible values for entities are: "custom_entity", "dna_sequence", or "aa_sequence"\n    description: Plasmid schema of interest  # Optional\n    fieldDefinitions:\n      - name: My Backbone\n      - name: My Resistances\n  - name: Optical Density Assay\n    resourceType: assay-run-schema\n    fieldDefinitions:\n      - name: optical_density  # Run, result, and request schemas use the snake-cased "warehouse name"\n  - name: Resistance\n    resourceType: dropdown\n    options:\n      - name: 1 - Ampicillin\n      - name: 2 - Penicillin\n  - name: My Project\n    resourceType: project\n```\nAny resource type which is served by the Benchling API can be referenced, using its kebab-cased name. Below is the full list of possible values for `resourceType`. Schema types:\n- entity-schema\n- container-schema\n- plate-schema\n- box-schema\n- location-schema\n- assay-result-schema\n- assay-run-schema\n- request-schema\n- entry-schema\n- workflow-task-schema\n- dropdown\n- workflow-task-status\n\nIndividual resource types:\n- aa-sequence\n- assay-result\n- assay-run\n- automation-input-generator\n- automation-output-processor\n- blob\n- box\n- container\n- custom-entity\n- dna-alignment\n- dna-oligo\n- dna-sequence\n- entry\n- folder\n- label-printer\n- label-template\n- location\n- plate\n- project\n- registry\n- request\n\nOnce you\'ve declared the dependencies, you can generate the `dependencies.py` file and the model classes (in this case `my_plasmid.py`, `optical_density_assay.py`, and `resistance.py`) using the command:\n```bash\n# Optional arguments `--manifest-file-path`, `dependencies_file_path`, `model_directory_path` to specify the exact paths\npoetry run benchling-sdk benchbot dependencies scaffold\n```\n\nNext, once a Benchling tenant has been set up where you want to run the integration, you can link each dependency to its corresponding Benchling API ID using the command:\n```bash\n# Replace `cedev` with the appropriate tenant and deployment\npoetry run benchling-sdk benchbot dependencies link parameters/cedev.json https://cedev.bnch.org\n```\nThis same command can also be used to make sure all existing dependency links are up-to-date with the Benchling tenant.\n\nNow the integration will have full access to all its required dependencies. See the documentation in the generated files for more detailed instructions on usage in the integration code.\n\n## Submodule Dependency\nThis project relies on a forked version of [openapi-python-client](https://github.com/triaxtec/openapi-python-client) defined in `.gitmodules`.\nWhen cloning the project you can pass `--recursive` like this:\n```bash\ngit clone git@github.com:benchling/benchling-sdk.git --recursive\n```\n\nIf you have already cloned the repo, you can use:\n\n```bash\ngit submodule update --init\n```\n\n## Submodule Dependency\nThis project relies on a forked version of [openapi-python-client](https://github.com/triaxtec/openapi-python-client) defined in `.gitmodules`.\nWhen cloning the project you can pass `--recursive` like this:\n```bash\ngit clone git@github.com:benchling/benchling-sdk.git --recursive\n```\n\nIf you have already cloned the repo, you can use:\n\n```bash\ngit submodule update --init\n```\n\n## Submodule Dependency\nThis project relies on a forked version of [openapi-python-client](https://github.com/triaxtec/openapi-python-client) defined in `.gitmodules`.\nWhen cloning the project you can pass `--recursive` like this:\n```bash\ngit clone git@github.com:benchling/benchling-sdk.git --recursive\n```\n\nIf you have already cloned the repo, you can use:\n\n```bash\ngit submodule update --init\n```\n\n## Submodule Dependency\nThis project relies on a forked version of [openapi-python-client](https://github.com/triaxtec/openapi-python-client) defined in `.gitmodules`.\nWhen cloning the project you can pass `--recursive` like this:\n```bash\ngit clone git@github.com:benchling/benchling-sdk.git --recursive\n```\n\nIf you have already cloned the repo, you can use:\n\n```bash\ngit submodule update --init\n```\n\n## Submodule Dependency\nThis project relies on a forked version of [openapi-python-client](https://github.com/triaxtec/openapi-python-client) defined in `.gitmodules`.\nWhen cloning the project you can pass `--recursive` like this:\n```bash\ngit clone git@github.com:benchling/benchling-sdk.git --recursive\n```\n\nIf you have already cloned the repo, you can use:\n\n```bash\ngit submodule update --init\n```\n\n## General Usage\n\nFor more detailed usage of the SDK, refer to the [public release notes](https://pypi.org/project/benchling-sdk/), which are stored as part of the project \nin `publish/README.public.md`.\n\nSimple usage example iterating through DNA sequences:\n\n```python\nfrom benchling_sdk.auth.api_key_auth import ApiKeyAuth\nfrom benchling_sdk.benchling import Benchling\n\nbenchling = Benchling(url="https://my.benchling.com", auth_method=ApiKeyAuth("api_key"))\n\ndna_sequence_pages = benchling.dna_sequences.list()\n\nfor page in dna_sequence_pages:\n    for dna_sequence in page:\n        print(dna_sequence.bases)\n```\n\n## Developer Notes\n\nThe `benching_sdk.benchling.Benchling` object serves as the point of entry for the SDK. API calls are organized into\nservices that generally correspond to [Capillary documentation](https://docs.benchling.com/reference).\n\nEach method calling the API is wrapped with an `@api_method` decorator. This decorator applies several global\nbehaviors which may not be readily obvious including:\n* Conditionally adding some logging on each method call\n* Applying retries via the backoff library when `RetryStrategy` is configured\n\nLogging in the SDK follows the [Python best practice](https://docs.python-guide.org/writing/logging/#logging-in-a-library)\nof only adding the `logging.NullHandler()`. An example of enabling basic logging:\n\n```python\nimport logging\nlogging.basicConfig(level=logging.INFO)\n```\n\nFor more details on configuring or disabling `RetryStrategy`, refer to *Advanced Use Cases* in `publish/README.public.md`.\n\nHTTP errors like `404` not found are all caught via `raise_for_status()` and transformed into\na standardized `BenchlingError` which wraps the underlying error for a better general error handling experience.\nA caught BenchlingError can be inspected to learn the status triggering it, and the full contents of the error \nresponse returned from the Benchling server.\n\n### Exporting Models\n\nAlthough generated models are packaged in `benchling_api_client.models` \nand its files, we externalize the models via `benchling_sdk.models` in\norder to abstract `benchling_api_client` from users such that they may\nsimply import `benchling_sdk.models.ExampleModelClass`.\n\nThis is accomplished in `benchling_sdk/models/__init__.py`. This file\nis automatically generated from a Jinja template in `templates/` by \nrunning `poetry run task models`. Changes should be committed to source\ncontrol. All tasks should be run from the root directory of the project.\n\nMissing models from `benchling_api_client` are verified by unit\ntest in `benchling-sdk/tests/unit/test_models.py`.\n\n## Configuring pre-push Git Hooks\n\n```bash\npoetry run pre-commit install --hook-type pre-push\n```\n\n## Publishing Releases\n\nTo create a release of the SDK, create a tag in Git from the `main` branch. CI will then\ninitiate a build, generate the client, and publish the resulting packages.\n\nThe published version will reflect the tag, so a tag of `1.0.4` will publish version `1.0.4`. Tags that do not meet\nPoetry\'s [version format](https://semver.org/) will create a failed build when publishing is attempted.\n\nThis README will not be published alongside the public package. To modify the public README, modify \n`publish/README.public.md`. The changes will be copied over when preparing for publishing.\n\n*NOTE*: There are some scripts executed that make changes to the working directory and its files with the intention\nof them being discarded (e.g., during CI). If running the scripts locally, exercise caution and save your changes\nfirst.\n\n## Code Generation Unit Tests\n\nThis project uses a feature of the `openapi-python-client` dependency to override one of the templates used for code \ngeneration in that project.  Since this project alters how code generation works, it includes unit testing around that\ngeneration in the form of diffing against a known-good version of the generated code, referred to as the `golden-record`\n(taken from the upstream\'s naming for their version of this test).  Unit testing will break if the overridden template \nwhich lives under `benchling_sdk/codegen/templates` is altered in a way which changes the output of the generated code.\n\nIn the event that the breaking changes to this test are intentional, you can regenerate the golden-record:\n\n```\npoetry run task regenerate_golden_record\n```\n\n## Integration Tests\n\nIntegration tests must be run manually, either via IDE test runners or by command line:\n\n```bash\npoetry run task integration\n```\n\nIntegration tests will not run under CI yet and are currently tightly coupled to cesdktest.bnch.org. They\nare most effective for quickly running manual regression testing.\n',
    'author': 'Benchling Customer Engineering',
    'author_email': 'ce-team@benchling.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
