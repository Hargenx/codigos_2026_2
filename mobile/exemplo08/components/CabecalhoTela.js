import { Pressable, Text, View } from "react-native";
import { Ionicons } from "@expo/vector-icons";
import styles, { cores } from "../style/estilo";

export default function CabecalhoTela({ titulo, subtitulo, voltaPara }) {
  return (
    <View style={styles.screenHeader}>
      <Pressable
        onPress={voltaPara}
        style={({ pressed }) => [styles.backButton, pressed && { opacity: 0.65 }]}
        accessibilityRole="button"
        accessibilityLabel="Voltar para o menu"
      >
        <Ionicons name="arrow-back" size={21} color={cores.texto} />
      </Pressable>

      <View style={styles.screenHeaderText}>
        <Text style={styles.screenTitle}>{titulo}</Text>
        {subtitulo ? <Text style={styles.screenSubtitle}>{subtitulo}</Text> : null}
      </View>
    </View>
  );
}
