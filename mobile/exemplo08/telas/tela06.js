import { useState } from "react";
import { Pressable, ScrollView, Text, TextInput, View } from "react-native";
import CabecalhoTela from "../components/CabecalhoTela";
import styles from "../style/estilo";

export default function FormularioExemplo({ voltaPara }) {
  const [nome, setNome] = useState("");
  const [email, setEmail] = useState("");
  const [mensagem, setMensagem] = useState("");

  const enviar = () => {
    if (!nome.trim() || !email.trim()) {
      setMensagem("Preencha nome e e-mail antes de enviar.");
      return;
    }

    setMensagem(`Cadastro recebido para ${nome}.`);
  };

  return (
    <View style={styles.container}>
      <CabecalhoTela
        titulo="Formulário"
        subtitulo="Inputs controlados por estado"
        voltaPara={voltaPara}
      />

      <ScrollView contentContainerStyle={styles.scrollContent} keyboardShouldPersistTaps="handled">
        <View style={styles.panel}>
          <View style={styles.formGroup}>
            <Text style={styles.label}>Nome</Text>
            <TextInput
              value={nome}
              onChangeText={setNome}
              placeholder="Digite seu nome"
              style={styles.input}
            />
          </View>

          <View style={styles.formGroup}>
            <Text style={styles.label}>E-mail</Text>
            <TextInput
              value={email}
              onChangeText={setEmail}
              placeholder="nome@exemplo.com"
              keyboardType="email-address"
              autoCapitalize="none"
              style={styles.input}
            />
          </View>

          <Pressable
            onPress={enviar}
            style={({ pressed }) => [
              styles.primaryButton,
              pressed && styles.primaryButtonPressed,
            ]}
          >
            <Text style={styles.primaryButtonText}>Enviar cadastro</Text>
          </Pressable>

          {mensagem ? (
            <View style={styles.resultBox}>
              <Text style={styles.resultText}>{mensagem}</Text>
            </View>
          ) : null}
        </View>
      </ScrollView>
    </View>
  );
}
