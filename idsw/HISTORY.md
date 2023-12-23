# History

## 1.2.0
### Fixed
- Deprecated structures

### Added
- New functionalities added.

### Reshape of project design.
- New division into modules and new names for functions and classes.

### Removed
- Removed support for Python < 3.7

## 1.2.1
### Fixed
- Setup issues.

## 1.2.2
### Fixed
- Setup issues: need for rigid and specific versions of the libraries.

## 1.2.3
### Fixed
- Setup issues.

## 1.2.4
### Fixed
- Import bugs.
- Introduced function for Excel writing.

## 1.2.5
### Fixed
- Matplotlib export figures bugs.
- 'quality' argument is no longer supported by plt.savefig function (Matplotlib), so it was removed.
- This modification was needed for allowing the correct functioning of the steelindustrysimulator, which is based on idsw.
- Check simulator project on: https://github.com/marcosoares-92/steelindustrysimulator
	- The Ideal Tool for Process Improvement, and Data Collection, Analyzing and Modelling Training.

## 1.2.6
### Fixed
- Export of figures generated a message like with '{new_file_path}.png.png'. Fixed to '{new_file_path}.png'.

