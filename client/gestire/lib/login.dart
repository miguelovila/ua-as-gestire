import 'package:flutter/material.dart';

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
                      width: 350,
                    ),
                    const SizedBox(height: 100),
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
                        helperText: 'johndoe@ua.pt',
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
                      ),
                    ),
                    const SizedBox(height: 20),
                    SizedBox(
                      width: double.infinity,
                      child: FilledButton(
                        child: const Padding(
                          padding: EdgeInsets.all(17.0),
                          child: Text('Sign in'),
                        ),
                        onPressed: () {
                          if (_formKey.currentState!.validate()) {
                            ScaffoldMessenger.of(context).showSnackBar(
                              const SnackBar(
                                content: Text('Processing Data'),
                              ),
                            );
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
