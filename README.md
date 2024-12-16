# oura-ring-relay
Serverless functions for reading/extracting data from the Oura Ring API

### Overview

This repo is a collection of serverless lamba functions to automate data collection and processing for my own biometric/sleep data from the [Oura API](https://cloud.ouraring.com/) and loading it another permanent store.

The motivation is that Oura provides a large number of interesting sleep metrics, however they do not have all of the visualization options I want. In particular I am trying to control my bed time and maintain my bed and wake times to specific times.


### Detailed Design
For version 1, I want to schedule the function to run once a day and read sleep data from Oura and load it into a specific Google Sheet.

For [Oura API Reference](https://cloud.ouraring.com/v2/docs). Using the [Oura Ring](https://pypi.org/project/oura-ring/) python library.

This function will call `/v2/usercollection/sleep` to fetch the past 7 days of sleep documents. The single document route requires knowning the `document_id`, which you can't know without a previous fetch.

From this document it will gather:
- `id`
- `day`
- `bedtime_start`
- `bedtime_end`
- `time_in_bed`
- `total_sleep_duration`
- `rem_sleep_duration`
- `deep_sleep_duration`
- `light_sleep_duration`
- `awake_time`
- `efficiency`

The function will then connect to Google Sheets and add it to a new row in a pre-defined Sheet.

Then I can set up graphs/visualizations in Google Sheets itself.