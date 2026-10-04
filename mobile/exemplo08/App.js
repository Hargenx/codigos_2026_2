import { useState } from "react";
import { Pressable, SafeAreaView, ScrollView, Text, View } from "react-native";
import { StatusBar } from "expo-status-bar";
import { Ionicons } from "@expo/vector-icons";
import Tela01 from "./telas/tela01";
import Tela02 from "./telas/tela02";
import Tela03 from "./telas/tela03";
import Tela04 from "./telas/tela04";
import Tela05 from "./telas/tela05";
import Tela06 from "./telas/tela06";
import styles, { cores } from "./style/estilo";

const opcoes = [
  {
    tela: "Tela01",
    titulo: "FlatList",
    descricao: "Lista eficiente para grandes quantidades de dados.",
    icone: "list-outline",
  },
  {
    tela: "Tela02",
    titulo: "SectionList",
    descricao: "Dados agrupados em seções com cabeçalhos.",
    icone: "albums-outline",
  },
  {
    tela: "Tela03",
    titulo: "ScrollView",
    descricao: "Conteúdo rolável renderizado de uma só vez.",
    icone: "swap-vertical-outline",
  },
  {
    tela: "Tela04",
    titulo: "Carrossel",
    descricao: "Paginação horizontal responsiva com ScrollView.",
    icone: "images-outline",
  },
  {
    tela: "Tela05",
    titulo: "Dashboard",
    descricao: "Cards, indicadores e composição de uma tela moderna.",
    icone: "grid-outline",
  },
  {
    tela: "Tela06",
    titulo: "Formulário",
    descricao: "Inputs controlados, validação simples e feedback visual.",
    icone: "create-outline",
  },
];

export default function App() {
  const [telaAtual, setTelaAtual] = useState(null);

  const navegaParaTela = (nomeTela) => {
    setTelaAtual(nomeTela);
  };

  const voltarAoMenu = () => setTelaAtual(null);

  const desenhaTela = () => {
    switch (telaAtual) {
      case "Tela01":
        return <Tela01 voltaPara={voltarAoMenu} />;
      case "Tela02":
        return <Tela02 voltaPara={voltarAoMenu} />;
      case "Tela03":
        return <Tela03 voltaPara={voltarAoMenu} />;
      case "Tela04":
        return <Tela04 voltaPara={voltarAoMenu} />;
      case "Tela05":
        return <Tela05 voltaPara={voltarAoMenu} />;
      case "Tela06":
        return <Tela06 voltaPara={voltarAoMenu} />;
      default:
        return (
          <SafeAreaView style={styles.safeArea}>
            <ScrollView contentContainerStyle={styles.content}>
              <View style={styles.hero}>
                <Text style={styles.eyebrow}>React Native • Exemplo 08</Text>
                <Text style={styles.title}>Interfaces e listas</Text>
                <Text style={styles.subtitle}>
                  Exemplos curtos para comparar componentes de interface mantendo a navegação manual com estado e switch.
                </Text>
              </View>

              <View style={styles.menuGrid}>
                {opcoes.map((opcao) => (
                  <Pressable
                    key={opcao.tela}
                    onPress={() => navegaParaTela(opcao.tela)}
                    style={({ pressed }) => [
                      styles.menuCard,
                      pressed && styles.menuCardPressed,
                    ]}
                  >
                    <View style={styles.menuIcon}>
                      <Ionicons name={opcao.icone} size={24} color={cores.primaria} />
                    </View>

                    <View style={styles.menuText}>
                      <Text style={styles.menuTitle}>{opcao.titulo}</Text>
                      <Text style={styles.menuDescription}>{opcao.descricao}</Text>
                    </View>

                    <Ionicons name="chevron-forward" size={20} color={cores.textoSecundario} />
                  </Pressable>
                ))}
              </View>
            </ScrollView>
          </SafeAreaView>
        );
    }
  };

  return (
    <View style={styles.app}>
      <StatusBar style="dark" />
      {desenhaTela()}
    </View>
  );
}
