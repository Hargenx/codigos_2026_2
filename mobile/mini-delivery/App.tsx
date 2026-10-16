import React, { useEffect, useState } from "react";
import {
  ActivityIndicator,
  Alert,
  Button,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  View,
} from "react-native";
import { SafeAreaProvider, SafeAreaView } from "react-native-safe-area-context";
import AsyncStorage from "@react-native-async-storage/async-storage";

type Carrinho = Record<string, number>;
const K = {
  nome: "@delivery:nome",
  endereco: "@delivery:endereco",
  carrinho: "@delivery:carrinho",
};
const produtos = [
  { id: "pizza", nome: "Pizza individual", preco: 29.9 },
  { id: "suco", nome: "Suco natural", preco: 9.5 },
  { id: "brownie", nome: "Brownie", preco: 12.0 },
];
const reais = (v: number) =>
  v.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });

export default function App() {
  const [nome, setNome] = useState("");
  const [endereco, setEndereco] = useState("");
  const [carrinho, setCarrinho] = useState<Carrinho>({});
  const [carregando, setCarregando] = useState(true);
  const [ocupado, setOcupado] = useState(false);

  // Recupera todos os dados ao abrir o app.
  useEffect(() => {
    let ativo = true;
    (async () => {
      try {
        const [[, n], [, e], [, c]] = await AsyncStorage.multiGet(
          Object.values(K),
        );
        if (!ativo) return;
        setNome(n ?? "");
        setEndereco(e ?? "");
        setCarrinho(c ? (JSON.parse(c) as Carrinho) : {});
      } catch {
        Alert.alert("Erro", "Falha ao recuperar os dados.");
      } finally {
        if (ativo) setCarregando(false);
      }
    })();
    return () => {
      ativo = false;
    };
  }, []);

  // Centraliza o tratamento de erros de gravação e leitura.
  async function executar(acao: () => Promise<void>) {
    if (ocupado) return;
    setOcupado(true);
    try {
      await acao();
    } catch {
      Alert.alert("Erro", "Operação não realizada.");
    } finally {
      setOcupado(false);
    }
  }

  function salvarCadastro() {
    if (!nome.trim() || !endereco.trim()) {
      Alert.alert("Atenção", "Informe nome e endereço.");
      return;
    }
    void executar(async () => {
      await AsyncStorage.multiSet([
        [K.nome, nome.trim()],
        [K.endereco, endereco.trim()],
      ]);
      Alert.alert("Salvo", "Dados disponíveis na próxima abertura.");
    });
  }

  function alterarProduto(id: string, delta: number) {
    void executar(async () => {
      const novo = { ...carrinho };
      const quantidade = Math.max(0, (novo[id] ?? 0) + delta);
      if (quantidade) novo[id] = quantidade;
      else delete novo[id];
      await AsyncStorage.setItem(K.carrinho, JSON.stringify(novo));
      setCarrinho(novo);
    });
  }

  function finalizar() {
    void executar(async () => {
      const [raw, n, e] = await Promise.all([
        AsyncStorage.getItem(K.carrinho),
        AsyncStorage.getItem(K.nome),
        AsyncStorage.getItem(K.endereco),
      ]);
      const pedido: Carrinho = raw ? JSON.parse(raw) : {};
      const itens = Object.values(pedido).reduce((a, b) => a + b, 0);
      if (!n || !e || !itens) {
        Alert.alert("Atenção", "Salve o cadastro e adicione produtos.");
        return;
      }
      await AsyncStorage.removeItem(K.carrinho);
      setCarrinho({});
      Alert.alert(
        "Pedido simulado",
        `${itens} item(ns) para ${n}. Nada foi enviado.`,
      );
    });
  }

  function apagarDados() {
    Alert.alert("Confirmação", "Apagar cadastro e carrinho?", [
      { text: "Cancelar", style: "cancel" },
      {
        text: "Apagar",
        style: "destructive",
        onPress: () => {
          void executar(async () => {
            await AsyncStorage.multiRemove(Object.values(K));
            setNome("");
            setEndereco("");
            setCarrinho({});
          });
        },
      },
    ]);
  }

  function inspecionar() {
    void executar(async () => {
      const chaves = (await AsyncStorage.getAllKeys()).filter((chave) =>
        chave.startsWith("@delivery:"),
      );
      Alert.alert("Chaves do app", chaves.join("\n") || "Nenhuma");
    });
  }

  const total = produtos.reduce(
    (soma, p) => soma + p.preco * (carrinho[p.id] ?? 0),
    0,
  );

  return (
    <SafeAreaProvider>
      <SafeAreaView style={s.area}>
        <ScrollView contentContainerStyle={s.conteudo}>
          <Text style={s.titulo}>Mini Delivery</Text>
          {carregando ? (
            <ActivityIndicator />
          ) : (
            <>
              <Text style={s.secao}>1. Dados do cliente</Text>
              <TextInput
                style={s.campo}
                placeholder="Nome"
                value={nome}
                onChangeText={setNome}
              />
              <TextInput
                style={s.campo}
                placeholder="Endereço de entrega"
                value={endereco}
                onChangeText={setEndereco}
              />
              <Button
                title="Salvar cadastro"
                onPress={salvarCadastro}
                disabled={ocupado}
              />

              <Text style={s.secao}>2. Cardápio</Text>
              {produtos.map((p) => (
                <View key={p.id} style={s.linha}>
                  <Text style={{ flex: 1 }}>
                    {p.nome}
                    {"\n"}
                    {reais(p.preco)}
                    {"  "}× {carrinho[p.id] ?? 0}
                  </Text>
                  <Button
                    title="−"
                    disabled={ocupado || !carrinho[p.id]}
                    onPress={() => alterarProduto(p.id, -1)}
                  />
                  <Button
                    title="+"
                    disabled={ocupado}
                    onPress={() => alterarProduto(p.id, 1)}
                  />
                </View>
              ))}
              <Text style={s.total}>Total: {reais(total)}</Text>
              <Button
                title="Finalizar pedido (simulado)"
                onPress={finalizar}
                disabled={ocupado}
              />

              <Text style={s.secao}>3. Armazenamento</Text>
              <Button
                title="Ver chaves salvas"
                onPress={inspecionar}
                disabled={ocupado}
              />
              <View style={{ height: 10 }} />
              <Button
                title="Apagar meus dados"
                color="#b91c1c"
                onPress={apagarDados}
                disabled={ocupado}
              />
            </>
          )}
        </ScrollView>
      </SafeAreaView>
    </SafeAreaProvider>
  );
}

const s = StyleSheet.create({
  area: { flex: 1, backgroundColor: "#f8fafc" },
  conteudo: { padding: 20, paddingBottom: 32 },
  titulo: { fontSize: 28, fontWeight: "bold", color: "#0f172a" },
  secao: { fontSize: 18, fontWeight: "bold", marginTop: 24, marginBottom: 10 },
  campo: {
    padding: 12,
    marginBottom: 8,
    backgroundColor: "white",
    borderWidth: 1,
    borderColor: "#cbd5e1",
    borderRadius: 8,
  },
  linha: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
    padding: 12,
    backgroundColor: "white",
    borderRadius: 8,
    marginBottom: 8,
  },
  total: { fontSize: 22, fontWeight: "bold", marginVertical: 18 },
});
