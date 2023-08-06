
# Changelog
All notable changes to tailbone-quickbooks will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [0.1.5] - 2023-06-01
### Changed
- Stop passing `newstyle` kwarg to `Form.validate()`.
- Replace `setup.py` contents with `setup.cfg`.

## [0.1.4] - 2023-02-21
### Changed
- Show invoice amounts as currency.

## [0.1.3] - 2023-02-20
### Changed
- Refactor `Query.get()` => `Session.get()` per SQLAlchemy 1.4.
- Catch/display error when exporting QB invoices.
- Fix fieldname for invoice view.

## [0.1.2] - 2023-01-26
### Changed
- Commit session when refreshing invoices.

## [0.1.1] - 2023-01-25
### Changed
- Only include "export invoice" logic if user has perm.
- Add "refresh results" for QB exportable invoices.

## [0.1.0] - 2022-12-21
### Added
- Initial version, mostly for sake of "export invoices to Quickbooks" feature.
