# The Masked Manual - Python backend

## Flask

```
export FLASK_APP=app
export FLASK_ENV=development
flask run
```

The latest data is served on `data_latest`.

## Mask and respirator types

* `SURGICAL_MASK_EUA` - Surgical mask [approved under EUA](https://www.fda.gov/medical-devices/coronavirus-disease-2019-covid-19-emergency-use-authorizations-medical-devices/personal-protective-equipment-euas#surgicalmasks) but **not** FDA approved.
* `SURGICAL_MASK_FDA` - Surgical mask that is FDA approved.
* `RESPIRATOR_EUA` - Respirator (N95 or otherwise) that is [approved under EUA](https://www.fda.gov/medical-devices/coronavirus-disease-2019-covid-19-emergency-use-authorizations-medical-devices/personal-protective-equipment-euas#nonniosh) but **not** NIOSH and **not** FDA approved.
* `RESPIRATOR_EUA_EXPIRED_AUTH` - Respirator (N95 or otherwise) that is [no longer approved under the EUA](https://www.fda.gov/medical-devices/coronavirus-disease-2019-covid-19-emergency-use-authorizations-medical-devices/personal-protective-equipment-euas#nonniosh) and **not** NIOSH and **not** FDA approved.
* `RESPIRATOR_N95_NIOSH` - [N95 respirator that is NIOSH approved](https://www.cdc.gov/niosh/npptl/topics/respirators/disp_part/N95list1.html) but **not** FDA approved.
* `RESPIRATOR_N95_NIOSH_FDA` - [N95 respirator that is both NIOSH and FDA approved](https://www.cdc.gov/niosh/npptl/topics/respirators/disp_part/respsource3surgicaln95.html) - also known as surgical respirators.