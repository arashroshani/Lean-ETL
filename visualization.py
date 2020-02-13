import pandas as pd
import plotly
import plotly.graph_objs as go


class MapGen:
    """This object generates a visualization map"""

    def __init__(self, report_df, location_df):
        self.report_df = report_df
        self.location_df = location_df

    def agg_map(self, report_df_target_col='reach', report_df_city_col='region', location_df_city_col='City',
                output_image='map.png', longitude='Longitude', latitude='Latitude', limit=7, scale=1.5):
        """Groups the report's data frame by city and aggregates over the target column and joins it
        with the locations assigned to each city. Outputs map's image."""
        # report_df_target_col = The column that defines the size of the bubbles
        # report_df_city_col = location column in report_df
        # location_df_city_col = location column in location_df
        # output_image = destination address of map on local host
        # longitude = Name of the longitude column in location_df
        # latitude = Name of the latitude column in location_df
        # limit = Number of cities(bubbles) to appear on the map
        # scale = scale of the bubbles

        ### Group by report_df_city_col and aggregate
        # plotly.io.orca.config.executable = 'miniconda3/bin/orca'
        limited_report_df = self.report_df[[report_df_target_col, report_df_city_col]]
        report_df_agg = limited_report_df.groupby([report_df_city_col], as_index=False).agg('sum')
        report_df_agg.rename({report_df_city_col: location_df_city_col}, axis='columns', inplace=True)
        report_df_agg_merged = report_df_agg.merge(self.location_df, on=location_df_city_col, how='left')
        report_df_agg_merged.sort_values(by=[report_df_target_col], ascending=False, inplace=True)
        report_df_agg_merged.reset_index(drop=True, inplace=True)

        cities = []

        number_of_bubbles_on_map = min(report_df_agg_merged.shape[0], limit)
        ### Add one bubble for each city on the map. The bubble size is proportional to the report_df_target_col entry
        for i in range(number_of_bubbles_on_map):
            df_sub = report_df_agg_merged.iloc[[i]]
            city = go.Scattergeo(
                locationmode='USA-states',
                lon=df_sub[longitude],
                lat=df_sub[latitude],
                marker=go.scattergeo.Marker(
                    size=df_sub[report_df_target_col] / scale,
                    line=go.scattergeo.marker.Line(width=0.5, color='rgb(40,40,40)'), sizemode='area'
                ),
                name='{} -- {}: {:,}'.format(df_sub[location_df_city_col].values[0],
                                             report_df_target_col,
                                             df_sub[report_df_target_col].values[0])
            )
            cities.append(city)
        ### Layout of the map
        layout = go.Layout(
            showlegend=True,
            geo=go.layout.Geo(
                scope='usa',
                projection=go.layout.geo.Projection(type='albers usa'),
                showland=True,
                landcolor='rgb(217, 217, 217)',
                subunitwidth=1,
                countrywidth=1,
                subunitcolor="rgb(255, 255, 255)",
                countrycolor="rgb(255, 255, 255)",
            )
        )

        fig = go.Figure(data=cities, layout=layout)
        fig.update_layout(legend=dict(x=0.82, y=0))
        fig.write_image(output_image, scale=3)


if __name__ == "__main__":
    df_stats = pd.read_csv('HGcampaign_Stats.csv')
    locations_df = pd.read_csv('statelatlong.csv')
    MG = MapGen(df_stats, locations_df)
    MG.agg_map('reach', 'region', 'City')
