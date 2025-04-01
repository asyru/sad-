import flet as ft
from datetime import datetime, timedelta
import re
import os

# قائمة لتخزين الأوقات المضافة
time_list = []

# متغيرات عالمية لتخزين القيم المدخلة في صفحة الإدخال
last_date_input = ""
last_time_input = ""
last_minutes_input = ""

# دالة عالمية لتحديث محتوى الصفحة بناءً على الشاشة الحالية
def update_page(page):
    page.controls.clear()
    if page.current_screen == "menu":
        page.controls.append(main_menu(page))
    elif page.current_screen == "converter":
        page.controls.append(time_converter(page))
    elif page.current_screen == "add_time":
        page.controls.append(add_time(page))
    elif page.current_screen == "time_table":
        page.controls.append(time_table(page))
    page.update()

def main(page: ft.Page):
    page.title = "تطبيق الوقت"
    page.current_screen = "menu"
    # تغيير الأيقونة
    page.window.icon = "icon.png"
    # تدرج لوني للخلفية
    page.bgcolor = ft.LinearGradient(
    begin=ft.alignment.top_left,
    end=ft.alignment.bottom_right,
    colors=["#0D47A1", "#1976D2", "#42A5F5"]
)
    page.window.bgcolor = ft.LinearGradient(
        begin=ft.alignment.top_left,
        end=ft.alignment.bottom_right,
        colors=["#0D47A1", "#1976D2", "#42A5F5"]
    )

    # إضافة الصوت عند النقر
    click_sound = ft.Audio(
        src="IQXRs015ds0.mp3",  # صوت النقر
        autoplay=False,
        volume=1,
    )
    page.overlay.append(click_sound)

    # إضافة الصوت عند المرور بالمؤشر
    hover_sound = ft.Audio(
        src="hrkat.mp3",  # صوت المرور بالمؤشر
        autoplay=False,
        volume=1,
    )
    page.overlay.append(hover_sound)

    # دالة لتشغيل صوت النقر
    def play_click_sound():
        try:
            click_sound.play()
        except Exception as e:
            print("خطأ في تشغيل صوت النقر:", e)

    # دالة لتشغيل صوت المرور
    def play_hover_sound(e):
        try:
            hover_sound.play()
        except Exception as e:
            print("خطأ في تشغيل صوت المرور:", e)

    # إضافة الدوال إلى الصفحة لاستخدامها لاحقًا
    page.play_click_sound = play_click_sound
    page.play_hover_sound = play_hover_sound

    # تحديث الأبعاد عند تغيير حجم الشاشة
    def on_resize(e):
        update_page(page)
        page.update()

    page.on_resize = on_resize
    update_page(page)

# القائمة الرئيسية
def main_menu(page: ft.Page):
    button_width = min(300, page.width * 0.8)
    button_height = 60 if page.height > 600 else 50

    def go_to_converter(e):
        page.play_click_sound()
        page.current_screen = "converter"
        update_page(page)

    def go_to_add_time(e):
        page.play_click_sound()
        page.current_screen = "add_time"
        update_page(page)

    def exit_app(e):
        page.play_click_sound()
        page.window.close()

    return ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Text("تطبيق الوقت", size=32, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                    bgcolor="#212121",
                    padding=10,
                    border_radius=10,
                ),
                ft.ElevatedButton(
                    "تحويل بين 12 و24 ساعة",
                    on_click=go_to_converter,
                    on_hover=page.play_hover_sound,  # صوت عند المرور
                    width=button_width,
                    height=button_height,
                    bgcolor="#1976D2",
                    color="#FFFFFF",
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10),
                        elevation=5,
                        shadow_color="#000000",
                        overlay_color=ft.colors.with_opacity(0.2, "#FFFFFF"),
                    ),
                ),
                ft.ElevatedButton(
                    "إضافة وقت إلى ساعة محددة",
                    on_click=go_to_add_time,
                    on_hover=page.play_hover_sound,  # صوت عند المرور
                    width=button_width,
                    height=button_height,
                    bgcolor="#F57C00",
                    color="#FFFFFF",
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10),
                        elevation=5,
                        shadow_color="#000000",
                        overlay_color=ft.colors.with_opacity(0.2, "#FFFFFF"),
                    ),
                ),
                ft.ElevatedButton(
                    "خروج",
                    on_click=exit_app,
                    on_hover=page.play_hover_sound,  # صوت عند المرور
                    width=button_width,
                    height=button_height,
                    bgcolor="#D32F2F",
                    color="#FFFFFF",
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10),
                        elevation=5,
                        shadow_color="#000000",
                        overlay_color=ft.colors.with_opacity(0.2, "#FFFFFF"),
                    ),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
        ),
        padding=15,
        border_radius=15,
        bgcolor=ft.colors.with_opacity(0.98, "#FFFFFF"),
        shadow=ft.BoxShadow(
            spread_radius=2,
            blur_radius=20,
            color="#000000",
            offset=ft.Offset(0, 5),
        ),
        alignment=ft.alignment.center,
        expand=True,
    )

