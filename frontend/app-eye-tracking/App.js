import React, { useState, useEffect, useRef } from 'react';
import { StatusBar } from 'expo-status-bar';
import { SafeAreaView, StyleSheet, Text, View, TouchableOpacity, Modal, Image } from 'react-native';
import { Camera } from 'expo-camera'
import { AntDesign, MaterialCommunityIcons } from '@expo/vector-icons';

export default function App() {
  const camRef = useRef(null);
  const [type, setType] = useState(Camera.Constants.Type.front);
  const [hasPermission, setHasPermission] = useState(null);
  const [capturedPhoto, setCapturedPhoto] = useState(null);
  const [open, setOpen] = useState(false);

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

  async function takePicture(){
    if(camRef){
      const data = await camRef.current.takePictureAsync();
      setCapturedPhoto(data.uri);
      setOpen(true);
      console.log(data);
    }
  }

  return (
    <SafeAreaView style={styles.container}>
      <Camera
        style={styles.images}//{flex: 1 }
        type={type}
        ref={camRef}
      />
      
      <TouchableOpacity style={styles.button_record} onPress={ takePicture }>
        <MaterialCommunityIcons name="record-circle-outline" size={40} color="black" />
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


      {capturedPhoto &&
        <Modal
          animationType = "slide"
          transparent = {false}
          visible={open}
          >
            <View style={{flex: 1, justifyContent: 'center', alignItems:'center', margin: 20}}>
              <TouchableOpacity style={{margin:10}} onPress={ () => setOpen(false)}>
                <FontAwesome name="window-close" size={50} color="red"/>
              </TouchableOpacity>
            
            <Image 
              style={styles.images}
              source={{uri: capturedPhoto}}
            />

            </View> 
        </Modal>
      }
          
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
