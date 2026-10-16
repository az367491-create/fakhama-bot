import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8605151509:AAG-Hq9svFQWUx1Qd1JE6iqu5SPf1J1c3cU"
ADMIN_ID = 7404211847

PRODUCTS = {
 "1": {"name": "بارتي ستار 10k", "price": "$12"},
 "2": {"name": "بينمو شات 11300", "price": "$5"},
 "3": {"name": "سحب سناب شات", "price": "$8"},
}

carts = {}
logging.basicConfig(level=logging.INFO)

def main_kb():
    kb = []
    for pid, p in PRODUCTS.items():
        kb.append([InlineKeyboardButton(f"{p['name']} - {p['price']}", callback_data=f"view_{pid}")])
    kb.append([InlineKeyboardButton("🌐 المتجر", url="https://amhd2pcom.mtjry.online")])
    kb.append([InlineKeyboardButton("🛒 السلة", callback_data="cart")])
    return InlineKeyboardMarkup(kb)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔥 فخامة كارت 🔥\nاختار:", reply_markup=main_kb())

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = q.from_user.id
    data = q.data
    if data.startswith("view_"):
        pid = data.split("_")[1]
        p = PRODUCTS[pid]
        kb = [[InlineKeyboardButton(f"اضف للسلة {p['price']}", callback_data=f"add_{pid}")],[InlineKeyboardButton("رجوع", callback_data="back")]]
        await q.edit_message_text(f"{p['name']}\nالسعر: {p['price']}", reply_markup=InlineKeyboardMarkup(kb))
    elif data.startswith("add_"):
        pid = data.split("_")[1]
        carts.setdefault(uid, []).append(pid)
        await q.answer("تمت الاضافة ✅", show_alert=True)
    elif data == "cart":
        items = carts.get(uid, [])
        if not items:
            await q.edit_message_text("السلة فاضية", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("رجوع", callback_data="back")]]))
            return
        txt = "\n".join([PRODUCTS[i]['name'] for i in items])
        kb = [[InlineKeyboardButton("تأكيد الطلب ✅", callback_data="checkout")],[InlineKeyboardButton("رجوع", callback_data="back")]]
        await q.edit_message_text(f"سلتك:\n{txt}", reply_markup=InlineKeyboardMarkup(kb))
    elif data == "checkout":
        items = carts.get(uid, [])
        txt = "\n".join([PRODUCTS[i]['name'] for i in items])
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"طلب جديد من {q.from_user.full_name} - {uid}\n{txt}")
        carts[uid] = []
        await q.edit_message_text("تم ارسال طلبك ✅ راح نتواصل معك", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("الرئيسية", callback_data="back")]]))
    elif data == "back":
        await q.edit_message_text("🔥 فخامة كارت 🔥", reply_markup=main_kb())

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(handle))
app.run_polling()