# صفحة تحويل الوقت
def time_converter(page: ft.Page):
    input_width = min(200, page.width * 0.6)
    input_height = 50 if page.height > 600 else 40
    button_width = min(150, page.width * 0.4)
    button_height = 60 if page.height > 600 else 50

    time_input = ft.TextField(
        hint_text="أدخل الوقت",
        width=input_width,
        height=input_height,
        text_size=20,
        text_align=ft.TextAlign.CENTER,
        hint_style=ft.TextStyle(size=16, color="#B0BEC5"),
        border_radius=10,
        bgcolor="#FFFFFF",
        border_color="#1976D2",
    )
    result_text = ft.Text("", size=24, weight=ft.FontWeight.BOLD, color="#212121")

    def convert_time(e):
        page.play_click_sound()
        time_str = time_input.value.strip().replace('.', ':')
        if not time_str:
            result_text.value = "إدخال غير صالح!"
            result_text.color = "#F44336"
            page.update()
            return

        is_12_hour_format = "AM" in time_str.upper() or "PM" in time_str.upper()
        if is_12_hour_format:
            if not re.match(r'^\d{1,2}(:\d{0,2})?\s*(AM|PM|am|pm)$', time_str, re.IGNORECASE):
                result_text.value = "تنسيق الوقت غير صالح! استخدم HH:MM AM/PM أو HH AM/PM"
                result_text.color = "#F44336"
                page.update()
                return
            time_part = time_str.upper().replace("AM", "").replace("PM", "").strip()
            period = "AM" if "AM" in time_str.upper() else "PM"
            try:
                if ':' not in time_part:
                    time_part = f"{int(time_part):02d}:00"
                elif len(time_part.split(':')) == 2:
                    hours, minutes = time_part.split(':')
                    hours = int(hours)
                    minutes = int(minutes) if minutes else 0
                    time_part = f"{hours:02d}:{minutes:02d}"
                hours, minutes = map(int, time_part.split(':'))
                if hours < 1 or hours > 12 or minutes < 0 or minutes > 59:
                    result_text.value = "الساعات: 1-12، الدقائق: 0-59!"
                    result_text.color = "#F44336"
                    page.update()
                    return
                time_obj = datetime.strptime(f"{time_part} {period}", "%H:%M %p")
                result_text.value = f"الوقت بنظام 24 ساعة: {time_obj.strftime('%H:%M')}"
                result_text.color = "#4CAF50"
            except ValueError:
                result_text.value = "إدخال غير صالح!"
                result_text.color = "#F44336"
        else:
            if not re.match(r'^\d{1,2}(:\d{0,2})?$', time_str):
                result_text.value = "تنسيق الوقت غير صالح! استخدم HH:MM أو HH"
                result_text.color = "#F44336"
                page.update()
                return
            try:
                if ':' not in time_str:
                    time_str = f"{int(time_str):02d}:00"
                elif len(time_str.split(':')) == 2:
                    hours, minutes = time_str.split(':')
                    hours = int(hours)
                    minutes = int(minutes) if minutes else 0
                    time_str = f"{hours:02d}:{minutes:02d}"
                hours, minutes = map(int, time_str.split(':'))
                if hours < 0 or hours > 23 or minutes < 0 or minutes > 59:
                    result_text.value = "الساعات: 0-23، الدقائق: 0-59!"
                    result_text.color = "#F44336"
                    page.update()
                    return
                time_obj = datetime.strptime(time_str, "%H:%M")
                result_text.value = f"الوقت بنظام 12 ساعة: {time_obj.strftime('%I:%M %p')}"
                result_text.color = "#4CAF50"
            except ValueError:
                result_text.value = "إدخال غير صالح!"
                result_text.color = "#F44336"
        page.update()

    def go_to_menu(e):
        page.play_click_sound()
        page.current_screen = "menu"
        update_page(page)

    return ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Text("تحويل تنسيق الوقت", size=30, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                    bgcolor="#212121",
                    padding=10,
                    border_radius=10,
                ),
                time_input,
                ft.ElevatedButton(
                    "تحويل",
                    on_click=convert_time,
                    on_hover=page.play_hover_sound,  # صوت عند المرور
                    bgcolor="#1976D2",
                    color="#FFFFFF",
                    width=button_width,
                    height=button_height,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10),
                        elevation=5,
                        shadow_color="#000000",
                        overlay_color=ft.colors.with_opacity(0.2, "#FFFFFF"),
                    ),
                ),
                result_text,
                ft.ElevatedButton(
                    "الرئيسية",
                    on_click=go_to_menu,
                    on_hover=page.play_hover_sound,  # صوت عند المرور
                    bgcolor="#616161",
                    color="#FFFFFF",
                    width=button_width,
                    height=button_height,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10),
                        elevation=5,
                        shadow_color="#000000",
                        overlay_color=ft.colors.with_opacity(0.2, "#FFFFFF"),
                    ),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
        ),
        padding=15,
        border_radius=15,
        bgcolor=ft.colors.with_opacity(0.98, "#FFFFFF"),
        shadow=ft.BoxShadow(
            spread_radius=2,
            blur_radius=20,
            color="#000000",
            offset=ft.Offset(0, 5),
        ),
        alignment=ft.alignment.center,
        expand=True,
    )

