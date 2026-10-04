import { SectionList, Text, View } from "react-native";
import CabecalhoTela from "../components/CabecalhoTela";
import styles from "../style/estilo";

const dados = [
  { plataforma: "Xbox", data: ["Halo", "Forza", "Gears of War"] },
  { plataforma: "PlayStation", data: ["God of War", "Spider-Man", "Uncharted"] },
  { plataforma: "Nintendo Switch", data: ["Zelda", "Metroid", "Mario"] },
  { plataforma: "PC", data: ["Crusader Kings III", "Baldur's Gate 3", "Mount & Blade II"] },
  { plataforma: "Multiplataforma", data: ["Tekken 8", "Metal Gear Solid"] },
];

export default function SectionListExemplo({ voltaPara }) {
  return (
    <View style={styles.container}>
      <CabecalhoTela
        titulo="SectionList"
        subtitulo="Itens organizados por categoria"
        voltaPara={voltaPara}
      />

      <SectionList
        sections={dados}
        keyExtractor={(item, index) => `${item}-${index}`}
        contentContainerStyle={styles.listContent}
        stickySectionHeadersEnabled
        renderSectionHeader={({ section }) => (
          <Text style={styles.sectionHeader}>{section.plataforma}</Text>
        )}
        renderItem={({ item }) => (
          <View style={styles.sectionItem}>
            <Text style={styles.sectionItemText}>{item}</Text>
          </View>
        )}
      />
    </View>
  );
}
