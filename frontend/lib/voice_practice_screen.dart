import 'package:flutter/material.dart';
import 'dart:async';

class VoicePracticeScreen extends StatefulWidget {
  final String userName;

  VoicePracticeScreen({required this.userName});

  @override
  _VoicePracticeScreenState createState() => _VoicePracticeScreenState();
}

class _VoicePracticeScreenState extends State<VoicePracticeScreen> {
  int _secondsRemaining = 120; // 2 minutes = 120 seconds
  late Timer _timer;
  bool _isFeedbackEnabled = false;

  @override
  void initState() {
    super.initState();
    _startTimer();
  }

  void _startTimer() {
    _timer = Timer.periodic(Duration(seconds: 1), (timer) {
      if (_secondsRemaining > 0) {
        setState(() {
          _secondsRemaining--;
        });
      } else {
        setState(() {
          _isFeedbackEnabled = true; // Enable the feedback button
        });
        _timer.cancel();
      }
    });
  }

  String _formatTime(int seconds) {
    int minutes = seconds ~/ 60;
    int remainingSeconds = seconds % 60;
    return '$minutes:${remainingSeconds.toString().padLeft(2, '0')}';
  }

  @override
  void dispose() {
    _timer.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.green.shade50,
      appBar: AppBar(
        title: Text(
          '🎙️ Voice Practice',
          style: TextStyle(
            fontSize: 24,
            fontWeight: FontWeight.bold,
            color: Colors.white,
          ),
        ),
        centerTitle: true,
        backgroundColor: Colors.green,
      ),
      body: Center( // Centering the entire column
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 20),
          child: Column(
            mainAxisSize: MainAxisSize.min, // Center vertically
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              // Title
              Text(
                'Voice Practice',
                style: TextStyle(
                  fontSize: 30,
                  fontWeight: FontWeight.bold,
                  color: Colors.green,
                ),
              ),

              SizedBox(height: 20),

              // Logo Image
              Image.asset(
                'assets/selogos/sembv1.png',
                width: 180,
                height: 180,
              ),

              SizedBox(height: 10),

              // Username Display
              Text(
                'User: ${widget.userName}',
                style: TextStyle(
                  fontSize: 18,
                  color: Colors.grey[700],
                  fontWeight: FontWeight.w500,
                ),
              ),

              SizedBox(height: 30),

              // Countdown Timer
              Container(
                padding: EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(10),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.grey.withOpacity(0.3),
                      blurRadius: 5,
                      spreadRadius: 2,
                      offset: Offset(0, 2),
                    ),
                  ],
                ),
                child: Text(
                  'Time Remaining: ${_formatTime(_secondsRemaining)}',
                  style: TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                    color: Colors.red,
                  ),
                ),
              ),

              SizedBox(height: 30),

              // GIF Animation
              Image.asset(
                'assets/selogos/sembv2.gif',
                width: 250,
                height: 100,
              ),

              SizedBox(height: 40),

              // "Tap to Continue" Button
              ElevatedButton(
                onPressed: () {
                  // Add voice practice logic here
                },
                child: Text('Tap to Continue'),
                style: ElevatedButton.styleFrom(
                  padding: EdgeInsets.symmetric(horizontal: 40, vertical: 15),
                  textStyle: TextStyle(fontSize: 18),
                  backgroundColor: Colors.green,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(10),
                  ),
                ),
              ),

              SizedBox(height: 20),

              // "Get Feedback" Button (Disabled initially)
              ElevatedButton(
                onPressed: _isFeedbackEnabled
                    ? () {
                  // Implement feedback logic here
                }
                    : null, // Button remains disabled until timer ends
                child: Text('Get Feedback'),
                style: ElevatedButton.styleFrom(
                  padding: EdgeInsets.symmetric(horizontal: 40, vertical: 15),
                  textStyle: TextStyle(fontSize: 18),
                  backgroundColor: Colors.blue,
                  disabledBackgroundColor: Colors.grey, // Grey when disabled
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(10),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

