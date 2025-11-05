import time
from collections import defaultdict

_attempts = defaultdict(list)
BLOCK_TIME_SECONDS = 300  # 5 minutos
MAX_ATTEMPTS = 3
WINDOW_SECONDS = 300  # janela para contar tentativas

def register_attempt(ip: str):
    now = time.time()
    # limpa tentativas fora da janela
    _attempts[ip] = [t for t in _attempts[ip] if now - t <= WINDOW_SECONDS]
    _attempts[ip].append(now)

def is_blocked(ip: str) -> bool:
    now = time.time()
    tries = [t for t in _attempts[ip] if now - t <= WINDOW_SECONDS]
    if len(tries) >= MAX_ATTEMPTS:
        last = tries[-1]
        # se o último ocorreu dentro do período de bloqueio, está bloqueado
        if now - last <= BLOCK_TIME_SECONDS:
            return True
    return False

def reset_attempts(ip: str):
    if ip in _attempts:
        del _attempts[ip]
