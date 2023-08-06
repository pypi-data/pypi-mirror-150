def reset_sigpipe_handling():
    '''Restore the default `SIGPIPE` handler on supporting platforms.
    Python's `signal` library traps the SIGPIPE signal and translates it
    into an IOError exception, forcing the caller to handle it explicitly.

    Simpler applications that would rather silently die can revert to the
    default handler. See https://stackoverflow.com/a/30091579/1026 for details.
    '''
    try:
        from signal import signal, SIGPIPE, SIG_DFL
        signal(SIGPIPE, SIG_DFL)
    except ImportError:  # If SIGPIPE is not available (win32),
        pass             # we don't have to do anything to ignore it.
