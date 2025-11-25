import threading
import time

class RecursoOtimista:
    def __init__(self):
        self.valor = 0
        self.versao = 0
        self.lock = threading.Lock()  # usado apenas para ler/escrever com segurança

    def incrementar(self):
        while True:
            # Leitura protegida
            with self.lock:
                versao_atual = self.versao
                valor_local = self.valor

            print(f"{threading.current_thread().name} leu valor {valor_local} (versão {versao_atual})")

            # Simula processamento independente
            time.sleep(0.3)

            valor_local += 1  # prepara nova versão

            # Tenta salvar (lock otimista: só grava se ninguém mexeu)
            with self.lock:
                if versao_atual == self.versao:
                    self.valor = valor_local
                    self.versao += 1
                    print(f"{threading.current_thread().name} atualizou para {self.valor} (nova versão {self.versao})")
                    break
                else:
                    print(f"{threading.current_thread().name} falhou (versão mudou). Tentando novamente...")

if __name__ == "__main__":
    recurso = RecursoOtimista()
    threads = []

    # Três threads tentando atualizar simultaneamente
    for i in range(3):
        t = threading.Thread(target=recurso.incrementar, name=f"Worker-{i+1}")
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"\nValor final do recurso (otimista): {recurso.valor}")
