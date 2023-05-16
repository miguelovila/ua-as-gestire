import 'package:flutter/material.dart';

final usernameController = TextEditingController();
final passwordController = TextEditingController();
final _formKey = GlobalKey<FormState>();

// Individual Elememts

class ObscuredTextField extends StatelessWidget {
  const ObscuredTextField({super.key});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(left: 20, right: 20, bottom: 20),
      child: SizedBox(
        width: 300,
        child: TextFormField(
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
      ),
    );
  }
}

class NormalTextField extends StatelessWidget {
  const NormalTextField({super.key});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(left: 20, right: 20, bottom: 20, top: 30),
      child: SizedBox(
        width: 300,
        child: TextFormField(
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
      ),
    );
  }
}

class TitleText extends StatelessWidget {
  const TitleText({super.key});

  @override
  Widget build(BuildContext context) {
    return const SizedBox(
      width: 300,
      child: Text(
        'Sign in to Gestire with your UA account!',
        textAlign: TextAlign.center,
        style: TextStyle(
          fontSize: 25,
          fontWeight: FontWeight.bold,
        ),
      ),
    );
  }
}

class CustomUaLogo extends StatelessWidget {
  const CustomUaLogo({super.key});

  @override
  Widget build(BuildContext context) {
    final isDarkMode = Theme.of(context).brightness == Brightness.dark;
    return Image(
      image: AssetImage(isDarkMode
          ? 'assets/ua-logo-dark-mode.png'
          : 'assets/ua-logo-light-mode.png'),
      width: 400,
    );
  }
}

class CustomButton extends StatelessWidget {
  const CustomButton({Key? key, required this.text}) : super(key: key);

  final String text;

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 300,
      child: ElevatedButton(
        child: Padding(
          padding: const EdgeInsets.all(13.0),
          child: Text(text),
        ),
        onPressed: () {},
      ),
    );
  }
}

// Main View

class Login extends StatelessWidget {
  const Login({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: SingleChildScrollView(
          child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                const CustomUaLogo(),
                const TitleText(),
                Form(
                    key: _formKey,
                    child: Column(children: const [
                      NormalTextField(),
                      ObscuredTextField(),
                      CustomButton(text: 'Sign in'),
                    ]))
              ]),
        ),
      ),
    );
  }
}
