
# Sistema de Controle de Presença Escolar

Aplicação web desenvolvida com **Python, Flask, SQLite, HTML e CSS**, criada para facilitar o cadastro de alunos, o registro de frequência escolar e a consulta de relatórios.

## Funcionalidades

- Cadastro e gerenciamento de alunos.
- Registro de presença, ausência e falta justificada.
- Organização das chamadas por turma e data.
- Consulta de registros de frequência.
- Visualização de relatórios de presença e ausência.
- Armazenamento dos dados em banco de dados SQLite.

## Requisitos

- Python 3.10 ou superior (recomendado).
- pip (gerenciador de pacotes Python).
- Navegador web atualizado.

## Instalação

### Windows (PowerShell ou Prompt de Comando)

1. Abra o terminal na pasta do projeto.
2. Crie um ambiente virtual:

   ```bash
   python -m venv .venv
   ```

3. Ative o ambiente virtual:

   ```bash
   .venv\Scripts\activate
   ```

4. Instale as dependências:

   ```bash
   python -m pip install -r requirements.txt
   ```

5. Execute a aplicação:

   ```bash
   python app.py
   ```

### Linux

1. Abra o terminal na pasta do projeto.
2. Crie um ambiente virtual:

   ```bash
   python3 -m venv .venv
   ```

3. Ative o ambiente virtual:

   ```bash
   source .venv/bin/activate
   ```

4. Instale as dependências:

   ```bash
   python -m pip install -r requirements.txt
   ```

5. Execute a aplicação:

   ```bash
   python app.py
   ```

## Como acessar o sistema

Após iniciar a aplicação, consulte o endereço exibido no terminal. Se estiver utilizando a configuração padrão do Flask, abra o navegador e acesse:

```text
http://127.0.0.1:5000
```

Mantenha o terminal aberto enquanto estiver utilizando o sistema.

## Como utilizar

### 1. Cadastrar alunos

Acesse a área de cadastro e informe os dados solicitados para adicionar os estudantes ao sistema.

### 2. Registrar a frequência

Selecione a turma e a data da aula. Em seguida, marque a situação de cada aluno como presente, ausente ou justificado, conforme as opções disponíveis.

### 3. Salvar a chamada

Confirme o registro para armazenar as informações no banco de dados.

### 4. Consultar relatórios

Utilize a área de consulta para verificar os registros de frequência e acompanhar a participação dos estudantes, conforme os recursos disponíveis na aplicação.

### 5. Acompanhar as faltas

Consulte os registros para identificar alunos com frequência baixa e auxiliar no acompanhamento escolar.

## Banco de dados

O sistema utiliza **SQLite** para armazenar os dados. Dependendo da configuração do projeto, o arquivo do banco de dados pode ser criado automaticamente durante a execução.

Recomenda-se realizar cópias de segurança periódicas para evitar a perda de informações.

## Solução de problemas

- **Python não encontrado:** verifique se o Python está instalado e disponível no PATH.
- **Erro ao instalar dependências:** confirme que o arquivo `requirements.txt` está na pasta do projeto e tente atualizar o pip.
- **Erro ao executar `app.py`:** confira se o ambiente virtual está ativado e se todas as dependências foram instaladas.
- **Página não abre:** verifique se a aplicação está em execução e se está utilizando o endereço correto indicado no terminal.

## Segurança e privacidade

- Utilize dados fictícios durante os testes.
- Restrinja o acesso a pessoas autorizadas.
- Proteja os dados pessoais dos alunos.
- Antes de disponibilizar o sistema publicamente, implemente autenticação, controle de acesso e medidas adicionais de segurança.

## Tecnologias utilizadas

- **Python:** lógica e processamento da aplicação.
- **Flask:** framework web.
- **SQLite:** banco de dados.
- **HTML:** estrutura das páginas.
- **CSS:** apresentação visual.

## Autor

[Luiz Paulo Dutra Perira]

## Licença





