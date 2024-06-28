// load_flash_screen.dart
import 'dart:async';
import 'dart:async';

import 'package:cardic_function_assement_2/api_result.dart';
import 'package:cardic_function_assement_2/result_screen.dart';
import 'package:flutter/material.dart';

class LoadingScreen extends StatefulWidget {
  const LoadingScreen({super.key});

  @override
  State<LoadingScreen> createState() => _LoadingScreenState();
}

class _LoadingScreenState extends State<LoadingScreen> {
  @override
  void initState() {
    super.initState();
    _initializeScreen(); // Call the asynchronous initialization method
  }

  Future<void> _initializeScreen() async {
    // Simulate a delay of 5 seconds using Timer
    // await Future.delayed(const Duration(seconds: 6));
    await APIResult.sendVideoAndGetResponse().then((_) {
// Navigate to the next screen after initialization
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (context) => ResultsScreen()),
      );
    }); //.catchError((e) => print("The Error is $e"));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Container(
          width: double.infinity,
          decoration: const BoxDecoration(
            image: DecorationImage(
              image: AssetImage("assets/images/analyzing Heart.png"),
              fit: BoxFit.cover,
            ),
          ),
          child: Padding(
            padding: const EdgeInsetsDirectional.only(start: 10),
            child: Column(
              // mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: <Widget>[
                SizedBox(height: 535),
                Container(
                  alignment: Alignment.bottomCenter,
                  child: const Text(
                    'ANALYZING',
                    style: TextStyle(
                      fontSize: 30,
                      color: Colors.white,
                      fontWeight: FontWeight.bold,
                    ),
                    textAlign: TextAlign.center,
                  ),
                ),
                Container(
                  alignment: Alignment.bottomCenter,
                  child: const Text(
                    'YOUR ECHOCARDIOGRAM',
                    style: TextStyle(
                      fontSize: 35,
                      color: Colors.blueAccent,
                      fontWeight: FontWeight.bold,
                    ),
                    textAlign: TextAlign.center,
                  ),
                ),
                SizedBox(height: 30),
                Container(
                  alignment: Alignment.bottomCenter,
                  child: const CircularProgressIndicator(
                    backgroundColor: Colors.blueAccent,
                    color: Colors.white,
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
