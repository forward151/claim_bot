from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from pdf_reader import get_text
from gpt_request import get_response
from rules import request_list

TOKEN = ""

res1 = ""
res2 = ""
res3 = ""


async def get_file(update, context):
    global res1, res2, res3
    path = "doc.pdf"
    if update.message.document is None:
        if update.message.text == "/start":
            update.message.reply_text("Пришлите документ с жалобой или введите ее вручную")
            return
        else:
            data = update.message.text
    else:
        file = await context.bot.get_file(update.message.document.file_id)
        await file.download_to_drive(path)
        print("downloaded")
        data = get_text(path)
    print(data)
    req = f"{request_list[0]}\n\n{data}\n\n{request_list[1]}\n{request_list[2]}{request_list[3]}{request_list[4]}"
    print(req)
    res = get_response(req).split("\n\n")
    if "НЕ УДОВЛЕТВОРИТЬ ЗАПРОС" in res[2]:
        res1 = f"Анализ жалобы:\n\n{res[0]}"
        res2 = f"Алгоритм принятия решения:\n\n{res[1]}"
        res3 = f"Вердикт:\n\nНЕ УДОВЛЕТВОРИТЬ ЗАПРОС"
    else:
        res1 = f"Анализ жалобы:\n\n{res[0]}"
        res2 = f"Алгоритм принятия решения:\n\n{res[1]}"
        res3 = f"Вердикт:\n\nУДОВЛЕТВОРИТЬ ЗАПРОС"
    print(res)
    await update.message.reply_text(res1,
                                    reply_markup=InlineKeyboardMarkup(
                                        inline_keyboard=[
                                            [InlineKeyboardButton("Какой алгоритм принятия решения?",
                                                                  callback_data='res2')]
                                        ])
                                    )


async def callback_processing(update, context):
    query = update.callback_query
    data = query.data
    await query.answer()
    if data == 'res2':
        await query.message.reply_text(res2,
                                       reply_markup=InlineKeyboardMarkup(
                                           inline_keyboard=[
                                               [InlineKeyboardButton("Прими решение",
                                                                     callback_data='res3')]
                                           ])
                                       )
    if data == 'res3':
        await query.message.reply_text(res3)


def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT | filters.Document.DOC | filters.Document.DOCX | filters.Document.PDF,
                                   get_file))
    app.add_handler(CallbackQueryHandler(callback_processing))

    app.run_polling()


if __name__ == '__main__':
    main()
