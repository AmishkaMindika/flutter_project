import 'package:flutter/material.dart';
import 'Login_screen.dart';  // Import the login screen

class splash_screen extends StatefulWidget {
  @override
  _SplashScreenState createState() => _SplashScreenState();
}

class _SplashScreenState extends State<splash_screen> {
  @override
  void initState() {
    super.initState();
    _navigateToLogin();
  }

  _navigateToLogin() async {
    await Future.delayed(Duration(seconds: 4), () {});

    Navigator.pushReplacement(
      context,
      MaterialPageRoute(builder: (context) => login_screen()),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.green.shade50,
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Image.asset(
              'assets/selogos/semb2.gif',
              width: 310,
              height: 300,
            ),
            SizedBox(height: 20),

            SizedBox(height: 10),

          ],
        ),
      ),

    );
  }
}