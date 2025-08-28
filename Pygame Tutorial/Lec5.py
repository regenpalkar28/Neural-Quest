# Filtering events
# my_event = pygame.event.Event(KEYDOWN, key=K_SPACE, mod=0, unicode=u'')
#   - pgame.event.post(my_event)

# my_event = pygame.event.Event(KEYDOWN, {"key":K_SPACE, "mod":0, "unicode":u''})

# CATONKEYBOARD = USEREVENT+1
# my_event = pygame.event.Event(CATONKEYBOARD, message="Bad cat!")
#   pgame.event.post(my_event)

# for event in pygame.event.get():
#   if event.type == CATONKEYBOARD:
#       print(event.message)
