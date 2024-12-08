from time import sleep

from Xlib import X, XK, display, protocol
sleep(1)
d=display.Display()
root=d.screen().root
s=d.keysym_to_keycode(XK.XK_s)
ev=protocol.event.KeyPress(time=0, root=root, window=root, same_screen=1, child=0, state=X.Mod4Mask, detail=s, root_x=0, root_y=0, event_x=0, event_y=0)
root.send_event(ev, propagate=True)
ev=protocol.event.KeyRelease(time=0, root=root, window=root, same_screen=1, child=0, state=X.Mod4Mask, detail=s, root_x=0, root_y=0, event_x=0, event_y=0)
root.send_event(ev, propagate=True)
d.sync()
d.flush()
