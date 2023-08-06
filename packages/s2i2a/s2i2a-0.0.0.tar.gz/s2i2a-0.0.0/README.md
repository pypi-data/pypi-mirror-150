# litreview

Maps a parameter sweep to an int and then back again.

# Install

```
pip3 install s2i2a
```

# Usage

```
s2i2a <direction> <command> <sweep arguments>
```

The goal is to support all the sweep syntax used by [hydra's](https://github.com/facebookresearch/hydra) default sweeper.

But for now, `s2i2a` just supports sweeps of the shape `arg=val1,val2,val3,...`.


A help message is also provided

```
s2i2a --help
```

## Sample usage

Call `s2i2a s2i` with all the shell arguments necessary to run your script, plus your script's arguments, plus your sweeps.

```
s2i2a s2i python3 train.py 'non-sweep argument' another_non-sweep_arg arg1=val1,val2 arg2=val3,val4,val5
```

Generates a `s2i.txt` file in your local directory containing

```
arg1=val1 arg2=val3
arg1=val1 arg2=val4
arg1=val1 arg2=val5
arg1=val2 arg2=val3
arg1=val2 arg2=val4
arg1=val2 arg2=val5
python3 train.py 'non-sweep argument' another_non-sweep_arg
```

You then build a Docker/Singularity image containing said file, and you
install s2i2a inside that image.

Then you can call at the end of a `.sh` file (say, an SBATCH script containing an iterator integer): 

```
s2i2a i2a 3
```

This calls `execvp`, replace s2i2a by 

```
python3 train.py 'non-sweep argument' another_non-sweep_arg arg1=val2 arg2=val3
```

## Quick debugging

You probably don't want to mess up your sweeps *after* uploading to the cluster.
Instead, you can invoke `test_s2i2a.py`. This will run a dummy `execvp` invokation and will print
what arguments got passed to the script. *Be aware that it will rewrite the path of the script to point to s2i2a's installation folder*.
