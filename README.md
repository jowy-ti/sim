# HOW TO EXECUTE A SIMULATION

In order to execute a simulation:
> python3 main.py

Almost all the parameters are tuned in **topolgy.yml** file. This file is composed by three sections:

- **Factors.** each factor is quantitative and the interval permited is defined in the right

- **Components.** Definition Queues with its respective amount of servers and mean services time

- **Topology.** The topology defines a sequential flow starting with a virtual entry queue. A queue can have at most one next queue; setting the next field to END explicitly terminates the path.

### Dependencies

Can be found in 'requirements.txt'

### Validation

To perform the validation we need to execute
> python3 model_validation.py

It will output the p-values by performing t-tests to the metrics *avg_wait_time* and *avg_queue_length* of the results of the created simulation engine and the GPSS implementation. If we decide to execute the GPSS implementation we should be carefule because the results will be added to the file 'OutputFile.TXT' and not overwritten, so it is necessary to leave only the results that we want to perform the analysis otherwise the validation will not work.

To perform the RNG validation we need to execute:
> python3 rng_validation.py