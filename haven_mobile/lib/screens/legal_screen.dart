import 'package:flutter/material.dart';
import 'package:haven_mobile/api/haven_client.dart';

class LegalScreen extends StatefulWidget {
  const LegalScreen({Key? key}) : super(key: key);

  @override
  State<LegalScreen> createState() => _LegalScreenState();
}

class _LegalScreenState extends State<LegalScreen> {
  final TextEditingController _controller = TextEditingController();
  final List<Map<String, String>> _messages = [
    {
      "sender": "bot",
      "text": "Welcome to HAVEN Legal Guidance. Ask me about Indian women's rights, domestic violence laws, or workplace harassment."
    }
  ];
  bool _isLoading = false;

  Future<void> _askQuestion() async {
    if (_controller.text.trim().isEmpty) return;

    final query = _controller.text;
    setState(() {
      _messages.add({"sender": "user", "text": query});
      _controller.clear();
      _isLoading = true;
    });

    try {
      final response = await HavenClient.askLegalQuestion(query);
      if (mounted) {
        setState(() {
          _messages.add({"sender": "bot", "text": response['response'] ?? "I could not find an answer."});
        });
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          _messages.add({"sender": "bot", "text": "Error getting legal guidance."});
        });
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
        title: const Text('Legal Guidance'),
        backgroundColor: const Color(0xFF1f2d3d),
        foregroundColor: Colors.white,
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.all(16.0),
              itemCount: _messages.length,
              itemBuilder: (context, index) {
                final isUser = _messages[index]['sender'] == 'user';
                return Align(
                  alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
                  child: Container(
                    margin: const EdgeInsets.symmetric(vertical: 4.0),
                    padding: const EdgeInsets.all(16.0),
                    decoration: BoxDecoration(
                      color: isUser ? Colors.purple[100] : Colors.grey[200],
                      borderRadius: BorderRadius.circular(12.0),
                      border: isUser ? null : Border.all(color: Colors.grey[400]!),
                    ),
                    child: Text(
                      _messages[index]['text']!,
                      style: const TextStyle(fontSize: 15),
                    ),
                  ),
                );
              },
            ),
          ),
          if (_isLoading)
            const Padding(
              padding: EdgeInsets.all(8.0),
              child: CircularProgressIndicator(color: Colors.purple),
            ),
          Container(
            padding: const EdgeInsets.all(8.0),
            color: Colors.white,
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _controller,
                    decoration: const InputDecoration(
                      hintText: 'Ask a legal question...',
                      border: OutlineInputBorder(),
                    ),
                    onSubmitted: (_) => _askQuestion(),
                  ),
                ),
                const SizedBox(width: 8.0),
                IconButton(
                  icon: const Icon(Icons.gavel, color: Colors.purple),
                  onPressed: _askQuestion,
                )
              ],
            ),
          )
        ],
      ),
    );
  }
}
