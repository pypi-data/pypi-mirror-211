<div align="center">
    <img src="./docs/assets/nydok-logo.png" width="70%">
</div>


**nydok** is a combined specification writing and testing framework, for producing consistent and traceable specification documents.

Write your requirements and risk assessment alongside your Python code, ensuring 1:1 mapping between requirements and the code you're writing.

It is implemented as a plugin for `py.test` for running the tests, alongside with a CLI for creating reports.

## Features

Some notable features are:

- Lets you write specification documents including requirements as normal Markdown.
- Keeps track of which requirements are missing test cases.
- Supports a risk assessment process where you can link mitigations to your requirements.
- Can generate several types of reports in Markdown format for use in a Computerized System Validation process, such as:
    - Traceability matrix
    - Code review reports (Gitlab)
    - Risk assessment report
    - Test summary report
    - CI pipeline logs report (Gitlab)


## Installation


**Note!** nydok is still under development and hasn't yet had a v1.0.0 release, so expect breaking changes.


To install nydok using `pip`:

```
pip install nydok
```

or using Poetry:

```
poetry add nydok --group dev
```

## Usage

See documentation for details on how to use nydok, the following is just meant as a quick glimpse of how it works. nydok has a lot more features than what is shown here.

Create a new `cowsay.spec.md` specification file:

```markdown
# Cowsay functional specification

## Functional requirements

- REQ001: The program must take as input a text string
- REQ002: The program must return a string with a cow in ASCII art, displaying the input text as a speech bubble
```

and a `test_cowsay.py` file:

```python
from nydok import testcase
import cowsay


@testcase(["REQ001", "REQ002"])
def test_cowsay():
    assert cowsay("Hello world") == """
     _____________
    < Hello world >
     -------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
    """

```

Next, run `py.test` to check the specification. Each requirement listed in the specification file is counted as a test item, and will pass or fail depending on it's test case.

## License

`nydok` is released under the MIT license. See [LICENSE](LICENSE) for details.