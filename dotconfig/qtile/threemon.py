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

from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen, KeyChord
from libqtile.lazy import lazy
from qtile_extras import widget
from qtile_extras.widget.decorations import RectDecoration
from qtile_extras.bar import Bar
from Xlib import X, display
from Xlib.ext import randr

mod = "mod4"
terminal = "alacritty"

glyphs = {
    "k8s": "󱃾",
    "docker": "󰡨",
    "terraform": "󱁢",
    "azure": "󰠅",
    "code": "",
    "chrome": "",
    "spotify": "",
    "chat": "󰻞",
    "monitoring": "",
}

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen on the focused window"),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawn("rofi -show run")),
    Key([mod], "s", lazy.spawn("rofi -show rofi-sound -modi rofi-sound:rofi-sound-output-chooser")),
    Key([mod, "mod1"], "c", lazy.spawn("google-chrome --profile-directory=Profile\ 2 --app=https://mail.google.com/chat/u/0/#chat/home/")),
    Key([mod, "mod1"], "l", lazy.spawn("i3lock-fancy"), desc="Lock computer"),
    Key([mod], "comma", lazy.prev_screen(), desc='Keyboard focus to prev screen'),
    Key([mod], "period", lazy.next_screen(), desc='Keyboard focus to next screen'),

    # For growing/shrinking windows, etc.
    KeyChord([mod], "z", [
        Key([], "h", lazy.layout.grow_left()),
        Key([], "j", lazy.layout.grow_down()),
        Key([], "k", lazy.layout.grow_up()),
        Key([], "l", lazy.layout.grow_right()),
        Key([], "m", lazy.layout.maximize()),
        Key([], "n", lazy.layout.normalize())],
        mode=True,
        name="Windows"
    )
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


# groups = [Group(i) for i in "1234567890"]
groups = [
    Group(
        name = "1",
        label = glyphs["code"],
    ),
    Group(
        name = "2",
        label = glyphs["chrome"],
    ),
    Group(
        name = "3",
        label = glyphs["spotify"],
    ),
    Group(
        name = "4",
        label = glyphs["chat"],
        # spawn="google-chrome --profile-directory=Profile\ 2 --app=https://mail.google.com/chat/u/0/#chat/home/",
        # matches=[Match(wm_class='mail.google.com__chat_u_0')]
    ),
    Group(
        name = "5",
        label = glyphs["monitoring"],
    ),
]