# صفحة إضافة الوقت
def add_time(page: ft.Page):
    global last_date_input, last_time_input, last_minutes_input

    input_width = min(200, page.width * 0.6)
    input_height = 50 if page.height > 600 else 40
    button_width = min(150, page.width * 0.4)
    button_height = 60 if page.height > 600 else 50

    last_added_text = ft.Text("", size=20, weight=ft.FontWeight.BOLD, color="#212121")
    date_input = ft.TextField(
        value=last_date_input,
        hint_text="يوم/شهر/سنة",
        width=input_width,
        height=input_height,
        text_size=20,
        text_align=ft.TextAlign.CENTER,
        hint_style=ft.TextStyle(size=16, color="#B0BEC5"),
        border_radius=10,
        bgcolor="#FFFFFF",
        border_color="#1976D2",
    )
    time_input = ft.TextField(
        value=last_time_input,
        hint_text="ساعة:دقيقة",
        width=input_width,
        height=input_height,
        text_size=20,
        text_align=ft.TextAlign.CENTER,
        hint_style=ft.TextStyle(size=16, color="#B0BEC5"),
        border_radius=10,
        bgcolor="#FFFFFF",
        border_color="#1976D2",
    )
    minutes_input = ft.TextField(
        value=last_minutes_input,
        hint_text="أدخل الدقائق المضافة",
        width=input_width,
        height=input_height,
        text_size=20,
        text_align=ft.TextAlign.CENTER,
        hint_style=ft.TextStyle(size=16, color="#B0BEC5"),
        input_filter=ft.InputFilter(regex_string=r'[0-9]'),
        border_radius=10,
        bgcolor="#FFFFFF",
        border_color="#1976D2",
    )
    message_label = ft.Text("", size=18, color="#212121")

    if time_list:
        last_entry = time_list[-1]
        last_added_text.value = f"آخر إضافة: {last_entry['new_time'].strftime('%I:%M %p')} ({last_entry['new_time'].strftime('%H:%M')}) بتاريخ {last_entry['date_str']}"
        last_added_text.color = "#4CAF50"

    def add_time_entry(e):
        page.play_click_sound()
        global last_date_input, last_time_input, last_minutes_input

        time_str = time_input.value.strip().replace('.', ':')
        minutes_str = minutes_input.value.strip()
        date_str = date_input.value.strip()
        if not time_str or not minutes_str or not date_str:
            message_label.value = "يرجى ملء جميع الحقول!"
            message_label.color = "#F44336"
            page.update()
            return

        if not re.match(r'^\d{1,2}(:\d{0,2})?$', time_str):
            message_label.value = "تنسيق الوقت غير صالح! استخدم HH:MM أو HH"
            message_label.color = "#F44336"
            page.update()
            return

        try:
            if ':' not in time_str:
                time_str = f"{int(time_str):02d}:00"
            hours, minutes = map(int, time_str.split(':'))
            if hours < 0 or hours > 23 or minutes < 0 or minutes > 59:
                message_label.value = "الساعات: 0-23، الدقائق: 0-59!"
                message_label.color = "#F44336"
                page.update()
                return
        except ValueError:
            message_label.value = "تنسيق الوقت غير صالح!"
            message_label.color = "#F44336"
            page.update()
            return

        if '-' in date_str:
            date_str = date_str.replace('-', '/')
        elif '.' in date_str:
            date_str = date_str.replace('.', '/')
        try:
            day, month, year = date_str.split('/')
            day, month = day.zfill(2), month.zfill(2)
            if len(year) == 2:
                year = f"20{year}"
            date_str = f"{day}/{month}/{year}"
            date_input.value = date_str
        except ValueError:
            message_label.value = "تنسيق التاريخ غير صالح! استخدم DD/MM/YYYY"
            message_label.color = "#F44336"
            page.update()
            return

        try:
            minutes_to_add = int(minutes_str)
            if minutes_to_add < 0:
                message_label.value = "الدقائق يجب أن تكون موجبة!"
                message_label.color = "#F44336"
                page.update()
                return
            time_obj = datetime.strptime(f"01/01/2000 {time_str}", "%d/%m/%Y %H:%M")
            new_time = time_obj + timedelta(minutes=minutes_to_add)
            time_list.append({
                'date_str': date_str,
                'original_time': time_obj,
                'new_time': new_time,
                'added_minutes': minutes_to_add
            })
            last_added_text.value = f"آخر إضافة: {new_time.strftime('%I:%M %p')} ({new_time.strftime('%H:%M')}) بتاريخ {date_str}"
            last_added_text.color = "#4CAF50"
            message_label.value = "تمت الإضافة بنجاح"
            message_label.color = "#4CAF50"
            last_date_input = date_str
            last_time_input = time_str
            last_minutes_input = minutes_str
        except ValueError:
            message_label.value = "إدخال غير صالح!"
            message_label.color = "#F44336"
        page.update()

    def go_to_time_table(e):
        page.play_click_sound()
        global last_date_input, last_time_input, last_minutes_input
        last_date_input = date_input.value.strip()
        last_time_input = time_input.value.strip()
        last_minutes_input = minutes_input.value.strip()
        page.current_screen = "time_table"
        update_page(page)

    def go_to_menu(e):
        page.play_click_sound()
        global last_date_input, last_time_input, last_minutes_input
        last_date_input = date_input.value.strip()
        last_time_input = time_input.value.strip()
        last_minutes_input = minutes_input.value.strip()
        page.current_screen = "menu"
        update_page(page)

    return ft.Container(
        content=ft.Column(
            [
                last_added_text,
                ft.Container(
                    content=ft.Text("إضافة تاريخ ووقت ومدة", size=30, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                    bgcolor="#212121",
                    padding=10,
                    border_radius=10,
                ),
                date_input,
                time_input,
                minutes_input,
                ft.ElevatedButton(
                    "إضافة وقت",
                    on_click=add_time_entry,
                    on_hover=page.play_hover_sound,  # صوت عند المرور
                    bgcolor="#5D4037",
                    color="#FFFFFF",
                    width=button_width,
                    height=button_height,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10),
                        elevation=5,
                        shadow_color="#000000",
                        overlay_color=ft.colors.with_opacity(0.2, "#FFFFFF"),
                    ),
                ),
                ft.ElevatedButton(
                    "عرض جدول الأوقات",
                    on_click=go_to_time_table,
                    on_hover=page.play_hover_sound,  # صوت عند المرور
                    bgcolor="#1976D2",
                    color="#FFFFFF",
                    width=button_width,
                    height=button_height,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10),
                        elevation=5,
                        shadow_color="#000000",
                        overlay_color=ft.colors.with_opacity(0.2, "#FFFFFF"),
                    ),
                ),
                ft.ElevatedButton(
                    "الرئيسية",
                    on_click=go_to_menu,
                    on_hover=page.play_hover_sound,  # صوت عند المرور
                    bgcolor="#616161",
                    color="#FFFFFF",
                    width=button_width,
                    height=button_height,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10),
                        elevation=5,
                        shadow_color="#000000",
                        overlay_color=ft.colors.with_opacity(0.2, "#FFFFFF"),
                    ),
                ),
                message_label,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
        ),
        padding=15,
        border_radius=15,
        bgcolor=ft.colors.with_opacity(0.98, "#FFFFFF"),
        shadow=ft.BoxShadow(
            spread_radius=2,
            blur_radius=20,
            color="#000000",
            offset=ft.Offset(0, 5),
        ),
        alignment=ft.alignment.center,
        expand=True,
    )

