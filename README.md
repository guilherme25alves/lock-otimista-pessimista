# 🔐 Exemplos de Lock Pessimista e Otimista em Python

Este repositório apresenta um exemplo prático de **concorrência em Python**, demonstrando a diferença entre **Lock Pessimista** e **Lock Otimista** utilizando threads.  
O objetivo é ajudar a entender como cada abordagem lida com **recursos compartilhados** em contextos multithreaded.

---

## 📌 Conteúdo

- [Introdução](#introdução)
- [Lock Pessimista](#lock-pessimista)
- [Lock Otimista](#lock-otimista)
- [Como Executar](#como-executar)
- [Resumo das Diferenças](#resumo-das-diferenças)

---

## 🧠 Introdução

Quando múltiplas threads acessam e modificam um mesmo recurso, podem ocorrer **condições de corrida** (*race conditions*).  
Para evitar esses problemas, existem diferentes estratégias de sincronização.  
Este script apresenta duas delas:

- **Lock Pessimista (Pessimistic Locking)**
- **Lock Otimista (Optimistic Locking)**

---

## 🔒 Lock Pessimista

O **Lock Pessimista** assume que conflitos são prováveis.  
Portanto, ele **bloqueia o recurso** sempre que uma thread deseja acessá-lo.

### ✔️ Características:
- Apenas **uma thread por vez** acessa o recurso.  
- Evita conflitos de forma segura.  
- Pode causar **esperas longas** se uma thread demorar para liberar o lock.

### 🧩 Como funciona no código:
```python
with lock:
    # Apenas uma thread entra aqui por vez
    local_copy = shared_resource
    time.sleep(1)
    shared_resource = local_copy + 1
```

Aqui, o `with lock`: garante que apenas uma thread entra no bloco crítico de cada vez.

---

## 🚀 Lock Otimista

O **Lock Otimista** assume que conflitos são raros.
Ele permite que várias threads trabalhem simultaneamente, mas valida antes de gravar se o valor ainda é o mesmo.

### ✔️ Características

- Permite alta concorrência, especialmente em cenários com baixa contenção.
- Threads mantêm cópias locais do recurso.
- Antes de atualizar, verifica se ninguém alterou o valor.
- Em caso de conflito, a operação é **repetida**.

### 🧩 Como funciona no código:
```python
with self.lock:
    current_version = self.version
    local_copy = self.value

time.sleep(0.1)
local_copy += 1

with self.lock:
    if current_version == self.version:
        self.value = local_copy
        self.version += 1
```

Se outra thread tiver modificado o valor, a atualização não é aplicada e o loop tenta novamente.

---

## ▶️ Como Executar

1. Instale o Python 3.
2. Salve o arquivo como `main.py`.
3. Execute o comando:

```bash
python main.py
```

---

## ⚖️ Resumo das Diferenças

| Característica        | Lock Pessimista        | Lock Otimista          |
|-----------------------|-------------------------|-------------------------|
| **Filosofia**         | Conflitos são prováveis | Conflitos são raros     |
| **Acesso ao recurso** | Exclusivo               | Concorrente             |
| **Desempenho**        | Menor em alta contenção | Maior em baixa contenção |
| **Tentativas repetidas** | Não                  | Sim                     |
| **Complexidade**      | Baixa                   | Moderada                |
| **Ideal para**        | Alta contenção          | Baixa contenção         |

