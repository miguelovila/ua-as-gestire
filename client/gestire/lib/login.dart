import 'package:flutter/material.dart';
import 'package:gestire/dashboard.dart';

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
                          if (_formKey.currentState!.validate()) {
                            // show a loading indicator and wait two seconds
                            showDialog(
                              context: context,
                              barrierDismissible: false,
                              builder: (context) {
                                return WillPopScope(
                                  onWillPop: () async => false,
                                  child: const AlertDialog(
                                    content: SizedBox(
                                      height: 100,
                                      child: Center(
                                        child: CircularProgressIndicator(),
                                      ),
                                    ),
                                  ),
                                );
                              },
                            );
                            Future.delayed(const Duration(seconds: 2), () {
                              // close the dialog and navigate to the home page
                              Navigator.pop(context);
                              if (usernameController.text == 'admin@ua.pt') {
                                Navigator.pushReplacement(
                                    context,
                                    MaterialPageRoute(
                                        builder: (context) =>
                                            const Dashboard()));
                              } else {
                                usernameController.clear();
                                passwordController.clear();
                                ScaffoldMessenger.of(context).showSnackBar(
                                  const SnackBar(
                                    content:
                                        Text('Invalid username or password!'),
                                  ),
                                );
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
}
