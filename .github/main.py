"""
Финансовый менеджер - МОБИЛЬНАЯ ВЕРСИЯ (ПОЛНАЯ)
С сохранением данных, настройками и всеми функциями
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.popup import Popup
from kivy.uix.modalview import ModalView
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.metrics import dp, sp
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
import json
import os
from datetime import datetime
import re
import hashlib

# ====================== МОБИЛЬНЫЕ НАСТРОЙКИ ======================
Window.softinput_mode = 'below_target'
Window.keyboard_anim_args = {'d': 0.2, 't': 'linear'}

# Определяем платформу
try:
    from kivy.utils import platform
    IS_MOBILE = platform in ['android', 'ios']
except:
    IS_MOBILE = True

# Настраиваем пути для данных
if IS_MOBILE:
    if platform == 'android':
        try:
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.WRITE_EXTERNAL_STORAGE,
                                Permission.READ_EXTERNAL_STORAGE])
            DATA_DIR = '/storage/emulated/0/FinanceManager/'
        except:
            DATA_DIR = './finance_data/'
    elif platform == 'ios':
        DATA_DIR = os.path.join(os.path.expanduser('~'), 'Documents', 'FinanceManager/')
    else:
        DATA_DIR = './finance_data/'
else:
    DATA_DIR = './finance_data/'

# Создаем директории если нет
os.makedirs(DATA_DIR, exist_ok=True)

# Файлы данных
DATA_FILE = os.path.join(DATA_DIR, "finance_data.json")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
SETTINGS_FILE = os.path.join(DATA_DIR, "settings.json")

# ====================== УТИЛИТЫ ДЛЯ ДАННЫХ ======================
def load_data():
    """Загрузка финансовых данных"""
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    """Сохранение финансовых данных"""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except:
        return False

def load_users():
    """Загрузка пользователей"""
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    """Сохранение пользователей"""
    try:
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=2)
        return True
    except:
        return False

def load_settings():
    """Загрузка настроек"""
    if not os.path.exists(SETTINGS_FILE):
        return {"theme": "Light", "language": "EN"}
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"theme": "Light", "language": "EN"}

def save_settings(settings):
    """Сохранение настроек"""
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(settings, f, ensure_ascii=False, indent=2)
        return True
    except:
        return False

# ====================== МОБИЛЬНЫЕ ТЕМЫ ======================
THEMES = {
    "Light": {
        "bg": get_color_from_hex("#F8F9FA"),
        "card_bg": get_color_from_hex("#FFFFFF"),
        "primary": get_color_from_hex("#007AFF"),
        "secondary": get_color_from_hex("#8E8E93"),
        "text": get_color_from_hex("#000000"),
        "success": get_color_from_hex("#34C759"),
        "danger": get_color_from_hex("#FF3B30"),
        "warning": get_color_from_hex("#FF9500"),
        "info": get_color_from_hex("#5AC8FA"),
        "border": get_color_from_hex("#C7C7CC"),
        "accent": get_color_from_hex("#5856D6")
    },
    "Dark": {
        "bg": get_color_from_hex("#000000"),
        "card_bg": get_color_from_hex("#1C1C1E"),
        "primary": get_color_from_hex("#0A84FF"),
        "secondary": get_color_from_hex("#98989D"),
        "text": get_color_from_hex("#FFFFFF"),
        "success": get_color_from_hex("#30D158"),
        "danger": get_color_from_hex("#FF453A"),
        "warning": get_color_from_hex("#FF9F0A"),
        "info": get_color_from_hex("#64D2FF"),
        "border": get_color_from_hex("#38383A"),
        "accent": get_color_from_hex("#BF5AF2")
    },
    "Blue": {
        "bg": get_color_from_hex("#001F3F"),
        "card_bg": get_color_from_hex("#003366"),
        "primary": get_color_from_hex("#0074D9"),
        "secondary": get_color_from_hex("#7FDBFF"),
        "text": get_color_from_hex("#FFFFFF"),
        "success": get_color_from_hex("#2ECC40"),
        "danger": get_color_from_hex("#FF4136"),
        "warning": get_color_from_hex("#FF851B"),
        "info": get_color_from_hex("#39CCCC"),
        "border": get_color_from_hex("#00509E"),
        "accent": get_color_from_hex("#B10DC9")
    },
    "Green": {
        "bg": get_color_from_hex("#003300"),
        "card_bg": get_color_from_hex("#006600"),
        "primary": get_color_from_hex("#2ECC40"),
        "secondary": get_color_from_hex("#90EE90"),
        "text": get_color_from_hex("#FFFFFF"),
        "success": get_color_from_hex("#01FF70"),
        "danger": get_color_from_hex("#FF4136"),
        "warning": get_color_from_hex("#FF851B"),
        "info": get_color_from_hex("#3D9970"),
        "border": get_color_from_hex("#004D00"),
        "accent": get_color_from_hex("#FFDC00")
    },
    "Purple": {
        "bg": get_color_from_hex("#2D004F"),
        "card_bg": get_color_from_hex("#4B0082"),
        "primary": get_color_from_hex("#9B30FF"),
        "secondary": get_color_from_hex("#DDA0DD"),
        "text": get_color_from_hex("#FFFFFF"),
        "success": get_color_from_hex("#00FA9A"),
        "danger": get_color_from_hex("#FF1493"),
        "warning": get_color_from_hex("#FFD700"),
        "info": get_color_from_hex("#9370DB"),
        "border": get_color_from_hex("#6A0DAD"),
        "accent": get_color_from_hex("#00CED1")
    }
}

# ====================== ЯЗЫКИ ======================
LANG = {
    "EN": {
        "title": "💰 Finance",
        "add": "➕ Add",
        "create_folder": "📁 New Folder",
        "back": "← Back",
        "name": "Name",
        "amount": "Amount",
        "currency": "Currency",
        "sign": "+/-",
        "date": "Date",
        "type": "Type",
        "delete": "🗑️",
        "income": "Income",
        "expense": "Expense",
        "total": "Total",
        "theme": "Theme",
        "language": "Language",
        "folder_name": "Folder name",
        "no_folders": "No folders yet",
        "confirm_delete": "Delete?",
        "login": "Login",
        "register": "Register",
        "email": "Email",
        "nickname": "Nickname",
        "logout": "Logout",
        "welcome": "Welcome",
        "save": "💾 Save",
        "cancel": "Cancel",
        "edit": "✏️ Edit",
        "settings": "⚙️ Settings",
        "export": "Export",
        "import": "Import",
        "statistics": "📊 Stats",
        "chart": "📈 Chart",
        "report": "📄 Report",
        "search": "🔍 Search",
        "filter": "Filter",
        "all": "All",
        "today": "Today",
        "week": "Week",
        "month": "Month",
        "year": "Year",
        "custom": "Custom"
    },
    "RU": {
        "title": "💰 Финансы",
        "add": "➕ Добавить",
        "create_folder": "📁 Новая папка",
        "back": "← Назад",
        "name": "Название",
        "amount": "Сумма",
        "currency": "Валюта",
        "sign": "+/-",
        "date": "Дата",
        "type": "Тип",
        "delete": "🗑️",
        "income": "Доход",
        "expense": "Расход",
        "total": "Итого",
        "theme": "Тема",
        "language": "Язык",
        "folder_name": "Название папки",
        "no_folders": "Папок пока нет",
        "confirm_delete": "Удалить?",
        "login": "Вход",
        "register": "Регистрация",
        "email": "Email",
        "nickname": "Никнейм",
        "logout": "Выход",
        "welcome": "Добро пожаловать",
        "save": "💾 Сохранить",
        "cancel": "Отмена",
        "edit": "✏️ Изменить",
        "settings": "⚙️ Настройки",
        "export": "Экспорт",
        "import": "Импорт",
        "statistics": "📊 Статистика",
        "chart": "📈 График",
        "report": "📄 Отчет",
        "search": "🔍 Поиск",
        "filter": "Фильтр",
        "all": "Все",
        "today": "Сегодня",
        "week": "Неделя",
        "month": "Месяц",
        "year": "Год",
        "custom": "Выбрать"
    }
}

CURRENCIES = ['$ USD', '€ EUR', '£ GBP', '₽ RUB', '¥ JPY', '₩ KRW', '₹ INR']

# ====================== СТИЛИ МОБИЛЬНЫХ ВИДЖЕТОВ ======================
class MobileButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = sp(16)
        self.background_normal = ''
        self.background_color = THEMES["Light"]["primary"]
        self.color = (1, 1, 1, 1)
        self.size_hint_y = None
        self.height = dp(50)
        self.border_radius = dp(25)
        self.padding = [dp(20), 0]

class MobileLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = sp(16)
        self.halign = 'left'
        self.valign = 'middle'
        self.size_hint_y = None
        self.height = dp(40)
        self.text_size = (None, None)

class MobileTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = sp(16)
        self.size_hint_y = None
        self.height = dp(50)
        self.background_normal = ''
        self.background_color = (1, 1, 1, 0.1)
        self.foreground_color = THEMES["Light"]["text"]
        self.multiline = False
        self.padding = [dp(15), dp(15)]
        self.border_radius = dp(10)
        self.write_tab = False

class MobileSpinner(Spinner):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = sp(16)
        self.size_hint_y = None
        self.height = dp(50)
        self.background_normal = ''
        self.background_color = (1, 1, 1, 0.1)
        self.color = THEMES["Light"]["text"]
        self.border_radius = dp(10)

# ====================== ЭКРАН АВТОРИЗАЦИИ ======================
class AuthScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(name='auth', **kwargs)
        
        # Фон
        with self.canvas.before:
            Color(*THEMES["Light"]["bg"])
            self.bg = Rectangle(size=Window.size)
        
        # Главный контейнер
        main = BoxLayout(orientation='vertical', padding=dp(30), spacing=dp(20))
        
        # Логотип и заголовок
        header = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(150))
        header.add_widget(Label(
            text="💰", 
            font_size=sp(50),
            size_hint_y=None,
            height=dp(70)
        ))
        header.add_widget(Label(
            text="Finance Manager", 
            font_size=sp(24),
            bold=True
        ))
        header.add_widget(Label(
            text="Control your money",
            font_size=sp(14),
            color=(0.5, 0.5, 0.5, 1)
        ))
        main.add_widget(header)
        
        # Форма
        form = BoxLayout(orientation='vertical', spacing=dp(15))
        
        self.email_input = MobileTextInput(hint_text="Email")
        self.nickname_input = MobileTextInput(hint_text="Nickname")
        
        form.add_widget(self.email_input)
        form.add_widget(self.nickname_input)
        main.add_widget(form)
        
        # Кнопки
        buttons = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None, height=dp(110))
        
        login_btn = MobileButton(text="Login")
        login_btn.bind(on_press=self.login)
        
        register_btn = MobileButton(
            text="Create Account",
            background_color=THEMES["Light"]["success"]
        )
        register_btn.bind(on_press=self.register)
        
        buttons.add_widget(login_btn)
        buttons.add_widget(register_btn)
        main.add_widget(buttons)
        
        # Футер
        footer = Label(
            text="No password required\nJust email & nickname",
            font_size=sp(12),
            color=(0.5, 0.5, 0.5, 1),
            halign='center'
        )
        main.add_widget(footer)
        
        self.add_widget(main)
        
    def login(self, instance):
        email = self.email_input.text.strip()
        nickname = self.nickname_input.text.strip()
        
        if not email or not nickname:
            self.show_popup("Error", "Enter email and nickname")
            return
            
        users = load_users()
        user_id = hashlib.md5(email.encode()).hexdigest()
        
        if user_id in users:
            if users[user_id]["nickname"] == nickname:
                self.manager.current_user = {
                    "email": email,
                    "nickname": nickname,
                    "user_id": user_id
                }
                # Загружаем данные пользователя
                user_data = users[user_id].get("data", {})
                main_screen = MainScreen(user_data=user_data)
                self.manager.add_widget(main_screen)
                self.manager.current = 'main'
            else:
                self.show_popup("Error", "Nickname doesn't match")
        else:
            self.show_popup("Error", "User not found. Please register.")
        
    def register(self, instance):
        email = self.email_input.text.strip()
        nickname = self.nickname_input.text.strip()
        
        if not email or not nickname:
            self.show_popup("Error", "Enter email and nickname")
            return
            
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            self.show_popup("Error", "Please enter a valid email")
            return
            
        if len(nickname) < 2:
            self.show_popup("Error", "Nickname must be at least 2 characters")
            return
            
        users = load_users()
        user_id = hashlib.md5(email.encode()).hexdigest()
        
        if user_id in users:
            self.show_popup("Error", "User already exists. Please login.")
            return
            
        users[user_id] = {
            "email": email,
            "nickname": nickname,
            "created_at": datetime.now().isoformat(),
            "data": {}
        }
        
        if save_users(users):
            self.manager.current_user = {
                "email": email,
                "nickname": nickname,
                "user_id": user_id
            }
            main_screen = MainScreen(user_data={})
            self.manager.add_widget(main_screen)
            self.manager.current = 'main'
        else:
            self.show_popup("Error", "Registration failed")
        
    def show_popup(self, title, text):
        popup = Popup(
            title=title,
            content=Label(text=text),
            size_hint=(0.8, 0.3)
        )
        popup.open()

# ====================== ГЛАВНЫЙ ЭКРАН ======================
class MainScreen(Screen):
    def __init__(self, user_data=None, **kwargs):
        super().__init__(name='main', **kwargs)
        self.user_data = user_data if user_data else {}
        self.settings = load_settings()
        self.theme = self.settings.get("theme", "Light")
        self.lang = self.settings.get("language", "EN")
        
        # Загружаем папки из данных пользователя
        self.folders = self.user_data.get("folders", {})
        
        self.build_ui()
        
    def build_ui(self):
        self.clear_widgets()
        
        # Фон
        with self.canvas.before:
            Color(*THEMES[self.theme]["bg"])
            self.bg = Rectangle(size=Window.size)
        
        # Главный контейнер
        main = BoxLayout(orientation='vertical')
        
        # Шапка
        header = BoxLayout(
            size_hint_y=None,
            height=dp(60),
            padding=[dp(15), 0],
            spacing=dp(10)
        )
        
        # Меню
        menu_btn = Button(
            text="☰",
            font_size=sp(24),
            size_hint_x=None,
            width=dp(50),
            background_normal='',
            background_color=(0, 0, 0, 0),
            color=THEMES[self.theme]["text"]
        )
        menu_btn.bind(on_press=self.show_menu)
        
        # Приветствие пользователя
        user_name = self.manager.current_user.get('nickname', 'User') if hasattr(self.manager, 'current_user') else 'User'
        title = Label(
            text=f"👋 {user_name}",
            font_size=sp(20),
            bold=True,
            color=THEMES[self.theme]["text"]
        )
        
        # Кнопка добавления папки
        add_btn = Button(
            text="📁",
            font_size=sp(24),
            size_hint_x=None,
            width=dp(50),
            background_normal='',
            background_color=(0, 0, 0, 0),
            color=THEMES[self.theme]["text"]
        )
        add_btn.bind(on_press=self.show_add_folder_popup)
        
        header.add_widget(menu_btn)
        header.add_widget(title)
        header.add_widget(add_btn)
        main.add_widget(header)
        
        # Общая статистика
        stats = self.create_stats_card()
        main.add_widget(stats)
        
        # Список папок
        folders_label = Label(
            text="📁 Your Folders" if self.lang == "EN" else "📁 Ваши папки",
            font_size=sp(18),
            bold=True,
            color=THEMES[self.theme]["text"],
            size_hint_y=None,
            height=dp(40),
            padding=[dp(15), 0]
        )
        main.add_widget(folders_label)
        
        # Скроллируемый список папок
        self.scroll = ScrollView(size_hint=(1, 1))
        self.folder_list = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint_y=None,
            padding=[dp(15), dp(10)]
        )
        self.folder_list.bind(minimum_height=self.folder_list.setter('height'))
        
        self.load_folders()
        
        self.scroll.add_widget(self.folder_list)
        main.add_widget(self.scroll)
        
        # Нижняя панель
        footer = BoxLayout(
            size_hint_y=None,
            height=dp(60),
            padding=[dp(20), dp(10)]
        )
        
        stats_btn = Button(
            text="📊",
            font_size=sp(24),
            background_normal='',
            background_color=(0, 0, 0, 0),
            color=THEMES[self.theme]["text"]
        )
        stats_btn.bind(on_press=self.show_stats)
        
        home_btn = Button(
            text="🏠",
            font_size=sp(24),
            background_normal='',
            background_color=(0, 0, 0, 0),
            color=THEMES[self.theme]["primary"]
        )
        
        settings_btn = Button(
            text="⚙️",
            font_size=sp(24),
            background_normal='',
            background_color=(0, 0, 0, 0),
            color=THEMES[self.theme]["text"]
        )
        settings_btn.bind(on_press=self.show_settings)
        
        footer.add_widget(stats_btn)
        footer.add_widget(home_btn)
        footer.add_widget(settings_btn)
        main.add_widget(footer)
        
        self.add_widget(main)
        
    def create_stats_card(self):
        """Создает карточку с общей статистикой"""
        total_income = 0
        total_expense = 0
        total_folders = len(self.folders)
        total_records = 0
        
        for folder_data in self.folders.values():
            records = folder_data.get('records', [])
            total_records += len(records)
            for record in records:
                try:
                    amount = float(record.get('amount', 0))
                    if record.get('type') == 'income':
                        total_income += amount
                    else:
                        total_expense += amount
                except:
                    pass
        
        balance = total_income - total_expense
        
        stats_card = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(130),
            padding=[dp(20), dp(15)],
            spacing=dp(10)
        )
        
        with stats_card.canvas.before:
            Color(*THEMES[self.theme]["card_bg"])
            stats_card.bg = RoundedRectangle(
                pos=stats_card.pos,
                size=stats_card.size,
                radius=[dp(15)]
            )
        
        stats_card.bind(pos=self.update_card_bg, size=self.update_card_bg)
        
        # Баланс
        balance_label = Label(
            text=f"Balance: ${balance:,.2f}",
            font_size=sp(24),
            bold=True,
            color=THEMES[self.theme]["success"] if balance >= 0 else THEMES[self.theme]["danger"]
        )
        
        # Статистика
        stats_row = BoxLayout(spacing=dp(15))
        
        income_box = BoxLayout(orientation='vertical')
        income_box.add_widget(Label(
            text="Income",
            font_size=sp(12),
            color=THEMES[self.theme]["secondary"]
        ))
        income_box.add_widget(Label(
            text=f"+${total_income:,.2f}",
            font_size=sp(16),
            color=THEMES[self.theme]["success"]
        ))
        
        expense_box = BoxLayout(orientation='vertical')
        expense_box.add_widget(Label(
            text="Expense",
            font_size=sp(12),
            color=THEMES[self.theme]["secondary"]
        ))
        expense_box.add_widget(Label(
            text=f"-${total_expense:,.2f}",
            font_size=sp(16),
            color=THEMES[self.theme]["danger"]
        ))
        
        folders_box = BoxLayout(orientation='vertical')
        folders_box.add_widget(Label(
            text="Folders",
            font_size=sp(12),
            color=THEMES[self.theme]["secondary"]
        ))
        folders_box.add_widget(Label(
            text=str(total_folders),
            font_size=sp(16),
            color=THEMES[self.theme]["info"]
        ))
        
        stats_row.add_widget(income_box)
        stats_row.add_widget(expense_box)
        stats_row.add_widget(folders_box)
        
        stats_card.add_widget(balance_label)
        stats_card.add_widget(stats_row)
        
        return stats_card
        
    def update_card_bg(self, instance, value):
        if hasattr(instance, 'bg'):
            instance.bg.pos = instance.pos
            instance.bg.size = instance.size
        
    def load_folders(self):
        self.folder_list.clear_widgets()
        
        if not self.folders:
            empty_label = Label(
                text=LANG[self.lang]["no_folders"],
                font_size=sp(16),
                color=THEMES[self.theme]["secondary"],
                size_hint_y=None,
                height=dp(150),
                halign='center',
                valign='middle'
            )
            self.folder_list.add_widget(empty_label)
            self.folder_list.height = dp(150)
            return
            
        for folder_name, folder_data in self.folders.items():
            card = self.create_folder_card(folder_name, folder_data)
            self.folder_list.add_widget(card)
            
        self.folder_list.height = len(self.folders) * dp(90)
        
    def create_folder_card(self, folder_name, folder_data):
        card = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(80),
            padding=[dp(15), dp(10)],
            spacing=dp(10)
        )
        
        with card.canvas.before:
            Color(*THEMES[self.theme]["card_bg"])
            card.bg = RoundedRectangle(
                pos=card.pos,
                size=card.size,
                radius=[dp(10)]
            )
        
        card.bind(pos=self.update_card_bg, size=self.update_card_bg)
        
        # Иконка папки
        icon = Label(
            text="📁",
            font_size=sp(30),
            size_hint_x=None,
            width=dp(50)
        )
        
        # Информация о папке
        info = BoxLayout(orientation='vertical', spacing=dp(5))
        
        name_label = Label(
            text=folder_name,
            font_size=sp(18),
            bold=True,
            halign='left',
            text_size=(Window.width * 0.5, None),
            color=THEMES[self.theme]["text"]
        )
        
        # Подсчет баланса папки
        balance = 0
        records_count = len(folder_data.get('records', []))
        for record in folder_data.get('records', []):
            try:
                amount = float(record.get('amount', 0))
                if record.get('type') == 'income':
                    balance += amount
                else:
                    balance -= amount
            except:
                pass
                
        details_label = Label(
            text=f"${balance:,.2f} • {records_count} records",
            font_size=sp(14),
            color=THEMES[self.theme]["secondary"],
            halign='left'
        )
        
        info.add_widget(name_label)
        info.add_widget(details_label)
        
        # Кнопка открытия
        open_btn = Button(
            text="→",
            font_size=sp(24),
            size_hint_x=None,
            width=dp(50),
            background_normal='',
            background_color=(0, 0, 0, 0),
            color=THEMES[self.theme]["primary"]
        )
        open_btn.bind(on_press=lambda x, fn=folder_name: self.open_folder(fn))
        
        card.add_widget(icon)
        card.add_widget(info)
        card.add_widget(open_btn)
        
        return card
        
    def show_add_folder_popup(self, instance):
        """Показывает попап для создания новой папки"""
        content = BoxLayout(orientation='vertical', spacing=dp(15), padding=dp(20))
        
        content.add_widget(Label(
            text="New Folder" if self.lang == "EN" else "Новая папка",
            font_size=sp(20),
            bold=True,
            size_hint_y=None,
            height=dp(40)
        ))
        
        name_input = TextInput(
            hint_text="Folder name",
            font_size=sp(16),
            size_hint_y=None,
            height=dp(50),
            background_color=(1, 1, 1, 0.1),
            foreground_color=THEMES[self.theme]["text"]
        )
        
        buttons = BoxLayout(spacing=dp(10), size_hint_y=None, height=dp(50))
        
        cancel_btn = Button(
            text="Cancel",
            background_color=THEMES[self.theme]["danger"]
        )
        
        create_btn = Button(
            text="Create",
            background_color=THEMES[self.theme]["success"]
        )
        
        def create_folder(inst):
            name = name_input.text.strip()
            if name:
                if name in self.folders:
                    self.show_message("Error", "Folder already exists")
                else:
                    self.folders[name] = {'records': []}
                    self.save_user_data()
                    self.load_folders()
                    popup.dismiss()
                    self.show_message("Success", f"Folder '{name}' created")
            else:
                self.show_message("Error", "Enter folder name")
                
        cancel_btn.bind(on_press=lambda x: popup.dismiss())
        create_btn.bind(on_press=create_folder)
        
        buttons.add_widget(cancel_btn)
        buttons.add_widget(create_btn)
        
        content.add_widget(name_input)
        content.add_widget(buttons)
        
        popup = Popup(
            title="",
            content=content,
            size_hint=(0.9, 0.4),
            separator_height=0
        )
        popup.open()
        
    def open_folder(self, folder_name):
        """Открывает экран папки"""
        if folder_name in self.folders:
            folder_screen = FolderScreen(
                folder_name=folder_name,
                records=self.folders[folder_name],
                go_back=self.back_to_main,
                update_data=self.update_folder_data,
                lang=self.lang,
                theme=self.theme
            )
            self.manager.add_widget(folder_screen)
            self.manager.current = folder_name
            
    def update_folder_data(self, folder_name, new_data):
        """Обновляет данные папки"""
        if folder_name in self.folders:
            self.folders[folder_name] = new_data
            self.save_user_data()
            
    def save_user_data(self):
        """Сохраняет данные пользователя"""
        if hasattr(self.manager, 'current_user'):
            users = load_users()
            user_id = self.manager.current_user.get('user_id')
            if user_id and user_id in users:
                users[user_id]["data"] = {"folders": self.folders}
                save_users(users)
                
    def back_to_main(self):
        """Возвращает на главный экран"""
        self.manager.current = 'main'
        # Обновляем UI
        self.build_ui()
        
    def show_menu(self, instance):
        """Показывает боковое меню"""
        menu = ModalView(size_hint=(0.8, 0.7))
        
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        # Информация о пользователе
        if hasattr(self.manager, 'current_user'):
            user_box = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(100))
            user_box.add_widget(Label(
                text="👤",
                font_size=sp(40),
                size_hint_y=None,
                height=dp(60)
            ))
            user_box.add_widget(Label(
                text=self.manager.current_user.get('nickname', 'User'),
                font_size=sp(18),
                bold=True
            ))
            user_box.add_widget(Label(
                text=self.manager.current_user.get('email', ''),
                font_size=sp(12),
                color=THEMES[self.theme]["secondary"]
            ))
            content.add_widget(user_box)
            
        # Разделитель
        content.add_widget(Label(
            text="─" * 20,
            color=THEMES[self.theme]["border"]
        ))
        
        # Опции меню
        menu_items = [
            ("📊 Statistics", self.show_stats),
            ("📄 Reports", self.show_reports),
            ("⚙️ Settings", self.show_settings),
            ("🔄 Backup", self.backup_data),
            ("❓ Help", self.show_help),
            ("🚪 Logout", self.logout)
        ]
        
        for text, callback in menu_items:
            btn = Button(
                text=text,
                font_size=sp(16),
                size_hint_y=None,
                height=dp(50),
                background_normal='',
                background_color=(0, 0, 0, 0),
                halign='left',
                color=THEMES[self.theme]["text"]
            )
            btn.bind(on_press=lambda x, cb=callback: (menu.dismiss(), cb(x)) if cb else menu.dismiss())
            content.add_widget(btn)
            
        menu.add_widget(content)
        menu.open()
        
    def show_stats(self, instance):
        """Показывает статистику"""
        total_folders = len(self.folders)
        total_records = sum(len(folder.get('records', [])) for folder in self.folders.values())
        
        content = BoxLayout(orientation='vertical', spacing=dp(15), padding=dp(20))
        content.add_widget(Label(
            text="📊 Statistics",
            font_size=sp(24),
            bold=True,
            size_hint_y=None,
            height=dp(50)
        ))
        
        stats_text = f"""
        Total Folders: {total_folders}
        Total Records: {total_records}
        
        Last Update: {datetime.now().strftime('%Y-%m-%d %H:%M')}
        Theme: {self.theme}
        Language: {self.lang}
        """
        
        content.add_widget(Label(
            text=stats_text,
            font_size=sp(16),
            halign='left'
        ))
        
        close_btn = Button(
            text="Close",
            size_hint_y=None,
            height=dp(50),
            background_color=THEMES[self.theme]["primary"]
        )
        close_btn.bind(on_press=lambda x: popup.dismiss())
        content.add_widget(close_btn)
        
        popup = Popup(
            title="",
            content=content,
            size_hint=(0.9, 0.6),
            separator_height=0
        )
        popup.open()
        
    def show_reports(self, instance):
        self.show_message("Info", "Reports feature coming soon!")
        
    def show_settings(self, instance=None):
        """Показывает настройки"""
        settings = ModalView(size_hint=(0.9, 0.7))
        
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        content.add_widget(Label(
            text="⚙️ Settings",
            font_size=sp(24),
            bold=True,
            size_hint_y=None,
            height=dp(50)
        ))
        
        # Тема
        theme_box = BoxLayout(orientation='vertical', spacing=dp(5))
        theme_box.add_widget(Label(
            text="Theme",
            font_size=sp(16),
            size_hint_y=None,
            height=dp(30)
        ))
        
        theme_spinner = Spinner(
            text=self.theme,
            values=list(THEMES.keys()),
            font_size=sp(16),
            size_hint_y=None,
            height=dp(50)
        )
        
        # Язык
        lang_box = BoxLayout(orientation='vertical', spacing=dp(5))
        lang_box.add_widget(Label(
            text="Language",
            font_size=sp(16),
            size_hint_y=None,
            height=dp(30)
        ))
        
        lang_spinner = Spinner(
            text=self.lang,
            values=list(LANG.keys()),
            font_size=sp(16),
            size_hint_y=None,
            height=dp(50)
        )
        
        # Кнопки
        buttons = BoxLayout(spacing=dp(10), size_hint_y=None, height=dp(50))
        
        def save_settings_callback(inst):
            self.theme = theme_spinner.text
            self.lang = lang_spinner.text
            
            # Сохраняем настройки
            self.settings = {"theme": self.theme, "language": self.lang}
            save_settings(self.settings)
            
            settings.dismiss()
            self.build_ui()  # Перестраиваем UI с новыми настройками
            
        save_btn = Button(
            text="Save",
            background_color=THEMES[self.theme]["success"]
        )
        save_btn.bind(on_press=save_settings_callback)
        
        cancel_btn = Button(
            text="Cancel",
            background_color=THEMES[self.theme]["danger"]
        )
        cancel_btn.bind(on_press=lambda x: settings.dismiss())
        
        buttons.add_widget(cancel_btn)
        buttons.add_widget(save_btn)
        
        theme_box.add_widget(theme_spinner)
        lang_box.add_widget(lang_spinner)
        
        content.add_widget(theme_box)
        content.add_widget(lang_box)
        content.add_widget(buttons)
        
        settings.add_widget(content)
        settings.open()
        
    def backup_data(self, instance):
        self.show_message("Info", "Backup feature coming soon!")
        
    def show_help(self, instance):
        help_text = """
        Finance Manager Mobile
        
        How to use:
        1. Create folders for different categories
        2. Add income/expense records
        3. Track your balance
        4. Change themes and language
        
        Developed by: [Your Name]
        Version: 1.0
        """
        
        self.show_message("Help", help_text)
        
    def logout(self, instance):
        self.manager.show_auth()
        
    def show_message(self, title, text):
        popup = Popup(
            title=title,
            content=Label(text=text),
            size_hint=(0.8, 0.4)
        )
        popup.open()

# ====================== ЭКРАН ПАПКИ ======================
class FolderScreen(Screen):
    def __init__(self, folder_name, records, go_back, update_data, lang, theme, **kwargs):
        super().__init__(name=folder_name, **kwargs)
        self.folder_name = folder_name
        self.records = records
        self.go_back = go_back
        self.update_data = update_data
        self.lang = lang
        self.theme = theme
        
        self.build_ui()
        
    def build_ui(self):
        self.clear_widgets()
        
        # Фон
        with self.canvas.before:
            Color(*THEMES[self.theme]["bg"])
            self.bg = Rectangle(size=Window.size)
        
        # Главный контейнер
        main = BoxLayout(orientation='vertical')
        
        # Шапка
        header = BoxLayout(
            size_hint_y=None,
            height=dp(60),
            padding=[dp(15), 0]
        )
        
        back_btn = Button(
            text="←",
            font_size=sp(24),
            size_hint_x=None,
            width=dp(50),
            background_normal='',
            background_color=(0, 0, 0, 0),
            color=THEMES[self.theme]["text"]
        )
        back_btn.bind(on_press=lambda x: self.go_back())
        
        title = Label(
            text=self.folder_name,
            font_size=sp(20),
            bold=True,
            color=THEMES[self.theme]["text"]
        )
        
        add_btn = Button(
            text="➕",
            font_size=sp(24),
            size_hint_x=None,
            width=dp(50),
            background_normal='',
            background_color=(0, 0, 0, 0),
            color=THEMES[self.theme]["text"]
        )
        add_btn.bind(on_press=self.show_add_record_popup)
        
        header.add_widget(back_btn)
        header.add_widget(title)
        header.add_widget(add_btn)
        main.add_widget(header)
        
        # Сводка папки
        summary = self.create_summary()
        main.add_widget(summary)
        
        # Список записей
        records_label = Label(
            text="Records" if self.lang == "EN" else "Записи",
            font_size=sp(18),
            bold=True,
            color=THEMES[self.theme]["text"],
            size_hint_y=None,
            height=dp(40),
            padding=[dp(15), 0]
        )
        main.add_widget(records_label)
        
        self.scroll = ScrollView(size_hint=(1, 1))
        self.records_list = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint_y=None,
            padding=[dp(15), dp(10)]
        )
        self.records_list.bind(minimum_height=self.records_list.setter('height'))
        
        self.load_records()
        
        self.scroll.add_widget(self.records_list)
        main.add_widget(self.scroll)
        
        self.add_widget(main)
        
    def create_summary(self):
        total_income = 0
        total_expense = 0
        
        for record in self.records.get('records', []):
            try:
                amount = float(record.get('amount', 0))
                if record.get('type') == 'income':
                    total_income += amount
                else:
                    total_expense += amount
            except:
                pass
                
        balance = total_income - total_expense
        records_count = len(self.records.get('records', []))
        
        summary = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(120),
            padding=[dp(20), dp(15)],
            spacing=dp(10)
        )
        
        with summary.canvas.before:
            Color(*THEMES[self.theme]["card_bg"])
            summary.bg = RoundedRectangle(
                pos=summary.pos,
                size=summary.size,
                radius=[dp(15)]
            )
            
        summary.bind(pos=self.update_summary_bg, size=self.update_summary_bg)
        
        # Баланс
        balance_label = Label(
            text=f"Balance: ${balance:,.2f}",
            font_size=sp(22),
            bold=True,
            color=THEMES[self.theme]["success"] if balance >= 0 else THEMES[self.theme]["danger"]
        )
        
        # Детали
        details = BoxLayout(spacing=dp(20))
        
        income_box = BoxLayout(orientation='vertical')
        income_box.add_widget(Label(
            text="Income",
            font_size=sp(12),
            color=THEMES[self.theme]["secondary"]
        ))
        income_box.add_widget(Label(
            text=f"+${total_income:,.2f}",
            font_size=sp(16),
            color=THEMES[self.theme]["success"]
        ))
        
        expense_box = BoxLayout(orientation='vertical')
        expense_box.add_widget(Label(
            text="Expense",
            font_size=sp(12),
            color=THEMES[self.theme]["secondary"]
        ))
        expense_box.add_widget(Label(
            text=f"-${total_expense:,.2f}",
            font_size=sp(16),
            color=THEMES[self.theme]["danger"]
        ))
        
        count_box = BoxLayout(orientation='vertical')
        count_box.add_widget(Label(
            text="Records",
            font_size=sp(12),
            color=THEMES[self.theme]["secondary"]
        ))
        count_box.add_widget(Label(
            text=str(records_count),
            font_size=sp(16),
            color=THEMES[self.theme]["info"]
        ))
        
        details.add_widget(income_box)
        details.add_widget(expense_box)
        details.add_widget(count_box)
        
        summary.add_widget(balance_label)
        summary.add_widget(details)
        
        return summary
        
    def update_summary_bg(self, instance, value):
        if hasattr(instance, 'bg'):
            instance.bg.pos = instance.pos
            instance.bg.size = instance.size
        
    def load_records(self):
        self.records_list.clear_widgets()
        
        records = self.records.get('records', [])
        
        if not records:
            empty_label = Label(
                text="No records yet",
                font_size=sp(16),
                color=THEMES[self.theme]["secondary"],
                size_hint_y=None,
                height=dp(100),
                halign='center',
                valign='middle'
            )
            self.records_list.add_widget(empty_label)
            self.records_list.height = dp(100)
            return
            
        for idx, record in enumerate(records):
            card = self.create_record_card(record, idx)
            self.records_list.add_widget(card)
            
        self.records_list.height = len(records) * dp(80)
        
    def create_record_card(self, record, index):
        card = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(70),
            padding=[dp(15), dp(10)],
            spacing=dp(10)
        )
        
        with card.canvas.before:
            Color(*THEMES[self.theme]["card_bg"])
            card.bg = RoundedRectangle(
                pos=card.pos,
                size=card.size,
                radius=[dp(10)]
            )
            
        card.bind(pos=self.update_card_bg, size=self.update_card_bg)
        
        # Иконка
        icon = Label(
            text="💰" if record.get('type') == 'income' else "💸",
            font_size=sp(24),
            size_hint_x=None,
            width=dp(40)
        )
        
        # Информация
        info = BoxLayout(orientation='vertical', spacing=dp(5))
        
        name_label = Label(
            text=record.get('name', 'No name'),
            font_size=sp(16),
            bold=True,
            halign='left',
            text_size=(Window.width * 0.4, None),
            color=THEMES[self.theme]["text"]
        )
        
        details = Label(
            text=f"{record.get('date', 'No date')} • {record.get('currency', '$')}",
            font_size=sp(12),
            color=THEMES[self.theme]["secondary"],
            halign='left'
        )
        
        info.add_widget(name_label)
        info.add_widget(details)
        
        # Сумма
        amount = float(record.get('amount', 0))
        amount_label = Label(
            text=f"${amount:,.2f}",
            font_size=sp(18),
            bold=True,
            color=THEMES[self.theme]["success"] if record.get('type') == 'income' else THEMES[self.theme]["danger"]
        )
        
        # Кнопка удаления
        delete_btn = Button(
            text="🗑️",
            font_size=sp(20),
            size_hint_x=None,
            width=dp(50),
            background_normal='',
            background_color=(0, 0, 0, 0),
            color=THEMES[self.theme]["danger"]
        )
        delete_btn.bind(on_press=lambda x, idx=index: self.delete_record(idx))
        
        card.add_widget(icon)
        card.add_widget(info)
        card.add_widget(amount_label)
        card.add_widget(delete_btn)
        
        return card
        
    def update_card_bg(self, instance, value):
        if hasattr(instance, 'bg'):
            instance.bg.pos = instance.pos
            instance.bg.size = instance.size
            
    def show_add_record_popup(self, instance):
        """Показывает попап для добавления записи"""
        from kivy.uix.togglebutton import ToggleButton
        
        form = ModalView(size_hint=(0.95, 0.7))
        
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        content.add_widget(Label(
            text="New Record",
            font_size=sp(24),
            bold=True,
            size_hint_y=None,
            height=dp(50)
        ))
        
        # Название
        name_input = TextInput(
            hint_text="Name (e.g., Salary, Rent)",
            font_size=sp(16),
            size_hint_y=None,
            height=dp(50),
            background_color=(1, 1, 1, 0.1),
            foreground_color=THEMES[self.theme]["text"]
        )
        
        # Сумма
        amount_input = TextInput(
            hint_text="Amount",
            font_size=sp(16),
            input_filter='float',
            size_hint_y=None,
            height=dp(50),
            background_color=(1, 1, 1, 0.1),
            foreground_color=THEMES[self.theme]["text"]
        )
        
        # Тип (Доход/Расход)
        type_box = BoxLayout(spacing=dp(10), size_hint_y=None, height=dp(50))
        
        income_btn = ToggleButton(
            text="Income",
            group='type',
            state='down',
            background_normal='',
            background_color=THEMES[self.theme]["success"]
        )
        
        expense_btn = ToggleButton(
            text="Expense",
            group='type',
            background_normal='',
            background_color=THEMES[self.theme]["danger"]
        )
        
        type_box.add_widget(income_btn)
        type_box.add_widget(expense_btn)
        
        # Валюта
        currency_spinner = Spinner(
            text=CURRENCIES[0],
            values=CURRENCIES,
            font_size=sp(16),
            size_hint_y=None,
            height=dp(50),
            background_color=(1, 1, 1, 0.1)
        )
        
        # Кнопки
        buttons = BoxLayout(spacing=dp(10), size_hint_y=None, height=dp(50))
        
        cancel_btn = Button(
            text="Cancel",
            background_color=THEMES[self.theme]["danger"]
        )
        
        save_btn = Button(
            text="Save",
            background_color=THEMES[self.theme]["success"]
        )
        
        def save_record(inst):
            if not name_input.text.strip():
                self.show_message("Error", "Enter record name")
                return
                
            if not amount_input.text.strip():
                self.show_message("Error", "Enter amount")
                return
                
            try:
                float(amount_input.text)
            except:
                self.show_message("Error", "Enter valid amount")
                return
            
            record_type = 'income' if income_btn.state == 'down' else 'expense'
            new_record = {
                'name': name_input.text,
                'amount': amount_input.text,
                'type': record_type,
                'currency': currency_spinner.text,
                'date': datetime.now().strftime("%d.%m.%Y %H:%M")
            }
            
            if 'records' not in self.records:
                self.records['records'] = []
            self.records['records'].append(new_record)
            
            # Обновляем данные в главном экране
            self.update_data(self.folder_name, self.records)
            
            self.load_records()
            form.dismiss()
            self.build_ui()  # Обновляем UI
            
        cancel_btn.bind(on_press=lambda x: form.dismiss())
        save_btn.bind(on_press=save_record)
        
        buttons.add_widget(cancel_btn)
        buttons.add_widget(save_btn)
        
        content.add_widget(name_input)
        content.add_widget(amount_input)
        content.add_widget(type_box)
        content.add_widget(currency_spinner)
        content.add_widget(buttons)
        
        form.add_widget(content)
        form.open()
        
    def delete_record(self, index):
        """Удаляет запись"""
        if 'records' in self.records and 0 <= index < len(self.records['records']):
            self.records['records'].pop(index)
            self.update_data(self.folder_name, self.records)
            self.load_records()
            self.build_ui()  # Обновляем UI
            
    def show_message(self, title, text):
        popup = Popup(
            title=title,
            content=Label(text=text),
            size_hint=(0.8, 0.3)
        )
        popup.open()

# ====================== МЕНЕДЖЕР ЭКРАНОВ ======================
class AppScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition = SlideTransition(duration=0.2)
        self.current_user = None
        self.show_auth()
        
    def show_auth(self):
        self.clear_widgets()
        self.current_user = None
        auth_screen = AuthScreen()
        self.add_widget(auth_screen)
        self.current = 'auth'
        
    def show_main(self):
        self.current = 'main'

# ====================== ПРИЛОЖЕНИЕ ======================
class FinanceMobileApp(App):
    def build(self):
        self.title = "Finance Mobile"
        return AppScreenManager()

# ====================== ЗАПУСК ======================
if __name__ == '__main__':
    if IS_MOBILE:
        Window.fullscreen = 'auto'
    else:
        Window.size = (360, 640)
        
    FinanceMobileApp().run()
