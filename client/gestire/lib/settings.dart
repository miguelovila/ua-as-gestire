import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

class Settings extends StatefulWidget {
  const Settings({Key? key}) : super(key: key);

  @override
  _SettingsState createState() => _SettingsState();
}

class _SettingsState extends State<Settings> {
  late SharedPreferences _sharedPreferences;
  String _name = '';
  int _mec = 0;
  String _token = '';
  String _email = '';
  String _profilePicture = '';

  @override
  void initState() {
    super.initState();
    _loadUserInformation();
  }

  Future<void> _loadUserInformation() async {
    _sharedPreferences = await SharedPreferences.getInstance();
    setState(() {
      _name = _sharedPreferences.getString('name') ?? '';
      _mec = _sharedPreferences.getInt('mec') ?? 0;
      _token = _sharedPreferences.getString('token') ?? '';
      _email = _sharedPreferences.getString('email') ?? '';
      _profilePicture = _sharedPreferences.getString('profile_picture') ?? '';
    });
  }

  Future<void> _logout() async {
    // Clear the shared preferences
    await _sharedPreferences.clear();
    // Navigate to the login page or any other desired page
    // Here, we assume there's a LoginPage widget defined
    Navigator.pushReplacement(
        context, MaterialPageRoute(builder: (_) => LoginPage()));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Settings'),
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'Name: $_name',
                style: Theme.of(context).textTheme.headline6,
              ),
              const SizedBox(height: 8.0),
              Text(
                'MEC: $_mec',
                style: Theme.of(context).textTheme.bodyText1,
              ),
              const SizedBox(height: 8.0),
              Text(
                'Token: $_token',
                style: Theme.of(context).textTheme.bodyText1,
              ),
              const SizedBox(height: 8.0),
              Text(
                'Email: $_email',
                style: Theme.of(context).textTheme.bodyText1,
              ),
              const SizedBox(height: 16.0),
              if (_profilePicture.isNotEmpty)
                Image.network(
                  _profilePicture,
                  width: 100,
                  height: 100,
                ),
              const SizedBox(height: 16.0),
              ElevatedButton(
                onPressed: _logout,
                child: const Text('Logout'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class LoginPage extends StatelessWidget {
  const LoginPage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Login'),
      ),
      body: Center(
        child: ElevatedButton(
          onPressed: () {
            // Perform login logic here
            // After successful login, navigate to the SettingsPage
            Navigator.pushReplacement(
                context, MaterialPageRoute(builder: (_) => Settings()));
          },
          child: const Text('Login'),
        ),
      ),
    );
  }
}
