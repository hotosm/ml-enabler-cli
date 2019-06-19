# ml-enabler-cli

Command line utilities for working with ML models and ml-enabler-api

## Background

ml-enabler-cli is a library to interact with ML Models, run prediction jobs, and submit results to the [ml-enabler-api](https://github.com/hotosm/ml-enabler). The CLI also has a utility to query OSM (only buildings now), and aggregate data at a defined tile level. See ml-enabler-cli for more information.

At the core of the library there are Predictors and Aggregators to work with models, and a command to upload predictions.

* Predictors
Predictors interact with a model hosted at a particular endpoint. At the moment, we've integrated Development Seed's looking-glass model and a building API that returns geometries for a given bbox. To see all the available predictors, [see here](https://github.com/hotosm/ml-enabler-cli/blob/master/ml_enabler/predictors/__init__.py).

* Aggregators
Aggregators take predictions from a model and then aggregate data at desired zoom level or tile size. The output is in the format acceptable by the ml-enabler-api. Aggregators can optionally query Overpass for OSM data and add that to the predictions. See the looking-glass [aggregator for example](https://github.com/hotosm/ml-enabler-cli/blob/master/ml_enabler/aggregators/LookingGlassAggregator.py#L44).

## Usage

### Setup
* Git clone this repo
* `cd ml-enabler-cli`
* `pip install -e`

### Looking Glass
To use looking-glass, first ensure looking-glass is hosted either on your computer or on a GPU cloud instance. Instructions to [this are here](https://render.githubusercontent.com/view/ipynb?commit=ec238b5a39bb4b254fa7ef05b90e1891037ddfc6&enc_url=68747470733a2f2f7261772e67697468756275736572636f6e74656e742e636f6d2f646576656c6f706d656e74736565642f6c6f6f6b696e672d676c6173732d7075622f656332333862356133396262346232353466613765663035623930653138393130333764646663362f646f636b65725f707265645f6578616d706c652e6970796e62&nwo=developmentseed%2Flooking-glass-pub&path=docker_pred_example.ipynb&repository_id=159652845&repository_type=Repository#Start-the-Looking-Glass-container).

#### Fetch predictions

To fetch predictions for a bbox, use:
`ml-enabler fetch_predictions --name looking_glass --bbox "-77.14, 38.82, -76.92, 38.95" --endpoint http://looking-glass.com --zoom 16 --outfile /tmp/looking_glass_output.json --errfile /tmp/looking_glass_errors.json`

The predictor options are:
* bbox - bbox required to fetch predictions for.
* endpoint - URL where the model is hosted. The model should be following the [TFServing schema](https://www.tensorflow.org/tfx/tutorials/serving/rest_simple)
* zoom - zoom level to be predicted at. This is usually determined by the model
* outfile - output file to store the predictions
* errfile - in case certain tiles fail to predict, these are stored in the errfile for further inspection

These options are available across all predictors.

### Adding a new model

### Aggregation and fetching OSM data

### Working with the API

### Development Setup

 - Create a virtualenv
 - Run pip install -e .
 - Run `ml-enabler help` to see a list of commands and options