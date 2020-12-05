# The Masked Manual - Python backend

This application lets you easily search for a face mask's qualifications from federal agencies in the U.S. Both surgical masks and respirators are supported.

<img src="static/logo_social_media.png" alt="drawing" width="400"/>

See also:
* [The iOS app source](https://github.com/smrfeld/the-masked-manual-ios).
* [Application website](https://the-masked-manual.herokuapp.com).

This is the Python backend for gathering the data. The data is gathered from:
* [openFDA of the U.S. Food and Drug Administration (FDA)](https://open.fda.gov/).
* [Emergency Use Authorizations for Medical Devices of the U.S. Food and Drug Administration (FDA)](https://www.fda.gov/medical-devices/coronavirus-disease-2019-covid-19-emergency-use-authorizations-medical-devices/personal-protective-equipment-euas).
* [National Personal Protective Technology Laboratory (NPPTL) of the Centers for Disease Control and Prevention (CDC)](https://www.cdc.gov/niosh/npptl/).

You can [read about the data source permissions on the application website here](https://the-masked-manual.herokuapp.com).

The list of currently indexed masks and respirators is below.

A Heroku hosted application reloads the data periodically and hosts it online.

## Running

You can run the Python script:
```
python fetch_latest.py
```
It will likely prompt for more options.

## Mask and respirator types

* `SURGICAL_MASK_EUA` - Surgical mask [approved under EUA](https://www.fda.gov/medical-devices/coronavirus-disease-2019-covid-19-emergency-use-authorizations-medical-devices/personal-protective-equipment-euas#surgicalmasks) but **not** FDA approved.
* `SURGICAL_MASK_FDA` - Surgical mask that is FDA approved.
* `RESPIRATOR_EUA` - Respirator (N95 or otherwise) that is [approved under EUA](https://www.fda.gov/medical-devices/coronavirus-disease-2019-covid-19-emergency-use-authorizations-medical-devices/personal-protective-equipment-euas#nonniosh) but **not** NIOSH and **not** FDA approved.
* `RESPIRATOR_EUA_EXPIRED_AUTH` - Respirator (N95 or otherwise) that is [no longer approved under the EUA](https://www.fda.gov/medical-devices/coronavirus-disease-2019-covid-19-emergency-use-authorizations-medical-devices/personal-protective-equipment-euas#nonniosh) and **not** NIOSH and **not** FDA approved.
* `RESPIRATOR_N95_NIOSH` - [N95 respirator that is NIOSH approved](https://www.cdc.gov/niosh/npptl/topics/respirators/disp_part/N95list1.html) but **not** FDA approved.
* `RESPIRATOR_N95_NIOSH_FDA` - [N95 respirator that is both NIOSH and FDA approved](https://www.cdc.gov/niosh/npptl/topics/respirators/disp_part/respsource3surgicaln95.html) - also known as surgical respirators.

## Developer

### iOS mockups for website

Courtesy of [smartmockups](https://smartmockups.com/mockup/iphone-11-pro-in-4-colors-h98h3GkI8T).

### To-do

Currently, only N95 and surgical N95 respirators are indexed from the [complete list here](https://www.cdc.gov/niosh/npptl/topics/respirators/disp_part/default.html).
TBD are:
* N99
* N100
* R95
* P95
* P99
* P100

### Google Cloud Storage Python interface

[Documentation can be found here.](https://googleapis.dev/python/storage/latest/index.html)

### Flask

Testing flask:
```
export FLASK_APP=app
export FLASK_ENV=development
flask run
```

The latest data is served on `data_latest`.

### Scheduled task on Heroku

See [guide here](https://devcenter.heroku.com/articles/clock-processes-python). Important to scale scheduler after deploying to Heroku:
```
heroku ps:scale scheduler=1
```
