

queue_helpers
===============
This is a project that is used to manage requests in queue.

Installing
============

.. code-block:: bash

    pip install queue_helpers

Usage
=====

.. code-block:: bash

    >>> def send_rpc_message(queue_name, request, rabbit_username, rabbit_password, rabbitserver, vhost):
    >>>     cfg_helper = ConfigHelper()
    >>>
    >>>     client = RpcClient(rabbit_server_host=rabbitserver,
    >>>                        virtual_host=vhost,
    >>>                        server_queue_name=queue_name,
    >>>                        username=rabbit_username,
    >>>                        password=rabbit_password)
    >>>
    >>>     resp = client.call(json.dumps(request))
    >>>
    >>>     response = json.loads(resp.decode("utf-8"))
    >>>
    >>>     return response