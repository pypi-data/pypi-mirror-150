# Mettle #

Bitsmiths-Mettle is the supporting code generators and python libraries for the Mettle project.

See our <a href="https://bitbucket.org/bitsmiths_za/mettle.git">repo</a> and main *README* for more details!


## Requirements ##

Python 3.7+


## Installation ##

```console
$ pip install bitsmiths-mettle

---> 100%
```

## Change History ##

### 2.1.13 ###

| Type   | Description |
| ------ | ----------- |
| New    | Angular makefile generators can now be dynamically extended with a different CC, and TARGS as well as have optional overwrite commands. |
| Bug    | Fixed configuration bug from the 2.1.12 where a null dataclass would cause a generation error. |

### 2.1.12 ###

| Type   | Description |
| ------ | ----------- |
| New    | Python database and braze models can now be generated with (pydantic, or dataclass, or attrs) as an option. |
| New    | Python database and braze models can now toggle (pk, serializer, dav, clear) features an and off. |

### 2.1.11 ###

| Type   | Description |
| ----   | ----------- |
| Bug    | Fixed a refactor of `errCode` to `err_code` that was not rippled through some of the base library code/ |


### 2.1.10 ###

| Type   | Description |
| ----   | ----------- |
| Change | General typing improvements, and minor bug fixes. |



## License ##

This project is licensed under the terms of the MIT license.
