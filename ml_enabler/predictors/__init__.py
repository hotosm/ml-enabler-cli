from ml_enabler.predictors.LookingGlassPredictor import LookingGlassPredictor
from ml_enabler.predictors.BuildingPredictor import BuildingPredictor
from ml_enabler.predictors.MapWithAIRoadStatsPredictor import MapWithAIRoadStatsPredictor


predictors = {
  'looking_glass': LookingGlassPredictor,
  'building_api': BuildingPredictor,
  'mapwithai_road_stats': MapWithAIRoadStatsPredictor
}
