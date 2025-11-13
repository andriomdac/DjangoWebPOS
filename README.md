# Projeto Django Web POS

Este repositório contém um projeto desenvolvido com **Django**.  
Abaixo estão as instruções para configurar o ambiente, preparar o banco de dados e iniciar o servidor local.

---

## 🚀 Configuração do Ambiente

### 1. Criar o ambiente virtual
```bash
python3 -m venv venv
```

### 2. Ativar o ambiente virtual
**Linux/Mac:**
```bash
source venv/bin/activate
```
**Windows:**
```bash
venv\Scripts\activate
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

---

## 🗃️ Banco de Dados

### 4. Criar as migrações
```bash
python3 manage.py makemigrations
```

### 5. Aplicar as migrações
```bash
python3 manage.py migrate
```

---

## 🖥️ Executar o Servidor

### 6. Iniciar o servidor local
```bash
python3 manage.py runserver
```

Acesse o projeto em:  
**http://127.0.0.1:8000/**

---

## 🖼️ Screenshots

| Tela | Imagem |
|------|--------|
| Página 1 | ![Screenshot_2025-08-12_20-27-22](https://github.com/user-attachments/assets/9be1e60d-6775-4e3a-8c7a-3dfbf158c67a) |
| Página 2 | ![Screenshot_2025-08-12_20-22-10](https://github.com/user-attachments/assets/1bcc8a13-2878-4466-8976-a8151f1ac41f) |
| Página 3 | ![Screenshot_2025-08-12_20-23-51](https://github.com/user-attachments/assets/4318c34b-2b91-4785-9afe-12ea0e4f9e61) |
| Página 4 | ![Screenshot_2025-08-12_20-25-39](https://github.com/user-attachments/assets/c70d1bf3-f880-4c4b-a44c-a02505787c27) |
| Página 5 | ![image](https://github.com/user-attachments/assets/6fc87f47-bb95-49cc-8a07-cf49a97ea0f9) |

---

## ⚙️ Tecnologias Utilizadas
- Python 3
- Django
- SQLite
- HTML/CSS
- Bootstrap 5

---

## 📄 Licença
Este projeto é de uso livre para estudo e desenvolvimento.
