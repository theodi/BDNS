# BDNS (Building Device Naming Specification)

This repository contains the source code for the BDNS Specification.

Access the [latest version of the BDNS specification](https://theodi.github.io/BDNS/).

Latest versions of pdf's and csv of the BDNS can be taken directly from the [BDNS specification website](https://theodi.github.io/BDNS/)
or directly via these links: 

- [BDNS_Governance_model](https://theodi.github.io/BDNS/BDNS_Governance_model.pdf)
- [BDNS_Scoping_guidelines_and_principles](https://theodi.github.io/BDNS/BDNS_Scoping_guidelines_and_principles.pdf)
- [BDNS_Specification_naming_syntax](https://theodi.github.io/BDNS/BDNS_Specification_naming_syntax.pdf)
- [BDNS_Abbreviations_Register](https://theodi.github.io/BDNS/BDNS_Abbreviations_Register.csv)

## Development

This repo contains the source markdown files which build the published [BDNS specification website](https://theodi.github.io/BDNS/).
The website is built using the [Quarto](https://quarto.org/) publishing system.
To test building the documentation locally:

Install [pixi](https://pixi.sh/latest/installation/) then run the commands below line-by-line.

```console
git clone https://github.com/theodi/BDNS.git
cd BDNS
pixi install # install environment dependencies
pixi run install-tinytex # install tinytex for pdf generation
pixi run # this will list all the available commands

# e.g. to build the docs
pixi run build-docs

# to check for duplicate abbreviations
pixi run check-duplicates
```