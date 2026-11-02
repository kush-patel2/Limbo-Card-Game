# Player setup dialog for configuring games

import tkinter as tk
from tkinter import ttk, messagebox


class PlayerSetupDialog:
    """Dialog for setting up player names and game options."""

    def __init__(self, parent, title="Player Setup", show_ai_options: bool = False):
        self.parent = parent
        self.show_ai_options = show_ai_options
        self.result = None

        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("500x400")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Center the dialog over the parent window
        self._center_dialog()

        # Build UI
        self._create_dialog_content()

        # Focus first entry widget
        self.player1_entry.focus_set()

        # Wait until dialog is closed (modal)
        self.dialog.wait_window()

    # ------------------------------------------------------------------
    # Layout helpers
    # ------------------------------------------------------------------
    def _center_dialog(self):
        """Center the dialog relative to its parent window."""
        self.dialog.update_idletasks()

        parent_x = self.parent.winfo_rootx()
        parent_y = self.parent.winfo_rooty()
        parent_w = self.parent.winfo_width()
        parent_h = self.parent.winfo_height()

        dlg_w, dlg_h = 500, 400
        x = parent_x + (parent_w - dlg_w) // 2
        y = parent_y + (parent_h - dlg_h) // 2

        self.dialog.geometry(f"{dlg_w}x{dlg_h}+{x}+{y}")

    def _create_dialog_content(self):
        """Create and arrange all widgets inside the dialog."""
        # Basic button styles
        style = ttk.Style(self.dialog)
        style.configure("Large.TButton", font=("Arial", 11, "bold"))
        style.configure("Medium.TButton", font=("Arial", 11))

        main = tk.Frame(self.dialog, bg="#f0f0f0", padx=20, pady=20)
        main.pack(fill="both", expand=True)

        tk.Label(
            main,
            text="Game Setup",
            font=("Arial", 18, "bold"),
            fg="#1a1a2e",
            bg="#f0f0f0",
        ).pack(pady=(0, 20))

        # Player setup section
        if self.show_ai_options:
            self._create_ai_setup(main)
        else:
            self._create_human_setup(main)

        # Game settings section
        self._create_target_score_section(main)

        # Action buttons
        self._create_buttons(main)

    # ------------------------------------------------------------------
    # Sections
    # ------------------------------------------------------------------
    def _create_human_setup(self, parent):
        """Setup for Human vs. Human."""
        frame = tk.LabelFrame(
            parent,
            text="Player Names",
            font=("Arial", 12, "bold"),
            fg="#16213e",
            bg="#f0f0f0",
            padx=10,
            pady=10,
        )
        frame.pack(fill="x", pady=(0, 20))

        tk.Label(frame, text="Player 1 Name:", font=("Arial", 11), bg="#f0f0f0").grid(
            row=0, column=0, sticky="w", pady=5
        )
        self.player1_entry = tk.Entry(frame, font=("Arial", 11), width=25)
        self.player1_entry.grid(row=0, column=1, padx=(10, 0), pady=5)
        self.player1_entry.insert(0, "Player 1")

        tk.Label(frame, text="Player 2 Name:", font=("Arial", 11), bg="#f0f0f0").grid(
            row=1, column=0, sticky="w", pady=5
        )
        self.player2_entry = tk.Entry(frame, font=("Arial", 11), width=25)
        self.player2_entry.grid(row=1, column=1, padx=(10, 0), pady=5)
        self.player2_entry.insert(0, "Player 2")

        frame.grid_columnconfigure(1, weight=1)

    def _create_ai_setup(self, parent):
        """Setup for Human vs. Computer."""
        frame = tk.LabelFrame(
            parent,
            text="Player Setup",
            font=("Arial", 12, "bold"),
            fg="#16213e",
            bg="#f0f0f0",
            padx=10,
            pady=10,
        )
        frame.pack(fill="x", pady=(0, 20))

        # Human player name
        tk.Label(frame, text="Your Name:", font=("Arial", 11), bg="#f0f0f0").grid(
            row=0, column=0, sticky="w", pady=5
        )
        self.player1_entry = tk.Entry(frame, font=("Arial", 11), width=25)
        self.player1_entry.grid(row=0, column=1, padx=(10, 0), pady=5)
        self.player1_entry.insert(0, "Player")

        # AI difficulty radio buttons
        tk.Label(frame, text="AI Difficulty:", font=("Arial", 11), bg="#f0f0f0").grid(
            row=1, column=0, sticky="w", pady=5
        )
        self.ai_difficulty_var = tk.StringVar(value="Medium")
        ai_frame = tk.Frame(frame, bg="#f0f0f0")
        ai_frame.grid(row=1, column=1, padx=(10, 0), pady=5, sticky="w")
        for diff in ("Easy", "Medium", "Hard"):
            ttk.Radiobutton(ai_frame, text=diff, variable=self.ai_difficulty_var, value=diff).pack(
                side="left", padx=(0, 15)
            )

        frame.grid_columnconfigure(1, weight=1)

    def _create_target_score_section(self, parent):
        """Game settings such as target score."""
        frame = tk.LabelFrame(
            parent,
            text="Game Settings",
            font=("Arial", 12, "bold"),
            fg="#16213e",
            bg="#f0f0f0",
            padx=10,
            pady=10,
        )
        frame.pack(fill="x", pady=(0, 20))

        tk.Label(frame, text="Target Score:", font=("Arial", 11), bg="#f0f0f0").grid(
            row=0, column=0, sticky="w", pady=5
        )
        self.target_score_var = tk.IntVar(value=200)
        tk.Spinbox(
            frame,
            from_=50,
            to=1000,
            increment=50,
            textvariable=self.target_score_var,
            font=("Arial", 11),
            width=10,
        ).grid(row=0, column=1, padx=(10, 0), pady=5, sticky="w")

        tk.Label(
            frame,
            text="(First player to reach this score wins)",
            font=("Arial", 9),
            fg="#666",
            bg="#f0f0f0",
        ).grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 5))

        frame.grid_columnconfigure(1, weight=1)

    def _create_buttons(self, parent):
        """Dialog action buttons."""
        frame = tk.Frame(parent, bg="#f0f0f0")
        frame.pack(fill="x", pady=(20, 0))

        ttk.Button(frame, text="🚀 Start Game", style="Large.TButton", command=self._on_start).pack(
            side="right", padx=(10, 0)
        )
        ttk.Button(frame, text="❌ Cancel", style="Medium.TButton", command=self._on_cancel).pack(
            side="right"
        )

        # Keyboard shortcuts
        self.dialog.bind("<Return>", lambda _: self._on_start())
        self.dialog.bind("<Escape>", lambda _: self._on_cancel())

    # ------------------------------------------------------------------
    # Event handlers & validation
    # ------------------------------------------------------------------
    def _on_start(self):
        """Validate input fields and close the dialog with a result tuple."""
        try:
            # Validate target score
            target_score = int(self.target_score_var.get())
            if not 50 <= target_score <= 1000:
                raise ValueError("Target score must be between 50 and 1000.")

            if self.show_ai_options:
                # Human vs. AI
                player_name = self.player1_entry.get().strip()
                if not player_name:
                    raise ValueError("Please enter your name.")
                self.result = (player_name, self.ai_difficulty_var.get(), target_score)
            else:
                # Human vs. Human
                p1 = self.player1_entry.get().strip()
                p2 = self.player2_entry.get().strip()
                if not p1:
                    raise ValueError("Please enter Player 1's name.")
                if not p2:
                    raise ValueError("Please enter Player 2's name.")
                if p1.lower() == p2.lower():
                    raise ValueError("Player names must be different.")
                self.result = (p1, p2, target_score)

            self.dialog.destroy()
        except ValueError as err:
            messagebox.showerror("Invalid Input", str(err))

    def _on_cancel(self):
        """Close the dialog without returning any data."""
        self.result = None
        self.dialog.destroy()
