import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# =========================================================
# مخزن الهنداوي - Telegram Store Bot
# =========================================================

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("BOT_TOKEN is not configured")


# =========================================================
# المنتجات
# السعر هنا هو السعر المرجعي من الكتالوك
# ويمكن تغييره لاحقاً إلى سعر الجملة الحقيقي
# =========================================================

PRODUCTS = {

    # ---------------- الحلويات والشوكولاتة ----------------

    1: ("ADICTO NESTLE CRISPY 15G", 500, "حلويات وشوكولاتة"),
    2: ("ADICTO NESTLE HAZELNUT 17G", 500, "حلويات وشوكولاتة"),
    3: ("ADICTO NESTLE HAZELNUT 60G", 1475, "حلويات وشوكولاتة"),
    4: ("ADICTO NESTLE MILK 17G", 500, "حلويات وشوكولاتة"),
    5: ("ADICTO NESTLE MILK 65G", 1475, "حلويات وشوكولاتة"),
    6: ("ADICTO NESTLE PISTACHIO 17G", 500, "حلويات وشوكولاتة"),
    7: ("ADICTO NESTLE PISTACHIO 60G", 1500, "حلويات وشوكولاتة"),
    8: ("ALBENI NESTLE CHOCOLATE 25G", 250, "حلويات وشوكولاتة"),
    9: ("ALBENI NESTLE FINGER VIVA MILK 25G", 250, "حلويات وشوكولاتة"),
    10: ("BUFALO ENERGY CHOCOLATE 20G", 1850, "حلويات وشوكولاتة"),
    11: ("CADBURY BUBBLY DAIRY MILK 24G", 875, "حلويات وشوكولاتة"),
    12: ("CADBURY BUBBLY 87G", 1825, "حلويات وشوكولاتة"),
    13: ("CADBURY DAIRY MILK 35G", 875, "حلويات وشوكولاتة"),
    14: ("CADBURY DAIRY MILK HAZELNUT 35G", 875, "حلويات وشوكولاتة"),
    15: ("CADBURY DAIRY MILK RAISINS NUTS 35G", 875, "حلويات وشوكولاتة"),
    16: ("CADBURY FLAKE DIPPED 32G", 900, "حلويات وشوكولاتة"),
    17: ("CADBURY FLAKE 15G", 500, "حلويات وشوكولاتة"),
    18: ("CADBURY FLAKE 32G", 900, "حلويات وشوكولاتة"),
    19: ("CADBURY MINI BUBBLY BAGS 156G", 4350, "حلويات وشوكولاتة"),
    20: ("CADBURY OREO 35G", 875, "حلويات وشوكولاتة"),

    # ---------------- مكسرات ونساتل ----------------

    21: ("ALAMIRA ELITE NUTS BLACK BOX 450G", 17025, "مكسرات ونساتل"),
    22: ("ALAMIRA LUXURY KERNEL NUTS RED BAG 250G", 6925, "مكسرات ونساتل"),
    23: ("ALAMIRA SUPER LUXURY NUTS GREEN BAG 250G", 4075, "مكسرات ونساتل"),
    24: ("CASTANIA CASHEWS 20G", 450, "مكسرات ونساتل"),
    25: ("CASTANIA CASHEWS 70G", 2875, "مكسرات ونساتل"),
    26: ("CASTANIA EXTRA 450G", 7000, "مكسرات ونساتل"),
    27: ("CASTANIA LARGE EGYPTIAN BEANS 300G", 4250, "مكسرات ونساتل"),
    28: ("CASTANIA METAL BALLS 400G", 12750, "مكسرات ونساتل"),
    29: ("CASTANIA NUTS EXTRA 250G", 3375, "مكسرات ونساتل"),
    30: ("CASTANIA NUTS EXTRA 400G", 5375, "مكسرات ونساتل"),
    31: ("CASTANIA NUTS KERNELS 250G", 7125, "مكسرات ونساتل"),
    32: ("CASTANIA NUTS SUPER EXTRA 300G", 4250, "مكسرات ونساتل"),
    33: ("CASTANIA OBAID PEELED 20G", 250, "مكسرات ونساتل"),
    34: ("CASTANIA SUNFLOWER 30G", 225, "مكسرات ونساتل"),
    35: ("CASTANIA SUNFLOWER SALT&VINEGAR 150G", 1875, "مكسرات ونساتل"),
    36: ("CASTANIA SUNFLOWER SEEDS 250G", 1625, "مكسرات ونساتل"),
    37: ("CASTANIA SUNFLOWER SEEDS WITHOUT SALT 250G", 1750, "مكسرات ونساتل"),
    38: ("NUTS EXTRA MIX 250G", 3375, "مكسرات ونساتل"),
    39: ("NUTS EXTRA MIX 400G", 5375, "مكسرات ونساتل"),
    40: ("KERNEL NUTS 250G", 7125, "مكسرات ونساتل"),

    # ---------------- كيك وبسكويت ----------------

    41: ("ADICTO CAKE COCOA 200G", 2825, "كيك وبسكويت"),
    42: ("EURO DOUBLE COCONUT CAKE 50G", 250, "كيك وبسكويت"),
    43: ("EURO JUMBO CROISSANT CHOCOLATE 50G", 250, "كيك وبسكويت"),
    44: ("EURO JUMBO SWISS ROLL CAKE 56G", 250, "كيك وبسكويت"),
    45: ("EURO JUMBO SWISS ROLL CHOCOLATE 50G", 250, "كيك وبسكويت"),
    46: ("EURO JUMBO SWISS ROLL ORANGE 56G", 250, "كيك وبسكويت"),
    47: ("HANIPERS CHOCOLATE CAKE 36G", 250, "كيك وبسكويت"),
    48: ("HANIPERS VANILLA CAKE 36G", 250, "كيك وبسكويت"),
    49: ("BRITONA CHOCOLATE CAKE 34G", 225, "كيك وبسكويت"),
    50: ("BRITONA CHOCOLATE RASPBERRY CAKE 34G", 225, "كيك وبسكويت"),
    51: ("CAPTAIN MILLER COCONUT WAFER 42G", 250, "كيك وبسكويت"),
    52: ("CAPTAIN MILLER MIXED WAFER 42G", 250, "كيك وبسكويت"),
    53: ("CHIC CHOC COCOA WAFER 20G", 125, "كيك وبسكويت"),
    54: ("BISKREM EXTRA BISCUITS 184G", 1350, "كيك وبسكويت"),
    55: ("BRITANNIA MILK FLAVORED BISCUITS 77G", 465, "كيك وبسكويت"),
    56: ("GULLON ANIMAL BISCUIT 600G", 3375, "كيك وبسكويت"),
    57: ("OREO BISCUIT ORIGINAL 147.2G", 1300, "كيك وبسكويت"),
    58: ("OREO CHOCOLATE CREAM BISCUIT 36.8G", 500, "كيك وبسكويت"),
    59: ("OREO GOLDEN BISCUIT 36.8G", 500, "كيك وبسكويت"),
    60: ("OLALA CHOCOLATE SOUFFLE CAKE 70G", 900, "كيك وبسكويت"),

    # ---------------- عصائر ومشروبات ----------------

    61: ("SUNQUICK APRICOT AND ORANGE CONCENTRATE 840ML", 6250, "عصائر ومشروبات"),
    62: ("SUNQUICK COCKTAIL CONCENTRATE 840ML", 6250, "عصائر ومشروبات"),
    63: ("SUNQUICK COCKTAIL JUICE 200ML", 250, "عصائر ومشروبات"),
    64: ("SUNQUICK LEMON CONCENTRATE 840ML", 6250, "عصائر ومشروبات"),
    65: ("SUNQUICK MANGO CONCENTRATE 840ML", 6250, "عصائر ومشروبات"),
    66: ("SUNQUICK ORANGE JUICE 1L", 1350, "عصائر ومشروبات"),
    67: ("SUNQUICK ORANGE JUICE 200ML", 250, "عصائر ومشروبات"),
    68: ("SUNQUICK ORANGE CONCENTRATE 840ML", 6250, "عصائر ومشروبات"),
    69: ("SUNQUICK ORANGE MIXED CONCENTRATE 840ML", 6250, "عصائر ومشروبات"),
    70: ("SUNQUICK PEACH AND ORANGE CONCENTRATE 840ML", 6250, "عصائر ومشروبات"),
    71: ("SUNQUICK PEACH JUICE 1L", 1350, "عصائر ومشروبات"),
    72: ("SUNQUICK PEACH JUICE 200ML", 250, "عصائر ومشروبات"),
    73: ("SUNQUICK PINEAPPLE JUICE 1L", 1350, "عصائر ومشروبات"),
    74: ("SUNQUICK PINEAPPLE JUICE 200ML", 250, "عصائر ومشروبات"),
    75: ("SUNQUICK RED FRUIT CONCENTRATE 840ML", 6250, "عصائر ومشروبات"),
    76: ("SUNQUICK RED FRUIT JUICE 200ML", 250, "عصائر ومشروبات"),
    77: ("TAZECH PLASTIC GRAPE JUICE 250ML", 240, "عصائر ومشروبات"),
    78: ("TAZECH POMEGRANATE JUICE 1L", 700, "عصائر ومشروبات"),
    79: ("TAZECH SUPER NECTAR GRAPE JUICE 1L", 950, "عصائر ومشروبات"),
    80: ("TAZECH SUPER NECTAR POMEGRANATE JUICE 1L", 950, "عصائر ومشروبات"),

    # ---------------- جبس وسناكات ----------------

    81: ("IRAQI CINEMA LEVANTINE SALT AND VINEGAR 50G", 875, "جبس وسناكات"),
    82: ("IRAQI CINEMA POP CORN BIG SALT 120G", 1300, "جبس وسناكات"),
    83: ("IRAQI CINEMA POP CORN FAMILY CARAMEL 120G", 1650, "جبس وسناكات"),
    84: ("IRAQI CINEMA POP CORN MEDIUM CARAMEL 60G", 875, "جبس وسناكات"),
    85: ("IRAQI CINEMA POP CORN MEDIUM CHEESE 50G", 875, "جبس وسناكات"),
    86: ("IRAQI CINEMA POP CORN MEDIUM GRILL 60G", 875, "جبس وسناكات"),
    87: ("IRAQI CINEMA POP CORN MEDIUM SALT 60G", 875, "جبس وسناكات"),
    88: ("IRAQI CINEMA POP CORN SMALL CARAMEL 20G", 450, "جبس وسناكات"),
    89: ("IRAQI CINEMA POP CORN SMALL SALT 15G", 450, "جبس وسناكات"),
    90: ("LORENZ CHIPS CURLY PEANUTS 120G", 2650, "جبس وسناكات"),
    91: ("LORENZ CHIPS HERBS BOX 100G", 2250, "جبس وسناكات"),
    92: ("LORENZ CHIPS MONSTER KETCHUP 75G", 2650, "جبس وسناكات"),
    93: ("LORENZ CHIPS MONSTER ORIGINAL 75G", 2650, "جبس وسناكات"),
    94: ("LORENZ CHIPS MONSTER PIZZA 75G", 2650, "جبس وسناكات"),
    95: ("LORENZ CHIPS MUENSTER CHEESE 75G", 2650, "جبس وسناكات"),
    96: ("LORENZ CRUNCHIES GRILLED 100G", 2650, "جبس وسناكات"),
    97: ("LORENZ CRUNCHIPS SALT 100G", 2650, "جبس وسناكات"),
    98: ("SNIPS POTATO CHIPS FRENCH CHEESE 28G", 500, "جبس وسناكات"),
    99: ("SNIPS POTATO CHIPS KETCHUP 60G", 950, "جبس وسناكات"),
    100: ("SNIPS POTATO CHIPS SALT 28G", 550, "جبس وسناكات"),
}


