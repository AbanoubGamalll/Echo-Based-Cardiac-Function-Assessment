// api_result.dart
import 'dart:typed_data';
import 'package:flutter/cupertino.dart';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:dio/dio.dart';
// import 'dart:io';

class APIResult {
  static var videoPath;
  static var value_ESV;
  static var value_EDV;
  static var value_EF;

  static var imageES_Transfomrer;
  static var imageED_Transfomrer;
  static var imageES_UNet;
  static var imageED_UNet;

  static Future<void> sendVideoAndGetResponse() async {
    // Instantiate Dio
    Dio dio = Dio();

    // Set up base URL
    // dio.options.baseUrl = 'https://dc70-35-237-116-74.ngrok-free.app/';
    // dio.options.baseUrl = 'https://fastapi-vf3r.onrender.com/';
    dio.options.baseUrl = 'http://10.0.2.2:8000';
    // dio.options.baseUrl = 'http://127.0.0.1:8000';

    try {
      // Create FormData object
      FormData formData = FormData.fromMap({
        'video': await MultipartFile.fromFile(videoPath
            // contentType: MediaType('video', 'mp4') // Specify content type here
            ),
      });

      print("***********************************************************");
      print("before post");
      print("***********************************************************");
      // Make POST request
      Response response = await dio.post('/', data: formData);

      print("***********************************************************");
      print("After post");
      print("***********************************************************");
      // Handle response
      if (response.statusCode == 200) {
        // Request successful
        value_ESV = await response.data['ESV Value'];
        value_EDV = await response.data['EDV Value'];
        value_EF = await response.data['EF Value'];

        imageES_Transfomrer = Image.memory(
            base64Decode(response.data['imgEST Value']),
            fit: BoxFit.cover);
        imageED_Transfomrer = Image.memory(
            base64Decode(response.data['imgEDT Value']),
            fit: BoxFit.cover);
        imageES_UNet = Image.memory(base64Decode(response.data['imgESU Value']),
            fit: BoxFit.cover);
        imageED_UNet = Image.memory(base64Decode(response.data['imgEDU Value']),
            fit: BoxFit.cover);

        // imageES_Transfomrer = Text(response.data['imgEST Value']);
        // imageED_Transfomrer = Text(response.data['imgEDT Value']);
        // imageES_UNet = Text(response.data['imgESU Value']);
        // imageED_UNet = Text(response.data['imgEDU Value']);
        print("***********************************************************");
        print("Response  is ${response.data}");
        // print('ESV Value : ${APIResult.value_ESV}');
        // print('EDV Value : ${APIResult.value_EDV}');
        // print('EF Value : ${APIResult.value_EF}');
        // print('imgEST String : ${APIResult.imageES_Transfomrer}');
        print("***********************************************************");
      } else {
        // Request failed
        print('Request failed with status: ${response.statusCode}');
      }
    } catch (e) {
      // Handle error
      print('Error: $e');
    }
  }
}
