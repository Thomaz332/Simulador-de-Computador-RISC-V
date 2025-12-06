• Simulador-de-Computador-RISC-V •

Um simulador da arquitetura RISC-V, desenvolvido em Python, com foco em demonstrar o funcionamento básico de um computador: CPU, memória, barramento e dispositivos de I/O.

• Objetivo do Projeto

O propósito deste simulador é fornecer uma implementação simples e didática de um computador RISC-V. Ele permite visualizar:

• Como uma CPU RISC-V processa instruções

• Como a memória e o barramento interagem com a CPU

• Como funciona o fluxo de execução de um programa

• Como dispositivos de entrada e saída são manipulados

Este projeto é voltado principalmente para fins acadêmicos e de aprendizado.

Estrutura do Projeto:
├── bus.py
├── cpu.py
├── io_device.py
├── main.py
├── memory.py

--------------------------------------

cpu.py

Implementa o núcleo da CPU RISC-V, responsável por:

• Buscar instruções na memória (fetch)

• Decodificar instruções

• Executar operações aritméticas e lógicas

• Manipular registradores

• Controlar o fluxo de execução

--------------------------------------

memory.py

• Gerencia a memória RAM simulada, incluindo:

• Leitura e escrita de bytes/words

• Armazenamento do programa carregado

• Endereçamento básico

--------------------------------------

bus.py

Simula o barramento que conecta CPU, memória e dispositivos I/O, permitindo:

• Roteamento de dados entre os componentes

• Comunicação centralizada no modelo de computador

--------------------------------------

io_device.py

Define um dispositivo simples de entrada/saída, possibilitando:

• Escrita em dispositivos externos simulados

• Leitura de dados básicos

--------------------------------------

main.py

Ponto de entrada do simulador. Ele:

• Inicializa CPU, barramento, memória e dispositivos

• Carrega o programa na memória

• Inicia o ciclo de execução da CPU

--------------------------------------

Como Funciona o Ciclo de Execução:

Fetch – CPU busca a instrução na memória

Decode – Instrução é decodificada

Execute – A operação é realizada (ADD, LOAD, STORE etc.)

A CPU usa o barramento para acessar memória/I-O
O Program Counter é atualizado
O ciclo se repete até o fim do programa

Esse é o ciclo clássico fetch → decode → execute.
