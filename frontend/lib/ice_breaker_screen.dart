import 'package:flutter/material.dart';
import 'voice_practice_screen.dart';

class IceBreakerScreen extends StatelessWidget {
  final String userName;

  IceBreakerScreen({required this.userName});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [Colors.white, Colors.green],
          ),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            SizedBox(height: 60),
            Text(
              "Ice Breaker",
              style: TextStyle(
                fontSize: 28,
                fontWeight: FontWeight.bold,
                color: Colors.black,
              ),
            ),
            Text(
              "Challenge",
              style: TextStyle(
                fontSize: 28,
                fontWeight: FontWeight.bold,
                color: Colors.green.shade600,
              ),
            ),
            SizedBox(height: 20),
            Text(
              "Your Daily Challenge Awaits",
              style: TextStyle(fontSize: 18, color: Colors.black54),
            ),
            SizedBox(height: 40),
            ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => VoicePracticeScreen(userName: userName),
                  ),
                );
              },
              child: Text(
                'Voice Practice',
                style: TextStyle(fontSize: 18, color: Colors.black),
              ),
              style: ElevatedButton.styleFrom(
                padding: EdgeInsets.symmetric(horizontal: 50, vertical: 15),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(20),
                ),
                backgroundColor: Colors.green.shade100,
                shadowColor: Colors.grey,
                elevation: 5,
              ),
            ),
            Spacer(),
            Padding(
              padding: const EdgeInsets.only(bottom: 20, left: 20, right: 20),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  IconButton(
                    icon: Icon(Icons.arrow_back, size: 30, color: Colors.black),
                    onPressed: () {
                      Navigator.pop(context);
                    },
                  ),
                  Text(
                    "SOCIAL EASE",
                    style: TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                      color: Colors.white,
                    ),
                  ),
                  IconButton(
                    icon: Icon(Icons.access_time, size: 30, color: Colors.black),
                    onPressed: () {
                      // Action for clock icon
                    },
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
