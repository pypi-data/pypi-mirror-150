# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hcl2_eval']

package_data = \
{'': ['*']}

install_requires = \
['hcl2-ast>=0.3.0,<0.4.0', 'typing-extensions>=3.10.0']

setup_kwargs = {
    'name': 'hcl2-eval',
    'version': '0.1.2',
    'description': '',
    'long_description': '# hcl2-eval\n\nEvaluate HCL2 configurations like a programming language. Based on [hcl2-ast][].\n\n  [hcl2-ast]: https://pypi.org/project/hcl2-ast/\n## Usage\n\nThe evaluation of the HCL2 AST uses three components: A *context*, an *evaluator* an\n*interpreter*. The context is responsible for performing attribute reads and writes, looking\nup functions as well as opening and closing *stanzas*. The evaluator\'s responsibility is to\nevaluate expressions in the AST to Python values, while the interpreter executes statement nodes.\n\n\n```py\nfrom hcl2_ast import parse_file\nfrom hcl2_eval import Context, Evaluator, Interpreter, Stanza\n\nclass HelloStanza(Stanza):\n    ...\n\nmodule = parse_file(open("hello.hcl"), close=True)\ncontext = Context.of(hello=HelloStanza)\nInterpreter(Evaluator()).execute(module, context)\n```\n\nCheck out the full example at [examples/hello.py](https://github.com/NiklasRosenstein/python-hcl2-eval/blob/develop/examples/hello.py).\n\n## Compatibility\n\nhcl2-eval requires Python 3.6 or higher.\n',
    'author': 'Niklas Rosenstein',
    'author_email': 'rosensteinniklas@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
