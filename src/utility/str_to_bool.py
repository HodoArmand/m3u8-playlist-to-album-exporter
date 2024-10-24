""" String to bool converter for CLi args. """
import argparse


def str_to_bool(v):
    """ String to bool converter for CLi args. """
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    if v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False

    raise argparse.ArgumentTypeError('Boolean value expected.')
