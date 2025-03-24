import 'package:flutter/material.dart';
import 'MyHomePage.dart';  // Import your home screen
import 'models/user.dart';  // Import the User model

class ProfileScreen extends StatefulWidget {
  final User user;

  ProfileScreen({required this.user});

  @override
  _ProfileScreenState createState() => _ProfileScreenState();
}

class _ProfileScreenState extends State<ProfileScreen> {
  late TextEditingController _nameController;
  late TextEditingController _emailController;
  late TextEditingController _passwordController;

  @override
  void initState() {
    super.initState();
    _nameController = TextEditingController(text: widget.user.name);
    _emailController = TextEditingController(text: widget.user.email);
    _passwordController = TextEditingController(text: widget.user.password);
  }

  @override
  void dispose() {
    _nameController.dispose();
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  void _saveProfile() {
    setState(() {
      widget.user.name = _nameController.text;
      widget.user.email = _emailController.text;
      widget.user.password = _passwordController.text;
    });
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('Profile details updated successfully!')),
    );
    Navigator.pushReplacement(
      context,
      MaterialPageRoute(
        builder: (context) => HomePage(user: widget.user),
      ),
    );
  }

  Widget _gradientTextField({
    required TextEditingController controller,
    required String labelText,
    bool obscureText = false,
  }) {
    return Card(
      elevation: 5,  // Shadow effect
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(10),
      ),
      child: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            colors: [Colors.green.shade50, Colors.white70],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
          borderRadius: BorderRadius.circular(10),
        ),
        child: TextField(
          controller: controller,
          obscureText: obscureText,
          decoration: InputDecoration(
            labelText: labelText,
            labelStyle: TextStyle(color: Colors.black),
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(10),
              borderSide: BorderSide.none,
            ),
            filled: true,
            fillColor: Colors.transparent,
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        title: Text(
          'Profile',
          style: TextStyle(
            fontSize: 24,
            fontWeight: FontWeight.bold,
            color: Colors.black,
          ),
        ),
        centerTitle: true,
        backgroundColor: Colors.green.shade200,
        actions: [
          IconButton(
            icon: Icon(Icons.save),
            onPressed: _saveProfile,
          ),
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(19.0),
        child: Column(
          children: [
            Image.asset(
              'assets/selogos/sembup4.gif',
              width: 240,
              height: 140,
            ),
            SizedBox(height: 35),
            _gradientTextField(
              controller: _nameController,
              labelText: 'New Name',
            ),
            SizedBox(height: 24),
            _gradientTextField(
              controller: _emailController,
              labelText: 'Add an Email',
            ),
            SizedBox(height: 24),
            _gradientTextField(
              controller: _passwordController,
              labelText: 'New Password',
              obscureText: true,
            ),
          ],
        ),
      ),
    );
  }
}