# صفحة جدول الأوقات
def time_table(page: ft.Page):
    button_width = min(150, page.width * 0.3)
    button_height = 60 if page.height > 600 else 50
    table_width = min(800, page.width * 0.9)
    table_height = min(500, page.height * 0.7)

    clear_message = ft.Text("", size=20, color="#F44336")
    undo_button = ft.ElevatedButton(
        "تراجع",
        disabled=True,
        bgcolor="#616161",
        color="#FFFFFF",
        width=button_width,
        height=button_height,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            elevation=5,
            shadow_color="#000000",
            overlay_color=ft.colors.with_opacity(0.2, "#FFFFFF"),
        ),
    )
    last_action = [None, None]  # [action_type, action_data]

    def update_table():
        table.rows.clear()
        if not time_list:
            table.rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text("لا توجد أوقات مدخلة بعد!")),
                ft.DataCell(ft.Text("")),
                ft.DataCell(ft.Text("")),
                ft.DataCell(ft.Text("")),
                ft.DataCell(ft.Text("")),
                ft.DataCell(ft.Text("")),
                ft.DataCell(ft.Text("")),
            ]))
        else:
            for i, entry in enumerate(time_list):
                duration_minutes = "0"
                if i > 0 and time_list[i]['date_str'] == time_list[i-1]['date_str']:
                    duration = time_list[i]['original_time'] - time_list[i-1]['original_time']
                    duration_minutes = str(duration.seconds // 60)

                delete_button = ft.ElevatedButton(
                    "حذف",
                    bgcolor="#D32F2F",
                    color="#FFFFFF",
                    data=i,
                    on_click=lambda e: delete_entry(e.control.data),
                    on_hover=page.play_hover_sound,  # صوت عند المرور
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=5),
                        elevation=3,
                        overlay_color=ft.colors.with_opacity(0.2, "#FFFFFF"),
                    ),
                )
                edit_button = ft.ElevatedButton(
                    "تعديل",
                    bgcolor="#388E3C",
                    color="#FFFFFF",
                    data=i,
                    on_click=lambda e: edit_entry(e.control.data),
                    on_hover=page.play_hover_sound,  # صوت عند المرور
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=5),
                        elevation=3,
                        overlay_color=ft.colors.with_opacity(0.2, "#FFFFFF"),
                    ),
                )

                table.rows.append(ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(i+1))),
                    ft.DataCell(ft.Text(entry['date_str'])),
                    ft.DataCell(ft.Text(entry['original_time'].strftime('%H:%M'))),
                    ft.DataCell(ft.Text(entry['new_time'].strftime('%H:%M'))),
                    ft.DataCell(ft.Text(duration_minutes)),
                    ft.DataCell(delete_button),
                    ft.DataCell(edit_button),
                ]))
        table_container.content = table
        page.update()

    def delete_entry(index):
        page.play_click_sound()
        nonlocal last_action
        if 0 <= index < len(time_list):
            last_action[0] = "delete"
            last_action[1] = (index, time_list[index])
            undo_button.disabled = False
            undo_button.bgcolor = "#1976D2"
            time_list.pop(index)
            update_table()

    def edit_entry(index):
        page.play_click_sound()
        nonlocal last_action
        if 0 <= index < len(time_list):
            entry = time_list[index]
            date_input = ft.TextField(value=entry['date_str'], hint_text="يوم/شهر/سنة", border_radius=10, bgcolor="#FFFFFF", border_color="#1976D2")
            time_input = ft.TextField(value=entry['original_time'].strftime('%H:%M'), hint_text="ساعة:دقيقة", border_radius=10, bgcolor="#FFFFFF", border_color="#1976D2")
            minutes_input = ft.TextField(value=str(entry['added_minutes']), hint_text="الدقائق المضافة", border_radius=10, bgcolor="#FFFFFF", border_color="#1976D2")

            def save_changes(e):
                page.play_click_sound()
                try:
                    new_date_str = date_input.value.strip()
                    if not re.match(r'^\d{2}/\d{2}/\d{4}$', new_date_str):
                        page.snack_bar = ft.SnackBar(ft.Text("خطأ: تنسيق التاريخ غير صالح! استخدم DD/MM/YYYY"))
                        page.snack_bar.open = True
                        page.update()
                        return

                    new_time_str = time_input.value.strip()
                    if not re.match(r'^\d{1,2}:\d{2}$', new_time_str):
                        page.snack_bar = ft.SnackBar(ft.Text("خطأ: تنسيق الوقت غير صالح! استخدم HH:MM"))
                        page.snack_bar.open = True
                        page.update()
                        return

                    hours, minutes = map(int, new_time_str.split(':'))
                    if hours < 0 or hours > 23 or minutes < 0 or minutes > 59:
                        page.snack_bar = ft.SnackBar(ft.Text("خطأ: الساعات: 0-23، الدقائق: 0-59!"))
                        page.snack_bar.open = True
                        page.update()
                        return

                    new_added_minutes = int(minutes_input.value.strip())
                    if new_added_minutes < 0:
                        page.snack_bar = ft.SnackBar(ft.Text("خطأ: الدقائق يجب أن تكون موجبة!"))
                        page.snack_bar.open = True
                        page.update()
                        return

                    new_time_obj = datetime.strptime(f"01/01/2000 {new_time_str}", "%d/%m/%Y %H:%M")
                    new_time = new_time_obj + timedelta(minutes=new_added_minutes)

                    last_action[0] = "edit"
                    last_action[1] = (index, time_list[index])
                    time_list[index] = {
                        'date_str': new_date_str,
                        'original_time': new_time_obj,
                        'new_time': new_time,
                        'added_minutes': new_added_minutes
                    }
                    undo_button.disabled = False
                    undo_button.bgcolor = "#1976D2"
                    update_table()
                    page.dialog.open = False
                    page.update()
                except Exception as err:
                    page.snack_bar = ft.SnackBar(ft.Text(f"خطأ أثناء التعديل: {str(err)}"))
                    page.snack_bar.open = True
                    page.update()

            dialog = ft.AlertDialog(
                title=ft.Text(f"تعديل الإدخال {index + 1}"),
                content=ft.Column([date_input, time_input, minutes_input], spacing=10),
                actions=[ft.ElevatedButton(
                    "حفظ",
                    on_click=save_changes,
                    on_hover=page.play_hover_sound,  # صوت عند المرور
                    bgcolor="#1976D2",
                    color="#FFFFFF"
                )],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            page.dialog = dialog
            dialog.open = True
            page.update()

    def undo_action(e):
        page.play_click_sound()
        nonlocal last_action
        global time_list
        if last_action[0] == "delete":
            index, entry = last_action[1]
            time_list.insert(index, entry)
        elif last_action[0] == "edit":
            index, entry = last_action[1]
            time_list[index] = entry
        elif last_action[0] == "clear":
            time_list.clear()
            time_list.extend(last_action[1])
        last_action[0] = None
        last_action[1] = None
        undo_button.disabled = True
        undo_button.bgcolor = "#616161"
        update_table()

    def clear_table(e):
        page.play_click_sound()
        nonlocal last_action
        if time_list:
            last_action[0] = "clear"
            last_action[1] = time_list.copy()
            time_list.clear()
            clear_message.value = "تم مسح الجدول!"
            undo_button.disabled = False
            undo_button.bgcolor = "#1976D2"
            update_table()

    def save_to_file(e):
        page.play_click_sound()
        if not time_list:
            page.snack_bar = ft.SnackBar(ft.Text("لا يوجد شيء للحفظ!"))
            page.snack_bar.open = True
            page.update()
            return
        try:
            with open("time_table.txt", "w", encoding="utf-8") as file:
                file.write("جدول الأوقات\n")
                for i, entry in enumerate(time_list):
                    file.write(f"{i+1}- الأصلي: {entry['original_time'].strftime('%H:%M')} بتاريخ {entry['date_str']}، الجديد: {entry['new_time'].strftime('%H:%M')} بتاريخ {entry['date_str']}\n")
                    duration_minutes = "0" if i == 0 or time_list[i]['date_str'] != time_list[i-1]['date_str'] else str((time_list[i]['original_time'] - time_list[i-1]['original_time']).seconds // 60)
                    file.write(f"   المدة: {duration_minutes} دقيقة\n")
            page.snack_bar = ft.SnackBar(ft.Text("تم الحفظ في time_table.txt"))
            page.snack_bar.open = True
        except Exception as err:
            page.snack_bar = ft.SnackBar(ft.Text(f"خطأ أثناء حفظ الملف: {str(err)}"))
            page.snack_bar.open = True
        page.update()

    def go_to_add_time(e):
        page.play_click_sound()
        page.current_screen = "add_time"
        update_page(page)

    def go_to_menu(e):
        page.play_click_sound()
        page.current_screen = "menu"
        update_page(page)

    def exit_app(e):
        page.play_click_sound()
        page.window.close()

    undo_button.on_click = undo_action
    undo_button.on_hover = page.play_hover_sound  # صوت عند المرور
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("الرقم", color="#FFFFFF")),
            ft.DataColumn(ft.Text("التاريخ", color="#FFFFFF")),
            ft.DataColumn(ft.Text("الوقت", color="#FFFFFF")),
            ft.DataColumn(ft.Text("الوقت الجديد", color="#FFFFFF")),
            ft.DataColumn(ft.Text("المدة\n(دقائق)", color="#FFFFFF")),
            ft.DataColumn(ft.Text("حذف", color="#FFFFFF")),
            ft.DataColumn(ft.Text("تعديل", color="#FFFFFF")),
        ],
        heading_row_color="#0D47A1",
        data_row_color="#FFFFFF",
        border=ft.border.all(1, "#1976D2"),
        rows=[],
    )

    table_container = ft.Container(
        content=table,
        bgcolor="#FFFFFF",
        width=table_width,
        height=table_height,
        padding=5,
        border_radius=10,
        shadow=ft.BoxShadow(
            spread_radius=2,
            blur_radius=20,
            color="#000000",
            offset=ft.Offset(0, 5),
        ),
    )

    update_table()

    return ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.ElevatedButton(
                                    "العودة للإدخال",
                                    on_click=go_to_add_time,
                                    on_hover=page.play_hover_sound,  # صوت عند المرور
                                    bgcolor="#1976D2",
                                    color="#FFFFFF",
                                    width=button_width,
                                    height=button_height,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=10),
                                        elevation=5,
                                        shadow_color="#000000",
                                        overlay_color=ft.colors.with_opacity(0.2, "#FFFFFF"),
                                    ),
                                ),
                                ft.ElevatedButton(
                                    "الرئيسية",
                                    on_click=go_to_menu,
                                    on_hover=page.play_hover_sound,  # صوت عند المرور
                                    bgcolor="#616161",
                                    color="#FFFFFF",
                                    width=button_width,
                                    height=button_height,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=10),
                                        elevation=5,
                                        shadow_color="#000000",
                                        overlay_color=ft.colors.with_opacity(0.2, "#FFFFFF"),
                                    ),
                                ),
                                ft.ElevatedButton(
                                    "مسح الجدول",
                                    on_click=clear_table,
                                    on_hover=page.play_hover_sound,  # صوت عند المرور
                                    bgcolor="#D32F2F",
                                    color="#FFFFFF",
                                    width=button_width,
                                    height=button_height,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=10),
                                        elevation=5,
                                        shadow_color="#000000",
                                        overlay_color=ft.colors.with_opacity(0.2, "#FFFFFF"),
                                    ),
                                ),
                                clear_message,
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=10,
                            width=button_width + 20,
                        ),
                        ft.Column(
                            [
                                ft.Text("جدول الأوقات", size=30, weight=ft.FontWeight.BOLD, bgcolor="#0D47A1", color="#FFFFFF", width=table_width, text_align=ft.TextAlign.CENTER),
                                table_container,
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            scroll=ft.ScrollMode.AUTO,
                        ),
                        ft.Column(
                            [
                                ft.ElevatedButton(
                                    "حفظ إلى ملف",
                                    on_click=save_to_file,
                                    on_hover=page.play_hover_sound,  # صوت عند المرور
                                    bgcolor="#1976D2",
                                    color="#FFFFFF",
                                    width=button_width,
                                    height=button_height,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=10),
                                        elevation=5,
                                        shadow_color="#000000",
                                        overlay_color=ft.colors.with_opacity(0.2, "#FFFFFF"),
                                    ),
                                ),
                                ft.ElevatedButton(
                                    "خروج",
                                    on_click=exit_app,
                                    on_hover=page.play_hover_sound,  # صوت عند المرور
                                    bgcolor="#D32F2F",
                                    color="#FFFFFF",
                                    width=button_width,
                                    height=button_height,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=10),
                                        elevation=5,
                                        shadow_color="#000000",
                                        overlay_color=ft.colors.with_opacity(0.2, "#FFFFFF"),
                                    ),
                                ),
                                undo_button,
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=10,
                            width=button_width + 20,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
        ),
        padding=15,
        border_radius=15,
        bgcolor=ft.colors.with_opacity(0.98, "#FFFFFF"),
        shadow=ft.BoxShadow(
            spread_radius=2,
            blur_radius=20,
            color="#000000",
            offset=ft.Offset(0, 5),
        ),
        alignment=ft.alignment.center,
        expand=True,
    )

if __name__ == "__main__":
    ft.app(target=main)
