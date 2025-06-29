#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# audiblez (patched for --list-chapters only)

import os
import platform
import traceback
import re
import time
from io import StringIO
from pathlib import Path
from string import Formatter
from types import SimpleNamespace
from glob import glob

import ebooklib
import spacy
from bs4 import BeautifulSoup
from ebooklib import epub
from tabulate import tabulate


def load_spacy():
    if not spacy.util.is_package("xx_ent_wiki_sm"):
        print("📦 Downloading SpaCy model xx_ent_wiki_sm...")
        spacy.cli.download("xx_ent_wiki_sm")


def chapter_beginning_one_liner(c, chars=60):
    s = c.extracted_text[:chars].strip().replace('\n', ' ').replace('\r', ' ')
    return s + '…' if s else ''


def find_document_chapters_and_extract_texts(book):
    document_chapters = []
    for chapter in book.get_items():
        if chapter.get_type() != ebooklib.ITEM_DOCUMENT:
            continue
        xml = chapter.get_body_content()
        soup = BeautifulSoup(xml, features='lxml')
        chapter.extracted_text = ''
        for tag in ['title', 'p', 'h1', 'h2', 'h3', 'h4', 'li']:
            for element in soup.find_all(tag):
                text = element.text.strip()
                if not text:
                    continue
                if not text.endswith('.'):
                    text += '.'
                chapter.extracted_text += text + '\n'
        document_chapters.append(chapter)
    for i, c in enumerate(document_chapters):
        c.chapter_index = i
    return document_chapters


def list_chapters(epub_path):
    """
    ✅ List all chapters in the given EPUB file
    """
    try:
        load_spacy()
        book = epub.read_epub(epub_path)
        chapters = find_document_chapters_and_extract_texts(book)
        if not chapters:
            print("❌ No chapters found.")
            return

        print(f"\n📚 Found {len(chapters)} chapters:\n")
        print(tabulate([
            [i + 1, ch.get_name(), len(ch.extracted_text), chapter_beginning_one_liner(ch)]
            for i, ch in enumerate(chapters)
        ], headers=["#", "Chapter Name", "Text Length", "Preview"]))
    except Exception as e:
        print("❌ Error listing chapters:", e)
        traceback.print_exc()
