# Release Checklist

_On the `develop` branch._

### Preamble

- [ ] Confirm that CI checks pass

### Version and change log

- [ ] Update the version number in `pyproject.toml`
- [ ] Check that the change log is current
- [ ] Check that the README is current
- [ ] Change the "Unreleased" heading to the new version

### Merge to `main`

- [ ] Commit and push the new version number and change log
- [ ] PR and merge into `main`

### Tag and release

- [ ] `git tag -s -a X.Y.Z`
- [ ] Use "Version X.Y.Z" for the tag title
- [ ] Use the change log for the contents
- [ ] Push tag to `main`
- [ ] Cut a release on GitHub with change log contents

### Update `develop`

- [ ] Merge `main` into `develop`
- [ ] Update `develop` to `X.Y.(Z+1).dev0`
- [ ] Add "Unreleased" to the change log with a diff link
