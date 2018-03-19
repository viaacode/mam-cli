#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  mam-cli.py
#
#  Copyleft 2018 VIAA vzw
#  <admin@viaa.be>
#
#  @author: https://github.com/maartends
#
#######################################################################
#
#  mam-cli.py
#
#  See README.md
#  
#######################################################################

import os
import sys
import csv
import json
import yaml
import logging
import argparse
# 3d party imports
import pika

# Get logger
log = logging.getLogger('mam-cli')
log.setLevel(logging.DEBUG)
# create handler and set level to debug
ch = logging.StreamHandler(stream=sys.stdout)
#~ ch = logging.FileHandler('./logging.log', mode='a')
ch.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(lineno)d - %(levelname)s - %(message)s')
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
log.addHandler(ch)

# Get some credentials from .env.secrets
log_fmt_str = 'Environment variable "%s" not present. Exiting.'
try:
    RABBIT_MQ_USER  = os.environ['RABBIT_MQ_USER']
except KeyError as e:
    log.error(log_fmt_str % 'RABBIT_MQ_USER')
    exit(1)
try:
    RABBIT_MQ_PASSWD = os.environ['RABBIT_MQ_PASSWD']
except KeyError as e:
    log.error(log_fmt_str % 'RABBIT_MQ_PASSWD')
    exit(1)

credentials = pika.PlainCredentials(RABBIT_MQ_USER, RABBIT_MQ_PASSWD)
parameters  = pika.ConnectionParameters(cfg['rabbitmq']['host'],
                                        cfg['rabbitmq']['port'],
                                        '/', credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
# Turn on delivery confirmations if need be
#~ channel.confirm_delivery()

def read_csv_input_file_to_list(input_file):
    with open(input_file) as f:
        reader = csv.DictReader(open(input_file, 'r'))
    return list(reader)

def mam_delete(records, cmd_args, cfg):
    for record in records:
        d = {
            'correlation_id': '/'.join([cmd_args.es_prefix or record['cp_name'],
                                        record['external_id']]),
            'fragment_id':    record['fragment_id'],
            'cp':             record['cp_name'],
        }
        log.debug('Queueing for deletion: %s' % d)
        if not cmd_args.dryrun:
            res = channel.basic_publish(exchange='',
                    routing_key=cfg['rabbitmq']['del_queue'],
                    body=json.dumps(d))
            log.debug(res)

def main(cmd_args):
    # Read in proper config file.
    cfgfile = 'prd.config.yaml' if cmd_args.prd else 'qas.config.yaml'
    with open(cfgfile, 'r') as yamlfile:
        cfg = yaml.load(yamlfile)
    if cmd_args.cmd != 'rm':
        log.warn('Not yet implemented: %s. Exiting.' % cmd_args.cmd)
        exit(0)
    log.info('Reading records from %s.' % cmd_args.input_file)
    records = read_csv_input_file_to_list(cmd_args.input_file)
    log.info('%s records read.' % len(records))
    mam_delete(records, cmd_args, cfg)
    connection.close()
    if cmd_args.dryrun:
        log.info('"dryrun" selected: nothing happened.')


if __name__ == '__main__':
    # Parse the command line
    parser = argparse.ArgumentParser(prog="mam-cli",
                description="""Act on MAM resources""")
    environment = parser.add_mutually_exclusive_group(required=True)
    environment.add_argument('--prd', action='store_true',
                        help='Run %(prog)s in production mode.')
    environment.add_argument('--qas', action='store_true',
                        help='Run %(prog)s in QAS mode.')
    parser.add_argument(dest='cmd', choices=['ls', 'find', 'cp', 'mv', 'rm'],
                        help='Command')
    parser.add_argument('-d', '--dryrun', dest='dryrun',
                        required=False, action='store_true',
                        default=False, help='''Practice run, ie.,
                        display the operations that would be performed
                        using the specified command without actually
                        running them. Only makes sense in non-safe
                        (destructive) operations.''')
    parser.add_argument('-e', '--es-prefix', type=str, dest='es_prefix',
                        required=False, help='''Prefix to be sent along to
                        ElasticSearch. Convenient for grouping together
                        the log entries''')
    parser.add_argument('-f', '--input_file', type=str, dest='input_file',
                        required=True, help='''CSV input file with the
                        resources to be deleted.''')
    cmd_args = parser.parse_args()
    main(cmd_args)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
