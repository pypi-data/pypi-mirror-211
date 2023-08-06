Description: 

    - This is a simple package.
    - This package support decorator for query, insert, update raw query and rollback transaction.
    - It's support for add multiple variable into AWS's logger too


WorkDirectory:


    ├─┬ aws_support
    │ ├─┬ database                              # support database
    │ │ ├─┬ insert.py                     # Directory for filter
    │ │ ├─┬ query.py                      # Directory for serializers
    │ │ ├─┬ update.py                     # Directory for urls
    │ ├─┬ log.py                                # Directory for manage logs
    │ ├─┬ transaction.py                        # Directory for test


Requiments:

    - python >= 3.7
    - sqlachemy >= 2.0.0

