Lean ETL
=======
This project merged in with the [HiGeorge](https://hi-george.com/) back-end production in Februrary 2020.  
The [presentation](https://docs.google.com/presentation/d/1mK1OKe9bXOSkPA-jcyNH0rwXlT49Bf4ys_a_pqeL9ls/edit#slide=id.g6eebf444bf_1_0)
slides are available for public view.

Who is HiGeorge
---
HiGeorge is a pre-seed startup that provides a crowd-funding platform for civic activism. They run different campaigns
targeting different civic issues on their platform and the public can contribute to and fund these campaigns.
HiGeorge then utilizes the funds to run advertisemnts on social media such as Facebook to reach out to a wide audiance 
in a call for action. Afterwards, the users' profiles get updated with the impact that the contribution of each user has made.

Scope of the project
---
Initially, the back-end ETL operations of HiGeorge used to be done manually. This project was executed in order to automate 
such processes.

ETL means the extract, transform, and load of data end-to-end. HiGeorge keeps the data about campaigns, expenditures, canvases and so on on a Mongo DataBase. We want to first look at the campaigns in the HiGeorge Mongo DataBase and for those campaigns that are active we want to extract Facebook ad insights which contain parameters like conversion, reach, and amount spent. Then from the extracted insight we want to create aggregated stats and visualizations. Afterwards, the visualizations need to be loaded on Google Cloud Storage and based on the aggregated stats the expenditures need to get updated. Lastly we need to update all the other canvases with the updated expenditures to provide users with statistics about how much of their funds have been spent and how far their contributions go. These steps have been shown in the fallowing diagram:

![ETL-Processes](/images/ETL-Processes.png "ETL Processes")


Architecture
---
The pipelines that automate the ETL processes look like this:

![Architecture](/images/Architecture.png "Architecture")

Disclaimer
---
To respect the intellectual property rights of HiGeorge and as part of the non-disclosure agreement signed between the 
parties involved parts of the scripts in this repository have been commented out in the form of 
pseudocode.
