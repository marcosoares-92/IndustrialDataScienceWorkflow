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

## 1.3.0
### Added
- New functionalities added.

### Reshape of project design.
- New division of functions and classes and correspondent modules.
- Refactoring of functions and classes to improve code efficiency.
- Added new pipelines for fetching data and modified the storage of connectors.
- It includes pipelines for fetching table regions in Excel files, even if they are stored in a same tab; and a pipeline for downloading files stored in MS SharePoint.
- Added ControlVars dataclass to store if the user wants to hide results and plots.

## 1.3.1
### Improved
- Benford algorith for fraud and outlier detection.
- Pipeline for fetching SharePoint and downloading files.