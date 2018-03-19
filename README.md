# mam-cli

**This documentation is a tentative roadmap pointing to what the 
functionality of the mam-cli should/could become. For now, the actual
functionality is nowhere near close to the documentation.
As such, "is" should be interpreted as "should be".**

## Description

The MAM Command Line Interface is a unified tool to manage resources
within MediaHaven.

It is heavily based on (some would say: stolen from) existing cli-tools,
particularly the [aws-cli](https://docs.aws.amazon.com/cli/latest/reference/).

Basically, it is a thin commmand-line wrapper around the
[MediaHaven api](https://archief.viaa.be/mediahaven-rest-api/).

## Synopsis

    mam [options] <command> [parameters]

--help:

    $ python mam-cli.py --help

    usage: mam-cli [-h] (--prd | --qas) [-d] [-e ES_PREFIX] -f INPUT_FILE
                   {ls,find,cp,mv,rm}

    Act on MAM resources

    positional arguments:
      {ls,find,cp,mv,rm}    Command

    optional arguments:
      -h, --help            show this help message and exit
      --prd                 Run mam-cli in production mode.
      --qas                 Run mam-cli in QAS mode.
      -d, --dryrun          Practice run, ie., display the operations that would
                            be performed using the specified command without
                            actually running them. Only makes sense in non-safe
                            (destructive) operations.
      -e ES_PREFIX, --es-prefix ES_PREFIX
                            Prefix to be sent along to ElasticSearch. Convenient
                            for grouping together the log entries
      -f INPUT_FILE, --input_file INPUT_FILE
                            CSV input file with the resources to be deleted.

    
## Available Commands

- ```find```	(TODO)
- ```cp```	(TODO)
- ```ls```	(TODO)
- ```mv```	(TODO)
- ```rm```

## Available Options

- ```--debug```	(boolean: TODO)
 
   Be verbose.
   
- ```--qas``` | ```--prd```
 
   Wich environment to act on. By convention will read configuration
   from ```qas.config.yaml``` and ```prd.config.yaml``` respectively.
   
   **Important!** Sensitive variables (usernames, passwords, apikeys,...)
   should be ```source```d from ```qas.env.secrets``` and
   ```prd.env.secrets``` respectively before running. Example files
   can be found along with the code. The program will exit of no such
   environment variables (as provided in the example files) are defined.
   (Also: see Examples.)

### find

TODO

### cp

TODO

### ls

TODO

### mv

TODO

### rm

Removes media resources.

#### Parameters

- ```--input```

   Takes a csv-file as input. This csv-file contains all the id's
   (fragment-id's) for the resources to be deleted and minimally contains
   following headers/information:
   
   - fragment_id
   - external_id
   - cp_name
   
   This csv-file can be obtained (exported) from following SQL:
   
   ```sql
    SELECT
      fragment_id AS fragment_id,
      external_id AS external_id,
      organisation AS cp_name
    FROM sips s
    WHERE <condition> ;
   ```
   
- ```--es-prefix```

   Optional string that will be prepended to the ElasticSearch entries
   to allow for easier grouping in logging, eg. "funky-delete-job-01".
   If omitted, the cp_name will be used.

- ```--dryrun```	(boolean)
 
   Show what will be deleted but don't actually perform any action.
   
#### Examples

    $ source qas.env.secrets
    $ python mam-cli.py -d --qas rm -f /path/to/csv/test.csv --es-prefix delete-job-01
   
## TODO

- Use docopt: [http://docopt.org/](http://docopt.org/),
- packaging: setup.py, pip, wheel,
- write tests,
- write more examples,
- structure code,
- all the TODO's...
