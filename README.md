Lean ETL
=======
This project was merged in with the [HiGeorge](https://hi-george.com/) back-end production in February 2020.  
The [presentation](https://docs.google.com/presentation/d/1mK1OKe9bXOSkPA-jcyNH0rwXlT49Bf4ys_a_pqeL9ls/edit#slide=id.g6eebf444bf_1_0)
slides are available for public view.

About HiGeorge
---
HiGeorge is a pre-seed startup that provides a crowd-funding platform for civic activism. They run different campaigns on their platform targeting different civic issues and the public can contribute to and fund these campaigns.
HiGeorge then utilizes the funds to run advertisements on social media such as Facebook to reach out to a wide audience 
in a call for action. Afterwards, the users' profiles get updated with the impact that the contribution of each user has made.

Scope of the project
---
Initially, the back-end ETL operations of HiGeorge used to be done manually. This project was executed to automate such processes.

ETL means the extract, transform, and load of data end-to-end. HiGeorge stores data about its campaigns, expenditures, canvases and so on in a Mongo DataBase. We want to first look at all the campaigns in the HiGeorge database and find the active ones and for those active campaigns we want to extract Facebook ads insights which contain metrics like conversion rate, reach, and amount spent. If there is an update in the ads insighs since the last time checked then we want to create aggregated stats and visualizations from the extracted insights. Afterwards, the visualizations need to be loaded on Google Cloud Storage and based on the aggregated stats the expenditures need to get updated. Lastly, we need to update the canvases according to the updated expenditures to provide users with statistics about how much of their funds have been spent and how far their contributions go. These steps are shown in the fallowing diagram:

![ETL-Processes](/images/ETL-Processes.png "ETL Processes")

Architecture
---
The pipelines that automate the ETL processes are as the fallowing:

![Architecture](/images/Architecture.png "Architecture")

Airflow's scheduler triggers the script at constant time intervals. The script queries MongoDB to extract active HiGeorge campaigns and then it queries facebook to get ads insights for those active campaigns. Then it aggregates the ads insights and creates a map which is going to be dumped on the Google Cloud Storage and it also updates the expenditures and canvases in the MongoDB accordingly.

Trade-off
---
The use of MongoDB in this project can be questioned as it is not the fastest possible database. Though, the performance of the database is not the only deciding factor. For a young startup with an evolving database schema having a flexible database that accommodates changes is vital. In the case of HiGeorge at its current stage the data throughput is not big and it can be argued that having a flexible database such as MongoDB is much more important than having the fastest database.

Possible future bottleneck
---
The writes to the MongoDB are tangibly slower than the reads from it. Therefore, the part of the pipeline that is used for the writes from the script to the MongoDB can become the bottleneck of the pipelines when the data throughput and the number of writes increase. A quick fixture for the mentioned blockage would be a queue between the script and the MongoDB for the writes.

![Quick_Fix](/images/HiGeorge-future-Architecture.png "Quick Fix")

Directory description
---
This repository contains the following

- `GScommunication.py` provides a function for dumping files on the Google Cloud Storage which returns the URL to the dumped files accordingly.  
- `visualization.py` provides an object for creating visualizations.  
- `update_map_and_expenditure.py` does the ETL operations. `update_map_and_expenditure.py` imports other modules including `GScommunication.py` and `visualization.py`.  
- `dags/` contains the dag file that Airflow uses to trigger the `update_map_and_expenditure.py` script automatically on specific time intervals.


Disclaimer
---
To respect the intellectual property rights of HiGeorge and the non-disclosure agreement signed between the 
parties involved parts of the scripts in this repository have been commented out in the form of 
pseudocode.
