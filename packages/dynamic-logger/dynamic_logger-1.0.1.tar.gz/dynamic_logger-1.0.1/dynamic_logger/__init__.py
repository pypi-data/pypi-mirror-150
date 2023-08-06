# Author: Ankit Jain <ajatkj@yahoo.co.in>
# Report any issues on GitHub <https://github.com/ajatkj> or via email 
# Version: 1.0.0
"""
Custom Logging (for logging) package to log non-standard items easily and dynamically. 
Provides 2 main interfaces to the users:
- Decorator "log_extras()" to log function input arguments. 
- Function "set_extras(dict)" to log static values.
- Additionally, use "clear()" to clear extras. 
Make sure to set-up formatter to include the extra format fields 
i.e. to log a field called "id", include %(id)s in formatter string.

To use, simply 'import dynamic_logger' and set logging.setLoggerClass(dynamic_logger.Logger)
"""

__author__  = "Ankit Jain <ajatkj@yahoo.co.in>"
__status__  = "production"
__version__ = "1.0.0"
__date__    = "09 April 2022"

import logging
from functools import wraps
import re

class Logger(logging.Logger):
    """
    Custom Logger class overrides logging.Logger to include "extras" in the logs
    """
    def __init__(self, name, level=0, extras:dict = None):
        self.__og_fmts = []
        self.__extras = {}
        self.__default_extras = {}
        if extras is not None:
            self.__default_extras = extras
        self.__decorated_funcs = set()
        logging.Logger.__init__(self, name=name, level=level)

    def info(self, msg, *args, **kwargs):
        self.__log(logging.INFO, msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.__log(logging.WARNING, msg, *args, **kwargs)
    
    def error(self, msg, *args, **kwargs):
        self.__log(logging.ERROR, msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self.__log(logging.DEBUG, msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.__log(logging.CRITICAL, msg, *args, **kwargs)

    def fatal(self, msg, *args, **kwargs):
        self.__log(logging.FATAL, msg, *args, **kwargs)

    def __log(self, level, msg, *args, **kwargs):
        # Reset _extras if caller function is not decorated
        caller = self.findCaller()[2]
        if caller not in self.__decorated_funcs:
            if self.__default_extras == {}:
                self.__extras.clear()
                self.__extras == {}
            else:
                self.__extras.update(self.__default_extras)
        else:
            self.__extras.update(self.__default_extras)
        if self.isEnabledFor(level):
            self.__switch_formatter()
            if self.__extras == {}:
                # stacklevel is set to 2 because __log is at 2nd level (program -> info () -> __log())
                # Setting to 1 which is default will return the name of logger function i.e. info, war etc.
                self._log(level, msg, args, **kwargs, stacklevel=2)
            else:
                self._log(level, msg, args, extra=self.__extras, **kwargs, stacklevel=2)
            self.__switch_formatter(switch='off')

    def log_extras(self,*fields,**kwfields):
        """
        Decorator to log additional (extras) fields
        The fields are extracted from the decorated function definition. 
        You can specify positional arguments to log the "value" or keyword arguments to log "key: value" information.
        - Positional decorator arguments can be argument name (ex. "id", "name") which appear in the funciton definition of the decorated function.
          In this case, formatter string should contain the argument name - i.e. %(id)d, %(name)s
        - Keyword decorator arguments can have value as either positions of positional argument of decorated function or keyword argument. 
          ex. log_extras(id="0") will extract 1st positional argument value. 
          ex. log_extras(id="0.user_id") will extract 1st positional argument value and extract user_id from it.
          ex. log_extras(id="UserObject.user_id") will extract keyword argument UserObject and extract user_id from it.
          All above will have no impact if formatter string doesn't contain %(id)s attribute.
        log_extras("id") -> Extract "id" from decorated function arguments and display in logs as [id]
        log_extras("model.customer_id") -> Extract "customer_id" from "model" model or "dictionary" as [customer_id]
        log_extras(cust_id "model.customer_id") -> Extract "customer_id" from "model" model or "dictionary" as [cust_id: customer_id]
        """
        def middle_func(func):
            self.__decorated_funcs.add(func.__name__)
            @wraps(func)
            def wrapper(*args,**kwargs):
                self.__set_up_extras(fields=fields,kwfields=kwfields,args=args, kwargs=kwargs)
                return func(*args,**kwargs)
            return wrapper
        return middle_func

    def set_extras(self,extras:dict) -> None:
        """
        Set default extras. Input is in key:value pair.
        Ex. set_extras(app="myapp"). Make sure "app" is added to formatter string as %(app)s
        """
        self.__default_extras = extras

    def clear(self,all=False) -> None:
        """
        Clear default extras. 
        Additionally clear all extras (generated by decorator) in case python version doesn't support Frames
        """
        self.__default_extras.clear()
        self.__default_extras = {}
        if all: 
            self.__extras.clear()
            self.__extras = {}

    def __switch_formatter(self, switch="on") -> None:
        """ 
        Function to update the format string dynamically based on extras values present
        Restore original format string when switch is "on"
        """
        eff_handlers = self.handlers
        if eff_handlers == []:
            eff_handlers = self.root.handlers
        if switch == 'on':
            for handler in eff_handlers:
                fmt = handler.formatter._fmt
                dtfmt = handler.formatter.datefmt
                self.__og_fmts.append([fmt,dtfmt])
                fmt = self.__remove_custom_format_attributes(fmt)
                handler.setFormatter(logging.Formatter(fmt=fmt, datefmt=dtfmt))
        else:
            for i, handler in enumerate(eff_handlers):
                fmt = self.__og_fmts[i][0]
                dtfmt = self.__og_fmts[i][1]
                self.__og_fmts.remove([fmt,dtfmt])
                handler.setFormatter(logging.Formatter(fmt=fmt, datefmt=dtfmt))
            self.__og_fmts = []

    def __remove_custom_format_attributes(self, fmt) -> str:
        """
        Match and remove custom format attributes which are not required for this logging call
        """
        # Regex to match all format attributes ex. %(name)s
        regex = r"[^ :]*%\(([a-zA-Z_]+)\)[-+]*[0-9]{0,2}[sd]{1}[^ :]*"
        # Regex to dynamically match custom attributes. Replace ==attrib== with attribute name before matching
        dyregex = r"[^ :]*%\(==attrib==\)[-+]*[0-9]{0,2}[sd]{1}[^ :]*"
        # Standard format attributes. Update this list if it is updated in logging module as well.
        st = ['name','levelno', 'levelname', 'pathname','filename','module', "lineno", "funcName", "created", "asctime", "msecs", "relativeCreated", "thread", "threadName", "process", "message"]
        attribs = re.findall(regex,fmt)
        attributes_to_be_removed = set()
        # Find out attributes to be removed by looking at the standard attributes list st and keys in self.__extras
        # If the attribute is not present in both, add to remove list
        for f in attribs:
            if f not in st and f not in self.__extras:
                attributes_to_be_removed.add(f)
        # Remove the attribs found above from the formatter
        for ff in attributes_to_be_removed:
            reg = re.sub("==attrib==",ff,dyregex)
            fmt = re.sub(reg,"",fmt)
        fmt = re.sub(" +"," ",fmt) # remove any additional spaces
        return fmt

    def __set_up_extras(self, fields, kwfields, args, kwargs) -> None:
        # Set-up custom fields (extras) for positional arguments
        extras = {}
        for f in fields:
            ef = self.__extract_field(f,args=args, kwargs=kwargs)
            if ef is not None:
                extras[f] = ef
        # Set-up custom fields (extras) for keyword arguments
        for f in kwfields:
            ef = self.__extract_field(kwfields[f], args=args, kwargs=kwargs)
            if ef is not None:
                extras[f] = f"{f}:{ef}"
        if extras:
            self.__extras = extras
        else:
            self.__extras = {}

    def __extract_field(self, field: str, args, kwargs) -> str:
        """
        Extract field from *args & **kwargs. Following happens:
        - If field contains a ".", it is split with "."
        - The first part of the resultant list is checked 
            + If it is a number, then it represents positional argument and respective value is returned if present
            + If it is a string, then it represents keyword argument. Respective keyword value is extracted if key is present
            + If value is a dict or has a dict() method, then it is further expanded
        - All subsequent parts after "." are treated as keys of sub-dict and traversed till the end
        - The function doesn't throw any error. If a field is not present, it is simply ignored
        """
        # If the field contains a "." that means it is an Object which is a dictionary or needs to be converted to a dictionary (like pydantic model)
        # The first field (i.e one before the ".") is the name of the Object while subsequent fields are either value or a key (in case of nested dictionary)
        fields = str(field).split(".")
        if len(fields) == 1: # not a dictionary, just return the value from kwargs
            if str(field).isnumeric():
                return args[field] if int(field) < len(args) else None
            return kwargs.get(field) if kwargs.get(field) else None
        # Check if first part of list is a numeric value
        if str(fields[0]).isnumeric():
            d = args[int(fields[0])] if int(fields[0]) < len(args) else {}
        else:
            # At this point, the field is an Object 
            d = kwargs.get(fields[0],{}) # if field not found in kwargs, return empty dict
        # Check if d is of type dict or has a method of type dict
        if isinstance(d,dict) or hasattr(d,'dict'):
            if hasattr(d,'dict'):
                d = d.dict()
        else:
            # Resultant object is neither a dict nor does it have a method dict"
            return None
        # Traverse the dict to get the final value            
        for i in range(1,len(fields)):
            d = d.get(fields[i],{})
        return d if d else None