# =========================================================
# سلة المستخدمين
# =========================================================

carts = {}


def get_cart(user_id):
    if user_id not in carts:
        carts[user_id] = {}
    return carts[user_id]


def money(value):
    return f"{value:,} د.ع"


# =========================================================
# القائمة الرئيسية
# =========================================================

def main_menu():
    keyboard = [
        [
            InlineKeyboardButton("🍫 الحلويات والشوكولاتة", callback_data="cat:حلويات وشوكولاتة")
        ],
        [
            InlineKeyboardButton("🥜 المكسرات والنساتل", callback_data="cat:مكسرات ونساتل")
        ],
        [
            InlineKeyboardButton("🍰 الكيك والبسكويت", callback_data="cat:كيك وبسكويت")
        ],
        [
            InlineKeyboardButton("🧃 العصائر والمشروبات", callback_data="cat:عصائر ومشروبات")
        ],
        [
            InlineKeyboardButton("🍟 الجبس والسناكات", callback_data="cat:جبس وسناكات")
        ],
        [
            InlineKeyboardButton("🛒 السلة", callback_data="cart"),
            InlineKeyboardButton("📞 تواصل معنا", callback_data="contact")
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


# =========================================================
# /start
# =========================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    text = (
        f"أهلاً وسهلاً بك {user.first_name} 🌹\n\n"
        "🛒 أهلاً بك في بوت مخزن الهنداوي\n\n"
        "يمكنك تصفح المنتجات وإضافتها إلى السلة "
        "ثم إرسال طلبك إلى المخزن.\n\n"
        "اختر القسم:"
    )

    await update.message.reply_text(
        text,
        reply_markup=main_menu()
    )


# =========================================================
# عرض المنتجات حسب القسم
# =========================================================

async def show_category(query, category):

    buttons = []

    for product_id, product in PRODUCTS.items():

        name, price, product_category = product

        if product_category == category:

            buttons.append([
                InlineKeyboardButton(
                    f"{name[:32]} — {money(price)}",
                    callback_data=f"product:{product_id}"
                )
            ])

    buttons.append([
        InlineKeyboardButton("⬅️ القائمة الرئيسية", callback_data="home")
    ])

    await query.edit_message_text(
        f"📦 {category}\n\nاختر المنتج:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


# =========================================================
# تفاصيل المنتج
# =========================================================

async def show_product(query, product_id):

    if product_id not in PRODUCTS:
        await query.answer("المنتج غير موجود")
        return

    name, price, category = PRODUCTS[product_id]

    keyboard = [
        [
            InlineKeyboardButton(
                "➕ إضافة إلى السلة",
                callback_data=f"add:{product_id}"
            )
        ],
        [
            InlineKeyboardButton(
                "⬅️ رجوع للقسم",
                callback_data=f"cat:{category}"
            )
        ],
        [
            InlineKeyboardButton(
                "🏠 الرئيسية",
                callback_data="home"
            )
        ]
    ]

    text = (
        f"🛍️ {name}\n\n"
        f"📦 القسم: {category}\n"
        f"💰 السعر المرجعي: {money(price)}\n\n"
        "اضغط على إضافة إلى السلة لإضافة المنتج."
    )

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =========================================================
# إضافة إلى السلة
# =========================================================

async def add_to_cart(query, product_id):

    user_id = query.from_user.id
    cart = get_cart(user_id)

    cart[product_id] = cart.get(product_id, 0) + 1

    await query.answer("تمت إضافة المنتج إلى السلة ✅")

    await show_product(query, product_id)


# =========================================================
# عرض السلة
# =========================================================

async def show_cart(query):

    user_id = query.from_user.id
    cart = get_cart(user_id)

    if not cart:

        keyboard = [
            [
                InlineKeyboardButton(
                    "🛍️ تصفح المنتجات",
                    callback_data="home"
                )
            ]
        ]

        await query.edit_message_text(
            "🛒 السلة فارغة حالياً.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        return

    total = 0
    lines = []

    for product_id, quantity in cart.items():

        name, price, category = PRODUCTS[product_id]

        subtotal = price * quantity
        total += subtotal

        lines.append(
            f"• {name}\n"
            f"  الكمية: {quantity} × {money(price)} = {money(subtotal)}"
        )

    text = (
        "🛒 سلتك:\n\n"
        + "\n\n".join(lines)
        + f"\n\n━━━━━━━━━━━━\n"
        f"💰 المجموع: {money(total)}"
    )

    keyboard = [
        [
            InlineKeyboardButton(
                "📨 إرسال الطلب",
                callback_data="order"
            )
        ],
        [
            InlineKeyboardButton(
                "🗑️ تفريغ السلة",
                callback_data="clear_cart"
            )
        ],
        [
            InlineKeyboardButton(
                "⬅️ الرئيسية",
                callback_data="home"
            )
        ]
    ]

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =========================================================
# إرسال الطلب
# =========================================================

async def send_order(query):

    user_id = query.from_user.id
    user = query.from_user
    cart = get_cart(user_id)

    if not cart:
        await query.answer("السلة فارغة")
        return

    total = 0
    lines = []

    for product_id, quantity in cart.items():

        name, price, category = PRODUCTS[product_id]

        subtotal = price * quantity
        total += subtotal

        lines.append(
            f"{name} | الكمية: {quantity} | {money(subtotal)}"
        )

    order_text = (
        "📦 طلب جديد - مخزن الهنداوي\n\n"
        f"👤 الاسم: {user.full_name}\n"
        f"🆔 Telegram ID: {user.id}\n\n"
        + "\n".join(lines)
        + f"\n\n💰 المجموع: {money(total)}"
    )

    # -----------------------------------------------------
    # ضع Telegram ID الخاص بمدير المخزن هنا لاحقاً
    # -----------------------------------------------------

    ADMIN_ID = os.getenv("ADMIN_ID")

    if ADMIN_ID:

        try:
            await query.get_bot().send_message(
                chat_id=int(ADMIN_ID),
                text=order_text
            )
        except Exception:
            logging.exception("Failed to send order to admin")

    await query.edit_message_text(
        "✅ تم استلام طلبك بنجاح.\n\n"
        "سيتواصل معك مخزن الهنداوي لتأكيد الطلب والتوصيل.",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "🏠 القائمة الرئيسية",
                    callback_data="home"
                )
            ]
        ])
    )

    # تفريغ السلة بعد إرسال الطلب
    carts[user_id] = {}


