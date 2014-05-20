Graviton
========

Gravity simulator in Python.

I've written about creating this application on my website: [jancorazza.com/category/projects/graviton/](http://jancorazza.com/category/projects/graviton/).  
This post sums up the features and the results I got from some simulations: [jancorazza.com/2013/03/graviton-has-been-finished/](http://jancorazza.com/2013/03/graviton-has-been-finished/).

![Orbit visualizations (Solar system)](http://jancorazza.com/wordpress/wp-content/uploads/2013/03/orbits_regular-1024x565.png)

## Running

To run Graviton, execute `./graviton <name> [params] [flags]`. This command will load the configuration file found in `unis/<name>.json` and begins simulating it based on the `[params]` and the `[flags]`.

## Parameters

None are required, parameter types are specified in angle brackets, all of these override settings.ini):

    -r      - report some state each <float> real time seconds seconds.
    -tu     - run the simulation for <float> simulated seconds.
    -tr     - run the simulation for <float> real seconds.
    -f      - save the simulation into a file named "unis/<string>.json" - recommended so the original doesn't get overwritten!
    -s      - save the simulation each <float> simulated seconds (best used with "-f alternative_name").
    -dts    - run the simlation <float> times faster than the real universe (-dts 2 makes the planets travel two times faster, for example).
    -cdt    - run the simulation with a constant delta-time of <float> (in seconds, overrides -dts).
    -do     - draw orbits. Update them each <float> real seconds and keep them in memory for <float> real seconds.
    -i      - call the interrupt_handler defined in userdata/user.py each <float> simulated seconds.

### Flags

None are required.

    -fe     - save it into a directory named "unis/{uni_name}/[at date].json" - recommended, overwrites -f.
    -cnt    - continue from the last save file. Only use if -fe has been used previously with the uni, otherwise just load the uni again from the original file and it will continue.
    -se     - save at exit.
    -min    - run the minimal version of Graviton (best used in conjunction with -cdt <float> for accurate measurements).
