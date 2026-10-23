
import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
import re

import customtkinter as ctk
import qrcode
from qrcode.constants import (
    ERROR_CORRECT_L, ERROR_CORRECT_M,
    ERROR_CORRECT_Q, ERROR_CORRECT_H
)
from PIL import Image, ImageTk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BG = "#080B14"
PANEL = "#101726"
BORDER = "#27364E"
TEXT = "#F3F7FF"
MUTED = "#93A4BF"
CYAN = "#49E5FF"
GREEN = "#5BE7B0"
VIOLET = "#A78BFA"

ERROR_LEVELS = {
    "Low · 7%": ERROR_CORRECT_L,
    "Medium · 15%": ERROR_CORRECT_M,
    "Quartile · 25%": ERROR_CORRECT_Q,
    "High · 30%": ERROR_CORRECT_H,
}


class QRNova(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("QR NOVA | Creative QR Studio")
        self.geometry("1240x850")
        self.minsize(1000, 700)
        self.configure(fg_color=BG)

        self.fg_color = "#FFFFFF"
        self.bg_color = "#FFFFFF"
        self.qr_image = None
        self.preview_photo = None
        self.fields = {}

        self.build_ui()
        self.generate_qr()

    def label(self, parent, text, size=12,
              color=TEXT, bold=False):
        return ctk.CTkLabel(
            parent,
            text=text,
            text_color=color,
            font=ctk.CTkFont(
                "Segoe UI", size,
                "bold" if bold else "normal"
            )
        )

    def card(self, parent, accent=BORDER, fill=PANEL):
        return ctk.CTkFrame(
            parent,
            fg_color=fill,
            corner_radius=18,
            border_width=1,
            border_color=accent
        )

    def build_ui(self):

        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(1, weight=1)

        # Header
        header = ctk.CTkFrame(
            self, fg_color="transparent"
        )
        header.grid(
            row=0, column=0, columnspan=2,
            sticky="ew", padx=28, pady=(22, 18)
        )

        logo = ctk.CTkFrame(
            header, width=48, height=48,
            corner_radius=14,
            fg_color="#173247",
            border_width=1,
            border_color="#27647A"
        )
        logo.pack(side="left", padx=(0, 13))
        logo.pack_propagate(False)

        self.label(
            logo, "⌗", 29, CYAN, True
        ).place(relx=0.5, rely=0.46, anchor="center")

        heading = ctk.CTkFrame(
            header, fg_color="transparent"
        )
        heading.pack(side="left", fill="x", expand=True)

        self.label(
            heading, "Q R   N O V A", 11, CYAN, True
        ).pack(anchor="w")

        self.label(
            heading, "Creative QR Studio", 26, TEXT, True
        ).pack(anchor="w", pady=(2, 0))

        self.label(
            heading,
            "Make a scan-worthy first impression.",
            12, MUTED
        ).pack(anchor="w")

        self.status = ctk.CTkLabel(
            header,
            text="● LOCAL GENERATION",
            text_color=GREEN,
            fg_color="#102D29",
            corner_radius=20,
            padx=14,
            pady=8,
            font=ctk.CTkFont(
                "Segoe UI", 10, "bold"
            )
        )
        self.status.pack(side="right")

        # Left workspace
        self.left = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=BORDER,
            scrollbar_button_hover_color=CYAN
        )
        self.left.grid(
            row=1, column=0, sticky="nsew",
            padx=(28, 12), pady=(0, 24)
        )

        # Right preview workspace
        self.right = ctk.CTkFrame(
            self, fg_color="transparent"
        )
        self.right.grid(
            row=1, column=1, sticky="nsew",
            padx=(12, 28), pady=(0, 24)
        )
        self.right.grid_columnconfigure(0, weight=1)
        self.right.grid_rowconfigure(0, weight=1)

        self.build_controls()
        self.build_preview()

    def section(self, parent, number, title, subtitle=""):
        self.label(
            parent, f"{number}  /  {title}",
            12, CYAN, True
        ).pack(anchor="w", padx=17, pady=(17, 8))

        if subtitle:
            self.label(
                parent, subtitle, 11, MUTED
            ).pack(anchor="w", padx=17, pady=(0, 12))

    def build_controls(self):

        # CONTENT
        content = self.card(self.left)
        content.pack(fill="x", pady=(0, 13))

        self.section(
            content, "01", "CONTENT TYPE",
            "Choose what your QR code should contain."
        )

        self.mode_var = tk.StringVar(value="Website URL")

        ctk.CTkOptionMenu(
            content,
            variable=self.mode_var,
            values=[
                "Text", "Website URL",
                "Wi-Fi", "vCard Contact"
            ],
            command=self.change_mode,
            height=38,
            corner_radius=10,
            fg_color="#22314A",
            button_color="#344B70",
            button_hover_color="#45618E"
        ).pack(fill="x", padx=17, pady=(0, 14))

        self.fields_frame = ctk.CTkFrame(
            content, fg_color="transparent"
        )
        self.fields_frame.pack(
            fill="x", padx=17, pady=(0, 16)
        )

        self.change_mode("Website URL")

        # VISUAL IDENTITY
        design = self.card(self.left)
        design.pack(fill="x", pady=(0, 13))

        self.section(
            design, "02", "VISUAL IDENTITY",
            "Create your own scan-friendly color palette."
        )

        color_row = ctk.CTkFrame(
            design, fg_color="transparent"
        )
        color_row.pack(
            fill="x", padx=17, pady=(0, 13)
        )

        self.fg_button = ctk.CTkButton(
            color_row,
            text="■  Code color",
            fg_color=self.fg_color,
            hover_color="#E5E7EB",
            text_color="#101726",
            command=self.choose_fg,
            height=38
        )
        self.fg_button.pack(
            side="left", fill="x", expand=True,
            padx=(0, 5)
        )

        self.bg_button = ctk.CTkButton(
            color_row,
            text="■  Canvas color",
            fg_color=self.bg_color,
            hover_color="#E5E7EB",
            text_color="#101726",
            command=self.choose_bg,
            height=38
        )
        self.bg_button.pack(
            side="left", fill="x", expand=True,
            padx=(5, 0)
        )

        margin_row = ctk.CTkFrame(
            design, fg_color="transparent"
        )
        margin_row.pack(fill="x", padx=17)

        self.label(
            margin_row, "Quiet-zone border",
            12, TEXT, True
        ).pack(side="left")

        self.margin_var = tk.IntVar(value=4)
        self.margin_label = self.label(
            margin_row, "4 modules", 11, CYAN, True
        )
        self.margin_label.pack(side="right")

        ctk.CTkSlider(
            design,
            from_=2, to=10, number_of_steps=8,
            variable=self.margin_var,
            progress_color=CYAN,
            button_color=CYAN,
            command=self.update_margin
        ).pack(
            fill="x", padx=17, pady=(7, 15)
        )

        self.label(
            design, "Error correction",
            12, TEXT, True
        ).pack(anchor="w", padx=17, pady=(0, 7))

        self.error_var = tk.StringVar(
            value="High · 30%"
        )

        ctk.CTkOptionMenu(
            design,
            variable=self.error_var,
            values=list(ERROR_LEVELS.keys()),
            fg_color="#22314A",
            button_color="#344B70",
            button_hover_color="#45618E",
            height=36
        ).pack(fill="x", padx=17, pady=(0, 16))

        # EXPORT
        export = self.card(self.left)
        export.pack(fill="x", pady=(0, 10))

        self.section(export, "03", "EXPORT SETTINGS")

        self.format_var = tk.StringVar(value="PNG")

        format_row = ctk.CTkFrame(
            export, fg_color="transparent"
        )
        format_row.pack(
            fill="x", padx=17, pady=(0, 12)
        )

        self.label(
            format_row, "File format", 12, MUTED
        ).pack(side="left")

        ctk.CTkSegmentedButton(
            format_row,
            values=["PNG", "JPEG"],
            variable=self.format_var,
            selected_color="#1A6D83",
            selected_hover_color="#248CA5",
            unselected_color="#1B2639",
            unselected_hover_color="#293953"
        ).pack(side="right")

        self.label(
            export, "Export resolution",
            12, MUTED
        ).pack(anchor="w", padx=17, pady=(0, 6))

        self.size_var = tk.StringVar(
            value="1024 × 1024"
        )

        ctk.CTkOptionMenu(
            export,
            variable=self.size_var,
            values=[
                "512 × 512",
                "1024 × 1024",
                "2048 × 2048"
            ],
            fg_color="#22314A",
            button_color="#344B70",
            height=36
        ).pack(fill="x", padx=17, pady=(0, 16))

        ctk.CTkButton(
            export,
            text="GENERATE QR   ↗",
            command=self.generate_qr,
            height=46,
            corner_radius=12,
            fg_color=CYAN,
            hover_color="#21C5E6",
            text_color="#07111F",
            font=ctk.CTkFont(
                "Segoe UI", 13, "bold"
            )
        ).pack(fill="x", padx=17, pady=(0, 9))

        ctk.CTkButton(
            export,
            text="Save image  ↓",
            command=self.save_image,
            height=40,
            corner_radius=11,
            fg_color="#24324A",
            hover_color="#334865",
            text_color=TEXT
        ).pack(fill="x", padx=17, pady=(0, 17))

    def build_preview(self):

        preview = self.card(
            self.right, accent="#24485A", fill="#0D1422"
        )
        preview.grid(
            row=0, column=0, sticky="nsew", pady=(0, 13)
        )

        self.section(
            preview, "LIVE", "QR PREVIEW",
            "Scan it with your phone after generating."
        )

        self.stage = ctk.CTkFrame(
            preview,
            fg_color="#F4F7FB",
            corner_radius=22
        )
        self.stage.pack(
            fill="both", expand=True,
            padx=18, pady=(2, 12)
        )

        self.preview_label = ctk.CTkLabel(
            self.stage,
            text="Your QR appears here",
            text_color="#52617C"
        )
        self.preview_label.pack(
            fill="both", expand=True, padx=12, pady=12
        )

        self.preview_caption = self.label(
            preview, "READY TO GENERATE",
            10, CYAN, True
        )
        self.preview_caption.pack(pady=(0, 17))

        details = self.card(self.right)
        details.grid(row=1, column=0, sticky="ew")

        self.section(details, "✦", "QUICK INSIGHTS")

        self.payload_label = self.label(
            details, "Payload: waiting for input",
            11, MUTED
        )
        self.payload_label.pack(
            anchor="w", padx=17, pady=(0, 8)
        )

        self.size_label = self.label(
            details, "Resolution: —", 11, MUTED
        )
        self.size_label.pack(
            anchor="w", padx=17, pady=(0, 8)
        )

        self.level_label = self.label(
            details, "Correction: High", 11, MUTED
        )
        self.level_label.pack(
            anchor="w", padx=17, pady=(0, 16)
        )

    def add_field(self, key, title, placeholder, show=None):
        self.label(
            self.fields_frame, title, 10, MUTED, True
        ).pack(anchor="w", pady=(5, 5))

        entry = ctk.CTkEntry(
            self.fields_frame,
            placeholder_text=placeholder,
            height=37,
            corner_radius=9,
            border_color=BORDER,
            fg_color="#0B1220",
            text_color=TEXT,
            show=show
        )
        entry.pack(fill="x", pady=(0, 5))
        self.fields[key] = entry
        return entry

    def change_mode(self, _value=None):
        for widget in self.fields_frame.winfo_children():
            widget.destroy()

        self.fields = {}
        mode = self.mode_var.get()

        if mode == "Text":
            self.add_field(
                "text", "YOUR TEXT",
                "Type anything you want to share"
            )

        elif mode == "Website URL":
            self.add_field(
                "url", "WEBSITE URL",
                "https://example.com"
            )

        elif mode == "Wi-Fi":
            self.add_field(
                "ssid", "NETWORK NAME",
                "Your Wi-Fi name"
            )
            self.add_field(
                "password", "PASSWORD",
                "Wi-Fi password", show="•"
            )

            self.security_var = tk.StringVar(value="WPA")

            self.label(
                self.fields_frame, "SECURITY",
                10, MUTED, True
            ).pack(anchor="w", pady=(5, 5))

            ctk.CTkOptionMenu(
                self.fields_frame,
                variable=self.security_var,
                values=["WPA", "WEP", "nopass"],
                fg_color="#22314A",
                button_color="#344B70",
                height=36
            ).pack(fill="x", pady=(0, 5))

            self.hidden_var = tk.BooleanVar(value=False)

            ctk.CTkCheckBox(
                self.fields_frame,
                text="Hidden network",
                variable=self.hidden_var,
                checkbox_width=18,
                checkbox_height=18,
                fg_color="#168AA3",
                hover_color="#21A7C3"
            ).pack(anchor="w", pady=(6, 4))

        elif mode == "vCard Contact":
            self.add_field(
                "name", "FULL NAME", "Alex Morgan"
            )
            self.add_field(
                "phone", "PHONE", "+1 555 0100"
            )
            self.add_field(
                "email", "EMAIL", "alex@example.com"
            )
            self.add_field(
                "org", "ORGANIZATION (OPTIONAL)",
                "Company or team"
            )
            self.add_field(
                "website", "WEBSITE (OPTIONAL)",
                "https://example.com"
            )

    def choose_fg(self):
        chosen = colorchooser.askcolor(
            color=self.fg_color,
            title="Choose QR code color"
        )

        if chosen and chosen[1]:
            self.fg_color = chosen[1]

            text_color = (
                "#101726"
                if self.is_light(self.fg_color)
                else "#FFFFFF"
            )

            self.fg_button.configure(
                fg_color=self.fg_color,
                text_color=text_color
            )

    def choose_bg(self):
        chosen = colorchooser.askcolor(
            color=self.bg_color,
            title="Choose canvas color"
        )

        if chosen and chosen[1]:
            self.bg_color = chosen[1]

            text_color = (
                "#101726"
                if self.is_light(self.bg_color)
                else "#FFFFFF"
            )

            self.bg_button.configure(
                fg_color=self.bg_color,
                text_color=text_color
            )

    @staticmethod
    def is_light(color):
        value = color.lstrip("#")
        r, g, b = (
            int(value[i:i + 2], 16)
            for i in (0, 2, 4)
        )
        return (
            0.299 * r + 0.587 * g + 0.114 * b
        ) > 145

    def update_margin(self, value):
        self.margin_label.configure(
            text=f"{int(float(value))} modules"
        )

    @staticmethod
    def escape_wifi(value):
        for char in ("\\", ";", ",", ":", '"'):
            value = value.replace(char, "\\" + char)
        return value

    def get_payload(self):
        mode = self.mode_var.get()

        if mode == "Text":
            payload = self.fields["text"].get().strip()

            if not payload:
                raise ValueError("Enter some text first.")

            return payload

        if mode == "Website URL":
            payload = self.fields["url"].get().strip()

            if not payload:
                raise ValueError("Enter a website URL.")

            if not re.match(
                r"^https?://", payload, re.IGNORECASE
            ):
                payload = "https://" + payload

            if not re.match(
                r"^https?://[^\s.]+(?:\.[^\s.]+)+",
                payload, re.IGNORECASE
            ):
                raise ValueError(
                    "Enter a valid URL, such as https://example.com."
                )

            return payload

        if mode == "Wi-Fi":
            ssid = self.fields["ssid"].get().strip()
            password = self.fields["password"].get()
            security = self.security_var.get()

            if not ssid:
                raise ValueError("Enter the Wi-Fi network name.")

            if security != "nopass" and not password:
                raise ValueError(
                    "Enter the Wi-Fi password or choose nopass."
                )

            hidden = (
                "true" if self.hidden_var.get() else "false"
            )

            return (
                f"WIFI:T:{security};"
                f"S:{self.escape_wifi(ssid)};"
                f"P:{self.escape_wifi(password)};"
                f"H:{hidden};;"
            )

        if mode == "vCard Contact":
            name = self.fields["name"].get().strip()
            phone = self.fields["phone"].get().strip()
            email = self.fields["email"].get().strip()
            org = self.fields["org"].get().strip()
            website = self.fields["website"].get().strip()

            if not name:
                raise ValueError("Enter the contact's full name.")

            if not phone and not email:
                raise ValueError(
                    "Enter at least a phone number or email."
                )

            parts = [
                "BEGIN:VCARD",
                "VERSION:3.0",
                f"FN:{name}",
                f"N:{name};;;;"
            ]

            if phone:
                parts.append(f"TEL;TYPE=CELL:{phone}")

            if email:
                parts.append(f"EMAIL:{email}")

            if org:
                parts.append(f"ORG:{org}")

            if website:
                if not re.match(
                    r"^https?://", website, re.IGNORECASE
                ):
                    website = "https://" + website

                parts.append(f"URL:{website}")

            parts.append("END:VCARD")
            return "\n".join(parts)

        raise ValueError("Unsupported content type.")

    def generate_qr(self):
        try:
            payload = self.get_payload()

            qr = qrcode.QRCode(
                version=None,
                error_correction=ERROR_LEVELS[
                    self.error_var.get()
                ],
                box_size=10,
                border=int(self.margin_var.get())
            )

            qr.add_data(payload)
            qr.make(fit=True)

            image = qr.make_image(
                fill_color=self.fg_color,
                back_color=self.bg_color
            ).convert("RGB")

            target_size = int(
                self.size_var.get().split()[0]
            )

            image = image.resize(
                (target_size, target_size),
                Image.Resampling.NEAREST
            )

            self.qr_image = image

            # Smaller display copy, full resolution retained for export.
            display = image.copy()
            display.thumbnail(
                (420, 420), Image.Resampling.NEAREST
            )

            self.preview_photo = ImageTk.PhotoImage(display)

            self.preview_label.configure(
                image=self.preview_photo,
                text=""
            )

            self.preview_caption.configure(
                text="● QR GENERATED SUCCESSFULLY",
                text_color=GREEN
            )

            self.payload_label.configure(
                text=f"Payload: {len(payload):,} characters"
            )

            self.size_label.configure(
                text=f"Resolution: {target_size} × {target_size}"
            )

            self.level_label.configure(
                text=f"Correction: {self.error_var.get()}"
            )

            self.status.configure(
                text="● READY TO SCAN",
                text_color=GREEN,
                fg_color="#102D29"
            )

        except ValueError as error:
            messagebox.showerror(
                "Check your input", str(error)
            )

        except Exception as error:
            messagebox.showerror(
                "QR generation failed", str(error)
            )

    def save_image(self):
        if self.qr_image is None:
            messagebox.showwarning(
                "No QR code",
                "Generate a QR code before saving."
            )
            return

        extension = self.format_var.get().lower()

        filetypes = (
            [("PNG image", "*.png")]
            if extension == "png"
            else [("JPEG image", "*.jpg *.jpeg")]
        )

        filename = filedialog.asksaveasfilename(
            title="Save QR code",
            defaultextension=f".{extension}",
            filetypes=filetypes,
            initialfile=f"qr_nova.{extension}"
        )

        if not filename:
            return

        try:
            if extension == "png":
                self.qr_image.save(filename, format="PNG")
            else:
                self.qr_image.convert("RGB").save(
                    filename, format="JPEG", quality=95
                )

            messagebox.showinfo(
                "Saved successfully",
                f"Your QR code has been saved:\n{filename}"
            )

        except OSError as error:
            messagebox.showerror(
                "Save failed", str(error)
            )


if __name__ == "__main__":
    app = QRNova()
    app.mainloop()
