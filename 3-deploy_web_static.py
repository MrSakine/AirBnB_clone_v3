#!/usr/bin/python3
"""
Creates and distributes an archive to your web servers
"""


def deploy():
    """
    Full deployment based on do_pack & do_deploy (task 2)
    """
    do_pack = __import__("1-pack_web_static").do_pack
    do_deploy_util = __import__("2-do_deploy_web_static").do_deploy

    path = do_pack()
    if path is None:
        return False
    return do_deploy_util(path)
