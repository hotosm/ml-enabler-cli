from ml_enabler.aggregators.BuildingAggregator import BuildingAggregator
from ml_enabler.aggregators.LookingGlassAggregator import LookingGlassAggregator
from ml_enabler.aggregators.MapWithAIRoadStatsAggregator import MapWithAIRoadStatsAggregator

aggregators = {
  'looking_glass': LookingGlassAggregator,
  'building_api': BuildingAggregator,
  'mapwithai_road_stats': MapWithAIRoadStatsAggregator,
}
