import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:gestire/dashboard.dart';
import 'constants.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:http/http.dart' as http;

final usernameController = TextEditingController();
final passwordController = TextEditingController();
final _formKey = GlobalKey<FormState>();

// Main View

class Login extends StatelessWidget {
  const Login({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final logoPath = Theme.of(context).brightness == Brightness.dark
        ? 'assets/ua-logo-dark-mode.png'
        : 'assets/ua-logo-light-mode.png';

    return Scaffold(
      body: Center(
        child: SingleChildScrollView(
          child: Padding(
            padding: const EdgeInsets.all(40.0),
            child: SizedBox(
              width: 400,
              child: Form(
                  key: _formKey,
                  child: Column(children: [
                    Image(
                      image: AssetImage(logoPath),
                      width: 320,
                    ),
                    const SizedBox(height: 130),
                    Text(
                      'Sign in to Gestire with your UA account!',
                      textAlign: TextAlign.center,
                      style: Theme.of(context).textTheme.headlineMedium,
                    ),
                    const SizedBox(height: 30),
                    TextFormField(
                      controller: usernameController,
                      keyboardType: TextInputType.emailAddress,
                      validator: (email) {
                        if (email == null || email.isEmpty) {
                          return 'Please enter your username';
                        } else if (!email.contains('@ua.pt')) {
                          return 'Please enter a valid UA email';
                        }
                        return null;
                      },
                      decoration: const InputDecoration(
                        border: OutlineInputBorder(),
                        labelText: 'Username',
                        helperText: 'Example: johndoe@ua.pt',
                      ),
                    ),
                    const SizedBox(height: 20),
                    TextFormField(
                      obscureText: true,
                      controller: passwordController,
                      validator: (password) {
                        if (password == null || password.isEmpty) {
                          return 'Please enter your password';
                        }
                        return null;
                      },
                      keyboardType: TextInputType.text,
                      decoration: const InputDecoration(
                        border: OutlineInputBorder(),
                        labelText: 'Password',
                        helperText: 'It better be a good one',
                      ),
                    ),
                    const SizedBox(height: 30),
                    SizedBox(
                      width: double.infinity,
                      child: FilledButton(
                        child: const Padding(
                          padding: EdgeInsets.all(17.0),
                          child: Text('Sign in'),
                        ),
                        onPressed: () {
                          FocusScopeNode currentFocus = FocusScope.of(context);
                          if (_formKey.currentState!.validate()) {
                            if (!currentFocus.hasPrimaryFocus) {
                              currentFocus.unfocus();
                            }
                            login().then((value) {
                              if (value) {
                                usernameController.clear();
                                passwordController.clear();
                                Navigator.pushReplacement(
                                    context,
                                    PageRouteBuilder(
                                      transitionDuration:
                                          const Duration(milliseconds: 500),
                                      pageBuilder: (context, animation,
                                              secondaryAnimation) =>
                                          FadeTransition(
                                        opacity: animation,
                                        child: const Dashboard(),
                                      ),
                                    ));
                              } else {
                                ScaffoldMessenger.of(context).showSnackBar(
                                    const SnackBar(
                                        content: Text(
                                            'Invalid username or password')));
                              }
                            });
                          }
                        },
                      ),
                    ),
                  ])),
            ),
          ),
        ),
      ),
    );
  }

  Future<bool> login() async {
    try {
      SharedPreferences sharedPreference =
          await SharedPreferences.getInstance();

      var url = Uri.http(BASE_URL, 'api/auth');
      var response = await http.post(url,
          headers: {"Content-Type": "application/json"},
          body: jsonEncode({
            "email": usernameController.text,
            "password": passwordController.text
          }));
      if (response.statusCode == 200) {
        await sharedPreference.setInt('mec', jsonDecode(response.body)['mec']);
        await sharedPreference.setString(
            'name', jsonDecode(response.body)['name']);
        await sharedPreference.setString(
            'email', jsonDecode(response.body)['email']);
        await sharedPreference.setString(
            'profile_picture', jsonDecode(response.body)['profile_picture']);
        await sharedPreference.setString(
            'token', jsonDecode(response.body)['token']);
        return true;
      } else {
        return false;
      }
    } catch (e) {
      print(e);
      return false;
    }
  }
}
