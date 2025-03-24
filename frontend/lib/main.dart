import 'package:flutter/material.dart';
import 'MyHomePage.dart';
import 'splash_screen.dart';
import 'package:flutter_project/style/colour.dart';
import 'Pages/community_page.dart';
import 'Pages/conversation_branch_page.dart';
import 'Pages/progress_tracking_page.dart';
import 'Pages/settings_page.dart';
import 'profile_screen.dart';
import 'voice_practice_screen.dart';
import 'community_chat_screen.dart';
import 'ice_breaker_screen.dart';
import 'models/user.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Social Ease',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),

      home: splash_screen(),
    );
  }
}








