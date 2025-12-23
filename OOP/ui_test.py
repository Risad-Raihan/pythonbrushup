from ui import *

render_header()
q = prompt_user_question()
render_thinking()
render_short_answer("This is a fake short answer just to test the UI layout.")
choice = ask_decision()
print("You chose:", choice)
