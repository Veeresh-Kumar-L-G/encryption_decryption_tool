import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from encryption import caesar, vigenere, xor_cipher, file_utils

class EncryptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔒 File & Text Encryption Tool")
        self.root.geometry("750x600")
        self.root.configure(bg="#f4f4f9")

        # Global font
        self.font = ("Segoe UI", 11)

        # Title
        title = tk.Label(root, text="🔐 Simple Encryption / Decryption Tool", 
                         font=("Segoe UI", 16, "bold"), bg="#283593", fg="white", pady=10)
        title.pack(fill="x")

        # --- Main Frame ---
        main_frame = ttk.Frame(root, padding=15)
        main_frame.pack(fill="both", expand=True)

        # Mode
        mode_frame = ttk.LabelFrame(main_frame, text="Mode", padding=10)
        mode_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5, columnspan=2)
        self.mode_var = tk.StringVar(value="Encrypt")
        ttk.Radiobutton(mode_frame, text="Encrypt", variable=self.mode_var, value="Encrypt").pack(side="left", padx=5)
        ttk.Radiobutton(mode_frame, text="Decrypt", variable=self.mode_var, value="Decrypt").pack(side="left", padx=5)

        # Algorithm
        algo_frame = ttk.LabelFrame(main_frame, text="Algorithm", padding=10)
        algo_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5, columnspan=2)
        self.algo_var = tk.StringVar(value="Caesar")
        algo_dropdown = ttk.Combobox(algo_frame, textvariable=self.algo_var, values=["Caesar", "Vigenere", "XOR"], state="readonly", width=20)
        algo_dropdown.pack(side="left", padx=5, pady=5)

        # Key
        key_frame = ttk.LabelFrame(main_frame, text="Key / Keyword", padding=10)
        key_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=5, columnspan=2)
        self.key_entry = ttk.Entry(key_frame, width=30, font=self.font)
        self.key_entry.pack(side="left", padx=5, pady=5)

        # Input Text
        input_frame = ttk.LabelFrame(main_frame, text="Input Text", padding=10)
        input_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        self.input_area = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, width=80, height=8, font=self.font, bg="#ffffff")
        self.input_area.pack(fill="both", expand=True)

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)
        ttk.Button(button_frame, text="⚡ Run on Text", command=self.run_text).pack(side="left", padx=10)
        ttk.Button(button_frame, text="📂 Run on File", command=self.run_file).pack(side="left", padx=10)
        ttk.Button(button_frame, text="❌ Clear", command=self.clear_fields).pack(side="left", padx=10)

        # Output
        output_frame = ttk.LabelFrame(main_frame, text="Output", padding=10)
        output_frame.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        self.output_area = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, width=80, height=8, font=self.font, bg="#f9f9f9")
        self.output_area.pack(fill="both", expand=True)

        # Configure resizing
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        main_frame.rowconfigure(5, weight=1)

    def clear_fields(self):
        self.input_area.delete("1.0", tk.END)
        self.output_area.config(state="normal")
        self.output_area.delete("1.0", tk.END)
        self.output_area.config(state="disabled")
        self.key_entry.delete(0, tk.END)

    def run_text(self):
        algo = self.algo_var.get()
        mode = self.mode_var.get()
        key = self.key_entry.get()
        text = self.input_area.get("1.0", tk.END).strip()

        if not key:
            messagebox.showerror("Error", "Please enter a key/keyword")
            return

        try:
            if algo == "Caesar":
                key = int(key)
                result = caesar.encrypt(text, key) if mode == "Encrypt" else caesar.decrypt(text, key)
            elif algo == "Vigenere":
                result = vigenere.encrypt(text, key) if mode == "Encrypt" else vigenere.decrypt(text, key)
            elif algo == "XOR":
                data = text.encode()
                result = xor_cipher.encrypt_decrypt(data, key).decode(errors="ignore")
            else:
                result = "Invalid Algorithm"
        except Exception as e:
            result = f"Error: {str(e)}"

        self.output_area.config(state="normal")
        self.output_area.delete("1.0", tk.END)
        self.output_area.insert(tk.END, result)
        self.output_area.config(state="disabled")

    def run_file(self):
        algo = self.algo_var.get()
        mode = self.mode_var.get()
        key = self.key_entry.get()
        file_path = filedialog.askopenfilename()

        if not file_path:
            return
        if not key:
            messagebox.showerror("Error", "Please enter a key/keyword")
            return

        try:
            if algo == "Caesar":
                key = int(key)
                content = file_utils.read_file(file_path, "r")
                result = caesar.encrypt(content, key) if mode == "Encrypt" else caesar.decrypt(content, key)
                out_file = file_utils.output_filename(file_path, mode.lower())
                file_utils.write_file(out_file, result, "w")

            elif algo == "Vigenere":
                content = file_utils.read_file(file_path, "r")
                result = vigenere.encrypt(content, key) if mode == "Encrypt" else vigenere.decrypt(content, key)
                out_file = file_utils.output_filename(file_path, mode.lower())
                file_utils.write_file(out_file, result, "w")

            elif algo == "XOR":
                content = file_utils.read_file(file_path, "rb")
                result = xor_cipher.encrypt_decrypt(content, key)
                out_file = file_utils.output_filename(file_path, mode.lower())
                file_utils.write_file(out_file, result, "wb")

            else:
                messagebox.showerror("Error", "Invalid Algorithm")
                return

            messagebox.showinfo("Success", f"Operation complete!\nFile saved as:\n{out_file}")

        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = EncryptionApp(root)
    root.mainloop()
