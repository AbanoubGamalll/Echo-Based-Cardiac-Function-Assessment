// final_result_screen.dart
import 'package:cardic_function_assement_2/login_screen.dart';
import 'package:cardic_function_assement_2/login_screen.dart';
import 'package:cardic_function_assement_2/video_upload_screen.dart';
import 'package:flutter/material.dart';

import 'api_result.dart';

class FinalResultsScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          toolbarHeight: 70,
          leading: IconButton(
              onPressed: () => Navigator.pop(context),
              icon: Icon(Icons.arrow_back, color: Colors.white)),
          title: const Center(
            child: Text(
              'Results CON.',
              style: TextStyle(
                color: Colors.white,
                fontWeight: FontWeight.bold,
                fontSize: 30,
              ),
              textAlign: TextAlign.center,
            ),
          ),
          backgroundColor: Colors.blueAccent,
        ),
        body: Padding(
          padding: const EdgeInsets.all(20.0),
          child: Column(
            children: [
              // const SizedBox(height: 60),
              Container(
                padding: const EdgeInsetsDirectional.all(30),
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(30),
                  color: Colors.blueAccent,
                ),
                child: Column(
                  children: [
                    Row(
                      children: [
                        const Expanded(
                          child: Text(
                            "ESV:",
                            style: TextStyle(
                                fontWeight: FontWeight.bold,
                                color: Colors.white,
                                fontSize: 40),
                            textAlign: TextAlign.center,
                          ),
                        ),
                        Expanded(
                          child: Text(
                            "${APIResult.value_ESV}",
                            style: const TextStyle(
                                fontWeight: FontWeight.bold,
                                color: Colors.white,
                                fontSize: 40),
                            textAlign: TextAlign.center,
                          ),
                        )
                      ],
                    ),
                    SizedBox(height: 45),
                    Row(
                      children: [
                        const Expanded(
                          child: Text(
                            "EDV:",
                            style: TextStyle(
                                fontWeight: FontWeight.bold,
                                color: Colors.white,
                                fontSize: 40),
                            textAlign: TextAlign.center,
                          ),
                        ),
                        Expanded(
                          child: Text(
                            "${APIResult.value_EDV}",
                            style: const TextStyle(
                                fontWeight: FontWeight.bold,
                                color: Colors.white,
                                fontSize: 40),
                            textAlign: TextAlign.center,
                          ),
                        )
                      ],
                    ),
                    const SizedBox(height: 45),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.start,
                      children: [
                        const Expanded(
                          child: Text(
                            'EF%: ',
                            style: TextStyle(
                                fontWeight: FontWeight.bold,
                                color: Colors.white,
                                fontSize: 40),
                            textAlign: TextAlign.center,
                          ),
                        ),
                        Expanded(
                          child: Text(
                            "${APIResult.value_EF}",
                            style: const TextStyle(
                                fontWeight: FontWeight.bold,
                                color: Colors.white,
                                fontSize: 40),
                            textAlign: TextAlign.center,
                          ),
                        )
                      ],
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 50),
              Container(
                width: double.infinity,
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(20),
                  color: Colors.white,
                ),
                child: Text(
                  50 < APIResult.value_EF && APIResult.value_EF < 70
                      ? "Normal..🥳"
                      : "AbNormal..😔",
                  style: TextStyle(
                      fontSize: 50,
                      fontWeight: FontWeight.w900,
                      color: 50 < APIResult.value_EF && APIResult.value_EF < 70
                          ? Colors.green
                          : Colors.red),
                  textAlign: TextAlign.center,
                ),
              ),
              const SizedBox(height: 60),
              Container(
                alignment: Alignment.bottomCenter,
                decoration:
                    BoxDecoration(borderRadius: BorderRadius.circular(30)),
                clipBehavior: Clip.antiAliasWithSaveLayer,
                child: MaterialButton(
                  minWidth: double.infinity,
                  height: 55,
                  onPressed: () {
                    Navigator.push(context, MaterialPageRoute(
                      builder: (context) {
                        return VideoUploadScreen();
                      },
                    ));
                  },
                  color: Colors.blueAccent,
                  child: const Text(
                    "Analyze Another Echo",
                    style: TextStyle(
                        color: Colors.white,
                        fontSize: 30,
                        fontWeight: FontWeight.bold),
                  ),
                ),
              ),
              SizedBox(height: 30),
              Container(
                alignment: Alignment.bottomRight,
                decoration:
                    BoxDecoration(borderRadius: BorderRadius.circular(30)),
                clipBehavior: Clip.antiAliasWithSaveLayer,
                child: MaterialButton(
                  minWidth: double.infinity,
                  height: 55,
                  onPressed: () {
                    Navigator.pushAndRemoveUntil(context, MaterialPageRoute(
                      builder: (context) {
                        return LoginScreen();
                      },
                    ), (route) {
                      return false;
                    });
                  },
                  color: Colors.blueAccent,
                  child: const Text(
                    "Log Out",
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 25,
                    ),
                  ),
                ),
              )
            ],
          ),
        ));
  }
}
