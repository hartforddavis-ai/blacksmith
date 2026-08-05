# BOUND RUN — EXECUTE KERNEL

Fixed. Does not change without a Law 1 ruling.

## ORDER

```
1  WATCH   python3.12 watch_bound.py <job> <model>   in the operator's own pane
2  RUN     python3.12 run_bound.py   <job> <model>
```

The watcher attaches to a file that appears after it starts. Started second,
there is nothing for it to attach to.

Backgrounded, its output goes where the operator does not look and the run is
blind. The heartbeat exists for the operator, not for whoever launched it.
