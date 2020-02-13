"""
Initiate connections with the database and Facebook API
"""
from statelatlong import locations_df
from campaign import Campaign as cp
from facebook_business.adobjects.campaign import *
from facebook_business.adobjects.adsinsights import *
import pandas as pd
from visualization import MapGen
from GScommunication import upload_blob
import datetime
from expenditures import Expenditure
from update_canvases_script import update_all_canvases
import numpy as np

### List of the conversion types to check
CONVERSION_TO_CHECK = ['submit_application_total']

class Error(Exception):
    """Base class for other exceptions"""
    pass

class NegativeSpent(Error):
    """Raised when current total spent of a HG campaign is less than the last total amount"""
    pass

if __name__ == "__main__":

    """
    HGcampaigns_expenditure: all the expenditures
    HGcampaigns: all the HiGeorge campaigns
    """
    for HGcampaign in HGcampaigns:
        ### Check if a HG campaign is active and has FB campaigns
        """
        if HGcampaign is active and contains Facebook campaigns:
        """
            ### Calculate the total reach and conversion of the active HG campaign
            HGcampaign_total_reach = 0
            HGcampaign_total_conversion = 0
            HGcampaign_total_amount_spent = 0
            """
            for FB_campaign_str in the Facobook campaigns of HGcampaign:
            """
                ### Retrieve each FB_campaign_obj from FB_campaign_str
                FB_campaign_obj = Campaign(FB_campaign_str)
                FB_campaign_insight = (FB_campaign_obj.get_insights(fields=[
                    AdsInsights.Field.campaign_id,
                    AdsInsights.Field.reach,
                    AdsInsights.Field.spend,
                    AdsInsights.Field.conversions
                ], params={
                    'level': AdsInsights.Level.campaign,
                    'date_preset': AdsInsights.DatePreset.lifetime
                }))
                for ads_insight in FB_campaign_insight:
                    if "spend" in ads_insight:
                        HGcampaign_total_amount_spent += int(np.floor(100.*float(ads_insight["spend"])+0.5)) #dollars to cents
                    if "reach" in ads_insight:
                        HGcampaign_total_reach += int(ads_insight["reach"])
                    if "conversions" in ads_insight:
                        for action in ads_insight["conversions"]:
                            if action["action_type"] in CONVERSION_TO_CHECK:
                                HGcampaign_total_conversion += int(action["value"])
            ### Check if there is an update
            expenditure_updated = True
            last_total_amount_spent = 0
            for HGcamp_expend in HGcampaigns_expenditure:
                """
                if the campaign id of HGcamp_expend and the id of HGcampaign are the same:
                    last_total_amount_spent += amount spent for the HGcamp_expend
                    
                if the campaign id of HGcamp_expend and the id of HGcampaign are the same and there is an update since last time:
                    expenditure_updated = False
                """
            ### If there is an update create new expenditure and new map
            if expenditure_updated:
                ### New expenditure
                try:
                    if HGcampaign_total_amount_spent < last_total_amount_spent:
                        raise NegativeSpent
                    """
                    Create a new expenditure to update the expenditures
                    """
                    new_expenditure.save()
                    update_all_canvases()
                except NegativeSpent:
                    print("ERROR : Campaign's current total spent amount cannot be less than its last total spent amount.")
                ### Get FB campaign insights with region for the map
                FB_campaigns_insight_list = []
                """
                for FB_campaign_str in the Facebook campaigns of HGcampaign:
                """
                    FB_campaign_obj = Campaign(FB_campaign_str)
                    FB_campaign_insight = (FB_campaign_obj.get_insights(fields=[
                        AdsInsights.Field.campaign_id,
                        AdsInsights.Field.reach
                    ], params={
                        'level': AdsInsights.Level.campaign,
                        'date_preset': AdsInsights.DatePreset.lifetime,
                        'breakdowns': [AdsInsights.Breakdowns.region]
                    }))
                    FB_campaign_insight_list = [dict(region_stats) for region_stats in FB_campaign_insight]
                    FB_campaigns_insight_list.extend(FB_campaign_insight_list)
                HGcampaign_df = pd.DataFrame(FB_campaigns_insight_list)

                HGcampaign_df = HGcampaign_df[['region', 'reach']]
                type_convert = {'region': str, 'reach': int}
                HGcampaign_df = HGcampaign_df.astype(type_convert)
                HGcampaign_df = HGcampaign_df.groupby(['region'], as_index=False).agg('sum')
                HGcampaign_df.sort_values(by=['reach'], inplace=True, ascending=False)
                HGcampaign_df.reset_index(drop=True, inplace=True)

                ### Dump the df on the local host
                HGcampaign_df.to_csv('HGcampaign_Stats.csv', index=False)

                MG = MapGen(HGcampaign_df, locations_df)

                ### Dump the map on the local host
                MG.agg_map(report_df_target_col='reach',
                           report_df_city_col='region',
                           location_df_city_col='City',
                           output_image='map.png'
                           )

                ### Upload stats and map to Google storage with HiGeorge campaign ID and UTC timestamp
                utc_t = datetime.datetime.utcnow()
                map_url = upload_blob(bucket_name='arashdataproject',
                            source_file_name='map.png',
                            destination_blob_name=str(HGcampaign.id) + '/' +
                                                  str(utc_t.date()) + '/' +
                                                  'maps' + '/' +
                                                  str(utc_t.time())
                            )
                stats_url = upload_blob(bucket_name='arashdataproject',
                            source_file_name='HGcampaign_Stats.csv',
                            destination_blob_name=str(HGcampaign.id) + '/' +
                                                  str(utc_t.date()) + '/' +
                                                  'stats' + '/' +
                                                  str(utc_t.time())
                            )
                """
                Update the map_url and stats_url on the HGcampaign
                """
                HGcampaign.save()
