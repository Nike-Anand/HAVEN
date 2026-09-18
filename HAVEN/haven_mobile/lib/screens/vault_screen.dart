import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:haven_mobile/api/haven_client.dart';

class VaultScreen extends StatefulWidget {
  const VaultScreen({super.key});

  @override
  State<VaultScreen> createState() => _VaultScreenState();
}

class _VaultScreenState extends State<VaultScreen> {
  final ImagePicker _picker = ImagePicker();
  final TextEditingController _textController = TextEditingController();
  
  bool _isLoading = false;
  Uint8List? _encodedImageBytes;
  String _extractedText = '';

  Future<void> _hideData() async {
    if (_textController.text.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Please enter text to hide.')),
      );
      return;
    }

    final XFile? image = await _picker.pickImage(source: ImageSource.gallery);
    if (image == null) return;

    setState(() {
      _isLoading = true;
      _encodedImageBytes = null;
    });

    try {
      final bytes = await image.readAsBytes();
      final resultBytes = await HavenClient.hideDataInImage(bytes, _textController.text);
      
      if (mounted) {
        setState(() {
          _encodedImageBytes = Uint8List.fromList(resultBytes);
          _textController.clear();
        });
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Data hidden successfully! Right-click image to save.')),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error: $e'), backgroundColor: Colors.red),
        );
      }
    } finally {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }

  Future<void> _extractData() async {
    final XFile? image = await _picker.pickImage(source: ImageSource.gallery);
    if (image == null) return;

    setState(() {
      _isLoading = true;
      _extractedText = '';
    });

    try {
      final bytes = await image.readAsBytes();
      final text = await HavenClient.extractDataFromImage(bytes);
      
      if (mounted) {
        setState(() {
          _extractedText = text;
        });
        if (text.isEmpty) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('No hidden data found in this image.')),
          );
        } else {
           showDialog(
             context: context,
             builder: (context) => AlertDialog(
               title: const Text('Hidden Data Found'),
               content: Text(text),
               actions: [
                 TextButton(
                   onPressed: () => Navigator.pop(context),
                   child: const Text('Close'),
                 )
               ],
             )
           );
        }
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error: $e'), backgroundColor: Colors.red),
        );
      }
    } finally {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Secure Vault'),
        backgroundColor: const Color(0xFF1f2d3d),
        foregroundColor: Colors.white,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Icon(Icons.security, size: 80, color: Colors.blueGrey),
            const SizedBox(height: 20),
            const Text(
              'Steganography Engine',
              textAlign: TextAlign.center,
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            const Text(
              'Hide or extract secret data invisibly inside image files.',
              textAlign: TextAlign.center,
              style: TextStyle(fontSize: 14, color: Colors.grey),
            ),
            const SizedBox(height: 40),
            
            // HIDE SECTION
            const Text('Hide Data', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 10),
            TextField(
              controller: _textController,
              maxLines: 3,
              decoration: const InputDecoration(
                hintText: 'Enter secret text to hide...',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 10),
            ElevatedButton.icon(
              icon: const Icon(Icons.lock),
              label: const Text('Pick Image & Hide Data'),
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color(0xFF1f2d3d),
                foregroundColor: Colors.white,
              ),
              onPressed: _isLoading ? null : _hideData,
            ),
            
            if (_encodedImageBytes != null) ...[
              const SizedBox(height: 20),
              const Text('Resulting Image (Data is hidden inside):', style: TextStyle(fontWeight: FontWeight.bold)),
              const SizedBox(height: 10),
              Image.memory(_encodedImageBytes!, height: 200),
            ],
            
            const Divider(height: 60, thickness: 2),
            
            // EXTRACT SECTION
            const Text('Extract Data', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 10),
            ElevatedButton.icon(
              icon: const Icon(Icons.lock_open),
              label: const Text('Pick Image & Extract Data'),
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.blueGrey,
                foregroundColor: Colors.white,
              ),
              onPressed: _isLoading ? null : _extractData,
            ),
            
            if (_isLoading)
              const Padding(
                padding: EdgeInsets.all(32.0),
                child: Center(child: CircularProgressIndicator()),
              ),
          ],
        ),
      ),
    );
  }
}
