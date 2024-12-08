from pynput.keyboard import Key

from dotool_keys import DotoolKeys

# Key.alt_r
# Key.alt_gr
# Key.caps_lock
# Key.cmd_r
# Key.ctrl
# Key.ctrl_r
# Key.page_down
# Key.page_up
# Key.shift
# Key.shift_r
# Key.media_play_pause
# Key.media_volume_mute
# Key.media_volume_down
# Key.media_volume_up
# Key.media_previous
# Key.media_next
# Key.num_lock
# Key.print_screen
# Key.scroll_lock

key_mapping = {
    'cmd': 'leftmeta',
    'cmd_r': 'rightmeta',
    'alt': 'leftalt',
    'alt_r': 'rightalt',
    'alt_gr': 'rightalt',
    'caps_lock': 'capslock',
    'scroll_lock': 'scrolllock',
    'num_lock': 'numlock',
    'ctrl': 'leftctrl',
    'ctrl_r': 'rightctrl',
    'shift': 'leftshift',
    'shift_r': 'rightshift',
    'page_down': 'pagedown',
    'page_up': 'pageup',
    'media_play_pause': 'playpause',
    'media_volume_mute': 'mute',
    'media_volume_down': 'volumedown',
    'media_volume_up': 'volumeup',
    'media_previous': 'previoussong',
    'media_next': 'nextsong',
    'print_screen': 'print',
}


def pynput_to_dotool_key(key: Key | str) -> str:
    if isinstance(key, Key):
        key = key.name
    res = key_mapping.get(key, key)
    return res


def main():
    dotool_keys = DotoolKeys()

    for key in Key:
        if pynput_to_dotool_key(key.name) not in dotool_keys.keys:
            print(key)
        # else:
        #     print(f'{key} in dotool_keys')


if __name__ == '__main__':
    main()
