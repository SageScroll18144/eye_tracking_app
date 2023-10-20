import React, { useState, useEffect } from 'react';
import { SafeAreaView, StyleSheet, Text, Image, View, TouchableOpacity } from 'react-native';
import { Camera } from 'expo-camera';
import { AntDesign, MaterialCommunityIcons } from '@expo/vector-icons';

export default function App() {
  const [camRef, setCameraRef] = useState(null);
  const [type, setType] = useState(Camera.Constants.Type.front);
  const [hasPermission, setHasPermission] = useState(null);
  const [recording, setRecording] = useState(false);
  const url = 'http://192.168.1.13:7800';
  const [POSX, setPOSX] = useState(315);

  useEffect(() => {
    if(recording){
      const intervalId = setInterval(() => {
        setPOSX((POSX) => (POSX === 630 ? 20 : 630));
      }, 2000);
  
      return () => {
        clearInterval(intervalId);
      };
    }
  }, [recording]);

  useEffect(() => {
    (async () => {
      const { status } = await Camera.requestCameraPermissionsAsync();
      setHasPermission(status === 'granted');
    })();
  }, []);

  if (hasPermission === null) {
    return <View />;
  }

  if (hasPermission === false) {
    return <Text> *Acesso negado* </Text>;
  }

  async function recordingCamera() {
    try {
      if (camRef && !recording) {  
        setPOSX(315);      
        setRecording(true);
        let video = await camRef.recordAsync({ mute: true, quality: '720p', fps: 30, maxDuration: 5});
        console.log("video", video);
        setRecording(false);
        camRef.stopRecording();
        let formData = new FormData();
        formData.append('mp4file', {
          name: "video.mp4", // Nome do arquivo
          uri: video.uri, // URI do arquivo
          type: 'video/mp4' // Tipo do arquivo
        });

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
      <View style={{ flex: 1 }}>
        <Camera
          style={styles.images}
          type={type}
          ref={(ref) => {
            setCameraRef(ref);
          }}
        />
        {recording && (
          <Image
            style={{
              position: 'absolute',
              top: POSX, // Y
              left: 180, //X
              width: 20,
              height: 20,
              borderRadius: 20,
              tintColor: 'red',
            }}
            source={{
              uri: 'https://placehold.it/150x150',
            }}
          />
        )}

      </View>

      <TouchableOpacity
        style={styles.button_record}
        onPress={recordingCamera}
      >
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
            !recording ? (type === Camera.Constants.Type.back
              ? Camera.Constants.Type.front
              : Camera.Constants.Type.back) : type
          );
        }}
      >
        <AntDesign name="swap" size={40} color="black" />
      </TouchableOpacity>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  button_swap: {
    position: 'absolute',
    bottom: 31,
    left: 20,
  },
  button_record: {
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
});