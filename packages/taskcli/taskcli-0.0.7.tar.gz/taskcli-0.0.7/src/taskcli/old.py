import inspect
import argparse


import logging


log = logging.getLogger("taskcli")

num_tasks = 0
task_data = {}


# References:
#  - decorators in general
#    https://stackoverflow.com/questions/739654/how-do-i-make-function-decorators-and-chain-them-together
#  - decorators with optional parenthesis
#    https://stackoverflow.com/questions/35572663/using-python-decorator-with-or-without-parentheses

import sys

if sys.stderr.isatty() and sys.stdout.isatty():
    RED = "\033[91m"
    ENDC = "\033[0m"
else:
    RED = ""
    ENDC = ""

# def log_error(msg):
#     log.error(f"{RED}{msg}{ENDC}")


def task(namespace=None, foo=None, env=None, required_env=None):
    """
    ns: command namespace. Allows for laying command in additional namespace
    env: environment variables to assert
    """
    # namespace = namespace
    global num_tasks
    num_tasks += 1

    def task_wrapper(fn):
        # Initialize an empty dictionary to store parameter information

        import os

        def wrapper(*args, **kwargs):
            func_name = fn.__name__

            # assert env vars
            if required_env:
                raise NotImplementedError("required_env not implemented yet")

            # Call the decorated function
            import sys

            if sys.stderr.isatty():
                GREEN = "\033[92m"
                ENDC = "\033[0m"
            else:
                GREEN = ""
                ENDC = ""

            loggg = log.debug
            if True:
                loggg = log.info
            loggg(f"{GREEN}---[{fn.__name__}]{'-'*50}{ENDC}")

            loggg = log.debug
            if True:
                loggg = log.info

            if args:
                for idx, arg in enumerate(args):
                    name_if_param = list(task_data[func_name]["params"].keys())[idx]
                    loggg(f"{GREEN}{name_if_param.rjust(12)} = {arg}{ENDC}")
            if required_env:
                for name in required_env:
                    loggg(f"{GREEN}{('$'+name).rjust(12)} = {os.environ[name]}{ENDC}")

            if args:
                try:
                    new_args = []
                    for idx, arg in enumerate(args):
                        name_if_param = list(task_data[func_name]["params"].keys())[idx]
                        typ = task_data[func_name]["params"][name_if_param]["type"]

                        supported_types = [int, float, bool, str, list[int], list[str]]

                        if typ != inspect._empty and typ in supported_types:
                            # Special conversion for bools
                            if typ == bool:
                                if arg in ["false", "0", "False"]:
                                    new_args.append(False)
                                else:
                                    new_args.append(True)
                            elif typ == list[int]:
                                raise Exception("list[int] not implemented yet")
                                # print("converting to list of ints")
                                arg = [int(x) for x in arg]
                                new_args.append(arg)

                            elif typ == list[str]:
                                raise Exception("list[str] not implemented yet")
                                # print("converting to list of strs")
                                arg = [str(x) for x in arg]
                                new_args.append(arg)
                            elif typ == list:
                                raise NotImplemented("..... not implemented")

                            else:
                                new_args.append(typ(arg))
                        else:
                            new_args.append(arg)
                except:
                    log.error(f"{RED}Error converting arguments to types specified in function signature.{ENDC}")
                    raise
                args = new_args

            # XXXXXXXXXXXxx

            # # hack in coversion. Not clear why it does not work now
            # if hasattr(fn, argh.decorators.ATTR_ARGS):
            #     print ("has attr args", fn, getattr(fn, argh.decorators.ATTR_ARGS))
            #     arg_decors = getattr(fn, argh.decorators.ATTR_ARGS)
            #     new_args = []
            #     for idx, arg_decor in enumerate(arg_decors):
            #         present =  "nargs" in arg_decor
            #         proper = arg_decor["nargs"] in ["+", "*", "?"]
            #         has_type = 'type' in arg_decor

            #         if present and proper and has_type:
            #             print("converting")
            #             target_type = arg_decor["type"]
            #             converted = [target_type(x) for x in args[idx]]
            #             new_args.append(converted)
            #         else:
            #             new_args.append(args[idx])
            #     args = new_args

            output = fn(*args, **kwargs)
            return output

        # Get the signature of the decorated function
        signature = inspect.signature(fn)

        # Extract parameter names and types
        parameters = signature.parameters

        # function name
        func_name = fn.__name__

        # Store parameter information in the dictionary
        parameters = signature.parameters
        parameter_info = {}
        for name, param in parameters.items():
            typ = param.annotation
            default_value = param.default
            parameter_info[name] = {"type": typ, "default": default_value}
            # print (name, typ, default_value)

        # Attach the parameter information to the wrapper function
        # task_data[func_name]["par"] = parameter_info

        nonlocal namespace
        if callable(namespace):
            namespace = None

        task_data[func_name] = {
            "name": func_name,
            "func": fn,
            "namespace": namespace,
            "params": parameter_info,
            "module": fn.__module__,
        }

        ###############################################################
        # argh hacks
        # replace the name of the wrapper
        wrapper.__name__ = func_name

        # replace the signature of the wrapper with the signature of the function
        # so that later argh properly reads it.
        sig = inspect.signature(fn)
        sig = sig.replace(parameters=tuple(sig.parameters.values()))
        wrapper.__signature__ = sig

        # copy any ATTR_ARGS set by the @argh.arg decorator
        # this way the order of @jj.task and @jj.arg does not matter

        for x in [
            argh.decorators.ATTR_ALIASES,
            argh.decorators.ATTR_ARGS,
            argh.decorators.ATTR_EXPECTS_NAMESPACE_OBJECT,
            argh.decorators.ATTR_NAME,
            argh.decorators.ATTR_WRAPPED_EXCEPTIONS,
            argh.decorators.ATTR_WRAPPED_EXCEPTIONS_PROCESSOR,
        ]:
            # pass
            if hasattr(fn, x):
                setattr(wrapper, x, getattr(fn, x))
        ###############################################################

        return wrapper

    if callable(namespace):
        return task_wrapper(namespace)  # return 'wrapper'
    else:
        return task_wrapper  # ... or 'decorator'


class CustomArgumentParser(argparse.ArgumentParser):
    pass


def cli():
    # Detect if we're running as a script or not
    frame = inspect.currentframe()
    module = inspect.getmodule(frame.f_back)
    if module.__name__ != "__main__":
        return
    print("about to parse..")
    parser = argparse.ArgumentParser()

    # 3 options:
    #  1) a single command
    #  2) multiple commands, no default one
    #  3) multiple commands, with a default one (no supported yet)
    # if len(task_data) == 1:
    if num_tasks == 1:
        the_task = list(task_data.values())[0]["func"]
        print("default task")
        argh.set_default_command(parser, the_task)
    else:
        for _, func in task_data.items():
            func_name = func["name"]
            import sys

            func = getattr(sys.modules[func["module"]], func_name)

            argh.add_commands(parser, [func])

    argh.dispatch(parser)
