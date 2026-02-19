Este guia apresenta uma estrutura detalhada para o seu arquivo `README.md`, organizando as informações dos arquivos fornecidos para que qualquer pessoa (ou você mesmo no futuro) entenda como o sistema de monitoramento funciona, desde o script local até a hospedagem na nuvem.

---

# 📋 Documentação do Projeto: Sistema de Monitoramento Remoto

Este projeto consiste em um sistema de captura de teclas (**Keylogger**) que envia os dados em tempo real para um servidor **Flask** hospedado na nuvem (Render).

## 🏗️ Estrutura do Projeto

* **`keylogger.py`**: O script cliente que captura as teclas e gerencia o envio assíncrono para o servidor.
* 
**`app.py`**: O servidor web (API) que recebe e exibe os logs.


* 
**`requirements.txt`**: Lista de dependências necessárias para o servidor rodar no ambiente de produção.


* 
**`key.bat`**: Script de automação para Windows que instala as bibliotecas e inicia o monitoramento local.



---

## 🚀 Como Configurar o Servidor (Nuvem)

Para manter o monitoramento ativo 24h por dia, recomenda-se o uso da plataforma **Render**.

### 1. Preparação

O servidor utiliza **Flask** para a rota de recebimento e **Gunicorn** como servidor HTTP de produção.

* 
**Arquivo de dependências**: `requirements.txt` deve conter `flask` e `gunicorn`.


* 
**Porta dinâmica**: O servidor está configurado para ler a porta da variável de ambiente `PORT`, garantindo compatibilidade com a nuvem.



### 2. Deploy no Render

1. Suba os arquivos `app.py` e `requirements.txt` para um repositório no GitHub.


2. No painel do Render, crie um novo **Web Service** conectado ao seu repositório.


3. 
**Comando de Inicialização (Start Command)**: `gunicorn app:app`.


4. Copie a URL gerada (ex: `https://seu-app.onrender.com`).



---

## 💻 Como Configurar o Cliente (`keylogger.py`)

O cliente captura as teclas e utiliza uma **Thread** separada para enviar os dados, garantindo que o programa não trave caso a internet oscile ou o servidor demore a responder.

### 1. Configuração de URL

No topo do arquivo `keylogger.py`, atualize a variável global:

```python
SERVER_URL = "https://sua-url-aqui.onrender.com/receber_dados"

```



### 2. Execução Rápida (Windows)

Basta executar o arquivo `key.bat`. Ele realizará os seguintes passos automaticamente:

* Instala as bibliotecas `pynput` e `requests` silenciosamente.


* Inicia o script de monitoramento.



---

## 🛠️ Detalhes Técnicos do Cliente

| Recurso | Descrição |
| --- | --- |
| **Captura** | Utiliza a biblioteca `pynput` para escutar eventos do teclado. |
| **Buffer** | Armazena as teclas em uma variável global (`buffer_nuvem`) para evitar perda de dados. |
| **Envio Assíncrono** | Uma thread secundária tenta enviar os dados a cada 5 segundos. |
| **Tratamento de Erros** | Se o servidor estiver "dormindo" (comum no plano gratuito do Render), o script aguarda sem interromper a captura. |

---

## 🛡️ Considerações de Segurança e Persistência

* **Autenticação**: Atualmente, a URL é pública. É recomendável adicionar uma **Chave de API** nos headers para validar a origem dos dados.


* **Armazenamento**: O servidor atual apenas imprime os logs no console do Render. Para persistência a longo prazo, deve-se integrar um banco de dados como **MongoDB** ou **Supabase**.


* 
**Limitação da Nuvem**: No plano gratuito do Render, a instância pode demorar alguns segundos para "acordar" após períodos de inatividade.

