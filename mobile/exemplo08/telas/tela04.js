import { useState } from "react";
import { ScrollView, Text, useWindowDimensions, View } from "react-native";
import CabecalhoTela from "../components/CabecalhoTela";
import styles from "../style/estilo";

const paginas = [
  {
    cor: "#2563EB",
    tag: "Interface",
    titulo: "Página responsiva",
    texto: "A largura agora acompanha o dispositivo, sem depender de um valor fixo como 400 pixels.",
  },
  {
    cor: "#7C3AED",
    tag: "Interação",
    titulo: "Paging nativo",
    texto: "O pagingEnabled faz cada página encaixar naturalmente durante o gesto horizontal.",
  },
  {
    cor: "#0F766E",
    tag: "Estado",
    titulo: "Página atual",
    texto: "O estado muda após a rolagem e atualiza os indicadores logo abaixo do carrossel.",
  },
];

export default function CarouselExemplo({ voltaPara }) {
  const [paginaAtual, setPaginaAtual] = useState(0);
  const { width } = useWindowDimensions();

  const handlePageChange = (event) => {
    const offset = event.nativeEvent.contentOffset.x;
    setPaginaAtual(Math.round(offset / width));
  };

  return (
    <View style={styles.carouselContainer}>
      <CabecalhoTela
        titulo="Carrossel"
        subtitulo="ScrollView horizontal com largura responsiva"
        voltaPara={voltaPara}
      />

      <ScrollView
        horizontal
        pagingEnabled
        showsHorizontalScrollIndicator={false}
        onMomentumScrollEnd={handlePageChange}
        style={styles.carouselViewport}
      >
        {paginas.map((pagina) => (
          <View key={pagina.titulo} style={[styles.page, { width }]}> 
            <View style={[styles.carouselCard, { backgroundColor: pagina.cor }]}> 
              <Text style={styles.carouselTag}>{pagina.tag}</Text>
              <Text style={styles.carouselTitle}>{pagina.titulo}</Text>
              <Text style={styles.carouselText}>{pagina.texto}</Text>
            </View>
          </View>
        ))}
      </ScrollView>

      <View style={styles.dots}>
        {paginas.map((pagina, index) => (
          <View
            key={pagina.titulo}
            style={[styles.dot, index === paginaAtual && styles.dotActive]}
          />
        ))}
      </View>
    </View>
  );
}
