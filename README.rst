=====
s3dir
=====

s3dir is CLI file manager with S3 and Kubernetes inspired from Pctools, Norton Commander and Mdir <https://www.huffingtonpost.kr/2016/05/19/story_n_10042448.html>.

s3dir requires Python version 3.9 and above, kubectl CLI tool, and also requires valid AWS or Kubernetes permissions on CLI environment.

----------
Screenshot
----------
.. image:: https://user-images.githubusercontent.com/1021138/164341194-719d496a-834c-451f-8f51-a48c0bba3c49.gif

---------------
Getting Started
---------------

Try it with::

    pip install s3dir
    s3dir s3://mybucket  # if you want to connect S3 bucket
    s3dir k  # if you want to connect k8s pod

You can clone the git repo::

    git clone https://github.com/rainygirl/s3dir
    cd s3dir
    python3 setup.py install
    s3dir k

-------------
Shortcut keys
-------------

* [Up], [Down] : Move selection
* [Space] : Select specific file to copy
* [Enter] : Open directory/folder
* [Tab], [Shift]+[Tab] : Change section between local and remote.
* [Alt] + [C] : Copy
* [ESC], [Ctrl]+[C] : Quit


------------
Contributing
------------

Feel free to fork & contribute!


-------
License
-------

s3dir is released under the MIT license.


-------
Credits
-------

* `Lee JunHaeng aka rainygirl <https://rainygirl.com/>`_.




