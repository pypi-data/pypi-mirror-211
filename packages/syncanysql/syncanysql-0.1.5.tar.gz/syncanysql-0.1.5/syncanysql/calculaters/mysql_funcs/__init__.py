# -*- coding: utf-8 -*-
# 2023/3/2
# create by: snower

from . import number_funcs
from . import string_funcs
from . import datetime_funcs
from . import logical_funcs
from . import json_funcs

funcs = {}
funcs.update(number_funcs.funcs)
funcs.update(string_funcs.funcs)
funcs.update(datetime_funcs.funcs)
funcs.update(logical_funcs.funcs)
funcs.update(json_funcs.funcs)