import 'package:flutter/material.dart';
import './home_page.dart';
import '../widgets/wood_background.dart';

class TopPage extends StatelessWidget {
  const TopPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('麻雀記録'),
        backgroundColor: Colors.black.withOpacity(0.5),
      ),
      body: WoodBackground(
        child: Center(
          child: Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                ElevatedButton.icon(
                  icon: const Icon(Icons.login),
                  onPressed: () {
                    // TODO: Implement Google Sign In
                  },
                  label: const Text('Googleでログイン'),
                ),
                const SizedBox(height: 16),
                ElevatedButton.icon(
                  icon: const Icon(Icons.apple),
                  onPressed: () {
                    // TODO: Implement Apple Sign In
                  },
                  label: const Text('Appleでログイン'),
                ),
                const SizedBox(height: 16),
                ElevatedButton.icon(
                  icon: const Icon(Icons.email),
                  onPressed: () {
                    // TODO: Implement Email/Password Sign In
                  },
                  label: const Text('メールアドレスでログイン'),
                ),
                const SizedBox(height: 32),
                TextButton(
                  onPressed: () {
                    Navigator.of(context).pushReplacement(
                      MaterialPageRoute(builder: (context) => const HomePage()),
                    );
                  },
                  child: const Text('ログインせずに続ける'),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
