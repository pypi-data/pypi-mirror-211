# Making a new release of jupysql-plugin

The extension can be published to `PyPI` and `npm` manually or using the [Jupyter Releaser](https://github.com/jupyter-server/jupyter_releaser).

## Manual release

### Python package

Create conda environment:

```bash
conda env create  -f environment.dev.yml -y
```

Bump the version using `hatch`. See the docs on [hatch-nodejs-version](https://github.com/agoose77/hatch-nodejs-version#semver) for details.

```bash
hatch version <new-version>
```

The previous command will update the version in the `package.json` file. You have to manually commit and create the tag:

```bash
git tag -a VERSION -m MESSAGE
git push --tag
```

To create a Python source package (`.tar.gz`) and the binary package (`.whl`) in the `dist/` directory, do:

*Note:* The following command needs NodeJS

```bash
python -m build
```

Then to upload the package to PyPI, do:

```bash
twine upload dist/*
```

### NPM package

To publish the frontend part of the extension as a NPM package, do:

```bash
npm login
npm publish --access public
```

## Automated releases with the Jupyter Releaser

The extension repository should already be compatible with the Jupyter Releaser.

Check out the [workflow documentation](https://github.com/jupyter-server/jupyter_releaser#typical-workflow) for more information.

Here is a summary of the steps to cut a new release:

- Fork the [`jupyter-releaser` repo](https://github.com/jupyter-server/jupyter_releaser)
- Add `ADMIN_GITHUB_TOKEN`, `PYPI_TOKEN` and `NPM_TOKEN` to the Github Secrets in the fork
- Go to the Actions panel
- Run the "Draft Changelog" workflow
- Merge the Changelog PR
- Run the "Draft Release" workflow
- Run the "Publish Release" workflow

## Publishing to `conda-forge`

If the package is not on conda forge yet, check the documentation to learn how to add it: https://conda-forge.org/docs/maintainer/adding_pkgs.html

Otherwise a bot should pick up the new version publish to PyPI, and open a new PR on the feedstock repository automatically.
