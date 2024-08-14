# Building Device and Asset Naming Standards release process

Status: *work in progress 1.2.1*

## Work in progress

While working on abbreviations and specification files between 
releases, each text `.md` file will be tagged manually at the top,
just below the document title, with the following status line:

Status: *work in progress #.#.#* 

The "work in progress" status will signal the fact that the files are
not part of a release and under development.

## Release

At the time of the release, each text `.md` file will be tagged
manually at the top, just between the document title, with the 
following status line:

Status: *release #.#.#* 

Once the release status line has been updated in all the `.md` files
the repository is ready for a GitHub release, that can be done 
following the standard [GitHub release procedure](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository).

If new pull requests are merged after a tagged release, the first
developer creating a pull request will ensure to revert the "release"
status to "work in progress" status in all the `.md` files.

