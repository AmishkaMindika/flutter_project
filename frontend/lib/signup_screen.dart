import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'MyHomePage.dart';
import 'login_screen.dart';
import 'models/user.dart';

class signup_screen extends StatelessWidget {
  final TextEditingController _nameController = TextEditingController();
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  final TextEditingController _confirmPasswordController = TextEditingController();

  Future<void> _signup(BuildContext context) async {
    if (_passwordController.text != _confirmPasswordController.text) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Passwords do not match')),
      );
      return;
    }

    final url = Uri.parse("http://localhost:5000/api/auth/signup");

    final response = await http.post(
      url,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'name': _nameController.text,
        'email': _emailController.text,
        'password': _passwordController.text,
      }),
    );

    if (response.statusCode == 201) {
      final data = jsonDecode(response.body);
      final user = User(
        name: data['user']['name'],
        email: data['user']['email'],
        password: '', // Don't store plain passwords
      );

      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (context) => HomePage(user: user)),
      );
    } else {
      final error = jsonDecode(response.body);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(error['message'] ?? 'Signup failed')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.green.shade50,
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: SingleChildScrollView( // <- Added scroll
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              SizedBox(height: 80),
              Text('Create', style: TextStyle(fontSize: 35, fontWeight: FontWeight.bold, color: Colors.green.shade700)),
              Text('an Account!', style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold, color: Colors.green.shade300)),
              SizedBox(height: 20),
              _buildTextField(_nameController, "User Name"),
              SizedBox(height: 15),
              _buildTextField(_emailController, "Email Address"),
              SizedBox(height: 15),
              _buildTextField(_passwordController, "Password", obscureText: true),
              SizedBox(height: 15),
              _buildTextField(_confirmPasswordController, "Confirm Password", obscureText: true),
              SizedBox(height: 20),
              ElevatedButton(
                onPressed: () => _signup(context),
                child: Text('SIGN UP'),
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.green.shade300,
                  padding: EdgeInsets.symmetric(horizontal: 50, vertical: 15),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                ),
              ),
              SizedBox(height: 10),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text("Already have an account?"),
                  TextButton(
                    onPressed: () {
                      Navigator.pushReplacement(context, MaterialPageRoute(builder: (context) => login_screen()));
                    },
                    child: Text('LOGIN'),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildTextField(TextEditingController controller, String hintText, {bool obscureText = false}) {
    return Container(
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(10),
        boxShadow: [BoxShadow(color: Colors.grey.withOpacity(0.2), spreadRadius: 2, blurRadius: 5)],
      ),
      child: TextField(
        controller: controller,
        obscureText: obscureText,
        decoration: InputDecoration(
          hintText: hintText,
          border: InputBorder.none,
          contentPadding: EdgeInsets.symmetric(horizontal: 20, vertical: 15),
        ),
      ),
    );
  }
}
