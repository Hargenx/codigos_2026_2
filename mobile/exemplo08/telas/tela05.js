import { ScrollView, Text, View } from "react-native";
import { Ionicons } from "@expo/vector-icons";
import CabecalhoTela from "../components/CabecalhoTela";
import styles, { cores } from "../style/estilo";

const indicadores = [
  { rotulo: "Usuários", valor: "1.248", icone: "people-outline" },
  { rotulo: "Pedidos", valor: "386", icone: "bag-outline" },
  { rotulo: "Conversão", valor: "4,8%", icone: "trending-up-outline" },
  { rotulo: "Avaliação", valor: "4,9", icone: "star-outline" },
];

export default function DashboardExemplo({ voltaPara }) {
  return (
    <View style={styles.container}>
      <CabecalhoTela
        titulo="Dashboard"
        subtitulo="Composição de cards e indicadores"
        voltaPara={voltaPara}
      />

      <ScrollView contentContainerStyle={styles.scrollContent}>
        <View style={styles.dashboardGrid}>
          {indicadores.map((item) => (
            <View key={item.rotulo} style={styles.statCard}>
              <Ionicons name={item.icone} size={22} color={cores.primaria} />
              <Text style={styles.statValue}>{item.valor}</Text>
              <Text style={styles.statLabel}>{item.rotulo}</Text>
            </View>
          ))}
        </View>

        <View style={styles.panel}>
          <Text style={styles.panelTitle}>Meta mensal</Text>
          <View style={styles.progressTrack}>
            <View style={styles.progressFill} />
          </View>
          <Text style={[styles.menuDescription, { marginTop: 10 }]}>68% da meta atingida</Text>
        </View>

        <View style={styles.panel}>
          <Text style={styles.panelTitle}>Por que este exemplo?</Text>
          <Text style={styles.subtitle}>
            Ele mostra que uma interface moderna normalmente nasce da composição de Views simples, tipografia, espaçamento, bordas e hierarquia visual.
          </Text>
        </View>
      </ScrollView>
    </View>
  );
}
