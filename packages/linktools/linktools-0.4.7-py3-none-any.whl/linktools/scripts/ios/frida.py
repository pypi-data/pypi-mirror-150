#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author  : Hu Ji
@file    : at_frida.py
@time    : 2018/11/25
@site    :
@software: PyCharm

              ,----------------,              ,---------,
         ,-----------------------,          ,"        ,"|
       ,"                      ,"|        ,"        ,"  |
      +-----------------------+  |      ,"        ,"    |
      |  .-----------------.  |  |     +---------+      |
      |  |                 |  |  |     | -==----'|      |
      |  | $ sudo rm -rf / |  |  |     |         |      |
      |  |                 |  |  |/----|`---=    |      |
      |  |                 |  |  |   ,/|==== ooo |      ;
      |  |                 |  |  |  // |(((( [33]|    ,"
      |  `-----------------'  |," .;'| |((((     |  ,"
      +-----------------------+  ;;  | |         |,"
         /_)______________(_/  //'   | +---------+
    ___________________________/___  `,
   /  oooooooooooooooo  .o.  oooo /,   \,"-----------
  / ==ooooooooooooooo==.o.  ooo= //   ,`\--{)B     ,"
 /_==__==========__==_ooo__ooo=_/'   /___________,"
"""

from linktools import logger, utils
from linktools.decorator import entry_point
from linktools.frida import FridaApplication, FridaShareScript, FridaScriptFile, FridaEvalCode
from linktools.ios import IOSArgumentParser, MuxError
from linktools.ios.frida import FridaIOSServer


@entry_point(known_errors=[MuxError])
def main():
    parser = IOSArgumentParser(description='easy to use frida')
    parser.add_argument('-b', '--bundle-id', action='store', default=None,
                        help='target bundle id (default: frontmost application)')
    parser.add_argument('--spawn', action='store_true', default=False,
                        help='inject after spawn (default: false)')

    parser.add_argument("-P", "--parameters", help="user script parameters", metavar=("KEY", "VALUE"),
                        action='append', nargs=2, dest="user_parameters", default=[])
    parser.add_argument("-l", "--load", help="load user script", metavar="SCRIPT",
                        action='append', dest="user_scripts", type=lambda o: FridaScriptFile(o), default=[])
    parser.add_argument("-e", "--eval", help="evaluate code", metavar="CODE",
                        action='append', dest="user_scripts", type=lambda o: FridaEvalCode(o))
    parser.add_argument("-c", "--codeshare", help="load share script url", metavar="URL",
                        action='append', dest="user_scripts", type=lambda o: FridaShareScript(o, cached=False))
    parser.add_argument("-cc", "--codeshare-cached", help="load share script url, use cache first", metavar="URL",
                        action='append', dest="user_scripts", type=lambda o: FridaShareScript(o, cached=True))

    parser.add_argument("-d", "--debug", action='store_true', default=False,
                        help="debug mode")

    args = parser.parse_args()
    device = args.parse_device()
    bundle_id = args.bundle_id

    user_parameters = {p[0]: p[1] for p in args.user_parameters}
    user_scripts = args.user_scripts

    class Application(FridaApplication):

        def on_spawn_added(self, spawn):
            logger.debug(f"Spawn added: {spawn}", tag="[✔]")
            if spawn.identifier == bundle_id:
                self.load_script(spawn.pid, resume=True)
            else:
                self.resume(spawn.pid)

        def on_session_detached(self, session, reason, crash) -> None:
            logger.info(f"Detach process: {session.process_name} ({session.pid}), reason={reason}", tag="[*]")
            if reason in ("connection-terminated", "device-lost"):
                self.stop()
            elif len(self._sessions) == 0:
                app.load_script(app.device.spawn(bundle_id), resume=True)

    with FridaIOSServer(device=device) as server:

        app = Application(
            server,
            debug=args.debug,
            user_parameters=user_parameters,
            user_scripts=user_scripts,
            enable_spawn_gating=True
        )

        target_pids = set()

        if utils.is_empty(bundle_id):
            target_app = app.get_frontmost_application()
            if target_app is None:
                raise RuntimeError("unknown frontmost application")
            bundle_id = target_app.identifier

        if not args.spawn:
            # 匹配所有app
            for target_app in app.enumerate_applications():
                if target_app.pid not in target_pids:
                    if target_app.pid > 0 and target_app.identifier == bundle_id:
                        app.load_script(target_app.pid)
                        target_pids.add(target_app.pid)

            # 匹配所有进程
            for target_process in app.enumerate_processes():
                if target_process.pid > 0 and target_process.pid not in target_pids:
                    if target_process.name == bundle_id:
                        app.load_script(target_process.pid)
                        target_pids.add(target_process.pid)

        if len(target_pids) == 0:
            # 直接启动进程
            app.load_script(app.spawn(bundle_id), resume=True)

        app.run()


if __name__ == '__main__':
    main()