for i in groups:
    keys.extend(
        [
            # mod1 + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    # layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    layout.MonadTall(),
    layout.MonadWide(),
    layout.Floating(),
    layout.Max(),
    #    layout.RatioTile(),
    #    layout.Tile(),
    #    layout.TreeTab(),
    #    layout.VerticalTile(),
    #    layout.Zoomy(),
]

widget_defaults = dict(
    font="FiraCode Nerd Font",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

defaultGroupBox = widget.GroupBox(
                    borderwidth=0,
                    highlight_method = 'line',
                    highlight_color = ['ccff00', 'f06d22'],
                    fontsize = 25,
                    margin_x = 20,
                )
colors =  [
        ["#00000000"],     # color 0
        ["#2e3440"], # color 1
        ["#adefd1"], # color 2
        ["#f8baaf"], # color 3
        ["#FF7696"], # color 4
        ["#f3f4f5"], # color 5
        ["#ffb18f"], # color 6
        ["#aec597"], # color 7
        ["#B591B0"], # color 8
        ["#0ee9af"],
        ["#9ED9CC"]] # color 8

decor = {
    "decorations": [
        RectDecoration(colour=colors[1], radius=13, filled=True, padding_y=0)
    ],
    "padding": 5,
}

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    font="space mono for powerline",
                    margin_y=4,
                    margin_x=5,
                    padding_y=9,
                    padding_x=8,
                    borderwidth=7,
                    inactive=colors[4],
                    active=colors[7],
                    rounded=True,
                    highlight_color=colors[4],
                    highlight_method="text",
                    this_current_screen_border=colors[9],
                    block_highlight_text_color=colors[1],
                    # background=colors[1],
                    **decor,
                ),
                widget.Spacer(),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                # widget.TextBox("default config", name="default"),
                # widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                widget.Clock(
                    format="%Y-%m-%d %a %T",
                    fontsize = 18,
                ),
                widget.Spacer(),
                widget.Systray(),
                widget.QuickExit(
                    default_text = '󰐥',
                    fontsize = 25,
                ),
            ],
            40,
            background="#00000000",
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
        wallpaper='~/Pictures/wallpapers/polaris-themortalcoil.png',
        wallpaper_mode='fill',
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),
    Screen(
        top=bar.Bar(
            [
                 widget.GroupBox(
                    font="space mono for powerline",
                    margin_y=4,
                    margin_x=5,
                    padding_y=9,
                    padding_x=8,
                    borderwidth=7,
                    inactive=colors[4],
                    active=colors[7],
                    rounded=True,
                    highlight_color=colors[4],
                    highlight_method="text",
                    this_current_screen_border=colors[9],
                    block_highlight_text_color=colors[1],
                    # background=colors[1],
                    **decor,
                ),
                # widget.TextBox("default config", name="default"),
                # widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                widget.Spacer(),
                widget.Clock(
                    format="%Y-%m-%d %a %I:%M %p",
                    fontsize = 18,
                ),
                widget.Spacer(),
                widget.QuickExit(
                    default_text = '󰐥',
                    fontsize = 25,
                    countdown_format = '{}',
                    padding = 20,
                ),
            ],
            40,
            background="#00000000",
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
        wallpaper='~/Pictures/wallpapers/polaris-themortalcoil.png',
        wallpaper_mode='fill',
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    font="space mono for powerline",
                    margin_y=4,
                    margin_x=5,
                    padding_y=9,
                    padding_x=8,
                    borderwidth=7,
                    inactive=colors[4],
                    active=colors[7],
                    rounded=True,
                    highlight_color=colors[4],
                    highlight_method="text",
                    this_current_screen_border=colors[9],
                    block_highlight_text_color=colors[1],
                    # background=colors[1],
                    **decor,
                ),
                # widget.TextBox("default config", name="default"),
                # widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                widget.Spacer(),
                widget.Clock(
                    format="%Y-%m-%d %a %I:%M %p",
                    fontsize = 18,
                ),
                widget.Spacer(),
                widget.QuickExit(
                    default_text = '󰐥',
                    fontsize = 25,
                    countdown_format = '{}',
                    padding = 20,
                ),
            ],
            40,
            background="#00000000",
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
        wallpaper='~/Pictures/wallpapers/polaris-themortalcoil.png',
        wallpaper_mode='fill',
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),
    Screen(
        top=bar.Bar(
            [
                 widget.GroupBox(
                    font="space mono for powerline",
                    margin_y=4,
                    margin_x=5,
                    padding_y=9,
                    padding_x=8,
                    borderwidth=7,
                    inactive=colors[4],
                    active=colors[7],
                    rounded=True,
                    highlight_color=colors[4],
                    highlight_method="text",
                    this_current_screen_border=colors[9],
                    block_highlight_text_color=colors[1],
                    # background=colors[1],
                    **decor,
                ),
                # widget.TextBox("default config", name="default"),
                # widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                widget.Spacer(),
                widget.Clock(
                    format="%Y-%m-%d %a %I:%M %p",
                    fontsize = 18,
                ),
                widget.Spacer(),
                widget.QuickExit(
                    default_text = '󰐥',
                    fontsize = 25,
                    countdown_format = '{}',
                    padding = 20,
                ),
            ],
            40,
            background="#00000000",
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
        wallpaper='~/Pictures/wallpapers/polaris-themortalcoil.png',
        wallpaper_mode='fill',
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    font="space mono for powerline",
                    margin_y=4,
                    margin_x=5,
                    padding_y=9,
                    padding_x=8,
                    borderwidth=7,
                    inactive=colors[4],
                    active=colors[7],
                    rounded=True,
                    highlight_color=colors[4],
                    highlight_method="text",
                    this_current_screen_border=colors[9],
                    block_highlight_text_color=colors[1],
                    # background=colors[1],
                    **decor,
                ),
                # widget.TextBox("default config", name="default"),
                # widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                widget.Spacer(),
                widget.Clock(
                    format="%Y-%m-%d %a %I:%M %p",
                    fontsize = 18,
                ),
                widget.Spacer(),
                widget.QuickExit(
                    default_text = '󰐥',
                    fontsize = 25,
                    countdown_format = '{}',
                    padding = 20,
                ),
            ],
            40,
            background="#00000000",
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
        wallpaper='~/Pictures/wallpapers/polaris-themortalcoil.png',
        wallpaper_mode='fill',
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),

]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the tayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"


# @hook.subscribe.startup_once
# def autostart():
#     script = os.path.expanduser("~/.config/qtile/autostart.sh")
#     subprocess.run([script])
