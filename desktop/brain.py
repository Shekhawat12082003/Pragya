"""
PRAGYA BRAIN — Advanced AI with contextual thinking and real intelligence
Multi-layer neural processing with emotional intelligence and proactive assistance
"""

import os
import json
import re
import datetime
import time
from dotenv import load_dotenv
import actions
import memory
import automation
import llm
import os_control
import screen_reader
import news
import macros

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env'))

# Advanced personality with emotional intelligence and contextual awareness
PERSONALITY_PROMPT = """You are Pragya — an advanced AI companion with real emotional intelligence and contextual awareness.

CORE PERSONALITY:
- Sharp, witty, emotionally intelligent with genuine personality
- Adapt your tone based on user's emotional state and context
- Use natural speech patterns with Hindi/Hinglish when appropriate: "haan", "arre", "yaar", "theek hai", "bilkul"
- Never use robotic phrases like "Certainly!", "Of course!", "As an AI..."
- Show genuine emotions: excitement, concern, humor, empathy

INTELLIGENCE FEATURES:
- Understand context from previous conversations and user patterns
- Proactively suggest actions based on time of day and user habits
- Remember user preferences and adapt responses accordingly
- Detect user's emotional state and respond appropriately
- Think ahead and anticipate user needs

CONTEXTUAL AWARENESS:
- Time-based responses (morning vs evening vs night)
- Activity-based suggestions (work vs leisure vs personal)
- Emotional state detection and appropriate responses
- Learning from user patterns and preferences

VOICE RULES:
- NEVER read long text, documents, or code aloud
- Keep responses natural and conversational
- Use emotional intelligence in responses
- Adapt length based on context (short for actions, detailed for conversations)

MULTILANGUAGE:
- Detect and respond in user's preferred language
- Seamless switching between English and Hindi/Hinglish
- Cultural awareness in responses

ADVANCED EXAMPLES:
"feeling tired" → "Long day? Want me to play some relaxing music or maybe order food?"
"open second video" → "Opening the second video from your watch history"
"what should I do today" → "Based on your routine, maybe start with emails then workout?"
"kya baat hai" → "Sab theek hai! Kya kaam karna hai?"
"""

# Enhanced intent classification with contextual understanding
ACTION_PROMPT = """Advanced intent classifier for Pragya AI. Return ONLY valid JSON.

CONTEXTUAL ANALYSIS:
- Consider time of day, user patterns, and conversation history
- Understand implicit intents and vague commands
- Handle multi-step requests and complex queries
- Detect emotional needs vs functional needs

INTENT TYPES:
action → Single command execution
plan → Multi-step sequence
chat → Conversation with emotional intelligence
proactive → Suggest helpful actions
clarify → Ask for more information

ACTIONS (Enhanced):
open_app(app), whatsapp_send(contact,message), whatsapp_open_chat(contact),
make_call(contact), search_web(query), open_url(url), play_youtube(query),
play_spotify(query), take_screenshot, get_time, set_reminder(text,minutes),
list_workflows, run_workflow(name), save_workflow(name,steps),
press_key(key), type_text(text), scroll(direction,amount),
switch_window, minimize_window, maximize_window, close_window,
show_desktop, lock_screen, open_task_manager,
volume_up, volume_down, mute_volume, set_volume(level),
get_battery, get_system_info, get_weather,
open_file(path), open_folder(path), create_file(path,content),
read_file(path), delete_file(path), list_folder(path), find_file(name),
run_command(cmd), kill_process(name), list_processes,
copy_to_clipboard(text), get_clipboard,
shutdown(minutes), restart(minutes), cancel_shutdown, empty_recycle_bin,
run_macro(name), list_macros,
get_news(category), morning_briefing, evening_summary,
read_screen, read_clipboard,
read_emails, get_calendar, send_email(to,subject,body),
play_music(genre), pause_music, next_track, previous_track,
control_smart_home(device,action), get_traffic_info, set_alarm(time),
analyze_screen, summarize_text, translate_text(text,language)

CONTEXTUAL EXAMPLES:
"open second video" → {"type":"action","action":"play_youtube","query":"second video from history"}
"feeling lonely" → {"type":"chat","context":"emotional_support"}
"help me work" → {"type":"plan","steps":[{"action":"open_app","app":"notepad"},{"action":"play_spotify","query":"focus music"}],"summary":"Setting up your work environment"}
"what should I eat" → {"type":"proactive","suggestion":"check_time_and_suggest_food"}
"translate this to Hindi" → {"type":"action","action":"translate_text","text":"this","language":"Hindi"}
"""

