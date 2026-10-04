# Exemplo 08 — Interfaces e Listas com React Native

Projeto desenvolvido com **React Native + Expo** com finalidade **exclusivamente didática**, pensado para uso em sala de aula durante o ensino de desenvolvimento mobile.

O objetivo deste projeto é apresentar diferentes formas de construir interfaces, exibir listas, trabalhar com componentes visuais e controlar a renderização de telas utilizando recursos básicos do React Native.

> Este projeto prioriza clareza e aprendizado. Algumas decisões foram mantidas propositalmente simples para facilitar a compreensão dos conceitos pelos alunos.

---

## Objetivos de aprendizagem

Ao utilizar este projeto, o aluno poderá praticar conceitos como:

- criação de componentes em React Native;
- organização de interfaces com `View`, `Text` e `Pressable`;
- uso de `ScrollView`;
- uso de `FlatList`;
- uso de `SectionList`;
- criação de carrossel horizontal;
- controle de estado com `useState`;
- uso de `TextInput`;
- criação de formulários controlados;
- composição de interfaces;
- reutilização de componentes;
- aplicação de estilos com `StyleSheet`;
- criação de interfaces responsivas;
- renderização condicional;
- navegação simples utilizando estado e `switch`.

---

## Navegação do projeto

Este exemplo **não utiliza React Navigation propositalmente**.

A troca entre as telas é feita utilizando um estado:

```js
const [telaAtual, setTelaAtual] = useState(null);
```

e um `switch` responsável por decidir qual componente será renderizado:

```js
switch (telaAtual) {
  case "Tela01":
    return <Tela01 voltaPara={voltarAoMenu} />;

  case "Tela02":
    return <Tela02 voltaPara={voltarAoMenu} />;

  default:
    return <Menu />;
}
```

Essa abordagem foi escolhida com finalidade didática.

Antes de apresentar bibliotecas completas de navegação, o aluno consegue observar diretamente a relação entre:

```text
Evento
   ↓
setState()
   ↓
Mudança do estado
   ↓
Nova renderização
   ↓
Componente exibido
```

Isso ajuda a compreender melhor o funcionamento do React antes da introdução de abstrações adicionais.

---

## Exemplos disponíveis

## 1. FlatList

Demonstra o uso do componente:

```js
<FlatList />
```

O `FlatList` é recomendado para exibição de listas maiores, pois renderiza os elementos de forma otimizada.

Entre os conceitos trabalhados estão:

- `data`;
- `renderItem`;
- `keyExtractor`;
- componentes reutilizáveis;
- renderização eficiente de listas.

### Discussão em sala

Uma comparação importante pode ser feita entre:

```text
ScrollView
```

e:

```text
FlatList
```

O `ScrollView` renderiza todos os seus elementos de uma vez, enquanto o `FlatList` possui mecanismos de virtualização e renderiza apenas os itens necessários.

---

## 2. SectionList

Demonstra a organização de dados em grupos utilizando:

```js
<SectionList />
```

O exemplo utiliza jogos separados por plataforma.

Esse componente permite trabalhar conceitos como:

- agrupamento de dados;
- cabeçalhos de seção;
- `renderSectionHeader`;
- `renderItem`;
- estruturação de objetos e arrays.

Exemplo de estrutura:

```js
const dados = [
  {
    title: "PlayStation",
    data: ["God of War", "The Last of Us"],
  },
  {
    title: "Nintendo",
    data: ["Mario", "Zelda"],
  },
];
```

---

## 3. ScrollView

Demonstra o funcionamento de:

```js
<ScrollView />
```

O objetivo principal desse exemplo é mostrar uma interface com conteúdo maior do que o espaço disponível na tela.

Também permite discutir uma questão importante:

> Quando utilizar `ScrollView` e quando utilizar `FlatList`?

Para pequenas quantidades de conteúdo, `ScrollView` pode ser suficiente.

Para listas grandes ou dinâmicas, normalmente é preferível utilizar `FlatList`.

---

## 4. Carrossel

O projeto apresenta um carrossel criado utilizando:

```js
<ScrollView
  horizontal
  pagingEnabled
/>
```

O exemplo trabalha conceitos como:

- rolagem horizontal;
- paginação;
- eventos de scroll;
- controle de índice;
- responsividade;
- indicadores de página.

A largura da interface é obtida dinamicamente utilizando:

```js
useWindowDimensions();
```

Isso evita valores fixos de largura e torna o exemplo adequado para diferentes tamanhos de dispositivos.

---

## 5. Dashboard

O exemplo de Dashboard foi criado para demonstrar como vários componentes simples podem ser combinados para formar uma interface com aparência mais próxima de uma aplicação real.

São utilizados elementos como:

- cards;
- indicadores;
- valores;
- títulos;
- organização em linhas;
- composição de componentes.

