# breakpoint.py
# implementation of IDE-free breakpoints
# (unless you count IPython as an IDE, which maybe it is)

from IPython.terminal.embed import *

def embed(s=2, **kwargs): #stolen from IPython/terminal/embed.py
    config = kwargs.get('config')
    header = kwargs.pop('header', '')
    compile_flags = kwargs.pop('compile_flags', None)
    if config is None:
        config = load_default_config()
        config.InteractiveShellEmbed = config.TerminalInteractiveShell
        kwargs['config'] = config
    shell = InteractiveShellEmbed.instance(**kwargs)
    shell(header=header, stack_depth=(s+1), compile_flags=compile_flags)


def breakpoint():
    embed(2)

def breakpoint2():
    "doesn't behave teh same"
    import IPython;    IPython.embed()

breakpoint = breakpoint

def callit():
   v =4
   breakpoint()


callit()
