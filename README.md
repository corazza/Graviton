Graviton
========

Gravity simulator in Python.

To run:

    ./graviton name [params]
    
        Simulate the universe found in unis/name.json file.
    
        Parameters (none are required, parameter types specified in angle brackets, all of these override settings.ini):
        
        -t - run the simulation for <float> seconds. Might not be precise.
        -f - save the simulation into a file named "unis/<string>.json" - recommended!
        -s - save the simulation each <int> updates.
        -dts - run the simlation <float> times faster than the real universe (-dts 2 makes the planets travel two times faster, for example).
        -cdt - run the simulation with a constant delta-time of <float> (in seconds, overrides).
        -min - run the minimal version of Graviton (best used in conjunction with -cdt <float>).
    
This software is licensed under the MIT license, provided in the doc/LICENSE.txt file.