O objetivo não é criar um sistema completo de indicadores, mas demonstrar como uma interface pode ser dividida em pequenas unidades reutilizáveis.

---

## 6. Formulário

O exemplo de formulário apresenta conceitos importantes para aplicações mobile.

Entre eles:

- `TextInput`;
- `useState`;
- campos controlados;
- eventos;
- validação simples;
- botões utilizando `Pressable`.

Exemplo:

```js
const [nome, setNome] = useState("");
```

```js
<TextInput
  value={nome}
  onChangeText={setNome}
/>
```

O aluno pode observar diretamente a relação entre o conteúdo digitado e o estado do componente.

---

## Estrutura do projeto

Uma organização simplificada do projeto é:

```text
exemplo08/
│
├── App.js
│
├── package.json
│
├── telas/
│   ├── tela01.js
│   ├── tela02.js
│   ├── tela03.js
│   ├── tela04.js
│   ├── tela05.js
│   └── tela06.js
│
├── componentes/
│   └── ...
│
└── style/
    └── estilo.js
```

A separação em arquivos facilita a apresentação gradual dos conteúdos durante a aula.

---

## Tecnologias utilizadas

- JavaScript
- React
- React Native
- Expo
- Expo Vector Icons

---

## Pré-requisitos

Antes de executar o projeto, é recomendado possuir:

- Node.js;
- npm;
- Expo;
- Android Studio ou dispositivo físico com Expo Go.

Para verificar a instalação do Node:

```bash
node --version
```

e do npm:

```bash
npm --version
```

---

## Instalação

Após baixar ou clonar o projeto, entre na pasta:

```bash
cd exemplo08
```

Instale as dependências:

```bash
npm install
```

Caso seja necessário instalar os módulos relacionados aos recursos do Expo:

```bash
npx expo install expo-asset
```

---

## Executando o projeto

Para iniciar o servidor Expo:

```bash
npx expo start
```

Ou:

```bash
npm start
```

Para executar diretamente no Android:

```bash
npm run android
```

Também é possível utilizar:

```bash
npx expo start
```

e posteriormente selecionar o dispositivo desejado pelo menu do Expo.

---

## Problemas comuns

## Erro relacionado ao `expo-asset`

Caso apareça:

```text
Unable to resolve "expo-asset"
```

execute:

```bash
npx expo install expo-asset
```

Depois limpe o cache:

```bash
npx expo start -c
```

---

## Problemas de dependência

O Expo disponibiliza uma ferramenta para verificar o projeto:

```bash
npx expo-doctor
```

Ela identifica possíveis incompatibilidades entre as versões instaladas e o SDK utilizado.

---

## Atividades para os alunos

O projeto também pode ser utilizado como base para exercícios.

### Atividade 1

Modificar os dados exibidos pelo `FlatList`.

---

### Atividade 2

Adicionar uma nova categoria ao `SectionList`.

---

### Atividade 3

Adicionar uma nova página ao carrossel.

---

### Atividade 4

Criar um novo card no Dashboard.

---

### Atividade 5

Adicionar um campo de e-mail ao formulário.

---

### Atividade 6

Criar uma nova tela e adicioná-la ao `switch`.

Exemplo:

```js
case "Tela07":
  return <Tela07 voltaPara={voltarAoMenu} />;
```

Essa atividade ajuda a reforçar a relação entre componentes, estado e renderização condicional.

---

## Observação sobre arquitetura

Em aplicações profissionais maiores, normalmente seria utilizada uma solução específica para navegação, como:

```text
React Navigation
```

Entretanto, neste projeto a navegação foi mantida manualmente com `useState` e `switch` de forma intencional.

Isso permite visualizar claramente o funcionamento interno da aplicação antes de utilizar bibliotecas que abstraem esse comportamento.

Posteriormente, este mesmo projeto pode ser utilizado como ponto de partida para uma aula de:

- Stack Navigation;
- Tab Navigation;
- Drawer Navigation.

Assim, os alunos conseguem comparar uma implementação manual com uma implementação utilizando uma biblioteca de navegação.

---

## Finalidade educacional

Este projeto foi criado como **material de apoio para ensino de React Native em sala de aula**.

O código busca equilibrar:

- boas práticas;
- simplicidade;
- legibilidade;
- exemplos próximos de aplicações reais;
- facilidade de explicação durante a aula.

Nem todas as soluções apresentadas devem ser interpretadas como a arquitetura definitiva para aplicações profissionais.

Em alguns pontos, a implementação foi propositalmente simplificada para tornar os conceitos mais visíveis para alunos que ainda estão aprendendo React e React Native.

---

## Professor

- **Raphael Mauricio Sanches de Jesus**

Material desenvolvido para utilização em aulas de desenvolvimento mobile e programação com React Native.
