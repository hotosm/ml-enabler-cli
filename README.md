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

### Install
* Git clone this repo
* `cd ml-enabler-cli`
* Create a virtualenv (recommended) `python3 -m venv env`
* `pip install -e .`
* `ml-enabler-cli --version` to check if the installation was successful
* `ml-enabler-cli --help` to see commands and options

### Looking Glass
To use looking-glass, first ensure looking-glass is hosted either on your computer or on a GPU cloud instance. Instructions to [this are here](https://render.githubusercontent.com/view/ipynb?commit=ec238b5a39bb4b254fa7ef05b90e1891037ddfc6&enc_url=68747470733a2f2f7261772e67697468756275736572636f6e74656e742e636f6d2f646576656c6f706d656e74736565642f6c6f6f6b696e672d676c6173732d7075622f656332333862356133396262346232353466613765663035623930653138393130333764646663362f646f636b65725f707265645f6578616d706c652e6970796e62&nwo=developmentseed%2Flooking-glass-pub&path=docker_pred_example.ipynb&repository_id=159652845&repository_type=Repository#Start-the-Looking-Glass-container).

#### Fetch predictions

To fetch predictions for a bbox, use:
```
ml-enabler fetch_predictions --name looking_glass --bbox "-77.14, 38.82, -76.92, 38.95" --endpoint http://looking-glass.com --tile-url https://api.mapbox.com/v4/mapbox.satellite/{z}/{x}/{y}.jpg?access_token={token}' --token abcd --zoom 16 --outfile /tmp/looking_glass_output.json --errfile /tmp/looking_glass_errors.json
```

The predictor options are:
* bbox - bbox required to fetch predictions for.
* endpoint - URL where the model is hosted. The model should be following the [TFServing schema](https://www.tensorflow.org/tfx/tutorials/serving/rest_simple)
* zoom - zoom level to be predicted at. This is usually determined by the model
* tile-url - tile url to pass to the model. This is usually determined by the model, and will be satellite imagery. For models/apis that don't need tile-url it's safe to ignore
* token - access token for the fetching tiles from the tile-url
* lg-weight - custom weight parameter. default is `auto`, and select the weight defined by the model
* concurrency - number of concurrent http requests to make (to the model as well as the tile server)
* outfile - output file to store the predictions
* errfile - in case certain tiles fail to predict, these are stored in the errfile for further inspection

### Aggregation and fetching OSM data

To aggregate predictions, use:

```
ml-enabler aggregate_predictions --name looking_glass --zoom 16 --infile /tmp/looking_glass_output.json --outfile /tmp/looking_glass_aggregated.json --errfile /tmp/looking_glass_aggregator_errors.json
```

The aggregator options are:
* zoom - zoom level to aggregate the predictions to. For example, if the predictions are at zoom 18, and if you want to aggregate them to zoom 14, specify 14
* overpass-url - optional overpass url. default is `https://lz4.overpass-api.de/api/interpreter`
* infile - input file with predictions. This is the output of `fetch_predictions` command
* outfile - file to store aggregated predictions
* errfile - file to store any errors generated while aggregating

### Working with the API

The ml-enabler-api acts as a gateway between models and mapping tools like Tasking Manager. The extendable API provides methods to fetch predictions at a bbox level as well as for custom polygons from a GeoJSON. The CLI allows to post results prepared from models to the API.

To upload predictions, the model should be registered first. To register the model, [check the API docs](https://github.com/hotosm/ml-enabler/blob/master/API.md#post-model).


The `model_name` is available in the `metadata` object of the prediction generated from the `fetch_predictions` command. ml-enabler-cli can upload predictions, using:

```
ml-enabler upload_predictions --infile /tmp/looking_glass_aggregated.json --api-url https://ml-enabler.hotosm.org/v1
```

### Adding a new model

To fetch predictions from a new model, it is required to add a `Predictor`. The base class `BasePredictor` offers all basic options and handles fetching command defaults. Once you create custom logic as a class, add this to [`predictors/__init__.py`](https://github.com/hotosm/ml-enabler-cli/blob/master/ml_enabler/predictors/__init__.py). Then the `fetch_predictions` can use the name to map the command to the new Predictor. See [`LookingGlassPredictor`](https://github.com/hotosm/ml-enabler-cli/blob/master/ml_enabler/predictors/LookingGlassPredictor.py) for example.

### Adding a new aggregator

Similar to a Predictor, the `BaseAggregator` offers a basic interface to work with aggregator logic. To create a new aggregator, subclass the BaseAggregator and write custom logic, and register this in [`aggregators/__init__.py`](https://github.com/hotosm/ml-enabler-cli/blob/master/ml_enabler/aggregators/__init__.py). The `aggregate_predictions` can use the name to map the command to the aggregator. See [`LookingGlassAggregator`](https://github.com/hotosm/ml-enabler-cli/blob/master/ml_enabler/aggregators/LookingGlassAggregator.py) for example.

## Development Setup

 - `python3 -m venv env` - create a virtualenv
 - Run `pip install -e .`
 - Run `ml-enabler --help` to see a list of commands and options