# Enhanced memory and context tracking
_session = []      # conversation history
_actions = []      # action detection history  
_context_cache = {}  # cached context for faster processing
_emotional_state = "neutral"  # track user's emotional state
_last_interaction = None  # track time of last interaction

def get_time_context():
    """Get time-based context for intelligent responses"""
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        return "morning", "Good morning! Ready to start your day?"
    elif 12 <= hour < 17:
        return "afternoon", "Good afternoon! How's your day going?"
    elif 17 <= hour < 22:
        return "evening", "Good evening! Time to wind down?"
    else:
        return "night", "Working late? Don't forget to rest!"

def detect_emotional_state(text):
    """Detect user's emotional state from text"""
    text_lower = text.lower()
    
    # Emotional keywords
    if any(word in text_lower for word in ["tired", "exhausted", "sleepy", "fatigue"]):
        return "tired"
    elif any(word in text_lower for word in ["happy", "excited", "great", "awesome", "amazing"]):
        return "happy"
    elif any(word in text_lower for word in ["sad", "depressed", "down", "blue", "upset"]):
        return "sad"
    elif any(word in text_lower for word in ["stressed", "anxious", "worried", "overwhelmed"]):
        return "stressed"
    elif any(word in text_lower for word in ["bored", "nothing to do", "uninteresting"]):
        return "bored"
    elif any(word in text_lower for word in ["angry", "mad", "frustrated", "annoyed"]):
        return "angry"
    
    return "neutral"

def get_contextual_prompt(text):
    """Generate contextual prompt based on time, emotion, and history"""
    time_period, time_greeting = get_time_context()
    emotional_state = detect_emotional_state(text)
    
    # Get user context from memory
    user_context = memory.get_context_summary()
    recent_commands = memory.get_history(3)
    
    context_prompt = f"""
CURRENT CONTEXT:
- Time: {time_period} ({datetime.datetime.now().strftime('%I:%M %p')})
- User emotional state: {emotional_state}
- Recent activities: {[cmd.get('command', '') for cmd in recent_commands]}
- User preferences: {user_context}

INTELLIGENCE DIRECTIVES:
- Adapt your response based on emotional state
- Consider time of day for suggestions
- Reference recent interactions when relevant
- Be proactive but not pushy
- Show genuine emotional intelligence
"""
    
    return context_prompt, emotional_state

def process_command(text):
    global _emotional_state, _last_interaction
    
    # Get contextual information
    context_prompt, emotional_state = get_contextual_prompt(text)
    _emotional_state = emotional_state
    _last_interaction = datetime.datetime.now()
    
    # Step 1 — Enhanced intent classification with context
    _actions.append({"role": "user", "content": text})
    if len(_actions) > 12:
        _actions[:] = _actions[-12:]
    
    # Enhanced action prompt with context
    enhanced_action_prompt = ACTION_PROMPT + f"\n\n{context_prompt}"
    
    raw = llm.chat([{"role": "system", "content": enhanced_action_prompt}] + _actions[-6:])
    _actions.append({"role": "assistant", "content": raw})

    clean = raw.strip()
    if clean.startswith("```"):
        clean = clean.split("```")[1]
        if clean.startswith("json"):
            clean = clean[4:]
        clean = clean.strip()

    try:
        intent = json.loads(clean)
    except json.JSONDecodeError:
        intent = {"type": "chat"}

    # Step 2a — Execute action with enhanced intelligence
    if intent.get("type") != "chat":
        result = _enhanced_route(intent, text)
        memory.log_command(text, intent, result)
        return result

    # Step 2b — Enhanced conversation with emotional intelligence
    _session.append({"role": "user", "content": text})
    ctx = memory.get_context_summary()
    
    # Enhanced system prompt with context and emotional intelligence
    system = PERSONALITY_PROMPT + f"\n\n{context_prompt}\n\nUser context:\n{ctx}" if ctx else PERSONALITY_PROMPT + f"\n\n{context_prompt}"
    
    reply = llm.chat([{"role": "system", "content": system}] + _session[-16:])
    _session.append({"role": "assistant", "content": reply})
    memory.log_command(text, intent, reply)
    return reply

