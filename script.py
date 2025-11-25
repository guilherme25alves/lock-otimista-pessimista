# Lock Example in Python

import threading
import time

# Lock Pessimistic Example
lock = threading.Lock()
shared_resource = 0

def pessimistic_worker():
    # O Lock pessimista é usado para garantir que apenas uma thread possa acessar o recurso compartilhado por vez.
    # Isso evita condições de corrida, mas pode levar a bloqueios se uma thread demorar muito para liberar o lock.
    # Aqui, usamos o lock para proteger o acesso ao recurso compartilhado.
    # Note que o lock é adquirido antes de acessar o recurso e liberado automaticamente ao sair do bloco with.
    # Isso garante que o recurso seja acessado de forma segura.
    global shared_resource
    with lock:
        print(f"{threading.current_thread().name} acquired the lock.")
        local_copy = shared_resource
        time.sleep(1)  # Simulate some processing
        local_copy += 1
        shared_resource = local_copy
        print(f"{threading.current_thread().name} released the lock.")

# Lock Optimistic Example
class OptimisticLock:
    # O Lock otimista permite que múltiplas threads acessem o recurso compartilhado simultaneamente.
    # Cada thread trabalha com uma cópia local do recurso e, ao tentar salvar as alterações
    # de volta ao recurso compartilhado, verifica se o recurso foi modificado por outra thread.
    # Se o recurso foi modificado, a thread descarta suas alterações e tenta novamente.
    # Isso pode levar a menos bloqueios e maior concorrência, mas pode resultar em mais tentativas.    
    def __init__(self):
        self.value = 0
        self.version = 0
        self.lock = threading.Lock()

    def increment(self):
        while True:
            with self.lock:
                print(f"{threading.current_thread().name} reading value.")
                current_version = self.version
                local_copy = self.value

            time.sleep(0.1)  # Simulate some processing

            local_copy += 1

            with self.lock:
                if current_version == self.version:
                    print(f"{threading.current_thread().name} updating value.")
                    self.value = local_copy
                    self.version += 1
                    return


if __name__ == "__main__":
    # Pessimistic Locking Example
    threads = []
    for i in range(5):
        t = threading.Thread(target=pessimistic_worker, name=f"PessimisticWorker-{i+1}")
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"Final shared resource value (Pessimistic): {shared_resource}")

    # Optimistic Locking Example
    optimistic_lock = OptimisticLock()
    threads = []
    for i in range(5):
        t = threading.Thread(target=optimistic_lock.increment, name=f"OptimisticWorker-{i+1}")
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"Final shared resource value (Optimistic): {optimistic_lock.value}")

    # Diferença entre Lock Pessimista e Otimista:

    # O Lock pessimista bloqueia o acesso ao recurso compartilhado, garantindo que apenas uma thread possa acessá-lo por vez.
    # Isso é útil quando há alta contenção pelo recurso.
    
    # O Lock otimista permite acesso simultâneo ao recurso, mas verifica se houve modificações antes de salvar as alterações.
    # Isso é útil quando a contenção pelo recurso é baixa, permitindo maior concorrência.
