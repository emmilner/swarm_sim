#!/bin/sh
#
#PBS -l nodes=1:ppn=1,walltime=24:00:00
module add languages/python-3.7.7-anaconda-2020.20-gprMAX

# Change into working directory 
cd swarm_and_boxes

# Execute code
time python run_task2c.py
sleep 60 
