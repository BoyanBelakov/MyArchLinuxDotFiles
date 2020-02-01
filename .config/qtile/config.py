# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile.config import Key, Screen, Group, Match, Drag, Click, hook
from libqtile.command import lazy
from libqtile import layout, bar, widget

from typing import List  # noqa: F401

import os
import subprocess

# Hooks
@hook.subscribe.startup_once
def autostart():
    script = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([script]) 


# mod4 normally is Window key
mod = 'mod4'

# control key
ctrl = 'control'

colors = {
    'bg': '#252932',
    'active': '#ebcb8b',
    'inactive': '#c0c5ce',
    'highlight': '#3b3f47',
    'focus': '#1ec4d9',
    'fg1': '#bf616a',
    'fg2': '#a3be8c',
}

keys = [
    # Switch between windows in current stack pane
    Key([mod], 'j', lazy.layout.up()),
    Key([mod], 'k', lazy.layout.down()),

    # Switch window focus to other pane(s) of stack
    Key([mod], 'space', lazy.layout.next()),
    
    # Start xterm 
    Key([mod], 'Return', lazy.spawn('xterm')),

    # Toggle between different layouts
    Key([mod], 'Tab', lazy.next_layout()),
    
    # Close window
    Key([mod], 'w', lazy.window.kill()),

    # Restart qtile with new config
    Key([mod, ctrl], 'r', lazy.restart()),

    # Shutdown
    Key([mod, ctrl], 'q', lazy.shutdown()),
   
    # Run commands
    Key([mod], 'r', lazy.spawncmd()),   
]

groups = [
    Group(
        '1',
        label=u'1 \uf120',
        matches=[
            Match(wm_class=['XTerm'])
        ],
        spawn='xterm'
    ),
    Group(
        '2',
        label='2 DEV',
        matches=[
            Match(wm_class=['code'])
        ]
    ),
    Group(
        '3',
        label='3 WEB',
        matches=[
            Match(wm_class=['Firefox'], role=['browser']),
            Match(wm_class=['transmission-qt']),
        ]
    ),
    Group(
        '4',
        label='4 DOC',
        matches=[
            Match(wm_class=['Xreader'])
        ]
    ),
    Group(
        '5',
        label='5 VID',
        matches=[
            Match(wm_class=['vlc'])
        ]
    )
]

for g in groups:
    keys.append(
        # mod + name of group = switch to group
        Key([mod], g.name, lazy.group[g.name].toscreen()),
    )

layout_theme = {
    'border_focus': colors['focus'],
}

layouts = [
    layout.Max(),
    layout.Stack(num_stacks=2, **layout_theme)
]

widget_defaults = dict(
    font='font-awesome',
    fontsize=16,
    padding=4,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        bottom=bar.Bar(
            [
                widget.GroupBox(
                    active=colors['active'],
                    inactive=colors['inactive'],
                    highlight_color=colors['highlight'],
                    highlight_method='line',
                    borderwidth=2,
                    this_current_screen_border=colors['active']
                ),
                widget.Prompt(),
                widget.WindowName(),
                widget.Systray(),
                widget.KeyboardLayout(
                    configured_keyboards=['us', 'bg'],
                    foreground=colors['fg1']
                ),
                widget.Clock(
                    format='%d-%m-%Y %a %I:%M %p',
                    foreground=colors['fg2']
                ),
            ],
            32,
            background=colors['bg']
        ),
    ),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
])
auto_fullscreen = True
focus_on_window_activation = 'smart'

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = 'LG3D'
