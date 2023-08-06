# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['multikeyjwt', 'multikeyjwt.jwt', 'multikeyjwt.middleware']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0,<9.0',
 'libadvian>=1.0,<2.0',
 'pendulum>=2.1,<3.0',
 'pyjwt[crypto]>=2.6,<3.0']

extras_require = \
{'all': ['fastapi>0.89,<1.0'], 'fastapi': ['fastapi>0.89,<1.0']}

entry_points = \
{'console_scripts': ['multikeyjwt = multikeyjwt.console:multikeyjwt_cli']}

setup_kwargs = {
    'name': 'multikeyjwt',
    'version': '1.1.0',
    'description': 'Verify JWTs with multiple public keys, FastAPI middleware for auth',
    'long_description': '===========\nmultikeyjwt\n===========\n\nVerify JWTs with multiple public keys, FastAPI middleware for auth\n\nCreating signing keys\n---------------------\n\n.. code-block:: bash\n\n    echo "My very g00d Passphrase" >/tmp/jwtRS256_passphrase.txt\n    ./make_keypair.sh\n\n\nDocker\n------\n\nFor more controlled deployments and to get rid of "works on my computer" -syndrome, we always\nmake sure our software works under docker.\n\nIt\'s also a quick way to get started with a standard development environment.\n\nSSH agent forwarding\n^^^^^^^^^^^^^^^^^^^^\n\nWe need buildkit_::\n\n    export DOCKER_BUILDKIT=1\n\n.. _buildkit: https://docs.docker.com/develop/develop-images/build_enhancements/\n\nAnd also the exact way for forwarding agent to running instance is different on OSX::\n\n    export DOCKER_SSHAGENT="-v /run/host-services/ssh-auth.sock:/run/host-services/ssh-auth.sock -e SSH_AUTH_SOCK=/run/host-services/ssh-auth.sock"\n\nand Linux::\n\n    export DOCKER_SSHAGENT="-v $SSH_AUTH_SOCK:$SSH_AUTH_SOCK -e SSH_AUTH_SOCK"\n\nCreating a development container\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\nBuild image, create container and start it::\n\n    docker build --ssh default --target devel_shell -t multikeyjwt:devel_shell .\n    docker create --name multikeyjwt_devel -v `pwd`":/app" -it `echo $DOCKER_SSHAGENT` multikeyjwt:devel_shell\n    docker start -i multikeyjwt_devel\n\npre-commit considerations\n^^^^^^^^^^^^^^^^^^^^^^^^^\n\nIf working in Docker instead of native env you need to run the pre-commit checks in docker too::\n\n    docker exec -i multikeyjwt_devel /bin/bash -c "pre-commit install"\n    docker exec -i multikeyjwt_devel /bin/bash -c "pre-commit run --all-files"\n\nYou need to have the container running, see above. Or alternatively use the docker run syntax but using\nthe running container is faster::\n\n    docker run --rm -it -v `pwd`":/app" multikeyjwt:devel_shell -c "pre-commit run --all-files"\n\nTest suite\n^^^^^^^^^^\n\nYou can use the devel shell to run py.test when doing development, for CI use\nthe "tox" target in the Dockerfile::\n\n    docker build --ssh default --target tox -t multikeyjwt:tox .\n    docker run --rm -it -v `pwd`":/app" `echo $DOCKER_SSHAGENT` multikeyjwt:tox\n\nProduction docker\n^^^^^^^^^^^^^^^^^\n\nThere\'s a "production" target as well for running the application, remember to change that\narchitecture tag to arm64 if building on ARM::\n\n    docker build --ssh default --target production -t multikeyjwt:latest .\n    docker run -it --name multikeyjwt multikeyjwt:amd64-latest\n\nDevelopment\n-----------\n\nTLDR:\n\n- Create and activate a Python 3.8 virtualenv (assuming virtualenvwrapper)::\n\n    mkvirtualenv -p `which python3.8` my_virtualenv\n\n- change to a branch::\n\n    git checkout -b my_branch\n\n- install Poetry: https://python-poetry.org/docs/#installation\n- Install project deps and pre-commit hooks::\n\n    poetry install\n    pre-commit install\n    pre-commit run --all-files\n\n- Ready to go.\n\nRemember to activate your virtualenv whenever working on the repo, this is needed\nbecause pylint and mypy pre-commit hooks use the "system" python for now (because reasons).\n',
    'author': 'Eero af Heurlin',
    'author_email': 'eero.afheurlin@iki.fi',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/pvarki/python-multikeyjwt/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
