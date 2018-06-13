# Release Notes

These are the release notes for the Unidata CloudIDV project.

## 1.3.0 June 13, 2018

* Bumped IDV to version 5.4.
* Updated to `cloudstream 1.3.0`.
* Added new environmental variable, `IDVMEM`, which is used to specify how much memory is available to the JVM when running the IDV.  The default value is `512M`.
* Added a front-end python panel to launch the IDV.  This will prevent the docker container from exiting if the IDV closes unexpectedly.  It is simplistic for the time being but will be fleshed out.
* Added `COPYRIGHT_CLOUDIDV.md` file to project.
* Parameterized build with Docker `ARGS` option.
  * `CLOUDIDV_VERSION can now be specified at build time.`

## 1.1.0 Released February 5, 2016

* Added a `RELEASE_NOTES.md` file to track release notes, changes, etc.

## 1.0.0 Released January 8, 2016

* Initial release.
