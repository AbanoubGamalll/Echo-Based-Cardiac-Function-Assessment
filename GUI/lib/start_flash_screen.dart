import 'dart:async';

import 'package:flutter/material.dart';

import 'login_screen.dart';

class StartFlashScreen extends StatefulWidget {
  const StartFlashScreen({super.key});

  @override
  State<StartFlashScreen> createState() => _StartFlashScreenState();
}

class _StartFlashScreenState extends State<StartFlashScreen> {
  @override
  void initState() {
    super.initState();
    _initializeScreen(); // Call the asynchronous initialization method
  }

  Future<void> _initializeScreen() async {
    // Simulate a delay of 5 seconds using Timer
    await Future.delayed(const Duration(seconds: 5));

    // Navigate to the next screen after initialization
    Navigator.pushReplacement(
      context,
      MaterialPageRoute(builder: (context) => const LoginScreen()),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Container(
          width: double.infinity,
          decoration: const BoxDecoration(
            image: DecorationImage(
              image: AssetImage(
                  "assets/images/vecteezy_human-heart-with-cardiogram-for-medical-heart-health-care_25433788.jpg"),
              fit: BoxFit.cover,
            ),
          ),
          child: Padding(
            padding: const EdgeInsetsDirectional.only(start: 10),
            child: Column(
              // mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: <Widget>[
                SizedBox(height: 100),
                const Text(
                  'CARDIAC',
                  style: TextStyle(
                    fontSize: 38,
                    color: Colors.redAccent,
                    fontWeight: FontWeight.bold,
                  ),
                  textAlign: TextAlign.center,
                ),
                const Text(
                  'FUNCTION',
                  style: TextStyle(
                    fontSize: 38,
                    color: Colors.redAccent,
                    fontWeight: FontWeight.bold,
                  ),
                  textAlign: TextAlign.center,
                ),
                SizedBox(height: 450),
                Container(
                  alignment: Alignment.bottomCenter,
                  child: const CircularProgressIndicator(
                    backgroundColor: Colors.redAccent,
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
