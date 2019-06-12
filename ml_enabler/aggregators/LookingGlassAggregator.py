from ml_enabler.aggregators.BaseAggregator import BaseAggregator
import functools
import mercantile

class LookingGlassAggregator(BaseAggregator):

    async def aggregate(self):
        agg_quadkeys = self.get_agg_quadkeys()

    def get_agg_quadkeys():
        '''
            Returns the list of unique quadkeys in the dataset at the destination zoom level
        '''
        all_quadkeys = [d['quadkey'] for d in self.source_data]
        return list(set([q[0:self.zoom] for q in all_quadkeys]))

    async def get_values_for_quadkey(self, quadkey):
        '''
            Returns consolidated data values for a quadkey
        '''
        filtered_quadkeys = filter(lambda d: d['quadkey'].startswith(quadkey), self.source_data)
        total_building_area = functools.reduce(lambda a,b: a['data']['ml_prediction'] + b['data']['ml_prediction'], filtered_quadkeys)
        tile = mercantile.quadkey_to_tile(quadkey)
        osm_building_area = await get_building_area(tile)
        return {
            'quadkey': quadkey,
            'center': get_center(tile)
            'data': {
                'ml_prediction': total_building_area,
                'osm_building_area': osm_building_area
            }
        }