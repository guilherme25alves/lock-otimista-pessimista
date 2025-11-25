import threading
import time

# Recurso compartilhado
contador = 0

# Lock pessimista
lock = threading.Lock()

def incrementar():
    global contador
    for _ in range(3):
        # Bloqueio explícito para garantir acesso exclusivo
        with lock:
            valor_atual = contador
            print(f"{threading.current_thread().name} leu o valor {valor_atual}")
            time.sleep(0.5)  # simula alguma operação lenta
            contador = valor_atual + 1
            print(f"{threading.current_thread().name} atualizou para {contador}")

        # Fora do bloco 'with', o lock é liberado
        time.sleep(0.1)

if __name__ == "__main__":
    threads = []

    # Criamos 2 threads para disputar o recurso
    for i in range(2):
        t = threading.Thread(target=incrementar, name=f"Thread-{i+1}")
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"\nValor final do contador (pessimista): {contador}")
