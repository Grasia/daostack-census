# daostack-census
Scripts and data for a Daostack census

## Metrics and plots
* [Activity chart by DAO](https://github.com/Grasia/daostack-census/blob/master/ploters/activity_plot.py)
* [Boosting correlation chart](https://github.com/Grasia/daostack-census/blob/master/ploters/boosting_correlation_plot.py)
* [DAO's budget chart by token](https://github.com/Grasia/daostack-census/blob/master/ploters/budget_plot.py)
* [DAO stats correlation](https://github.com/Grasia/daostack-census/blob/master/ploters/dao_stats_correlation_plot.py)
   * User vs proposals correlation 
   * Users vs votes correlation
   * Users vs stakes correlation
   * Users vs holdings correlation
* [DAO stats distribution](https://github.com/Grasia/daostack-census/blob/master/ploters/distribution_plot.py)
   * Users distribution
   * Proposals distribution
   * Votes distribution
   * Stakes distribution
* [Prediction rate by DAO](https://github.com/Grasia/daostack-census/blob/master/ploters/prediction_rate_plot.py)
* [Timeseries metrics of DAOstack](https://github.com/Grasia/daostack-census/blob/master/ploters/time_serie_plot.py)
   * Active DAOs
   * Active users
   * New proposals
   * Activity


## Installing
Requirements:
* Python >= 3.6
* tkinter

Install all python dependencies with:

`pip install -r requirements.txt`

For ploting you need tkinter, so, if you are in Ubuntu install it with:

`sudo apt-get install python3-tk`

## How does it works?
You have to load the `datawarehouse/` to use the plot scripts. So, to update it, use the following script:

`chmod +x collectors/update_datawarehouse.sh`

`./collectors/update_datawarehouse.sh`

Now, you are able to show the data in `datawarehouse/`, do it using the scripts located in `ploters/`.

E.g. `python distribution_plot.py`

## Publications
* El Faqir, Y., Arroyo, J., Hassan, S. (2020). An overview of Decentralized Autonomous Organizations on the blockchain. Proceedings of the 16th International Symposium on Open Collaboration (Opensym 2020) 11:1-11:8. ACM. 
    * [Freely available here](https://opensym.org/wp-content/uploads/2020/08/os20-paper-a11-el-faqir.pdf).

## Acknowledgements
This work is funded by the Spanish Ministry of Science and Innovation and the [P2P Models](https://p2pmodels.eu/) project, which is funded by the European Research Council.
