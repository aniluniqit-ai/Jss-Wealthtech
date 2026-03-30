"""Auto Strategy Loader"""
import os, importlib

def load_all_strategies():
    strategies = {}
    base = os.path.dirname(os.path.abspath(__file__))
    
    try:
        from .multi_scalping import STRATEGY as S1
        strategies['multi_scalping'] = S1
    except: pass
    
    try:
        from .expiry_heropatla import STRATEGY as S2
        strategies['expiry_heropatla'] = S2
    except: pass
    
    try:
        from .momentum_follow import STRATEGY as S3
        strategies['momentum_follow'] = S3
    except: pass
    
    try:
        from .reversal_scalp import STRATEGY as S4
        strategies['reversal_scalp'] = S4
    except: pass
    
    for f in os.listdir(base):
        if f.endswith('.py') and f not in ['__init__.py', 'base_strategy.py']:
            name = f[:-3]
            if name not in strategies:
                try:
                    spec = importlib.util.spec_from_file_location(name, os.path.join(base, f))
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    if hasattr(mod, 'STRATEGY'):
                        strategies[name] = mod.STRATEGY
                except: pass
    
    return strategies