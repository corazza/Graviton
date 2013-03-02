Graviton
========

<pre>
Gravity simulator in Python.

To run:

    ./graviton name [params]

        Simulate the universe found in unis/name.json file.

        Parameters (none are required, parameter types are specified in angle brackets, all of these override settings.ini):

            -r      - report some state each <float> real time seconds seconds.
            -tu     - run the simulation for <float> universe seconds.
            -tr     - run the simulation for <float> real seconds.
            -f      - save the simulation into a file named "unis/<string>.json" - recommended so the original doesn't get overwritten'!
            -s      - save the simulation each <float> universe seconds (best used with "-f alternative_name").
            -dts    - run the simlation <float> times faster than the real universe (-dts 2 makes the planets travel two times faster, for example).
            -cdt    - run the simulation with a constant delta-time of <float> (in seconds, overrides -dts).

        Flags (none required):

            -fe     - save it into a directory named "unis/uni_name/[at date].json" - recommended, overwrites -f.
            -cnt    - continue from the last save file. Only use if -fe has been used previously with the uni, otherwise just load the uni again from the original file and it will continue.
            -se     - save at exit.
            -min    - run the minimal version of Graviton (best used in conjunction with -cdt <float> for accurate measurements).

This software is licensed under the MIT license, provided in the doc/LICENSE.txt file.
</pre>
