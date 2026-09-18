import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  final _storage = const FlutterSecureStorage();
  final TextEditingController _pinController = TextEditingController();
  String _status = '';

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    final v = await _storage.read(key: 'decoy_pin') ?? '8080=';
    _pinController.text = v;
  }

  Future<void> _save() async {
    final v = _pinController.text.trim();
    if (v.isEmpty) return;
    await _storage.write(key: 'decoy_pin', value: v);
    setState(() => _status = 'Saved');
    await Future.delayed(const Duration(seconds: 1));
    if (mounted) setState(() => _status = '');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Settings'),
        backgroundColor: const Color(0xFF1f2d3d),
        foregroundColor: Colors.white,
      ),
      body: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          children: [
            const Text('Change decoy PIN (enter sequence including =):'),
            const SizedBox(height: 12),
            TextField(controller: _pinController, decoration: const InputDecoration(border: OutlineInputBorder())),
            const SizedBox(height: 12),
            ElevatedButton(onPressed: _save, child: const Text('Save PIN')),
            const SizedBox(height: 12),
            Text(_status, style: const TextStyle(color: Colors.green)),
          ],
        ),
      ),
    );
  }
}
