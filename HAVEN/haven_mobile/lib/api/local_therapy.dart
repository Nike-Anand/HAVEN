class LocalTherapy {
  // Minimal offline therapy responses mirroring backend intents.
  static String generateResponse(String message) {
    final text = message.toLowerCase();
    if (text.contains('suicide') || text.contains('kill myself') || text.contains('end my life')) {
      return "I'm really sorry you're feeling this way. Please contact local emergency services or a hotline immediately. You are not alone.";
    }
    if (text.contains('hit') || text.contains('abuse') || text.contains('beating') || text.contains('hurt')) {
      return "What is happening to you is not your fault. If you're in immediate danger try to get to a safer place and call emergency services.";
    }
    if (text.contains('scared') || text.contains('afraid') || text.contains('panic')) {
      return "I hear that you're scared. Try a grounding exercise: 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, 1 you can taste.";
    }
    if (text.contains('alone') || text.contains('lonely')) {
      return "You are not alone. If you can, reach out to one person you trust. Would you like some helplines or resources?";
    }
    // Default supportive reply
    return "I'm here with you. Tell me a bit more about how you're feeling or what happened, and we can make a small plan together.";
  }
}
