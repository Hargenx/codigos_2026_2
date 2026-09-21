import React, { useEffect, useState } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  FlatList,
  SectionList,
  Image,
  StyleSheet,
} from "react-native";

export default function App() {
  // Hooks
  const [motorista, setMotorista] = useState("Raphael");
  const [observacao, setObservacao] = useState("");
  const [entregas, setEntregas] = useState([
    { id: "1", cliente: "Mercado Central", status: "Pendente" },
    { id: "2", cliente: "Farmácia Saúde", status: "Pendente" },
    { id: "3", cliente: "Loja Tech", status: "Entregue" },
    { id: "4", cliente: "Padaria Brasil", status: "Pendente" },
    { id: "5", cliente: "Livraria Saber", status: "Entregue" },
    { id: "6", cliente: "Supermercado Sul", status: "Pendente" },
    { id: "7", cliente: "Loja Mobile", status: "Pendente" },
    { id: "8", cliente: "Papelaria Rio", status: "Entregue" },
  ]);

  // useEffect: executa sempre que a lista de entregas mudar
  useEffect(() => {
    const totalEntregues = entregas.filter(
      (item) => item.status === "Entregue"
    ).length;

    console.log(`Entregas concluídas: ${totalEntregues}`);
  }, [entregas]);

  function confirmarEntrega(id) {
    const novaLista = entregas.map((entrega) =>
      entrega.id === id
        ? { ...entrega, status: "Entregue" }
        : entrega
    );

    setEntregas(novaLista);
  }

  const secoes = [
    {
      title: "Resumo",
      data: [
        `Total: ${entregas.length}`,
        `Entregues: ${
          entregas.filter((e) => e.status === "Entregue").length
        }`,
        `Pendentes: ${
          entregas.filter((e) => e.status === "Pendente").length
        }`,
      ],
    },
  ];

  return (
    <View style={styles.container}>

      {/* Imagem local */}
      <Image
        source={require("./assets/icon.png")}
        style={styles.logo}
      />

      <Text style={styles.titulo}>
        Controle de Entregas
      </Text>

      {/* Imagem remota */}
      {<Image
        source={{
          uri: "https://randomuser.me/api/portraits/men/32.jpg",
        }}
        style={styles.avatar}
      />}

      <Text style={styles.label}>Motorista</Text>

      {/* TextInput */}
      <TextInput
        style={styles.input}
        value={motorista}
        onChangeText={setMotorista}
        placeholder="Nome do motorista"
      />

      <Text style={styles.subtitulo}>
        Entregas de {motorista}
      </Text>

      {/* FlatList */}
      <FlatList
        data={entregas}

        // Renderiza inicialmente apenas 5 registros
        initialNumToRender={5}

        // Chave única de cada elemento
        keyExtractor={(item) => item.id}

        // Define como cada item aparecerá
        renderItem={({ item }) => (
          <View style={styles.card}>

            <View>
              <Text style={styles.cliente}>
                {item.cliente}
              </Text>

              <Text>
                Status: {item.status}
              </Text>
            </View>

            {item.status === "Pendente" && (
              <TouchableOpacity
                style={styles.botao}
                onPress={() => confirmarEntrega(item.id)}
              >
                <Text style={styles.textoBotao}>
                  Confirmar
                </Text>
              </TouchableOpacity>
            )}

          </View>
        )}
      />

      <Text style={styles.label}>
        Observação da entrega
      </Text>

      {/* TextInput multilinha */}
      <TextInput
        style={styles.textArea}
        value={observacao}
        onChangeText={setObservacao}
        placeholder="Digite uma observação..."
        multiline
        numberOfLines={4}
      />

      {/* TouchableOpacity */}
      <TouchableOpacity
        style={styles.botaoEnviar}
        onPress={() => {
          console.log("Observação:", observacao);
          setObservacao("");
        }}
      >
        <Text style={styles.textoBotao}>
          Salvar observação
        </Text>
      </TouchableOpacity>

      {/* SectionList */}
      <SectionList
        sections={secoes}
        keyExtractor={(item, index) =>
          `${item}-${index}`
        }
        renderSectionHeader={({ section }) => (
          <Text style={styles.subtitulo}>
            {section.title}
          </Text>
        )}
        renderItem={({ item }) => (
          <Text style={styles.resumo}>
            {item}
          </Text>
        )}
      />

    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    paddingTop: 50,
    backgroundColor: "#f4f4f4",
  },

  titulo: {
    fontSize: 26,
    fontWeight: "bold",
    textAlign: "center",
    marginBottom: 15,
  },

  subtitulo: {
    fontSize: 18,
    fontWeight: "bold",
    marginTop: 15,
    marginBottom: 10,
  },

  label: {
    fontWeight: "bold",
    marginTop: 10,
    marginBottom: 5,
  },

  logo: {
    width: 60,
    height: 60,
    alignSelf: "center",
  },

  avatar: {
    width: 90,
    height: 90,
    borderRadius: 45,
    alignSelf: "center",
    marginBottom: 10,
  },

  input: {
    backgroundColor: "#fff",
    borderWidth: 1,
    borderColor: "#ccc",
    padding: 10,
    borderRadius: 8,
  },

  textArea: {
    backgroundColor: "#fff",
    borderWidth: 1,
    borderColor: "#ccc",
    padding: 10,
    borderRadius: 8,
    minHeight: 90,
    textAlignVertical: "top",
  },

  card: {
    backgroundColor: "#fff",
    padding: 15,
    marginBottom: 10,
    borderRadius: 8,
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },

  cliente: {
    fontWeight: "bold",
    fontSize: 16,
  },

  botao: {
    backgroundColor: "#222",
    padding: 10,
    borderRadius: 6,
  },

  botaoEnviar: {
    backgroundColor: "#222",
    padding: 14,
    borderRadius: 8,
    marginTop: 10,
    alignItems: "center",
  },

  textoBotao: {
    color: "#fff",
    fontWeight: "bold",
  },

  resumo: {
    backgroundColor: "#fff",
    padding: 8,
  },
});