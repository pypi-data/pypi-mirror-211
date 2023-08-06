# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['textual_textarea']

package_data = \
{'': ['*']}

install_requires = \
['textual>=0.27.0,<0.28.0']

setup_kwargs = {
    'name': 'textual-textarea',
    'version': '0.1.1',
    'description': 'A text area (multi-line input) with syntax highlighting for Textual',
    'long_description': '# Textual Textarea\n\n# Installation\n\n```\npip install textual-textarea\n```\n\n# Usage\n\n## Initializing the Widget\n\nThe TextArea is a Textual Widget. You can add it to a Textual\napp using `compose` or `mount`:\n\n```python\nfrom textual_textarea import TextArea\nfrom textual.app import App, ComposeResult\n\nclass TextApp(App, inherit_bindings=False):\n    def compose(self) -> ComposeResult:\n        yield TextArea(language="python", theme="solarized-dark")\n\n    def on_mount(self) -> None:\n        ta = self.query_one(TextArea)\n        ta.focus()\n\napp = TextApp()\napp.run()\n```\n\nIn addition to the standard Widget arguments, TextArea accepts two additional, optional arguments when initializing the widget:\n\n- language: Must be `None` or the short name of a [Pygments lexer](https://pygments.org/docs/lexers/), e.g., `python`, `sql`, `as3`. Defaults to None.\n- theme: Must be name of a [Pygments style](https://pygments.org/styles/), e.g., `bw`, `github-dark`, `solarized-light`. Defaults to `monokai`.\n\nThe TextArea supports many actions and key bindings. **For proper binding of `ctrl+c` to the COPY action,\nyou must initialize your App with `inherit_bindings=False`** (as shown above), so that `ctrl+c` does not quit the app. The TextArea implements `ctrl+q` as quit; you way wish to mimic that in your app so that other in-focus widgets use the same behavior.\n\n## Interacting with the Widget\n\n### Getting and Setting Text\n\nThe TextArea exposes a `text` property that contains the full text contained in the widget. You can retrieve or set the text by interacting with this property:\n\n```python\nta = self.query_one(TextArea)\nold_text = ta.text\nta.text = "New Text!\\n\\nMany Lines!"\n```\n\n### Getting Theme Colors\n\nIf you would like the rest of your app to match the colors from the TextArea\'s theme, they are exposed via the `theme_colors` property.\n\n```python\nta = self.query_one(TextArea)\ncolor = ta.theme_colors.contrast_text_color\nbgcolor = ta.theme_colors.bgcolor\nhighlight = ta.theme_colors.selection_bgcolor\n```\n\nYou cannot set these colors this way, however.',
    'author': 'Ted Conbeer',
    'author_email': 'tconbeer@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tconbeer/textual-textarea',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
