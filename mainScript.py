import tkinter as tk
from tkinter import ttk, filedialog, colorchooser, messagebox, font
from PIL import Image, ImageEnhance, ImageDraw, ImageFont, ImageTk
import os
import shutil
from pathlib import Path
import threading
from datetime import datetime


class ModernWatermarkApp:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_variables()
        self.setup_styles()

        # Create assets directory
        self.assets_dir = Path("assets")
        self.assets_dir.mkdir(exist_ok=True)

        self.create_widgets()
        self.load_existing_assets()



    def setup_window(self):
        self.root.title("WaterMark Pro - Advanced Image Processor")
        self.root.geometry("1300x850")
        self.root.minsize(1300, 850)
        self.root.configure(bg='#0f0f23')

        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1300 // 2)
        y = (self.root.winfo_screenheight() // 2) - (850 // 2)
        self.root.geometry(f"1300x850+{x}+{y}")

    def setup_variables(self):
        self.watermark_path = tk.StringVar()
        self.header_path = tk.StringVar()
        self.footer_path = tk.StringVar()
        self.custom_text = tk.StringVar()
        self.text_color = tk.StringVar(value="#FFFFFF")
        self.text_bg_color = tk.StringVar(value="#000000")
        self.opacity = tk.DoubleVar(value=80.0)
        self.footer_margin = tk.IntVar(value=20)
        self.footer_bottom_margin = tk.IntVar(value=10)
        self.header_top_margin = tk.IntVar(value=10)
        self.font_size = tk.IntVar(value=30)
        self.add_text = tk.BooleanVar(value=False)
        self.text_bold = tk.BooleanVar(value=False)
        self.text_italic = tk.BooleanVar(value=False)
        self.text_shadow = tk.BooleanVar(value=True)
        self.text_background = tk.BooleanVar(value=False)
        self.text_position = tk.StringVar(value="bottom-left")
        self.text_outline = tk.BooleanVar(value=False)
        self.text_outline_color = tk.StringVar(value="#000000")

    def setup_styles(self):
        # Configure ttk styles for modern look
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Custom styles
        self.style.configure('Title.TLabel',
                             background='#0f0f23',
                             foreground='#ffffff',
                             font=('Segoe UI', 24, 'bold'))

        self.style.configure('Subtitle.TLabel',
                             background='#0f0f23',
                             foreground='#a0a0c0',
                             font=('Segoe UI', 12))

        self.style.configure('Section.TLabel',
                             background='#1a1a3a',
                             foreground='#ffffff',
                             font=('Segoe UI', 14, 'bold'))

    def create_gradient_frame(self, parent, color1, color2, **kwargs):
        """Create a frame with gradient-like appearance"""
        frame = tk.Frame(parent, **kwargs)

        # Create canvas for gradient effect
        canvas = tk.Canvas(frame, highlightthickness=0)
        canvas.pack(fill='both', expand=True)

        def draw_gradient():
            canvas.delete("gradient")
            width = canvas.winfo_width()
            height = canvas.winfo_height()
            if width > 1 and height > 1:
                for i in range(height):
                    ratio = i / height
                    # Simple gradient simulation
                    r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
                    r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
                    r = int(r1 + (r2 - r1) * ratio)
                    g = int(g1 + (g2 - g1) * ratio)
                    b = int(b1 + (b2 - b1) * ratio)
                    color = f"#{r:02x}{g:02x}{b:02x}"
                    canvas.create_line(0, i, width, i, fill=color, tags="gradient")

        canvas.bind('<Configure>', lambda e: draw_gradient())
        return frame, canvas

    def create_modern_card(self, parent, title, icon, gradient_colors, content_func):
        """Create a modern card with gradient header"""
        card_frame = tk.Frame(parent, bg='#1a1a3a', relief='flat', bd=0)

        # Header with gradient effect
        header_frame = tk.Frame(card_frame, bg=gradient_colors[0], height=60)
        header_frame.pack(fill='x', padx=2, pady=2)
        header_frame.pack_propagate(False)

        # Header content
        header_content = tk.Frame(header_frame, bg=gradient_colors[0])
        header_content.pack(expand=True, fill='both')

        title_label = tk.Label(header_content,
                               text=f"{icon} {title}",
                               bg=gradient_colors[0],
                               fg='white',
                               font=('Segoe UI', 16, 'bold'))
        title_label.pack(expand=True)

        # Content area
        content_frame = tk.Frame(card_frame, bg='#2a2a4a', relief='flat')
        content_frame.pack(fill='both', expand=True, padx=2, pady=(0, 2))

        # Call content function
        content_func(content_frame)

        return card_frame

    def create_widgets(self):
        # Main container
        main_container = tk.Frame(self.root, bg='#0f0f23')
        main_container.pack(fill='both', expand=True, padx=20, pady=20)

        # Header
        self.create_header(main_container)

        # Content area with three columns
        content_frame = tk.Frame(main_container, bg='#0f0f23')
        content_frame.pack(fill='both', expand=True, pady=(20, 0))

        # Left column - Assets
        left_column = tk.Frame(content_frame, bg='#0f0f23')
        left_column.pack(side='left', fill='both', expand=True, padx=(0, 10))

        # Middle column - Text & Settings
        middle_column = tk.Frame(content_frame, bg='#0f0f23')
        middle_column.pack(side='left', fill='both', expand=True, padx=10)

        # Right column - Actions & Status
        right_column = tk.Frame(content_frame, bg='#0f0f23')
        right_column.pack(side='right', fill='both', expand=True, padx=(10, 0))

        # Create cards
        self.create_asset_card(left_column)
        self.create_text_card(middle_column)
        self.create_settings_card(middle_column)
        self.create_actions_card(right_column)
        self.create_status_card(right_column)

    def create_header(self, parent):
        header_frame = tk.Frame(parent, bg='#0f0f23', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        # Animated title
        title_label = tk.Label(header_frame,
                               text="🎨 WaterMark Pro",
                               bg='#0f0f23',
                               fg='#00d4ff',
                               font=('Segoe UI', 28, 'bold'))
        title_label.pack(side='left', pady=20)

        subtitle_label = tk.Label(header_frame,
                                  text="Advanced Bulk Image Processing Suite",
                                  bg='#0f0f23',
                                  fg='#a0a0c0',
                                  font=('Segoe UI', 14))
        subtitle_label.pack(side='left', padx=(20, 0), pady=20)

        # Status indicator
        status_frame = tk.Frame(header_frame, bg='#0f0f23')
        status_frame.pack(side='right', pady=20)

        dirs_ready = self.directories_exist()
        status_color = '#10b981' if dirs_ready else '#ef4444'
        status_text = '🟢 Ready' if dirs_ready else '🔴 Setup Required'

        tk.Label(status_frame,
                 text=status_text,
                 bg='#0f0f23',
                 fg=status_color,
                 font=('Segoe UI', 12, 'bold')).pack()

    def create_asset_card(self, parent):
        def create_asset_content(content_frame):
            assets = [
                ("Watermark", "🖼️", self.watermark_path, self.choose_watermark, "watermark.png", "#8b5cf6"),
                ("Header", "📄", self.header_path, self.choose_header, "header.png", "#3b82f6"),
                ("Footer", "📋", self.footer_path, self.choose_footer, "footer.png", "#06b6d4")
            ]

            for i, (name, icon, path_var, command, filename, color) in enumerate(assets):
                self.create_asset_row(content_frame, name, icon, path_var, command, filename, color)

        card = self.create_modern_card(parent, "Asset Management", "📁", ("#4f46e5", "#3730a3"), create_asset_content)
        card.pack(fill='both', expand=True, pady=(0, 15))

    def create_asset_row(self, parent, name, icon, path_var, command, filename, color):
        row_frame = tk.Frame(parent, bg='#3a3a5a', relief='flat', bd=1)
        row_frame.pack(fill='x', padx=15, pady=8)

        # Left side
        left_frame = tk.Frame(row_frame, bg='#3a3a5a')
        left_frame.pack(side='left', fill='x', expand=True, padx=15, pady=12)

        # Icon and name
        header = tk.Frame(left_frame, bg='#3a3a5a')
        header.pack(fill='x')

        tk.Label(header, text=icon, bg='#3a3a5a', fg=color, font=('Segoe UI', 14)).pack(side='left')
        tk.Label(header, text=name, bg='#3a3a5a', fg='white', font=('Segoe UI', 12, 'bold')).pack(side='left',
                                                                                                  padx=(8, 0))

        # Status
        status_label = tk.Label(left_frame, text="No file selected", bg='#3a3a5a', fg='#9ca3af', font=('Segoe UI', 10))
        status_label.pack(anchor='w', pady=(5, 0))
        setattr(self, f"{name.lower()}_status", status_label)

        # Right side - buttons
        button_frame = tk.Frame(row_frame, bg='#3a3a5a')
        button_frame.pack(side='right', padx=15, pady=12)

        # Preview button
        preview_btn = tk.Button(button_frame,
                                text="👁️",
                                command=lambda: self.preview_asset(path_var.get() or str(self.assets_dir / filename)),
                                bg='#6b7280', fg='white', relief='flat',
                                font=('Segoe UI', 10), width=3, height=1,
                                activebackground='#4b5563', activeforeground='white',
                                cursor='hand2')
        preview_btn.pack(side='right', padx=(8, 0))

        # Choose button
        choose_btn = tk.Button(button_frame,
                               text="Choose",
                               command=command,
                               bg=color, fg='white', relief='flat',
                               font=('Segoe UI', 10, 'bold'), width=8, height=1,
                               activebackground=self.darken_color(color), activeforeground='white',
                               cursor='hand2')
        choose_btn.pack(side='right')

    def create_text_card(self, parent):
        def create_text_content(content_frame):
            # Text enable checkbox
            check_frame = tk.Frame(content_frame, bg='#2a2a4a')
            check_frame.pack(fill='x', padx=15, pady=15)

            # Custom checkbox style
            self.text_check = tk.Checkbutton(
                check_frame,
                text="Enable Text Overlay",
                variable=self.add_text,
                command=self.toggle_text_options,
                bg='#2a2a4a', fg='white',
                font=('Segoe UI', 12, 'bold'),
                selectcolor='#10b981',
                activebackground='#2a2a4a',
                activeforeground='white',
                cursor='hand2'
            )
            self.text_check.pack(anchor='w')

            # Text options frame (initially hidden)
            self.text_options_frame = tk.Frame(content_frame, bg='#2a2a4a')

            # Text input
            input_frame = tk.Frame(self.text_options_frame, bg='#2a2a4a')
            input_frame.pack(fill='x', padx=15, pady=(0, 15))

            tk.Label(input_frame, text="💬 Text Content:", bg='#2a2a4a', fg='white',
                     font=('Segoe UI', 11, 'bold')).pack(anchor='w')

            self.text_entry = tk.Entry(input_frame,
                                       textvariable=self.custom_text,
                                       bg='#1a1a3a', fg='white', relief='flat',
                                       font=('Segoe UI', 12), bd=0,
                                       insertbackground='white')
            self.text_entry.pack(fill='x', pady=(8, 0), ipady=8)

            # Font controls
            font_frame = tk.Frame(self.text_options_frame, bg='#2a2a4a')
            font_frame.pack(fill='x', padx=15, pady=(0, 15))

            tk.Label(font_frame, text="🔤 Font Settings:", bg='#2a2a4a', fg='white',
                     font=('Segoe UI', 11, 'bold')).pack(anchor='w')

            font_controls = tk.Frame(font_frame, bg='#2a2a4a')
            font_controls.pack(fill='x', pady=(8, 0))

            # Font size
            size_frame = tk.Frame(font_controls, bg='#2a2a4a')
            size_frame.pack(side='left', fill='x', expand=True)

            tk.Label(size_frame, text="Size:", bg='#2a2a4a', fg='#a0a0c0', font=('Segoe UI', 9)).pack(anchor='w')
            tk.Scale(size_frame, from_=12, to=100, orient='horizontal',
                     variable=self.font_size, bg='#2a2a4a', fg='white',
                     highlightthickness=0, troughcolor='#1a1a3a',
                     activebackground='#10b981', font=('Segoe UI', 9)).pack(fill='x')

            # Style checkboxes
            style_frame = tk.Frame(font_controls, bg='#2a2a4a')
            style_frame.pack(side='right', padx=(15, 0))

            styles = [
                ("Bold", self.text_bold, "#f59e0b"),
                ("Italic", self.text_italic, "#8b5cf6"),
                ("Shadow", self.text_shadow, "#06b6d4"),
                ("Background", self.text_background, "#ef4444"),
                ("Outline", self.text_outline, "#10b981")
            ]

            for i, (text, var, color) in enumerate(styles):
                cb = tk.Checkbutton(style_frame, text=text, variable=var,
                                    bg='#2a2a4a', fg=color, selectcolor=color,
                                    font=('Segoe UI', 9, 'bold'),
                                    activebackground='#2a2a4a', activeforeground=color,
                                    cursor='hand2')
                cb.grid(row=i // 3, column=i % 3, sticky='w', padx=5, pady=2)

            # Color controls
            color_frame = tk.Frame(self.text_options_frame, bg='#2a2a4a')
            color_frame.pack(fill='x', padx=15, pady=(0, 15))

            tk.Label(color_frame, text="🎨 Colors:", bg='#2a2a4a', fg='white',
                     font=('Segoe UI', 11, 'bold')).pack(anchor='w')

            colors_row = tk.Frame(color_frame, bg='#2a2a4a')
            colors_row.pack(fill='x', pady=(8, 0))

            # Text color
            text_color_frame = tk.Frame(colors_row, bg='#2a2a4a')
            text_color_frame.pack(side='left', fill='x', expand=True)

            tk.Label(text_color_frame, text="Text", bg='#2a2a4a', fg='#a0a0c0', font=('Segoe UI', 9)).pack()

            text_color_btn = tk.Button(text_color_frame,
                                       bg=self.text_color.get(),
                                       width=6, height=2, relief='flat',
                                       command=lambda: self.choose_text_color('text'),
                                       cursor='hand2')
            text_color_btn.pack(pady=5)
            self.text_color_btn = text_color_btn

            # Background color
            bg_color_frame = tk.Frame(colors_row, bg='#2a2a4a')
            bg_color_frame.pack(side='left', fill='x', expand=True, padx=(10, 0))

            tk.Label(bg_color_frame, text="Background", bg='#2a2a4a', fg='#a0a0c0', font=('Segoe UI', 9)).pack()

            bg_color_btn = tk.Button(bg_color_frame,
                                     bg=self.text_bg_color.get(),
                                     width=6, height=2, relief='flat',
                                     command=lambda: self.choose_text_color('background'),
                                     cursor='hand2')
            bg_color_btn.pack(pady=5)
            self.text_bg_color_btn = bg_color_btn

            # Outline color
            outline_color_frame = tk.Frame(colors_row, bg='#2a2a4a')
            outline_color_frame.pack(side='left', fill='x', expand=True, padx=(10, 0))

            tk.Label(outline_color_frame, text="Outline", bg='#2a2a4a', fg='#a0a0c0', font=('Segoe UI', 9)).pack()

            outline_color_btn = tk.Button(outline_color_frame,
                                          bg=self.text_outline_color.get(),
                                          width=6, height=2, relief='flat',
                                          command=lambda: self.choose_text_color('outline'),
                                          cursor='hand2')
            outline_color_btn.pack(pady=5)
            self.text_outline_color_btn = outline_color_btn

            # Position selection
            pos_frame = tk.Frame(self.text_options_frame, bg='#2a2a4a')
            pos_frame.pack(fill='x', padx=15, pady=(0, 15))

            tk.Label(pos_frame, text="📍 Position:", bg='#2a2a4a', fg='white',
                     font=('Segoe UI', 11, 'bold')).pack(anchor='w')

            positions = [
                ("Top Left", "top-left"), ("Top Center", "top-center"), ("Top Right", "top-right"),
                ("Center Left", "center-left"), ("Center", "center"), ("Center Right", "center-right"),
                ("Bottom Left", "bottom-left"), ("Bottom Center", "bottom-center"), ("Bottom Right", "bottom-right")
            ]

            pos_grid = tk.Frame(pos_frame, bg='#2a2a4a')
            pos_grid.pack(pady=(8, 0))

            for i, (text, value) in enumerate(positions):
                rb = tk.Radiobutton(pos_grid, text=text, variable=self.text_position, value=value,
                                    bg='#2a2a4a', fg='white', selectcolor='#10b981',
                                    font=('Segoe UI', 9), activebackground='#2a2a4a',
                                    activeforeground='white', cursor='hand2')
                rb.grid(row=i // 3, column=i % 3, sticky='w', padx=5, pady=2)

        card = self.create_modern_card(parent, "Text Styling", "✏️", ("#ef4444", "#dc2626"), create_text_content)
        card.pack(fill='x', pady=(0, 15))

    def create_settings_card(self, parent):
        def create_settings_content(content_frame):
            # Opacity control
            opacity_frame = tk.Frame(content_frame, bg='#2a2a4a')
            opacity_frame.pack(fill='x', padx=15, pady=15)

            tk.Label(opacity_frame, text="💧 Watermark Opacity:", bg='#2a2a4a', fg='white',
                     font=('Segoe UI', 11, 'bold')).pack(anchor='w')

            opacity_controls = tk.Frame(opacity_frame, bg='#2a2a4a')
            opacity_controls.pack(fill='x', pady=(8, 0))

            self.opacity_scale = tk.Scale(opacity_controls, from_=10, to=100, orient='horizontal',
                                          variable=self.opacity, command=self.update_opacity_label,
                                          bg='#2a2a4a', fg='white', highlightthickness=0,
                                          troughcolor='#1a1a3a', activebackground='#7c3aed',
                                          font=('Segoe UI', 10))
            self.opacity_scale.pack(fill='x')

            self.opacity_label = tk.Label(opacity_controls, bg='#2a2a4a', fg='#7c3aed',
                                          font=('Segoe UI', 12, 'bold'))
            self.opacity_label.pack(pady=(5, 0))
            self.update_opacity_label(self.opacity.get())

            # Margins
            margins_frame = tk.Frame(content_frame, bg='#2a2a4a')
            margins_frame.pack(fill='x', padx=15, pady=(0, 15))

            tk.Label(margins_frame, text="📏 Positioning:", bg='#2a2a4a', fg='white',
                     font=('Segoe UI', 11, 'bold')).pack(anchor='w')

            margin_grid = tk.Frame(margins_frame, bg='#2a2a4a')
            margin_grid.pack(pady=(8, 0))

            margins = [
                ("Side", self.footer_margin, "#f59e0b"),
                ("Bottom", self.footer_bottom_margin, "#ef4444"),
                ("Top", self.header_top_margin, "#10b981")
            ]

            for i, (label, var, color) in enumerate(margins):
                frame = tk.Frame(margin_grid, bg='#1a1a3a', relief='flat', bd=1)
                frame.grid(row=0, column=i, padx=5, pady=5, sticky='ew')

                tk.Label(frame, text=label, bg='#1a1a3a', fg=color,
                         font=('Segoe UI', 10, 'bold')).pack(pady=(8, 2))

                entry = tk.Entry(frame, textvariable=var, bg='#2a2a4a', fg='white',
                                 relief='flat', font=('Segoe UI', 11), justify='center',
                                 width=8, insertbackground='white')
                entry.pack(pady=(0, 8), padx=5)

            margin_grid.grid_columnconfigure(0, weight=1)
            margin_grid.grid_columnconfigure(1, weight=1)
            margin_grid.grid_columnconfigure(2, weight=1)

        card = self.create_modern_card(parent, "Settings", "⚙️", ("#7c3aed", "#6d28d9"), create_settings_content)
        card.pack(fill='x')

    def create_actions_card(self, parent):
        def create_actions_content(content_frame):
            button_frame = tk.Frame(content_frame, bg='#2a2a4a')
            button_frame.pack(expand=True, fill='both', pady=30)

            # Setup directories (conditional)
            if not self.directories_exist():
                setup_btn = tk.Button(button_frame,
                                      text="📁 Setup Directories",
                                      command=self.setup_directories,
                                      bg='#f59e0b', fg='white', relief='flat',
                                      font=('Segoe UI', 14, 'bold'),
                                      height=2, cursor='hand2',
                                      activebackground='#d97706', activeforeground='white')
                setup_btn.pack(fill='x', padx=20, pady=8)

            # Process button
            self.process_btn = tk.Button(button_frame,
                                         text="🎯 Process Images",
                                         command=self.run_processing_threaded,
                                         bg='#10b981', fg='white', relief='flat',
                                         font=('Segoe UI', 16, 'bold'),
                                         height=2, cursor='hand2',
                                         activebackground='#059669', activeforeground='white')
            self.process_btn.pack(fill='x', padx=20, pady=8)

            # Quick actions
            quick_frame = tk.Frame(button_frame, bg='#2a2a4a')
            quick_frame.pack(fill='x', padx=20, pady=(15, 0))

            actions = [
                ("📂 Results", lambda: os.startfile("Done") if os.path.exists("Done") else messagebox.showinfo("Info",
                                                                                                              "No processed images yet"),
                 "#8b5cf6"),
                ("👀 Preview", self.preview_all_assets, "#06b6d4"),
                ("🔄 Reset", self.reset_settings, "#ef4444")
            ]

            for text, command, color in actions:
                btn = tk.Button(quick_frame, text=text, command=command,
                                bg=color, fg='white', relief='flat',
                                font=('Segoe UI', 10, 'bold'),
                                width=12, height=1, cursor='hand2',
                                activebackground=self.darken_color(color), activeforeground='white')
                btn.pack(side='left', padx=5, fill='x', expand=True)

        card = self.create_modern_card(parent, "Actions", "🚀", ("#10b981", "#059669"), create_actions_content)
        card.pack(fill='x', pady=(0, 15))

    def create_status_card(self, parent):
        def create_status_content(content_frame):
            # Status text area
            self.status_text = tk.Text(content_frame,
                                       height=12, state='disabled',
                                       bg='#1a1a3a', fg='#e5e7eb',
                                       relief='flat', bd=0,
                                       font=('Consolas', 10),
                                       wrap='word')
            self.status_text.pack(fill='both', expand=True, padx=15, pady=(15, 10))

            # Progress section
            progress_frame = tk.Frame(content_frame, bg='#2a2a4a')
            progress_frame.pack(fill='x', padx=15, pady=(0, 15))

            self.progress_label = tk.Label(progress_frame,
                                           text="Ready to process images",
                                           bg='#2a2a4a', fg='#06b6d4',
                                           font=('Segoe UI', 11, 'bold'))
            self.progress_label.pack(pady=(0, 8))

            # Custom progress bar
            progress_bg = tk.Frame(progress_frame, bg='#1a1a3a', height=20, relief='flat')
            progress_bg.pack(fill='x')

            self.progress_fill = tk.Frame(progress_bg, bg='#10b981', height=18)
            self.progress_fill.place(x=1, y=1, width=0, height=18)

            # Store reference for updates
            self.progress_bg = progress_bg

        card = self.create_modern_card(parent, "Status Monitor", "📊", ("#1f2937", "#111827"), create_status_content)
        card.pack(fill='both', expand=True)

    def toggle_text_options(self):
        """Show/hide text options based on checkbox"""
        if self.add_text.get():
            self.text_options_frame.pack(fill='x', pady=(0, 15))
            self.log_status("✏️ Text overlay enabled")
        else:
            self.text_options_frame.pack_forget()
            self.log_status("❌ Text overlay disabled")

    def choose_text_color(self, color_type):
        """Choose color for text, background, or outline"""
        title_map = {
            'text': 'Choose Text Color',
            'background': 'Choose Background Color',
            'outline': 'Choose Outline Color'
        }

        color = colorchooser.askcolor(title=title_map.get(color_type, 'Choose Color'))
        if color[1]:
            if color_type == 'text':
                self.text_color.set(color[1])
                self.text_color_btn.configure(bg=color[1])
            elif color_type == 'background':
                self.text_bg_color.set(color[1])
                self.text_bg_color_btn.configure(bg=color[1])
            elif color_type == 'outline':
                self.text_outline_color.set(color[1])
                self.text_outline_color_btn.configure(bg=color[1])

    def darken_color(self, hex_color):
        """Darken a hex color for hover effects"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
        darkened = tuple(max(0, int(c * 0.8)) for c in rgb)
        return f"#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}"

    def update_opacity_label(self, value):
        """Update opacity label with percentage"""
        self.opacity_label.configure(text=f"{float(value):.0f}%")

    def directories_exist(self):
        """Check if all required directories exist"""
        required_dirs = ["RAW", "Done", "Archive"]
        return all(os.path.exists(dir_name) for dir_name in required_dirs)

    def choose_watermark(self):
        self.choose_and_copy_asset("watermark", "watermark.png", self.watermark_path)

    def choose_header(self):
        self.choose_and_copy_asset("header", "header.png", self.header_path)

    def choose_footer(self):
        self.choose_and_copy_asset("footer", "footer.png", self.footer_path)

    def choose_and_copy_asset(self, asset_type, filename, path_var):
        file_path = filedialog.askopenfilename(
            title=f"Choose {asset_type.title()} Image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff *.webp"),
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("All files", "*.*")
            ]
        )

        if file_path:
            try:
                # Copy to assets directory
                destination = self.assets_dir / filename
                shutil.copy2(file_path, destination)
                path_var.set(str(destination))

                # Update status
                status_label = getattr(self, f"{asset_type}_status")
                status_label.configure(text=f"✅ {Path(file_path).name}", fg="#10b981")

                self.log_status(f"📁 {asset_type.title()} updated: {Path(file_path).name}")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to copy {asset_type}: {str(e)}")

    def preview_asset(self, path):
        if os.path.exists(path):
            try:
                # Create modern preview window
                preview_window = tk.Toplevel(self.root)
                preview_window.title(f"Preview - {Path(path).name}")
                preview_window.geometry("600x600")
                preview_window.configure(bg='#0f0f23')
                preview_window.transient(self.root)
                preview_window.grab_set()

                # Header
                header_frame = tk.Frame(preview_window, bg='#2d5aa0', height=60)
                header_frame.pack(fill='x')
                header_frame.pack_propagate(False)

                tk.Label(header_frame,
                         text=f"👁️ {Path(path).name}",
                         bg='#2d5aa0', fg='white',
                         font=('Segoe UI', 16, 'bold')).pack(expand=True)

                # Image display
                img_frame = tk.Frame(preview_window, bg='#1a1a3a')
                img_frame.pack(fill='both', expand=True, padx=20, pady=20)

                img = Image.open(path)
                img.thumbnail((500, 500), Image.Resampling.LANCZOS)

                photo = ImageTk.PhotoImage(img)

                label = tk.Label(img_frame, image=photo, bg='#1a1a3a')
                label.pack(expand=True)
                label.image = photo

            except Exception as e:
                messagebox.showerror("Preview Error", f"Cannot preview image: {str(e)}")
        else:
            messagebox.showwarning("File Not Found", f"Asset not found: {Path(path).name}")

    def preview_all_assets(self):
        """Preview all loaded assets in a modern grid layout"""
        assets = [
            ("Watermark", self.watermark_path.get() or str(self.assets_dir / "watermark.png")),
            ("Header", self.header_path.get() or str(self.assets_dir / "header.png")),
            ("Footer", self.footer_path.get() or str(self.assets_dir / "footer.png"))
        ]

        existing_assets = [(name, path) for name, path in assets if os.path.exists(path)]

        if not existing_assets:
            messagebox.showinfo("No Assets", "No assets available to preview")
            return

        # Create preview window
        preview_window = tk.Toplevel(self.root)
        preview_window.title("Asset Gallery")
        preview_window.geometry("800x600")
        preview_window.configure(bg='#0f0f23')
        preview_window.transient(self.root)

        # Header
        header = tk.Frame(preview_window, bg='#2d5aa0', height=60)
        header.pack(fill='x')
        header.pack_propagate(False)

        tk.Label(header, text="🖼️ Asset Gallery", bg='#2d5aa0', fg='white',
                 font=('Segoe UI', 18, 'bold')).pack(expand=True)

        # Gallery grid
        gallery_frame = tk.Frame(preview_window, bg='#0f0f23')
        gallery_frame.pack(fill='both', expand=True, padx=30, pady=30)

        for i, (name, path) in enumerate(existing_assets):
            try:
                asset_frame = tk.Frame(gallery_frame, bg='#1a1a3a', relief='flat', bd=2)
                asset_frame.grid(row=i // 3, column=i % 3, padx=15, pady=15, sticky='nsew')

                tk.Label(asset_frame, text=name, bg='#1a1a3a', fg='white',
                         font=('Segoe UI', 12, 'bold')).pack(pady=(10, 5))

                img = Image.open(path)
                img.thumbnail((200, 150), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)

                label = tk.Label(asset_frame, image=photo, bg='#1a1a3a')
                label.pack(pady=(0, 10))
                label.image = photo

            except Exception as e:
                self.log_status(f"❌ Failed to preview {name}: {str(e)}")

        # Configure grid weights
        for i in range(3):
            gallery_frame.grid_columnconfigure(i, weight=1)

    def reset_settings(self):
        """Reset all settings to defaults"""
        self.opacity.set(80.0)
        self.footer_margin.set(20)
        self.footer_bottom_margin.set(10)
        self.header_top_margin.set(10)
        self.font_size.set(30)
        self.custom_text.set("")
        self.text_color.set("#FFFFFF")
        self.text_bg_color.set("#000000")
        self.text_outline_color.set("#000000")
        self.add_text.set(False)
        self.text_bold.set(False)
        self.text_italic.set(False)
        self.text_shadow.set(True)
        self.text_background.set(False)
        self.text_outline.set(False)
        self.text_position.set("bottom-left")

        # Update color buttons
        self.text_color_btn.configure(bg="#FFFFFF")
        self.text_bg_color_btn.configure(bg="#000000")
        self.text_outline_color_btn.configure(bg="#000000")

        # Hide text options
        self.toggle_text_options()

        self.log_status("🔄 All settings reset to defaults")

    def setup_directories(self):
        """Create necessary directories for processing"""
        dirs = ["RAW", "Done", "Archive"]
        created = []

        for directory in dirs:
            if not os.path.exists(directory):
                os.makedirs(directory)
                created.append(directory)

        if created:
            self.log_status(f"✅ Created directories: {', '.join(created)}")
            messagebox.showinfo("Success",
                                f"📁 Created directories: {', '.join(created)}\n\n🎯 Place your images in the 'RAW' folder to process them.")
        else:
            self.log_status("ℹ️ All directories already exist")
            messagebox.showinfo("Info",
                                "📁 All directories already exist.\n\n🎯 Place your images in the 'RAW' folder to process them.")

    def log_status(self, message):
        """Add a message to the status log with timestamp and colors"""
        timestamp = datetime.now().strftime("%H:%M:%S")

        self.status_text.configure(state='normal')

        # Color coding for different message types
        if "✅" in message or "🎉" in message:
            color = "#10b981"
        elif "❌" in message or "⚠️" in message:
            color = "#ef4444"
        elif "📁" in message or "🚀" in message:
            color = "#3b82f6"
        elif "✏️" in message:
            color = "#8b5cf6"
        else:
            color = "#e5e7eb"

        # Insert with color (simplified for basic tkinter)
        self.status_text.insert('end', f"[{timestamp}] {message}\n")
        self.status_text.configure(state='disabled')
        self.status_text.see('end')
        self.root.update()

    def update_progress(self, value):
        """Update the custom progress bar"""
        if hasattr(self, 'progress_bg'):
            total_width = self.progress_bg.winfo_width() - 2
            fill_width = int(total_width * value)
            self.progress_fill.place(width=fill_width)
            self.root.update()

    def run_processing_threaded(self):
        """Run image processing in a separate thread"""
        if not os.path.exists("RAW") or not os.listdir("RAW"):
            messagebox.showwarning("No Images", "📂 No images found in RAW folder.\nPlease add images to process.")
            return

        self.process_btn.configure(state='disabled', text="⏳ Processing...", bg='#6b7280')
        self.update_progress(0)
        self.progress_label.configure(text="Initializing processing...")

        thread = threading.Thread(target=self.run_processing)
        thread.daemon = True
        thread.start()

    def run_processing(self):
        """Process images with enhanced watermarking"""
        try:
            raw_dir, done_dir, archive_dir = "RAW", "Done", "Archive"

            for directory in [done_dir, archive_dir]:
                os.makedirs(directory, exist_ok=True)

            # Get supported image files
            supported_formats = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp'}
            image_files = [f for f in os.listdir(raw_dir)
                           if os.path.isfile(os.path.join(raw_dir, f))
                           and Path(f).suffix.lower() in supported_formats]

            total_files = len(image_files)

            if total_files == 0:
                self.log_status("❌ No supported images found in RAW folder")
                self.progress_label.configure(text="No images to process")
                return

            self.log_status(f"🚀 Starting batch processing of {total_files} images...")
            self.progress_label.configure(text=f"Processing {total_files} images...")

            # Load assets
            watermark = self.load_asset(self.watermark_path.get() or str(self.assets_dir / "watermark.png"))
            header = self.load_asset(self.header_path.get() or str(self.assets_dir / "header.png"))
            footer = self.load_asset(self.footer_path.get() or str(self.assets_dir / "footer.png"))

            # Apply watermark opacity
            if watermark:
                opacity_decimal = self.opacity.get() / 100.0
                watermark = self.apply_opacity(watermark, opacity_decimal)

            processed_count = 0
            failed_count = 0

            for i, image_file in enumerate(image_files):
                try:
                    raw_image_path = os.path.join(raw_dir, image_file)

                    # Update progress
                    progress = (i + 1) / total_files
                    self.update_progress(progress)
                    self.progress_label.configure(text=f"Processing {i + 1}/{total_files}: {image_file[:30]}...")

                    # Process image
                    processed_image = self.process_single_image(
                        raw_image_path, watermark, header, footer
                    )

                    # Save with optimized settings
                    file_ext = Path(image_file).suffix.lower()
                    if file_ext in ['.jpg', '.jpeg']:
                        final_path = os.path.join(done_dir, image_file)
                        processed_image.convert("RGB").save(final_path, "JPEG", quality=95, optimize=True)
                    else:
                        final_path = os.path.join(done_dir, f"{Path(image_file).stem}.png")
                        processed_image.save(final_path, "PNG", optimize=True)

                    # Archive original
                    shutil.move(raw_image_path, os.path.join(archive_dir, image_file))

                    processed_count += 1
                    self.log_status(f"✅ Processed: {image_file}")

                except Exception as e:
                    failed_count += 1
                    self.log_status(f"❌ Failed: {image_file} - {str(e)}")

            # Final status
            self.update_progress(1.0)
            if failed_count == 0:
                self.log_status(f"🎉 Batch processing completed successfully!")
                self.log_status(f"📊 Processed: {processed_count} images")
                self.progress_label.configure(text=f"✅ Complete! {processed_count} images processed")
            else:
                self.log_status(f"⚠️ Processing completed with {failed_count} errors")
                self.log_status(f"📊 Success: {processed_count}/{total_files}")
                self.progress_label.configure(text=f"⚠️ Complete: {processed_count}/{total_files} successful")

        except Exception as e:
            self.log_status(f"❌ Critical error during processing: {str(e)}")
            self.progress_label.configure(text="❌ Processing failed")
        finally:
            self.process_btn.configure(state='normal', text="🎯 Process Images", bg='#10b981')

    def load_asset(self, path):
        """Load an asset image if it exists"""
        if path and os.path.exists(path):
            try:
                return Image.open(path).convert("RGBA")
            except Exception as e:
                self.log_status(f"⚠️ Failed to load asset {Path(path).name}: {str(e)}")
        return None

    def apply_opacity(self, image, opacity):
        """Apply opacity to an image"""
        if image and 0 <= opacity <= 1:
            image_copy = image.copy()
            alpha = image_copy.split()[3]
            alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
            image_copy.putalpha(alpha)
            return image_copy
        return image

    def get_text_position(self, image_width, image_height, text_bbox):
        """Calculate text position based on selection"""
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        margin = 50

        positions = {
            "top-left": (margin, margin),
            "top-center": ((image_width - text_width) // 2, margin),
            "top-right": (image_width - text_width - margin, margin),
            "center-left": (margin, (image_height - text_height) // 2),
            "center": ((image_width - text_width) // 2, (image_height - text_height) // 2),
            "center-right": (image_width - text_width - margin, (image_height - text_height) // 2),
            "bottom-left": (margin, image_height - text_height - margin),
            "bottom-center": ((image_width - text_width) // 2, image_height - text_height - margin),
            "bottom-right": (image_width - text_width - margin, image_height - text_height - margin)
        }

        return positions.get(self.text_position.get(), positions["bottom-left"])

    def process_single_image(self, image_path, watermark, header, footer):
        """Process a single image with all overlays and advanced text styling"""
        raw_image = Image.open(image_path).convert("RGBA")
        raw_width, raw_height = raw_image.size

        # Paste header
        if header:
            header_width = raw_width - 2 * self.footer_margin.get()
            header_height = int(header.height * (header_width / header.width))
            resized_header = header.resize((header_width, header_height), Image.Resampling.LANCZOS)
            raw_image.paste(resized_header, (self.footer_margin.get(), self.header_top_margin.get()), resized_header)

        # Paste footer
        if footer:
            footer_width = raw_width - 2 * self.footer_margin.get()
            footer_height = int(footer.height * (footer_width / footer.width))
            resized_footer = footer.resize((footer_width, footer_height), Image.Resampling.LANCZOS)
            footer_y = raw_height - resized_footer.height - self.footer_bottom_margin.get()
            raw_image.paste(resized_footer, (self.footer_margin.get(), footer_y), resized_footer)

        # Paste watermark (centered)
        if watermark:
            wm_x = (raw_width - watermark.width) // 2
            wm_y = self.header_top_margin.get() + (resized_header.height if header else 0) + 20
            if raw_height < 600:
                wm_y += 100
            raw_image.paste(watermark, (wm_x, wm_y), watermark)

        # Add custom text with advanced styling
        if self.add_text.get() and self.custom_text.get().strip():
            self.add_styled_text(raw_image)

        return raw_image

    def add_styled_text(self, image):
        """Add styled text to image with advanced options"""
        draw = ImageDraw.Draw(image)
        text = self.custom_text.get().strip()

        # Load font with style
        try:
            font_style = "arial.ttf"
            if self.text_bold.get() and self.text_italic.get():
                font_style = "arialbi.ttf"
            elif self.text_bold.get():
                font_style = "arialbd.ttf"
            elif self.text_italic.get():
                font_style = "ariali.ttf"

            font = ImageFont.truetype(font_style, self.font_size.get())
        except:
            try:
                font = ImageFont.truetype("calibri.ttf", self.font_size.get())
            except:
                font = ImageFont.load_default()

        # Get text bounding box
        bbox = draw.textbbox((0, 0), text, font=font)
        text_x, text_y = self.get_text_position(image.width, image.height, bbox)

        # Add background if enabled
        if self.text_background.get():
            padding = 10
            bg_bbox = (text_x - padding, text_y - padding,
                       text_x + bbox[2] - bbox[0] + padding,
                       text_y + bbox[3] - bbox[1] + padding)
            draw.rectangle(bg_bbox, fill=self.text_bg_color.get())

        # Add shadow if enabled
        if self.text_shadow.get():
            shadow_offset = max(2, self.font_size.get() // 15)
            draw.text((text_x + shadow_offset, text_y + shadow_offset),
                      text, fill="#000000", font=font)

        # Add outline if enabled
        if self.text_outline.get():
            outline_width = max(1, self.font_size.get() // 20)
            for adj_x in range(-outline_width, outline_width + 1):
                for adj_y in range(-outline_width, outline_width + 1):
                    if adj_x != 0 or adj_y != 0:
                        draw.text((text_x + adj_x, text_y + adj_y),
                                  text, fill=self.text_outline_color.get(), font=font)

        # Draw main text
        draw.text((text_x, text_y), text, fill=self.text_color.get(), font=font)

    def load_existing_assets(self):
        """Load existing assets from the assets directory"""
        assets = {
            "watermark": ("watermark.png", self.watermark_path, "watermark_status"),
            "header": ("header.png", self.header_path, "header_status"),
            "footer": ("footer.png", self.footer_path, "footer_status")
        }

        for asset_type, (filename, path_var, status_attr) in assets.items():
            asset_path = self.assets_dir / filename
            if asset_path.exists():
                path_var.set(str(asset_path))
                if hasattr(self, status_attr):
                    getattr(self, status_attr).configure(text=f"✅ {filename}", fg="#10b981")
            else:
                if hasattr(self, status_attr):
                    getattr(self, status_attr).configure(text="❌ Not set", fg="#ef4444")

    def run(self):
        """Start the application"""
        self.log_status("🎨 WaterMark Pro initialized successfully")
        if self.directories_exist():
            self.log_status("📁 All directories ready for processing")
        else:
            self.log_status("⚠️ Please setup directories before processing")

        self.root.mainloop()


def main():
    app = ModernWatermarkApp()
    app.run()


if __name__ == "__main__":
    main()