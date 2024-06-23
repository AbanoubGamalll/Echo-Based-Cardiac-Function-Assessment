// main.dart
import 'package:cardic_function_assement_2/start_flash_screen.dart';
import 'package:cardic_function_assement_2/video_upload_screen.dart';
import 'package:flutter/material.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Project',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: StartFlashScreen(),
      debugShowCheckedModeBanner: false,
    );
  }
}
