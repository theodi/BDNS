
# Building Device and Asset Naming Standards initiative

Status: *work in progress 1.2.1*

## Scoping guidelines and principles

# Context and background

Building data is currently structured in many different ways, with no single standard. Although several attempts have been made to introduce a universal standard, these have not been universally adopted, and have often found to be insufficiently detailed to allow automated acquisition and surfacing of data from device (both input and outputs), into a structured database for use in end user and building operator applications.

The lack of standardised naming and labelling for building devices from design to operation means we are failing to leverage the value of data to allow interoperability, improve building efficiency/operations and increase occupant productivity and happiness. 

A naming and labelling standard (complementing other industry initiatives) will simplify and drive consistency, thus increasing value by unlocking the application of technologies such as machine learning.  

# Purpose

This project intends to provide an **industry wide naming convention framework** for  Information Technology (IT), Mechanical, Electrical and Public Health (MEP), and other Operational Technology (OT) devices and assets within buildings.

We believe that sharing data in an open and secure way would be a significant benefit for the industry, and is an important first step in being able to normalise data interactions in the future. 

Being able to efficiently collect, analyse and leverage data insights from buildings is a catalyst for optimising building performance, improving the use of resources and moving towards predictive maintenance and buildings that can respond to the climate emergency.

There is a number of initiatives around naming and tagging already in the industry, namely:

* [IFC](https://technical.buildingsmart.org/standards/ifc/ifc-schema-specifications/) (building information modelling)
* [Uniclass](https://www.thenbs.com/our-tools/uniclass-2015) and [Uniclass2](http://www.cpic.org.uk/uniclass2/) (asset management)
* [Omniclass](https://www.csiresources.org/standards/omniclass) (asset management)
* [CIBSE Symbols](https://www.cibse.org/knowledge/digital-knowledge-tools/symbols)
* [UDMI](https://github.com/faucetsdn/udmi) (IoT device communication encoding)
* [Web of Things](https://www.w3.org/WoT/) (IoT device communication encoding)
* [HyperCat](https://hypercatiot.github.io/) (IoT device communication encoding)
* [Project Haystack](https://project-haystack.org/) (tagging and linked data for control system)
* [Brick Schema](https://brickschema.org/) (linked data for control systems)
* [Digital Buildings Ontology](https://github.com/google/digitalbuildings)

The intent is not to replace these standards or create an overarching umbrella standard on top of existing initiatives, but to create a convention that is complementary and can address the correct naming of control system devices and associated maintainable assets (within the framework) from the early design stages through to operation, while ensuring relevance and suitability to all design and operational building stakeholders.

# Scope

The scope of this project is very focused: to provide an open naming convention and associated specifications for the naming of building control devices and associated items (within the defined framework) within buildings.

For the purpose of this standard, the definition of **building control devices** is _any equipment that can change state and is monitored within a building_. 

Example of controls devices are:

* temperature sensors,
* fan coil units,
* VAV boxes,
* pumps,
* luminaires.

**Associated items** are:

* manual devices that require maintenance or are used to setup a system - e.g. commissioning sets, regulating valves etc.
* architectural elements that may have a building control device associated with it - e.g. a door or a window.

The naming standard is applicable to fixed equipment only. Mobile equipment such as desk modules and portable sensors are not considered devices in the context of this project and therefore the naming convention is not applicable. 

Components that are part of a device, such as fan coil unit valves and controllers are not considered to be standalone devices, and therefore do not need individual names. Their data points can however be described and named using complementary standards such as [Project Haystack](https://project-haystack.org/),  [Brick Schema](https://brickschema.org/) and the [Digital Buildings Ontology](https://github.com/google/digitalbuildings).

# Deliverables

The following documents have been developed as part of the scope:

* A [specification for the naming syntax](BDNS_Specification_naming_syntax.md)
* A [register of building device and asset type abbreviations](BDNS_Abbreviations_Register.csv)
* A [governance model](BDNS_Governance_model.md) for the initiative

# Principles

The guiding principles for the standard are the following:

1. Granularity should be guided by defining the level of experience of people that have to apply naming.
2. Granularity should avoid ambiguity, introduce context and be what most people in industry would do.
3. The device identity and naming must remain consistent across the lifecycle of the device, throughout the design, construction and operational phases in order to enable seamless data transfer across phases.

Our recommendation is to store data in shared repositories and not standalone systems, and follow three key principles in data exchange:

* Utilisation of open standards
* Consistency of device identity across phases
* Transfer of design parameters from design model to operational models

# Process

The proposed governance principles and change process are documented in the [Building Device and Asset Naming Standard Proposed Governance](https://docs.google.com/document/d/141jJWvlckhQtMX-F310I1KpWGwD7rvurKyeMpwVq_-g/edit#) document. The document includes information on the open licensing of the work being driven by this initiative, communication mechanisms and a process for consensus building.

In practice, the proposed change process will rely on the GitHub platform:

* Changes to the syntax can be proposed by submitting an [issue](https://github.com/theodi/BDNS/issues) on the Github platform. Issues will be discussed and resolved on GitHub, and may be discussed additionally through the other communication mechanisms of the group, including mailing-list and semi-regular teleconferences.
* Additions to the register can be proposed by submitting a [pull request](https://docs.github.com/en/free-pro-team@latest/github/collaborating-with-issues-and-pull-requests/about-pull-requests) (PR) to the [Github repository](https://github.com/theodi/BDNS). Alternative submission mechanisms (e.g. through a mail address) may be made available if the Github PR mechanisms are deemed too technical.

# Future work

The intention is for this work to develop further to cover standardisation of naming for maintainable assets, but to exclude the naming of **metadata** and **data points**, which are meant to be named with a complementary standard, as discussed above.

For the purpose of this standard, the definition of a control point is _any data associated with a named building control device that one can read from or write to_. Examples of control point:

*   open/close position for valve,
*   lighting level.

For the purpose of this standard, the definition of metadata is data associated with an asset that provide information about its attributes. Examples of metadata:

*   manufacturer label,
*   device model label,
*   memory capacity.
