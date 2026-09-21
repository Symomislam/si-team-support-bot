import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# =========================
# SI TEAM SUPPORT BOT
# =========================
import os
import sqlite3

TOKEN = os.environ["BOT_TOKEN"]

ADMIN_ID = 8224442012

OWNER_USERNAME = "@Symom_Si_Team_Owner"
CAPTION_CHANNEL_LINK = "https://t.me/BANGLA_CAPTION_SI"
OWNER_LINK = "https://t.me/Symom_Si_Team_Owner"
CHANNEL_LINK = "https://t.me/Symom_Si_Team"

DB_NAME = "si_team_support.db"


# =========================
# DATABASE
# =========================

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            category TEXT,
            message TEXT,
            status TEXT DEFAULT 'open'
        )
    """)

    conn.commit()
    conn.close()


def save_user(user):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        INSERT OR REPLACE INTO users
        (user_id, username, first_name)
        VALUES (?, ?, ?)
    """, (
        user.id,
        user.username or "",
        user.first_name or ""
    ))

    conn.commit()
    conn.close()


# =========================
# START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    save_user(update.effective_user)

    keyboard = [
        [
            InlineKeyboardButton("🎫 Support", callback_data="support"),
            InlineKeyboardButton("❓ Help Center", callback_data="help")
        ],
        [
            InlineKeyboardButton("📜 Rules", callback_data="rules"),
            InlineKeyboardButton("👤 Owner", url=OWNER_LINK)
        ],
        [
            InlineKeyboardButton(
                "📢 Official Channel",
                url=CHANNEL_LINK
            )
        ],
        [
            InlineKeyboardButton("ℹ️ About", callback_data="about")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    text = (
        "╔════════════════════╗\n"
        "   🤖 SI TEAM SUPPORT BOT\n"
        "╚════════════════════╝\n\n"

        "👋 Welcome to SI TEAM SUPPORT!\n\n"

        "আপনার যেকোনো সমস্যা বা প্রশ্ন থাকলে\n"
        "নিচের Support অপশন ব্যবহার করুন।\n\n"

        "🆓 Support সম্পূর্ণ Free\n"
        "⚡ Fast Response\n"
        "🔐 Safe & Secure Support\n\n"

        "👇 নিচের Menu থেকে একটি অপশন নির্বাচন করুন।"
    )

    await update.message.reply_text(
        text,
        reply_markup=reply_markup
    )


# =========================
# HELP
# =========================

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = (
        "❓ HELP CENTER\n\n"
        "🎫 Support — আপনার সমস্যার জন্য Ticket তৈরি করুন।\n"
        "📜 Rules — Support ব্যবহারের নিয়ম দেখুন।\n"
        "👤 Owner — Owner-এর সাথে যোগাযোগ করুন।\n"
        "📢 Official Channel — আমাদের Official Channel।\n\n"
        "⚠️ Password, OTP বা ব্যক্তিগত গোপন তথ্য পাঠাবেন না।"
    )

    await update.message.reply_text(text)


# =========================
# BUTTON HANDLER
# =========================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query
    await query.answer()

    if query.data == "help":

        await query.message.reply_text(
            "❓ HELP CENTER\n\n"
            "Support পেতে প্রথমে Support Button চাপুন।\n\n"
            "🆓 আমাদের Support Free."
        )

    elif query.data == "rules":

        await query.message.reply_text(
            "📜 SI TEAM SUPPORT RULES\n\n"
            "1️⃣ ভদ্রভাবে কথা বলুন।\n"
            "2️⃣ Spam করবেন না।\n"
            "3️⃣ Password / OTP পাঠাবেন না।\n"
            "4️⃣ মিথ্যা তথ্য দেবেন না।\n"
            "5️⃣ Support-এর অপব্যবহার করবেন না।\n\n"
            "⚠️ নিয়ম ভঙ্গ করলে Support বন্ধ করা হতে পারে।"
        )

    elif query.data == "about":

        await query.message.reply_text(
            "ℹ️ ABOUT SI TEAM SUPPORT BOT\n\n"
            "🤖 Name: SI TEAM SUPPORT BOT\n"
            "🆓 Support: Free\n"
            "🌐 Language: Bangla + English\n\n"
            "👤 Owner: " + OWNER_USERNAME
        )

    elif query.data == "support":

        keyboard = [
            [
                InlineKeyboardButton(
                    "General Support",
                    callback_data="cat_general"
                )
            ],
            [
                InlineKeyboardButton(
                    "Account Help",
                    callback_data="cat_account"
                )
            ],
            [
                InlineKeyboardButton(
                    "Technical Help",
                    callback_data="cat_technical"
                )
            ],
            [
                InlineKeyboardButton(
                    "Other Problem",
                    callback_data="cat_other"
                )
            ]
        ]

        await query.message.reply_text(
            "🎫 SUPPORT CENTER\n\n"
            "আপনার সমস্যার Category নির্বাচন করুন:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data.startswith("cat_"):

        category_map = {
            "cat_general": "General Support",
            "cat_account": "Account Help",
            "cat_technical": "Technical Help",
            "cat_other": "Other Problem"
        }

        category = category_map.get(
            query.data,
            "Other Problem"
        )

        context.user_data["support_mode"] = True
        context.user_data["category"] = category

        await query.message.reply_text(
            f"✅ Category: {category}\n\n"
            "এখন আপনার সমস্যাটি বিস্তারিত লিখে পাঠান।\n\n"
            "✏️ আপনার Message লিখুন:"
        )

    elif query.data.startswith("reply_"):

        if query.from_user.id != ADMIN_ID:
            return

        ticket_id = int(query.data.split("_")[1])

        context.user_data["reply_ticket"] = ticket_id

        await query.message.reply_text(
            f"✏️ Ticket #{ticket_id}-এর জন্য Reply লিখুন:"
        )

    elif query.data.startswith("close_"):

        if query.from_user.id != ADMIN_ID:
            return

        ticket_id = int(query.data.split("_")[1])

        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()

        cur.execute(
            "UPDATE tickets SET status='closed' WHERE id=?",
            (ticket_id,)
        )

        conn.commit()
        conn.close()

        await query.message.reply_text(
            f"✅ Ticket #{ticket_id} closed."
        )


# =========================
# USER MESSAGE
# =========================

async def user_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if update.effective_user.id == ADMIN_ID:
        return

    if not context.user_data.get("support_mode"):
        return

    message = update.message.text
    category = context.user_data.get(
        "category",
        "Other Problem"
    )

    user = update.effective_user

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO tickets
        (user_id, category, message, status)
        VALUES (?, ?, ?, 'open')
    """, (
        user.id,
        category,
        message
    ))

    ticket_id = cur.lastrowid

    conn.commit()
    conn.close()

    context.user_data["support_mode"] = False

    username = (
        "@" + user.username
        if user.username
        else "No Username"
    )

    keyboard = [
        [
            InlineKeyboardButton(
                "✏️ Reply",
                callback_data=f"reply_{ticket_id}"
            ),
            InlineKeyboardButton(
                "🔒 Close",
                callback_data=f"close_{ticket_id}"
            )
        ]
    ]

    admin_text = (
        "🚨 NEW SUPPORT TICKET\n\n"
        f"🎫 Ticket ID: #{ticket_id}\n"
        f"👤 User: {user.first_name}\n"
        f"🔗 Username: {username}\n"
        f"🆔 User ID: {user.id}\n"
        f"📂 Category: {category}\n\n"
        f"💬 Message:\n{message}"
    )

    try:
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=admin_text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except Exception as e:
        print("Admin notification error:", e)

    await update.message.reply_text(
        f"✅ আপনার Support Ticket তৈরি হয়েছে!\n\n"
        f"🎫 Ticket ID: #{ticket_id}\n"
        "⏳ Admin আপনার Message দেখলে Reply করবেন।\n\n"
        "🆓 Support সম্পূর্ণ Free."
    )


# =========================
# ADMIN MESSAGE
# =========================

async def admin_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if update.effective_user.id != ADMIN_ID:
        return

    ticket_id = context.user_data.get("reply_ticket")

    if not ticket_id:
        return

    reply_text = update.message.text

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        "SELECT user_id FROM tickets WHERE id=?",
        (ticket_id,)
    )

    result = cur.fetchone()

    conn.close()

    if not result:
        await update.message.reply_text(
            "❌ Ticket পাওয়া যায়নি।"
        )
        return

    user_id = result[0]

    try:

        await context.bot.send_message(
            chat_id=user_id,
            text=(
                f"💬 SI TEAM SUPPORT REPLY\n\n"
                f"🎫 Ticket: #{ticket_id}\n\n"
                f"{reply_text}\n\n"
                "👤 SI TEAM SUPPORT"
            )
        )

        await update.message.reply_text(
            f"✅ Reply sent to Ticket #{ticket_id}"
        )

    except Exception as e:

        await update.message.reply_text(
            "❌ User-কে message পাঠানো যায়নি.\n"
            "User হয়তো Bot-এ /start করেননি।"
        )

        print("Reply error:", e)

    context.user_data["reply_ticket"] = None


# =========================
# STATS
# =========================

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM users")
    users = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM tickets")
    tickets = cur.fetchone()[0]

    cur.execute(
        "SELECT COUNT(*) FROM tickets WHERE status='open'"
    )
    open_tickets = cur.fetchone()[0]

    conn.close()

    await update.message.reply_text(
        "📊 SI TEAM SUPPORT STATS\n\n"
        f"👥 Users: {users}\n"
        f"🎫 Total Tickets: {tickets}\n"
        f"🔴 Open Tickets: {open_tickets}"
    )


# =========================
# MAIN
# =========================

def main():

    init_db()

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("stats", stats))

    app.add_handler(
        CallbackQueryHandler(button_handler)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            admin_message
        ),
        group=0
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            user_message
        ),
        group=1
    )

    print("SI TEAM SUPPORT BOT IS RUNNING...")

    app.run_polling()


if __name__ == "__main__":
    main()