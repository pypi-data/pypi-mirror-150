# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pckit']

package_data = \
{'': ['*']}

install_requires = \
['MPh>=1.1.5,<2.0.0', 'numpy>=1.22.3,<2.0.0', 'pandas>=1.4.2,<2.0.0']

setup_kwargs = {
    'name': 'pckit',
    'version': '0.2.2',
    'description': 'A simple package for parallel computing with Python',
    'long_description': "# pckit\n\nThis is a simple package for parallel computing with Python.\n\n## Usage\n### Multiprocessing\nIf you want to use any solver from the package you have to wrap your functions into a model. \nHere the example with square of 2 and 3 are evaluated by 2 workers.\n`MyModel` is a subclass of the package `Model`. The method `results` is required.\n\n```python\nimport pckit\n\n\nclass MyModel(pckit.Model):\n    def results(self, x):\n        # Solve here problem f(x) = x^2\n        return x ** 2\n\n\nif __name__ == '__main__':\n    model = MyModel()\n    worker = pckit.SimpleMultiprocessingWorker(model)\n    with pckit.get_solver(worker, workers_num=2) as solver:\n        # Create tasks to solve. You can put args or\n        # kwargs for model.results() method in the Task\n        tasks = [pckit.Task(2), pckit.Task(x=3)]\n        results = solver.solve(tasks)\n        print(results)\n        # >>> [4, 9]\n```\n\n### MPI\nYou can easily run scripts on the cluster with [mpi4py](https://github.com/mpi4py/mpi4py) implementation on MPI (See [mpi4py installation docs](https://mpi4py.readthedocs.io/en/stable/install.html)).\nSimply change `SimpleMultiprocessingWorker` to `SimpleMPIWorker` in the previous example and start the script with MPI `mpiexec -np 3 python -m mpi4py your_script.py`\n\n```python\nworker = pckit.SimpleMPIWorker(model)\n```\nMoreover, a multiprocessing solver can be started inside an MPI solver.\n\n### Single thread\nSingle threaded execution is also available with `SimpleWorker`\n\n```python\nworker = pckit.SimpleWorker(model)\n```\n\n### Examples\n[More examples](https://github.com/djiboshin/pckit/tree/main/examples)\n\n## Features\n### Cache\nDict based cache is available by `caching` argument in `get_solver()`.\n`tag` property in `Task` is required and has to be hashable.\n\n```python\nwith pckit.get_solver(worker, caching=True) as solver:\n    tasks = [pckit.Task(2, tag='2'), pckit.Task(2, tag='2')]\n```\nThe second task's solution will be reused from the cache.\n\n### Custom iterators\nYou can send the email or print anything with custom iterator.\n[tqdm](https://pypi.org/project/tqdm/) is also supported.\n```python\nimport tqdm\n\nresults = solver.solve(tasks, iterator=tqdm.tqdm)\n```\nSee [example](https://github.com/djiboshin/pckit/blob/main/examples/custom_iterator.py) to create your own iterator.\n\n### Comsol Models, Solvers, Workers\nBased on [MPh](https://pypi.org/project/MPh/) package.\n\n**TBD**ocumented\n",
    'author': 'djiboshin',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/djiboshin/pckit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
