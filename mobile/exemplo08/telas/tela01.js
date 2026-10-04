import { FlatList, Text, View } from "react-native";
import CabecalhoTela from "../components/CabecalhoTela";
import styles from "../style/estilo";

const dados = Array.from({ length: 100 }, (_, index) => ({
  id: String(index + 1),
  valor: index + 1,
}));

export default function FlatListExemplo({ voltaPara }) {
  return (
    <View style={styles.container}>
      <CabecalhoTela
        titulo="FlatList"
        subtitulo="Renderização eficiente e sob demanda"
        voltaPara={voltaPara}
      />

      <FlatList
        data={dados}
        keyExtractor={(item) => item.id}
        contentContainerStyle={styles.listContent}
        renderItem={({ item }) => (
          <View style={styles.itemCard}>
            <Text style={styles.itemNumber}>{item.valor}</Text>
            <Text style={styles.item}>Item da lista #{item.valor}</Text>
          </View>
        )}
      />
    </View>
  );
}