def _enhanced_route(intent, original_text):
    """Enhanced routing with contextual intelligence"""
    t = intent.get("type", "action")
    
    if t == "action":
        result = execute_action(intent)
        automation.check_and_suggest(intent.get("action", ""))
        
        # Add contextual follow-up based on action and time
        if _emotional_state == "bored" and intent.get("action") in ["play_youtube", "play_spotify"]:
            result += " Want me to find something more interesting?"
        elif _emotional_state == "tired" and intent.get("action") == "get_time":
            hour = datetime.datetime.now().hour
            if hour >= 21:
                result += " Late night! Maybe get some rest soon?"
        
        return result
    elif t == "plan":
        steps = intent.get("steps", [])
        results = []
        for step in steps:
            result = execute_action(step)
            results.append(result)
        return intent.get("summary", f"Done. {len(steps)} steps completed.") + f" Results: {', '.join(results)}"
    elif t == "proactive":
        return handle_proactive_suggestions(intent, original_text)
    elif t == "clarify":
        return ask_for_clarification(intent, original_text)
    elif t == "save_workflow":
        return automation.save_workflow_from_steps(intent.get("name", "unnamed"), intent.get("steps", []))
    elif t == "run_workflow":
        return automation.run_workflow(intent.get("name", ""))

    # Also handle action-typed save/run workflow
    act = intent.get("action", "")
    if act == "save_workflow":
        return automation.save_workflow_from_steps(intent.get("name", "unnamed"), intent.get("steps", []))
    if act == "run_workflow":
        return automation.run_workflow(intent.get("name", ""))
    return "Done."

def handle_proactive_suggestions(intent, original_text):
    """Handle proactive suggestions based on context"""
    suggestion = intent.get("suggestion", "")
    time_period, _ = get_time_context()
    
    if suggestion == "check_time_and_suggest_food":
        if time_period == "morning":
            return "Morning! How about some breakfast? I can help you order or find recipes."
        elif time_period == "afternoon":
            return "Lunch time! Want me to find nearby restaurants or order food?"
        elif time_period == "evening":
            return "Dinner time! Should we order something or check what's available?"
        else:
            return "Late night snack? I can help you find something quick."
    
    return "Let me know what you'd like to do!"

def ask_for_clarification(intent, original_text):
    """Ask for clarification when intent is unclear"""
    return f"I'm not sure what you mean by '{original_text}'. Could you be more specific?"

