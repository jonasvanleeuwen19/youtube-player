import re
import json
import subprocess
import requests
from io import BytesIO
from PIL import Image, ImageTk
from youtube_search import YoutubeSearch
import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as tb
import base64
from tkinter import PhotoImage

FAV_FILE = "favorites.json"
RECENT_FILE = "recent_played.json"

base64_icon = """
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
"""

def get_video_id(url):
    match = re.search(r"v=([a-zA-Z0-9_-]{11})", url)
    if match:
        return match.group(1)
    if len(url) == 11:
        return url
    if "youtu.be/" in url:
        return url.split("youtu.be/")[-1][:11]
    return None

def load_json(filename):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except Exception:
        return []

def save_json(filename, data):
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass

class YouTubeSearcher(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.favorites = load_json(FAV_FILE)
        self.recent_played = load_json(RECENT_FILE)
        self.thumb_cache = {}  
        self.current_process = None  
        self.is_paused = False  

        self.subtitles_enabled = tk.BooleanVar(value=True)
        self.audio_only = tk.BooleanVar(value=False)

        self.create_widgets()
        self.show_home()

    def create_widgets(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        sidebar = ttk.LabelFrame(self, text="⚙️ Settings", padding=10)
        sidebar.grid(row=0, column=0, sticky="ns", padx=(10, 5), pady=10)
        ttk.Checkbutton(sidebar, text="📄 Enable Subtitles", variable=self.subtitles_enabled).pack(anchor='w', pady=5)
        ttk.Checkbutton(sidebar, text="🎵 Audio Only", variable=self.audio_only).pack(anchor='w', pady=5)
        main = ttk.Frame(self)
        main.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)
        search_frame = ttk.Frame(main)
        search_frame.pack(fill=tk.X)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.search_entry.bind("<Return>", lambda e: self.do_search())
        self.search_btn = ttk.Button(search_frame, text="🔍 Search", command=self.do_search)
        self.search_btn.pack(side=tk.LEFT, padx=5)
        self.back_btn = ttk.Button(main, text="⬅ Back to Home", command=self.show_home)
        self.back_btn.pack(pady=(10, 5))
        self.back_btn.pack_forget()
        self.home_container = ttk.Frame(main)
        self.home_container.pack(fill=tk.BOTH, expand=True)
        self.recent_group = ttk.LabelFrame(self.home_container, text="🎵 Recently Played")
        self.recent_group.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.recent_canvas = tk.Canvas(self.recent_group, height=200)
        self.recent_scrollbar = ttk.Scrollbar(self.recent_group, orient=tk.VERTICAL, command=self.recent_canvas.yview)
        self.recent_scrollable_frame = ttk.Frame(self.recent_canvas)
        self.recent_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.recent_canvas.configure(scrollregion=self.recent_canvas.bbox("all"))
        )
        self.recent_canvas.create_window((0, 0), window=self.recent_scrollable_frame, anchor="nw")
        self.recent_canvas.configure(yscrollcommand=self.recent_scrollbar.set)
        self.recent_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.recent_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.fav_group = ttk.LabelFrame(self.home_container, text="⭐ Favorites")
        self.fav_group.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.fav_canvas = tk.Canvas(self.fav_group, height=200)
        self.fav_scrollbar = ttk.Scrollbar(self.fav_group, orient=tk.VERTICAL, command=self.fav_canvas.yview)
        self.fav_scrollable_frame = ttk.Frame(self.fav_canvas)
        self.fav_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.fav_canvas.configure(scrollregion=self.fav_canvas.bbox("all"))
        )
        self.fav_canvas.create_window((0, 0), window=self.fav_scrollable_frame, anchor="nw")
        self.fav_canvas.configure(yscrollcommand=self.fav_scrollbar.set)
        self.fav_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.fav_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_frame = ttk.Frame(main)
        self.results_canvas = tk.Canvas(self.results_frame)
        self.results_scrollbar = ttk.Scrollbar(self.results_frame, orient=tk.VERTICAL, command=self.results_canvas.yview)
        self.results_scrollable_frame = ttk.Frame(self.results_canvas)
        self.results_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.results_canvas.configure(scrollregion=self.results_canvas.bbox("all"))
        )
        self.results_canvas.create_window((0, 0), window=self.results_scrollable_frame, anchor="nw")
        self.results_canvas.configure(yscrollcommand=self.results_scrollbar.set)
        self.results_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.results_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_frame.pack_forget()
        self.bottom_bar = ttk.Frame(self, height=50)  
        self.bottom_bar.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        self.thumbnail_label = ttk.Label(self.bottom_bar)
        self.thumbnail_label.pack(side=tk.LEFT, padx=5)
        self.video_title_label = ttk.Label(self.bottom_bar, text="", font=("Segoe UI", 12))
        self.video_title_label.pack(side=tk.LEFT, padx=5)
        self.author_label = ttk.Label(self.bottom_bar, text="", font=("Segoe UI", 10), foreground="gray")
        self.author_label.pack(side=tk.LEFT, padx=5)
        self.play_pause_btn = ttk.Button(self.bottom_bar, text="▶️ Play", command=self.toggle_play_pause)
        self.play_pause_btn.pack(side=tk.RIGHT, padx=5)
        self.stop_btn = ttk.Button(self.bottom_bar, text="⏹️ Stop", command=self.stop_video)
        self.stop_btn.pack(side=tk.RIGHT, padx=5)

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def show_home(self):
        self.back_btn.pack_forget()
        self.results_frame.pack_forget()
        self.home_container.pack(fill=tk.BOTH, expand=True)
        self.show_recent_played()
        self.show_favorites()

    def show_recent_played(self):
        self.clear_frame(self.recent_scrollable_frame)
        if not self.recent_played:
            ttk.Label(self.recent_scrollable_frame, text="Nothing played yet.").pack(padx=5, pady=5)
            return
        for video in self.recent_played:
            self.create_video_widget(self.recent_scrollable_frame, video, is_recent=True).pack(fill=tk.X, pady=3, padx=5)

    def show_favorites(self):
        self.clear_frame(self.fav_scrollable_frame)
        if not self.favorites:
            ttk.Label(self.fav_scrollable_frame, text="No favorites.").pack(padx=5, pady=5)
            return
        for video in self.favorites:
            self.create_video_widget(self.fav_scrollable_frame, video, is_favorite=True).pack(fill=tk.X, pady=3, padx=5)

    def show_no_results_text(self):
        self.clear_frame(self.results_scrollable_frame)
        ttk.Label(self.results_scrollable_frame, text="No results found.", foreground="gray").pack(pady=20)

    def create_video_widget(self, parent, video, is_favorite=False, is_recent=False):
        frame = ttk.Frame(parent)
        frame.columnconfigure(1, weight=1)

        video_url = video['url']
        video_id = get_video_id(video_url)
        thumbnail_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg" if video_id else None

        thumb_label = ttk.Label(frame)
        thumb_label.grid(row=0, column=0, rowspan=2, sticky="w", padx=5, pady=5)

        if video_url in self.thumb_cache:
            thumb_label.config(image=self.thumb_cache[video_url])
        elif thumbnail_url:
            try:
                resp = requests.get(thumbnail_url, timeout=5)
                img = Image.open(BytesIO(resp.content)).resize((120, 90))
                photo = ImageTk.PhotoImage(img)
                thumb_label.config(image=photo)
                self.thumb_cache[video_url] = photo
            except:
                thumb_label.config(text="[No Image]")
        else:
            thumb_label.config(text="[No Image]")

        ttk.Label(frame, text=video.get("title", "No title"), font=("Segoe UI", 10, "bold"), wraplength=450).grid(row=0, column=1, sticky="nw", padx=5)
        ttk.Label(frame, text=video.get("channel", ""), foreground="gray").grid(row=1, column=1, sticky="nw", padx=5)

        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=0, column=2, rowspan=2, padx=5)

        ttk.Button(btn_frame, text="▶️ Play", width=12, command=lambda url=video_url: self.play_video(video)).pack(pady=2)

        if is_favorite:
            ttk.Button(btn_frame, text="❌ Remove", width=12, command=lambda v=video: self.remove_favorite(v)).pack(pady=2)
        elif not is_recent:
            ttk.Button(btn_frame, text="⭐ Favorite", width=12, command=lambda v=video: self.add_favorite(v)).pack(pady=2)

        return frame

    def do_search(self):
        query = self.search_var.get().strip()
        if not query:
            messagebox.showwarning("Warning", "Please enter a search term first.")
            return

        self.home_container.pack_forget()
        self.back_btn.pack(pady=(10, 5))
        self.results_frame.pack(fill=tk.BOTH, expand=True)

        self.clear_frame(self.results_scrollable_frame)

        try:
            results = YoutubeSearch(query, max_results=10).to_dict()
        except Exception as e:
            messagebox.showerror("Error", f"Search failed:\n{e}")
            return

        if not results:
            self.show_no_results_text()
            return

        for video in results:
            video_url = "https://www.youtube.com" + video['url_suffix']
            video_data = {
                "title": video['title'],
                "channel": video['channel'],
                "url": video_url,
            }
            self.create_video_widget(self.results_scrollable_frame, video_data).pack(fill=tk.X, pady=3, padx=5)

    def add_favorite(self, video):
        if any(f['url'] == video['url'] for f in self.favorites):
            messagebox.showinfo("Info", "Already in favorites.")
            return
        self.favorites.append(video)
        save_json(FAV_FILE, self.favorites)
        self.show_favorites()

    def remove_favorite(self, video):
        self.favorites = [f for f in self.favorites if f['url'] != video['url']]
        save_json(FAV_FILE, self.favorites)
        self.show_favorites()

    def add_to_recent(self, video):
        self.recent_played = [v for v in self.recent_played if v['url'] != video['url']]
        self.recent_played.insert(0, video)
        if len(self.recent_played) > 10:
            self.recent_played = self.recent_played[:10]
        save_json(RECENT_FILE, self.recent_played)
        self.show_recent_played()

    def play_video(self, video):
        if self.current_process:
            self.current_process.terminate() 
        self.add_to_recent(video)
        url = video['url']
        cmd = ["mpv"]
        if self.audio_only.get():
            cmd.append("--no-video")
        if self.subtitles_enabled.get():
            cmd.append("--sid=1")
            cmd.append("--sub-auto=all")
            cmd.append("--sub-visibility=yes")
        else:
            cmd.append("--no-sub")
        cmd += ["--fs", url]
        try:
            self.current_process = subprocess.Popen(cmd)
            self.is_paused = False
            self.update_now_playing(video)
            self.play_pause_btn.config(text="⏸️ Pause")  
            self.update_bottom_bar(video)  
        except Exception as e:
            messagebox.showerror("Error", f"Cannot play video:\n{e}")

    def update_now_playing(self, video):
        self.video_title_label.config(text=video['title'])
        self.author_label.config(text=video['channel'])
        self.thumbnail_label.config(image="")
        video_id = get_video_id(video['url'])
        thumbnail_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg" if video_id else None
        if thumbnail_url:
            try:
                resp = requests.get(thumbnail_url, timeout=5)
                img = Image.open(BytesIO(resp.content)).resize((50, 40))
                photo = ImageTk.PhotoImage(img)
                self.thumbnail_label.config(image=photo)
                self.thumbnail_label.image = photo  
            except:
                self.thumbnail_label.config(text="[No Image]")

        self.bottom_bar.grid()  

    def update_bottom_bar(self, video):
        self.video_title_label.config(text=video['title'])
        self.author_label.config(text=video['channel'])
        self.thumbnail_label.config(image="")
        video_id = get_video_id(video['url'])
        thumbnail_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg" if video_id else None
        if thumbnail_url:
            try:
                resp = requests.get(thumbnail_url, timeout=5)
                img = Image.open(BytesIO(resp.content)).resize((50, 40))
                photo = ImageTk.PhotoImage(img)
                self.thumbnail_label.config(image=photo)
                self.thumbnail_label.image = photo  
            except:
                self.thumbnail_label.config(text="[No Image]")

    def toggle_play_pause(self):
        if self.current_process:
            if self.is_paused:
                self.current_process.send_signal(subprocess.signal.SIGCONT)  
                self.play_pause_btn.config(text="⏸️ Pause")  
            else:
                self.current_process.send_signal(subprocess.signal.SIGSTOP)  
                self.play_pause_btn.config(text="▶️ Play")  
            self.is_paused = not self.is_paused  

    def stop_video(self):
        if self.current_process:
            self.current_process.terminate()  
            self.current_process = None
            self.is_paused = False
            self.video_title_label.config(text="")
            self.author_label.config(text="")
            self.thumbnail_label.config(image="")
            self.play_pause_btn.config(text="▶️ Play")  
            self.bottom_bar.grid_remove()  

def main():
    root = tb.Window(themename="darkly")
    root.title("🎬 YouTube Player")
    root.geometry("1000x700")
    app = YouTubeSearcher(root)
    app.pack(fill=tk.BOTH, expand=True)
    icon = PhotoImage(data=base64_icon)
    root.iconphoto(True, icon)
    root.mainloop()

if __name__ == "__main__":
    main()
