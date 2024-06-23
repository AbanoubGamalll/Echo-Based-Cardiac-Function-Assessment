import 'package:flutter/material.dart';

import 'api_result.dart';
import 'final_result_screen.dart';

class ResultsScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        toolbarHeight: 70,
        leading: Text(""),
        title: const Center(
          child: Text(
            'Results',
            style: TextStyle(
              color: Colors.white,
              fontWeight: FontWeight.bold,
              fontSize: 30,
            ),
            textAlign: TextAlign.center,
          ),
        ),
        actions: const [
          Icon(
            Icons.more_vert_rounded,
            color: Colors.white,
          ),
          SizedBox(width: 15)
        ],
        backgroundColor: Colors.blueAccent,
      ),
      body: Padding(
        padding: EdgeInsets.all(20.0),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Container(
            alignment: Alignment.centerLeft,
            child: const Text(
              "TRANSFORMER",
              style: TextStyle(
                  fontSize: 30,
                  fontWeight: FontWeight.bold,
                  color: Colors.blueAccent),
            ),
          ),
          Expanded(
            child: Row(
              children: [
                Expanded(
                  child: Container(
                      height: 250,
                      width: 250,
                      child: APIResult.imageES_Transfomrer),
                ),
                const SizedBox(width: 20),
                Expanded(
                  child: Container(
                    height: 250,
                    width: 250,
                    child: APIResult.imageED_Transfomrer,
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 10),
          const Row(
            children: [
              Expanded(
                child: Text(
                  "ES Frame",
                  style: TextStyle(
                    color: Colors.blueAccent,
                    fontSize: 23,
                    fontWeight: FontWeight.bold,
                  ),
                  textAlign: TextAlign.center,
                ),
              ),
              Expanded(
                child: Text(
                  "ED Frame",
                  style: TextStyle(
                    color: Colors.blueAccent,
                    fontSize: 23,
                    fontWeight: FontWeight.bold,
                  ),
                  textAlign: TextAlign.center,
                ),
              ),
            ],
          ),
          SizedBox(height: 30),
          Container(
            alignment: Alignment.centerLeft,
            child: const Text(
              "U-NET",
              style: TextStyle(
                  fontSize: 30,
                  fontWeight: FontWeight.bold,
                  color: Colors.blueAccent),
            ),
          ),
          Expanded(
            child: Row(
              children: [
                Expanded(
                  child: Container(
                    height: 250,
                    width: 250,
                    child: APIResult.imageES_UNet,
                  ),
                ),
                const SizedBox(width: 20),
                Expanded(
                  child: Container(
                    height: 250,
                    width: 250,
                    child: APIResult.imageED_UNet,
                  ),
                ),
              ],
            ),
          ),
          SizedBox(height: 10),
          const Row(
            children: [
              Expanded(
                child: Text(
                  "ES Frame",
                  style: TextStyle(
                    color: Colors.blueAccent,
                    fontSize: 23,
                    fontWeight: FontWeight.bold,
                  ),
                  textAlign: TextAlign.center,
                ),
              ),
              Expanded(
                child: Text(
                  "ED Frame",
                  style: TextStyle(
                    color: Colors.blueAccent,
                    fontSize: 23,
                    fontWeight: FontWeight.bold,
                  ),
                  textAlign: TextAlign.center,
                ),
              ),
            ],
          ),
          SizedBox(height: 40),
          Container(
            alignment: Alignment.bottomRight,
            child: MaterialButton(
              minWidth: 170,
              height: 55,
              onPressed: () {
                Navigator.push(context, MaterialPageRoute(
                  builder: (context) {
                    return FinalResultsScreen();
                  },
                ));
              },
              color: Colors.blueAccent,
              child: const Text(
                "Next",
                style: TextStyle(color: Colors.white, fontSize: 25),
              ),
            ),
          )
        ]),
      ),
    );
  }
}