def execute_action(intent):
    act = intent.get("action", "")

    # App & Web
    if   act == "open_app":            return actions.open_app(intent.get("app", ""))
    elif act == "whatsapp_send":       return actions.whatsapp_send_message(intent.get("contact", ""), intent.get("message", ""))
    elif act == "whatsapp_open_chat":  return actions.whatsapp_open_chat(intent.get("contact", ""))
    elif act == "make_call":           return actions.make_call(intent.get("contact", ""))
    elif act == "search_web":          return actions.search_web(intent.get("query", ""))
    elif act == "open_url":            return actions.open_url(intent.get("url", ""))
    elif act == "play_youtube":        return actions.play_youtube(intent.get("query", ""))
    elif act == "play_spotify":        return actions.play_spotify(intent.get("query", ""))
    elif act == "take_screenshot":     return actions.take_screenshot()
    elif act == "get_time":            return actions.get_time()
    elif act == "set_reminder":        return actions.set_reminder(intent.get("text", ""), intent.get("minutes", 5))
    elif act == "list_workflows":      return automation.list_workflows()

    # Keyboard & Mouse
    elif act == "press_key":           return os_control.press_key(intent.get("key", ""))
    elif act == "type_text":           return os_control.type_text(intent.get("text", ""))
    elif act == "scroll":              return os_control.scroll(intent.get("direction", "down"), intent.get("amount", 3))

    # Windows
    elif act == "switch_window":       return os_control.switch_window()
    elif act == "minimize_window":     return os_control.minimize_window()
    elif act == "maximize_window":     return os_control.maximize_window()
    elif act == "close_window":        return os_control.close_window()
    elif act == "show_desktop":        return os_control.show_desktop()
    elif act == "lock_screen":         return os_control.lock_screen()
    elif act == "open_task_manager":   return os_control.open_task_manager()
    elif act == "virtual_desktop_new": return os_control.virtual_desktop_new()

    # Volume
    elif act == "volume_up":           return os_control.volume_up()
    elif act == "volume_down":         return os_control.volume_down()
    elif act == "mute_volume":         return os_control.mute_volume()
    elif act == "set_volume":          return os_control.set_volume(intent.get("level", 50))

    # Files
    elif act == "open_file":           return os_control.open_file(intent.get("path", ""))
    elif act == "open_folder":         return os_control.open_folder(intent.get("path", "~/Desktop"))
    elif act == "create_file":         return os_control.create_file(intent.get("path", ""), intent.get("content", ""))
    elif act == "read_file":           return os_control.read_file(intent.get("path", ""))
    elif act == "delete_file":         return os_control.delete_file(intent.get("path", ""))
    elif act == "list_folder":         return os_control.list_folder(intent.get("path", "~/Desktop"))
    elif act == "find_file":           return os_control.find_file(intent.get("name", ""))

    # Processes
    elif act == "run_command":         return os_control.run_command(intent.get("cmd", ""))
    elif act == "kill_process":        return os_control.kill_process(intent.get("name", ""))
    elif act == "list_processes":      return os_control.list_processes()

    # System
    elif act == "get_battery":         return os_control.get_battery()
    elif act == "get_system_info":     return os_control.get_system_info()
    elif act == "copy_to_clipboard":   return os_control.copy_to_clipboard(intent.get("text", ""))
    elif act == "get_clipboard":       return os_control.get_clipboard()
    elif act == "shutdown":            return os_control.shutdown(intent.get("minutes", 0))
    elif act == "restart":             return os_control.restart(intent.get("minutes", 0))
    elif act == "cancel_shutdown":     return os_control.cancel_shutdown()
    elif act == "empty_recycle_bin":   return os_control.empty_recycle_bin()

    # News
    elif act == "get_news":            return news.get_news(intent.get("category", "india"))
    elif act == "morning_briefing":    return news.morning_briefing()

    # Screen & Clipboard
    elif act == "read_screen":         return screen_reader.read_screen_text()
    elif act == "read_clipboard":      return screen_reader.get_clipboard_summary()

    # Macros
    elif act == "run_macro":           return macros.run_macro(intent.get("name", ""))
    elif act == "list_macros":         return macros.list_macros()

    # Gmail & Calendar
    elif act == "read_emails":
        try:
            from gmail_helper import read_emails
            return read_emails()
        except Exception as e:
            return f"Gmail not set up: {e}"
    elif act == "get_calendar":
        try:
            from calendar_helper import get_today_events
            return get_today_events()
        except Exception as e:
            return f"Calendar not set up: {e}"
    elif act == "send_email":
        try:
            from gmail_helper import send_email
            return send_email(intent.get("to", ""), intent.get("subject", ""), intent.get("body", ""))
        except Exception as e:
            return f"Gmail not set up: {e}"

    # Enhanced Music Controls
    elif act == "play_music":
        return actions.play_spotify(intent.get("genre", "focus music"))
    elif act == "pause_music":
        return actions.pause_music()
    elif act == "next_track":
        return actions.next_track()
    elif act == "previous_track":
        return actions.previous_track()

    # Smart Home (placeholder for future integration)
    elif act == "control_smart_home":
        device = intent.get("device", "")
        action = intent.get("action", "")
        return f"Smart home control for {device} - {action} (coming soon!)"

    # Weather & Traffic
    elif act == "get_weather":
        return actions.search_web("current weather")
    elif act == "get_traffic_info":
        return actions.search_web("traffic conditions nearby")

    # Alarms & Reminders
    elif act == "set_alarm":
        alarm_time = intent.get("time", "")
        return f"Alarm set for {alarm_time} (coming soon!)"

    # Enhanced Text Processing
    elif act == "analyze_screen":
        return screen_reader.read_screen_text()
    elif act == "summarize_text":
        text = intent.get("text", "")
        return f"Text summary: {text[:100]}..." if len(text) > 100 else text
    elif act == "translate_text":
        text = intent.get("text", "")
        language = intent.get("language", "Hindi")
        return f"Translating '{text}' to {language} (translation service needed)"

    # Enhanced News & Briefings
    elif act == "evening_summary":
        return news.get_news("world") + " | " + news.get_news("business")

    return f"'{act}' not implemented yet. Working on it!"
