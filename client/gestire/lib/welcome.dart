import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:gestire/dashboard.dart';
import 'package:gestire/login.dart';
import 'package:gestire/constants.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;

class Welcome extends StatefulWidget {
  const Welcome({Key? key});

  @override
  State<Welcome> createState() => _WelcomeState();
}

class _WelcomeState extends State<Welcome> with SingleTickerProviderStateMixin {
  late AnimationController _animationController;
  late Animation<double> _animation;

  @override
  void initState() {
    super.initState();
    _animationController = AnimationController(
      duration: const Duration(milliseconds: 200),
      vsync: this,
    );
    _animation = CurvedAnimation(
      parent: _animationController,
      curve: Curves.easeOut,
    );

    _animationController.forward();

    // Store the BuildContext in a variable
    final currentContext = context;

    // wait for 2 seconds and then check if the user is logged in
    Future.delayed(const Duration(seconds: 2)).then((_) {
      checkToken().then((value) {
        if (value) {
          _navigateToPage(currentContext, const Dashboard());
        } else {
          _navigateToPage(currentContext, const Login());
        }
      });
    });
  }

  @override
  void dispose() {
    _animationController.dispose();
    super.dispose();
  }

  Future<void> _navigateToPage(BuildContext context, Widget page) async {
    await _animationController.reverse();
    Navigator.pushReplacement(
      context,
      PageRouteBuilder(
        transitionDuration: const Duration(milliseconds: 500),
        pageBuilder: (context, animation, secondaryAnimation) => FadeTransition(
          opacity: animation,
          child: page,
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: FadeTransition(
          opacity: _animation,
          child: const CircularProgressIndicator(),
        ),
      ),
    );
  }

  Future<bool> checkToken() async {
    SharedPreferences sharedPreference = await SharedPreferences.getInstance();
    if (sharedPreference.getString('token') == null) {
      return false;
    }

    var url = Uri.parse(API_CHECK_TOKEN_URL);
    var response = await http.post(url,
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({"token": sharedPreference.getString('token')}));
    if (response.statusCode == 200) {
      return true;
    } else {
      return false;
    }
  }
}
