#!/bin/bash
rm datawarehouse/activity_serie.csv
rm datawarehouse/census.csv
rm datawarehouse/proposals.csv

python collectors/census_collector.py
python collectors/proposal_collector.py
python collectors/timeserie_collector.py