##print(__file__,'imported')
from dialectics.imports import *
from loguru import logger
import time
LOGGER=None
HIDDEN_NOW=False

class Logger():
    def __init__(
            self,
            init_msg='',
            to_screen=TO_SCREEN,
            to_file=TO_FILE,
            fn=None,
            verbose=1,
            v=1,
            start=True,
            format="""[{time:HH:mm:ss.SSS}] {name}.<level>{function}</level>( <cyan>{message}</cyan> )""",
            format_info="""[{time:HH:mm:ss.SSS}] <level>{message}</level>""",
            fn_clear=True,
            fn_rotation="50MB",
            ):
        # set attrs
        self.format=format
        self.format_info=format_info
        self.to_screen=to_screen
        self.id_screen=None
        self.id_info=None

        self.to_file=to_file
        self.id_file=None
        self.fn_clear=fn_clear
        self.fn_rotation=fn_rotation
        self.fn=fn
        self.now=time.time()
        self.init_msg=init_msg.strip()
        self.init_verbose=v # for initial message

        self.verbose = verbose # general verbosity!

        # clear
        logger.remove()

        # start?
        if start: self.start()

        # init?
        
        if self.init_msg and self.verbose>=self.init_verbose:
            self(f'{self.init_msg}')

    

    def __lt__(self, other_num): return self.verbose<other_num
    def __le__(self, other_num): return self.verbose<=other_num
    def __gt__(self, other_num): return self.verbose>other_num
    def __ge__(self, other_num): return self.verbose>=other_num
    def __eq__(self, other_num): return self.verbose==other_num
    def __ne__(self, other_num): return self.verbose!=other_num
    def __bool__(self): return bool(self.verbose)
    __nonzero__=__bool__

    def set_verbose(self,verbose=1): self.verbose=1

    __call__ = logger.debug

    def __enter__(self):
        __call__ = self.logger.debug
        self.now=time.time()
        self.start_screen()
        return self

    def __exit__(self,*x): 
        if self.verbose >= self.init_verbose:
            delta=time.time()-self.now
            deltastr=humanize.precisedelta(delta,minimum_unit='microseconds',format="%0.4f")
            deltastr=deltastr.replace("microseconds","μs")
            deltastr=deltastr.replace("milliseconds","ms")
            deltastr=deltastr.replace("nanoseconds","ms")
            msg=' ' + self.init_msg[0].lower() + self.init_msg[1:].split(':')[0] if self.init_msg else ''
            # if self.verbose>=self.init_verbose: self(f'Completed{msg} (+{deltastr})\n')# in {deltastr}')
        if not self.to_screen: self.stop_screen()
    
    def start(self):
        self.start_info()
        if self.to_screen: self.start_screen()
        if self.to_file: self.start_file()

    def stop(self):
        self.stop_file()
        self.stop_screen()

    def start_info(self):
        if self.id_info is None:
            self.id_info=logger.add(
                sys.stderr,
                colorize=True,
                level="INFO",
                format=self.format_info
            )

    def start_screen(self):
        if self.id_screen is None:
            if not self.verbose: self.verbose=1
            self.id_screen=logger.add(sys.stderr, colorize=True, format=self.format)
            #logger.debug(f'log added: {self.id_screen}')
    
    def stop_screen(self):
        if self.id_screen is not None:
            #logger.debug('removing sceen log')
            try:
                logger.remove(self.id_screen)
            except ValueError:
                pass
            self.id_screen = None


    def start_file(self):
        if self.id_file is None and self.fn:
            from dialectics.utils import ensure_dir_exists,backup_fn,rmfn
            ensure_dir_exists(self.fn)
            if os.path.exists(self.fn): backup_fn(self.fn)
            rmfn(self.fn)
            
            self.id_file=logger.add(self.fn, rotation=self.fn_rotation, colorize=False, format=self.format)
            #logger.debug(f'log added: {self.id_file}')

    def stop_file(self):
        if self.id_file is not None:
            #logger.debug('removing file log')
            logger.remove(self.id_file)
            self.id_file = None

            # if self.fn_clear and self.fn:
                #logger.debug(f'removing log file: {self.fn}')
                # rmfn(self.fn)

    def __getattr__(self,name):
        from dialectics.utils import getattribute
        res = getattribute(self,name)
        if res is None: res = getattribute(self.logger,name)
        return res

    def hidden(self,verbose=0):
        return log_hidden(verbose=verbose,log=self)
    def shown(self,verbose=1):
        return log_shown(verbose=verbose,log=self)

    @property
    def showing(self): return self.shown()
    @property
    def hiding(self): return self.hidden()
    @property
    def silent(self): return self.hidden(verbose=0)
    @property
    def showing_v(self): return self.shown(verbose=2)
    @property
    def showing_vv(self): return self.shown_v(verbose=3)

    q=hiding
    quiet=hiding
    shh=hiding
    loud=showing_v
    v=showing_v
    vv=showing_vv


    def hide(self):
        self.to_screen=False
        self.stop_screen()
    off=hide
    def show(self):
        self.to_screen=True
        self.start_screen()
    on=show

    
    # def hide(self,verbose=0):
    #     if self.verbose>1: self('hiding log')
    #     self.verbose_was=self.verbose
    #     self.verbose=verbose
    # def show(self,verbose=1):
    #     self.verbose_was=self.verbose
    #     self.verbose=verbose
    #     if self.verbose>1: self('showing log')
    
    @property
    def logger(self):
        from loguru import logger as lgr
        return lgr


Log=Logger


# def Log(force=False,**kwargs):
#     global LOGGER
#     if force or LOGGER is None:
#         LOGGER = Logger(**kwargs)
#     return LOGGER

class log_hidden():
    def __init__(self,verbose=None,log=None):
        self.log=log if log is not None else Log()
        self.verbose=verbose
    def __enter__(self): 
        if self.verbose is not None:
            self.log.verbose_was=self.log.verbose
            self.log.verbose=self.verbose
        self.log.stop_screen()
        return self
    def __exit__(self,*x):
        if self.verbose is not None:
            self.log.verbose=self.log.verbose_was
            self.log.verbose_was=self.verbose
        if self.log.to_screen: self.log.start_screen()

class log_shown():
    def __init__(self,verbose=1,log=None):
        self.log=log if log is not None else Log()
        self.verbose=verbose
    def __enter__(self): 
        self.log.verbose_was=self.log.verbose
        self.log.verbose=self.verbose
        self.log.start_screen()
        return self
    def __exit__(self,*x):
        self.log.verbose=self.log.verbose_was
        self.log.verbose_was=self.verbose
        if not self.log.to_screen: self.log.stop_screen()

def hide_log(): return log_hidden()
def show_log(): return log_shown()