# =========================================================
# التعامل مع الأزرار
# =========================================================

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    data = query.data

    if data == "home":

        await query.edit_message_text(
            "🛒 مخزن الهنداوي\n\nاختر القسم:",
            reply_markup=main_menu()
        )

    elif data.startswith("cat:"):

        category = data.split(":", 1)[1]

        await show_category(
            query,
            category
        )

    elif data.startswith("product:"):

        product_id = int(
            data.split(":", 1)[1]
        )

        await show_product(
            query,
            product_id
        )

    elif data.startswith("add:"):

        product_id = int(
            data.split(":", 1)[1]
        )

        await add_to_cart(
            query,
            product_id
        )

    elif data == "cart":

        await show_cart(query)

    elif data == "clear_cart":

        user_id = query.from_user.id

        carts[user_id] = {}

        await query.edit_message_text(
            "🗑️ تم تفريغ السلة.",
            reply_markup=main_menu()
        )

    elif data == "order":

        await send_order(query)

    elif data == "contact":

        await query.edit_message_text(
            "📞 للتواصل مع مخزن الهنداوي:\n\n"
            "سيتم إضافة رقم الهاتف ووسائل التواصل هنا لاحقاً.",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "⬅️ الرئيسية",
                        callback_data="home"
                    )
                ]
            ])
        )


# =========================================================
# تشغيل البوت
# =========================================================

def main():

    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO
    )

    application = (
        Application.builder()
        .token(TOKEN)
        .build()
    )

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CallbackQueryHandler(button_handler)
    )

    print("Alhindawi Store Bot is running...")

    application.run_polling()


if __name__ == "__main__":
    main()
