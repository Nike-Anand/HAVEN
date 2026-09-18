import 'package:flutter/material.dart';
import 'package:haven_mobile/api/haven_client.dart';
import 'package:haven_mobile/screens/calculator_screen.dart';

class LegalScreen extends StatefulWidget {
  const LegalScreen({super.key});

  @override
  State<LegalScreen> createState() => _LegalScreenState();
}

class _LegalScreenState extends State<LegalScreen> {
  String _jurisdiction = 'India';
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
      // Try local canned responses first (supports India, US, UK).
      final local = _localAnswer(query, _jurisdiction);
      if (local != null) {
        if (mounted) {
          setState(() {
            _messages.add({"sender": "bot", "text": local});
          });
        }
      } else {
        final response = await HavenClient.askLegalQuestion(query, language: 'en');
        if (mounted) {
          setState(() {
            _messages.add({"sender": "bot", "text": response['response'] ?? "I could not find an answer."});
          });
        }
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

  String? _localAnswer(String query, String jurisdiction) {
    final q = query.toLowerCase();
    final india = {
      'emergency': 'Emergency numbers in India: Police/Ambulance — 112. Women helpline — 181. For immediate danger call 112.',
      'protection': 'In India you can apply for a protection order under the Protection of Women from Domestic Violence Act; contact the local police or a protection officer for help filing an application.',
      'fir': 'To report serious abuse, you can file an FIR at your local police station. If unsure, call 112 or the local women\'s helpline for guidance.'
    };
    final us = {
      'emergency': 'Emergency: 911. Many states have domestic violence hotlines and restraining orders (protective orders) — contact local police for immediate help.',
      'protection': 'In the US you can seek a protection/restraining order from a civil court — the process varies by state but law enforcement or a local domestic violence organisation can assist.',
    };
    final uk = {
      'emergency': 'Emergency: 999. National Domestic Abuse Helpline (England) — 0808 2000 247. If in immediate danger call 999.',
      'protection': 'In the UK you can apply for non-molestation or occupation orders through family courts; local domestic violence services and police can guide you.'
    };

    final map = {
      'India': india,
      'US': us,
      'UK': uk,
    };

    final rules = map[jurisdiction] ?? india;

    if (q.contains('emergency') || q.contains('help') || q.contains('police') || q.contains('ambulance')) return rules['emergency'];
    if (q.contains('protection') || q.contains('order') || q.contains('restrain')) return rules['protection'];
    if (q.contains('fir') || q.contains('report') || q.contains('file')) return rules['fir'] ?? rules['protection'];

    return null;
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
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
            child: Row(
              children: [
                const Text('Jurisdiction: ', style: TextStyle(fontWeight: FontWeight.bold)),
                const SizedBox(width: 8.0),
                DropdownButton<String>(
                  value: _jurisdiction,
                  items: const [
                    DropdownMenuItem(value: 'India', child: Text('India')),
                    DropdownMenuItem(value: 'US', child: Text('US')),
                    DropdownMenuItem(value: 'UK', child: Text('UK')),
                  ],
                  onChanged: (v) {
                    if (v != null) setState(() => _jurisdiction = v);
                  },
                ),
              ],
            ),
          ),
          const Divider(height: 1),
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
