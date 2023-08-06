#!/usr/bin/env python3
# -*- coding: utf-8 -*-





from .source import (par_scr,rep_kmeans2,rep_swkmeans,kmeans,swkmeans,swkmeans_app,justify,bic_run)
from .util import (gen_beta_nonoverlap,gen_var_nonoverlap,gen_beta_overlap,gen_var_overlap,
                   sse_calculate_hard,sse_calculate_soft,rmse_multi_hard,rmse_multi_soft)

name = 'heteroverlap'

__version__ = '0.0.3'
VERSION = __version__

__all__ = ['par_scr',
           'rep_kmeans2',
           'rep_swkmeans',
           'kmeans',
           'swkmeans',
           'swkmeans_app',
           'justify',
           'bic_run',
           'gen_beta_nonoverlap',
           'gen_var_nonoverlap',
           'gen_beta_overlap',
           'gen_var_overlap',
           'sse_calculate_hard',
           'sse_calculate_soft',
           'rmse_multi_hard',
           'rmse_multi_soft'
    ]
