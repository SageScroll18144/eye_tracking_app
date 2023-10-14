import React, { useState, useEffect, useRef } from 'react';
import { SafeAreaView, StyleSheet, Text, View, TouchableOpacity } from 'react-native';
import { Camera } from 'expo-camera'
import { AntDesign, MaterialCommunityIcons } from '@expo/vector-icons';
import { Animated, Easing } from 'react-native'; // Importe Animated

export default function App() {
  const [camRef, setCameraRef] = useState(null);
  const [type, setType] = useState(Camera.Constants.Type.front);
  const [hasPermission, setHasPermission] = useState(null);
  const [recording, setRecording] = useState(false);
  const url = 'http://192.168.1.13:7800';

  const [pointPosition, setPointPosition] = useState(new Animated.Value(0));

  // Função para atualizar a posição do ponto
  const updatePointPosition = () => {
    Animated.loop(
      Animated.timing(pointPosition, {
        toValue: 10, // Altere esse valor para controlar a animação
        duration: 1000, // Duração da animação em milissegundos
        easing: Easing.linear, // Easing da animação
        useNativeDriver: false, // Defina como true se possível
      })
    ).start();
  };

  useEffect(() => {
    if (recording) {
      updatePointPosition();
    } else {
      pointPosition.setValue(0);
      pointPosition.stopAnimation();
    }
  }, [recording]);

  useEffect(() => {
    (async () => {
      const {status} = await Camera.requestCameraPermissionsAsync();
      setHasPermission(status === 'granted');
    })();
  }, []);

  if(hasPermission === null) {
    return <View/>;
  }

  if(hasPermission === false){
    return <Text> *Acesso negado* </Text>
  }

  async function recordingCamera() {
    try {
      if (camRef && !recording) {
        setRecording(true);
        let video = await camRef.recordAsync({mute: true});
        console.log("video", video);

        let formData = new FormData();
        formData.append('mp4file', {
          name: "video.mp4", // Nome do arquivo
          uri: video.uri,     // URI do arquivo
          type: 'video/mp4'   // Tipo do arquivo
      });
        // formData.append('mp4file', video.uri, "video.mp4");
        formData.append("textdata", "1234567");

        try {
            let response = await fetch(url, {
                method: 'post',
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
                body: formData
            });
            return await response.json();
        }
        catch (error) {
            console.log('error : ' + error);
            return error;
        }
      } else {
        setRecording(false);
        camRef.stopRecording();
      }
    } catch (error) {
      console.error("Erro ao gravar o vídeo:", error);
    }
  }

  return (
    <SafeAreaView style={styles.container}>
      <Camera
        style={styles.images}//{flex: 1 }
        type={type}
        ref={(ref) => {
          setCameraRef(ref);
        }}
      />
      
      <Animated.View
        style={[
          styles.animatedPoint,
          {
            transform: [
              {
                translateX: pointPosition.interpolate({
                  inputRange: [0, 1],
                  outputRange: [0, 300], // Mude para a largura desejada da tela
                }),
              },
            ],
          },
        ]}
      ></Animated.View>

      <TouchableOpacity 
        style={styles.button_record} onPress={ recordingCamera }>
        <MaterialCommunityIcons name="record-circle-outline" size={40} color="black" />
        <View
          style={{
            borderWidth: 2,
            borderRadius: 25,
            borderColor: recording ? "red" : "blue",
            height: 10,
            width: 10,
            backgroundColor: recording ? "red" : "blue",
          }}
        ></View>
      </TouchableOpacity>

      <TouchableOpacity
        style={styles.button_swap}
        onPress={() => {
          setType(
            type === Camera.Constants.Type.back ? Camera.Constants.Type.front : Camera.Constants.Type.back
          );
        }}
        >
        <AntDesign name="swap" size={40} color="black" />
      </TouchableOpacity>
          
    </SafeAreaView >
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center', 
    alignItems: 'center',
  },
  button_swap:{
    position: 'absolute', 
    bottom: 31, 
    left: 20, 
  },
  button_record:{
    justifyContent: 'center', 
    alignItems: 'center',
    margin: 20,
    borderRadius: 20,
    width: 40,
    height: 40,
  },
  images: {
    width: 400,
    height: 650, 
    borderRadius: 100,
  },
  animatedPoint: {
    width: 10,
    height: 10,
    backgroundColor: 'red', // Cor do ponto
    position: 'absolute',
    top: 10, // Ajuste a posição vertical do ponto conforme necessário
  },

});
