# 0.0.40

- Fixed `got file not dir in tempdir, zip extraction error`
- Package modified to accommodate ZIP files in the following ways: 
  - Accept ZIP files containing all necessary files without any enclosing folder.
  - Accept ZIP files that include a single folder containing the required files.
  - Accept ZIP files with multiple levels of folders that ultimately contain the necessary files.
  - If ZIP file contains multiple non-empty folders, it would treat first folder as valid folder and process it accordingly.
- Updated version to 0.0.40

# 0.0.39

- Fixed `local variable 'schema_table' referenced before assignment`
- Updated version to 0.0.39

# 0.0.38

- Schema folder is not getting added to package, fixed that issue
- Updated version to 0.0.38

# 0.0.37

- Added rules and schemas directory to the package folder


# 0.0.36

- Added Unit test cases
- Added Pipeline to deploy to TestPYPI
- Added pipeline to deploy to PYPI
- Added pipeline to run the unit test cases