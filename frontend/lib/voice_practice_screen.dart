import 'package:flutter/material.dart';

class VoicePracticeScreen extends StatelessWidget {
  final String userName;

  VoicePracticeScreen({required this.userName});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.green.shade50,
      appBar: AppBar(
        title: Text(
          '🎙️',
          style: TextStyle(
            fontSize: 24,
            fontWeight: FontWeight.bold,
            color: Colors.white,
          ),
        ),
        centerTitle: true,
        backgroundColor: Colors.green,
      ),
      body: Padding(

        padding: const EdgeInsets.all(100.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              'Voice Practice',
              style: TextStyle(
                fontSize: 30,
                fontWeight: FontWeight.bold,
                color: Colors.green,
              ),
            ),
            SizedBox(height: 40),
            Image.asset(
              'assets/selogos/sembv1.png',
              width: 210,
              height: 200,
            ),
            Text(
              'User Name: $userName',
              style: TextStyle(
                fontSize: 18,
                color: Colors.grey,
              ),
            ),
            SizedBox(height: 50),
            Image.asset(
              'assets/selogos/sembv2.gif',
              width: 250,
              height: 100,
            ),
            ElevatedButton(
              onPressed: () {
                // Add voice practice logic here
              },
              child: Text('Top to Continue'),
              style: ElevatedButton.styleFrom(
                padding: EdgeInsets.symmetric(horizontal: 40, vertical: 15),
                textStyle: TextStyle(fontSize: 18),
                backgroundColor: Colors.green,
              ),
            ),
            SizedBox(height: 50),

          ],
        ),
      ),
    );
  }
}