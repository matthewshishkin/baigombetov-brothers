#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate PDF summary of app vision from conversation."""

import os
from fpdf import FPDF

FONT = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
OUT = os.path.join(os.path.dirname(__file__), "ТЗ-приложение-сводка-из-переписки.pdf")


class PDF(FPDF):
    def header(self):
        self.set_font("AppFont", "", 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, "Сводка требований к приложению (из переписки)", align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-12)
        self.set_font("AppFont", "", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 8, f"Стр. {self.page_no()}", align="C")


def section(pdf, title):
    pdf.ln(4)
    pdf.set_font("AppFont", "B", 12)
    pdf.set_text_color(25, 45, 85)
    pdf.multi_cell(0, 7, title)
    pdf.set_text_color(35, 35, 35)
    pdf.ln(1)


def row(pdf, label, text):
    pdf.set_font("AppFont", "B", 9)
    pdf.multi_cell(186, 5, label)
    pdf.set_font("AppFont", "", 9)
    pdf.multi_cell(186, 5, text)
    pdf.ln(2)


def compare_table(pdf, headers, data_rows):
    w = (38, 74, 74)
    pdf.set_font("AppFont", "B", 8)
    pdf.set_fill_color(230, 234, 244)
    for i, h in enumerate(headers):
        pdf.cell(w[i], 6, h, border=1, fill=True)
    pdf.ln(6)
    pdf.set_font("AppFont", "", 8)
    pdf.set_fill_color(255, 255, 255)
    for row in data_rows:
        h0 = pdf.get_y()
        if h0 > 255:
            pdf.add_page()
            h0 = pdf.get_y()
        x0 = pdf.get_x()
        x = x0
        max_h = 6
        for i, cell in enumerate(row):
            pdf.set_xy(x, h0)
            before = pdf.get_y()
            pdf.multi_cell(w[i], 4, cell, border=1)
            after = pdf.get_y()
            max_h = max(max_h, after - h0)
            x += w[i]
        pdf.set_xy(x0, h0 + max_h)


def main():
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=16)
    pdf.add_font("AppFont", "", FONT)
    pdf.add_font("AppFont", "B", FONT)
    pdf.add_page()

    pdf.set_font("AppFont", "B", 16)
    pdf.set_text_color(20, 30, 50)
    pdf.multi_cell(0, 9, "Идея приложения — сводка в таблицах")
    pdf.ln(1)
    pdf.set_font("AppFont", "", 10)
    pdf.set_text_color(45, 45, 45)
    pdf.multi_cell(
        0,
        5,
        "Собрано из вашего описания в переписке: функции, интеграции, подход к разработке и сравнение "
        "со скоростью создания узкого инструмента (перевод видео за 2 дня).",
    )

    section(pdf, "1. Маркетинг, сценарии и лендинги")
    for label, text in [
        ("Цель", "Автоматически: рекламные сценарии, оффер, затем сайт из готовой папки-шаблона на ПК (подстановка текстов)."),
        ("Тексты", "Генерация через API Claude; удобно структурированный вывод (JSON) для вставки в шаблон."),
        ("Шаблон", "Единый источник текстов (JSON / i18n / плейсхолдеры) надёжнее «любого HTML»."),
        ("Репозиторий", "Создание нового репозитория через gh CLI или GitHub API (не GitHub Desktop)."),
        ("Деплой", "Публикация на Vercel: связка репозитория с Vercel или Vercel CLI с токеном."),
        ("Секреты и стабильность", "Ключи только в env; обработка ошибок API; при необходимости очередь задач."),
    ]:
        row(pdf, label, text)

    section(pdf, "2. CRM и мобильный доступ")
    for label, text in [
        ("Продукт", "Небольшая CRM."),
        ("iPhone", "Адаптивный веб + PWA («На экран Домой»); при необходимости позже Capacitor / App Store."),
        ("Объём", "CRM отделена от конвейера «сценарий → сайт»; сроки растут с числом сущностей и пользователей."),
    ]:
        row(pdf, label, text)

    section(pdf, "3. ИИ-аватар и видеомонтаж")
    for label, text in [
        ("Аватар", "API провайдера (HeyGen, Synthesia, D-ID и т.п.); «обучение» = кастомный аватар у сервиса."),
        ("Монтаж", "По сценарию: тишина (ffmpeg/VAD), повторы (ASR + логика/LLM), субтитры (транскрипт + наложение)."),
        ("Инфраструктура", "Несколько стадий и внешних API; длинное видео — фоновые задачи и статусы."),
    ]:
        row(pdf, label, text)

    section(pdf, "4. Процесс, Google Sheets, настройка ИИ")
    for label, text in [
        ("Регламенты", "Разработка по мере описания регламентов — короткие итерации."),
        ("Google Таблицы", "Запись готовых текстов сценариев в таблицу (Sheets API + OAuth, сервисный аккаунт или Apps Script)."),
        ("Сценарии по параметрам", "Промпт + схема JSON + примеры; при необходимости fine-tuning или RAG."),
    ]:
        row(pdf, label, text)

    section(pdf, "5. Сравнение: перевод видео за 2 дня vs большой стек")
    compare_table(
        pdf,
        ["Критерий", "Перевод EN→RU", "Большой стек"],
        [
            ("Фокус", "Один конвейер", "Несколько конвейеров + оболочка"),
            ("Интеграции", "ASR, перевод, TTS, ffmpeg", "Claude, Git, Vercel, аватар, транскрипт, рендер"),
            ("MVP по времени", "Порядка дней при фокусе", "Недели/месяцы по глубине"),
        ],
    )

    pdf.ln(6)
    pdf.set_font("AppFont", "", 9)
    pdf.set_text_color(85, 85, 85)
    pdf.multi_cell(
        0,
        5,
        "Файл: ТЗ-приложение-сводка-из-переписки.pdf. Пересборка: python3 build_app_vision_pdf.py",
    )

    pdf.output(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
