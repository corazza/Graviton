Graviton
========

Gravity simulator in Python. Created using [Pygame](http://pygame.org) for the front end.

![Orbit visualizations (Solar system)](http://res.cloudinary.com/dhngozzmz/image/upload/v1443286118/orbits_regular_eix6lz.png)

**Features:**

1. Fourth order Runge-Kutta integrator
2. 3D geometry
3. Minimal mode with no graphics
4. Orbit and vector visualization
5. Reports (ETA calculation, important dates, timers, extensible via the user module)
6. An event system, where the user may override various event handlers for information extraction and custom reports

**Links:**

1. Posts about Graviton: [jancorazza.com/tag/graviton/](http://jancorazza.com/tag/graviton/).
2. This post sums up the features and the results I got from some simulations: [jancorazza.com/2013/03/24/graviton-has-been-finished/](http://jancorazza.com/2013/03/24/graviton-has-been-finished/).
3. [HORIZONS tutorial](http://jancorazza.com/2012/11/19/horizons/)

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
