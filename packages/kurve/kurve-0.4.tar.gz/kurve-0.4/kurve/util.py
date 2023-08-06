#!/usr/bin/env python


def check_is_unix_timestamp(samp, c):
    if samp[c].apply(lambda x: 1 if len(str(x)) == 10 else 0).sum() == len(samp):
        return True
    return False

