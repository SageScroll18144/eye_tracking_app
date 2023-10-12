import React, { useState, useEffect, useRef } from 'react';
import { SafeAreaView, StyleSheet, Text, View, TouchableOpacity } from 'react-native';
import { Camera } from 'expo-camera'
import { AntDesign, MaterialCommunityIcons } from '@expo/vector-icons';

export default function App() {
  const [camRef, setCameraRef] = useState(null);
  const [type, setType] = useState(Camera.Constants.Type.front);
  const [hasPermission, setHasPermission] = useState(null);
  const [recording, setRecording] = useState(false);

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
  }

});
