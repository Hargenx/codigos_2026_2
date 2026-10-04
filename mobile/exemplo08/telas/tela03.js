import { ScrollView, Text, View } from "react-native";
import CabecalhoTela from "../components/CabecalhoTela";
import styles from "../style/estilo";

const dados = Array.from({ length: 80 }, (_, index) => `Conteúdo ${index + 1}`);

export default function ScrollViewExemplo({ voltaPara }) {
  return (
    <View style={styles.container}>
      <CabecalhoTela
        titulo="ScrollView"
        subtitulo="Todos os elementos são renderizados de uma vez"
        voltaPara={voltaPara}
      />

      <ScrollView contentContainerStyle={styles.scrollContent}>
        {dados.map((item) => (
          <View style={styles.scrollItem} key={item}>
            <Text style={styles.item}>{item}</Text>
          </View>
        ))}
      </ScrollView>
    </View>
  );
}
